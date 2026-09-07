"""High-level LLM client facade for NAMM experiments."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import numpy as np

from namm.llm.env import load_env
from namm.llm.providers import BaseProvider, build_provider
from namm.llm.registry import (
    is_provider_configured,
    list_provider_ids,
    provider_config,
    resolve_provider,
)


@dataclass
class LLMClient:
    chat_provider: str
    embed_provider: str
    chat_model: str | None = None
    embed_model: str | None = None

    def _backend(self, name: str) -> BaseProvider:
        return build_provider(provider_config(name))

    def chat(self, prompt: str, *, system: str | None = None, model: str | None = None) -> str:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        model = model or self.chat_model or os.environ.get("NAMM_CHAT_MODEL") or None
        return self._chat_with_fallback(messages, model=model, primary=self.chat_provider)

    def _chat_with_fallback(self, messages: list[dict[str, str]], *, model: str | None, primary: str) -> str:
        from namm.llm.registry import auto_priority, is_provider_configured

        tried: list[str] = []
        order = [primary] + [p for p in auto_priority("chat") if p != primary]
        last_exc: Exception | None = None
        for name in order:
            if name in tried or not is_provider_configured(name):
                continue
            tried.append(name)
            try:
                return self._backend(name).chat(messages, model=model if name == primary else None)
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                continue
        if last_exc:
            raise last_exc
        raise RuntimeError("No chat provider available")

    def embed(self, texts: list[str] | str, *, model: str | None = None) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]
        model = model or self.embed_model or os.environ.get("NAMM_EMBED_MODEL") or None
        return self._backend(self.embed_provider).embed(texts, model=model)


def get_client(
    *,
    chat_provider: str | None = None,
    embed_provider: str | None = None,
    chat_model: str | None = None,
    embed_model: str | None = None,
) -> LLMClient:
    load_env()
    chat_provider = resolve_provider("chat", chat_provider or os.environ.get("NAMM_CHAT_PROVIDER", "auto"))
    embed_provider = resolve_provider("embed", embed_provider or os.environ.get("NAMM_EMBED_PROVIDER", "auto"))
    return LLMClient(
        chat_provider=chat_provider,
        embed_provider=embed_provider,
        chat_model=chat_model,
        embed_model=embed_model,
    )


def chat(prompt: str, *, system: str | None = None, provider: str | None = None, model: str | None = None) -> str:
    client = get_client(chat_provider=provider, chat_model=model)
    return client.chat(prompt, system=system, model=model)


def embed(texts: list[str] | str, *, provider: str | None = None, model: str | None = None) -> np.ndarray:
    client = get_client(embed_provider=provider, embed_model=model)
    return client.embed(texts, model=model)


def embed_batch(
    texts: list[str],
    *,
    provider: str | None = None,
    model: str | None = None,
    batch_size: int = 32,
    fallback: bool = True,
) -> np.ndarray:
    if not texts:
        return np.zeros((0, 0), dtype=np.float64)
    client = get_client(embed_provider=provider, embed_model=model)
    try:
        chunks: list[np.ndarray] = []
        for i in range(0, len(texts), batch_size):
            chunks.append(client.embed(texts[i : i + batch_size], model=model))
        return np.vstack(chunks)
    except Exception:
        if not fallback or provider not in (None, "auto"):
            raise
        from namm.llm.registry import auto_priority, is_provider_configured

        for name in auto_priority("embed"):
            if name == client.embed_provider or not is_provider_configured(name):
                continue
            fb = get_client(embed_provider=name, embed_model=model)
            chunks = []
            for i in range(0, len(texts), batch_size):
                chunks.append(fb.embed(texts[i : i + batch_size], model=model))
            return np.vstack(chunks)
        raise


def list_providers() -> list[str]:
    load_env()
    return list_provider_ids()


def provider_status() -> dict[str, Any]:
    load_env()
    rows: list[dict[str, Any]] = []
    for name in list_provider_ids():
        cfg = provider_config(name)
        configured = is_provider_configured(name)
        rows.append(
            {
                "id": name,
                "label": cfg.get("label", name),
                "kind": cfg.get("kind"),
                "configured": configured,
                "chat": configured and not cfg.get("embed_only"),
                "embed": configured and not cfg.get("chat_only"),
                "default_chat": cfg.get("default_chat"),
                "default_embed": cfg.get("default_embed"),
            }
        )
    chat_auto = embed_auto = None
    try:
        chat_auto = resolve_provider("chat", "auto")
    except RuntimeError:
        pass
    try:
        embed_auto = resolve_provider("embed", "auto")
    except RuntimeError:
        pass
    return {
        "providers": rows,
        "auto_chat": chat_auto,
        "auto_embed": embed_auto,
        "env_paths_loaded": [str(p) for p in __import__("namm.llm.env", fromlist=["env_search_paths"]).env_search_paths()],
    }
