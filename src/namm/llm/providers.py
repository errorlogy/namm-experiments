"""Provider backends: OpenAI-compatible, Gemini, Jina, local sentence-transformers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import numpy as np

from namm.llm.http import http_json
from namm.llm.registry import default_timeout, resolve_env_key


class BaseProvider(ABC):
    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg
        self.id = cfg["id"]
        self.timeout = default_timeout()

    @abstractmethod
    def chat(self, messages: list[dict[str, str]], *, model: str | None = None) -> str:
        ...

    @abstractmethod
    def embed(self, texts: list[str], *, model: str | None = None) -> np.ndarray:
        ...

    def supports_chat(self) -> bool:
        return not self.cfg.get("embed_only")

    def supports_embed(self) -> bool:
        return not self.cfg.get("chat_only")


class OpenAICompatProvider(BaseProvider):
    def _headers(self) -> dict[str, str]:
        headers = dict(self.cfg.get("extra_headers") or {})
        key = resolve_env_key(self.cfg)
        if key:
            headers["Authorization"] = f"Bearer {key}"
        return headers

    def _base(self) -> str:
        return self.cfg["base_url"].rstrip("/")

    def chat(self, messages: list[dict[str, str]], *, model: str | None = None) -> str:
        model = model or self.cfg.get("default_chat") or self.cfg["chat_models"][0]
        url = f"{self._base()}/chat/completions"
        payload = {"model": model, "messages": messages, "temperature": 0.2}
        data = http_json("POST", url, headers=self._headers(), payload=payload, timeout=self.timeout)
        return data["choices"][0]["message"]["content"]

    def embed(self, texts: list[str], *, model: str | None = None) -> np.ndarray:
        model = model or self.cfg.get("default_embed") or self.cfg["embed_models"][0]
        url = f"{self._base()}/embeddings"
        payload = {"model": model, "input": texts}
        data = http_json("POST", url, headers=self._headers(), payload=payload, timeout=self.timeout)
        rows = sorted(data["data"], key=lambda r: r["index"])
        return np.array([r["embedding"] for r in rows], dtype=np.float64)


class GeminiProvider(BaseProvider):
    def _key(self) -> str:
        key = resolve_env_key(self.cfg)
        if not key:
            raise RuntimeError("Gemini API key missing (GEMINI_API_KEY or GOOGLE_API_KEY)")
        return key

    def chat(self, messages: list[dict[str, str]], *, model: str | None = None) -> str:
        model = model or self.cfg.get("default_chat") or self.cfg["chat_models"][0]
        url = f"{self.cfg['base_url']}/models/{model}:generateContent?key={self._key()}"
        contents = []
        system_parts: list[str] = []
        for msg in messages:
            if msg["role"] == "system":
                system_parts.append(msg["content"])
                continue
            role = "user" if msg["role"] == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})
        payload: dict[str, Any] = {"contents": contents}
        if system_parts:
            payload["systemInstruction"] = {"parts": [{"text": "\n\n".join(system_parts)}]}
        data = http_json("POST", url, payload=payload, timeout=self.timeout)
        parts = data["candidates"][0]["content"]["parts"]
        return "".join(p.get("text", "") for p in parts)

    def embed(self, texts: list[str], *, model: str | None = None) -> np.ndarray:
        model = model or self.cfg.get("default_embed") or self.cfg["embed_models"][0]
        url = f"{self.cfg['base_url']}/models/{model}:embedContent?key={self._key()}"
        vectors: list[list[float]] = []
        for text in texts:
            payload = {
                "model": f"models/{model}",
                "content": {"parts": [{"text": text}]},
            }
            data = http_json("POST", url, payload=payload, timeout=self.timeout)
            vectors.append(data["embedding"]["values"])
        return np.array(vectors, dtype=np.float64)


class JinaProvider(BaseProvider):
    def _headers(self) -> dict[str, str]:
        key = resolve_env_key(self.cfg)
        if not key:
            raise RuntimeError("JINA_API_KEY missing")
        return {"Authorization": f"Bearer {key}"}

    def chat(self, messages: list[dict[str, str]], *, model: str | None = None) -> str:
        raise NotImplementedError("Jina provider is embed-only")

    def embed(self, texts: list[str], *, model: str | None = None) -> np.ndarray:
        model = model or self.cfg.get("default_embed") or self.cfg["embed_models"][0]
        url = f"{self.cfg['base_url']}/embeddings"
        payload = {"model": model, "input": texts, "task": "text-matching"}
        data = http_json("POST", url, headers=self._headers(), payload=payload, timeout=self.timeout)
        rows = data.get("data") or data.get("embeddings") or []
        if rows and isinstance(rows[0], dict) and "embedding" in rows[0]:
            return np.array([r["embedding"] for r in rows], dtype=np.float64)
        return np.array(rows, dtype=np.float64)


class LocalSTProvider(BaseProvider):
    _model = None

    def _get_model(self):
        if LocalSTProvider._model is None:
            from sentence_transformers import SentenceTransformer

            name = self.cfg.get("model", "all-MiniLM-L6-v2")
            LocalSTProvider._model = SentenceTransformer(name)
        return LocalSTProvider._model

    def chat(self, messages: list[dict[str, str]], *, model: str | None = None) -> str:
        raise NotImplementedError("local sentence-transformers is embed-only")

    def embed(self, texts: list[str], *, model: str | None = None) -> np.ndarray:
        enc = self._get_model().encode(texts, convert_to_numpy=True, normalize_embeddings=False)
        return np.asarray(enc, dtype=np.float64)


def build_provider(cfg: dict[str, Any]) -> BaseProvider:
    kind = cfg.get("kind")
    if kind == "openai_compat":
        return OpenAICompatProvider(cfg)
    if kind == "gemini":
        return GeminiProvider(cfg)
    if kind == "jina":
        return JinaProvider(cfg)
    if kind == "local_sentence_transformers":
        return LocalSTProvider(cfg)
    raise ValueError(f"Unknown provider kind: {kind}")
