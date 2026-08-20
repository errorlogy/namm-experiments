"""Tests for NAMM LLM provider layer (mocked HTTP, no live keys)."""

from __future__ import annotations

import json
from unittest.mock import patch

import numpy as np
import pytest

from namm.llm.env import parse_dotenv
from namm.llm.http import LLMHTTPError, http_json
from namm.llm.registry import is_provider_configured, resolve_provider
from namm.llm.providers import GeminiProvider, OpenAICompatProvider, build_provider
from namm.llm.client import embed, get_client, provider_status


def test_parse_dotenv(tmp_path):
    p = tmp_path / ".env"
    p.write_text('OPENAI_API_KEY="sk-test"\n# comment\nFOO=bar\n', encoding="utf-8")
    assert parse_dotenv(p) == {"OPENAI_API_KEY": "sk-test", "FOO": "bar"}


def test_openai_compat_embed():
    cfg = {
        "id": "openai",
        "kind": "openai_compat",
        "env_key": "OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1",
        "embed_models": ["text-embedding-3-small"],
        "default_embed": "text-embedding-3-small",
    }
    provider = OpenAICompatProvider(cfg)
    payload = {"data": [{"index": 0, "embedding": [0.1, 0.2, 0.3]}]}
    with patch("namm.llm.providers.http_json", return_value=payload):
        with patch("namm.llm.providers.resolve_env_key", return_value="sk-test"):
            mat = provider.embed(["hello"])
    assert mat.shape == (1, 3)
    assert mat[0, 0] == pytest.approx(0.1)


def test_gemini_chat():
    cfg = {
        "id": "gemini",
        "kind": "gemini",
        "env_keys": ["GEMINI_API_KEY"],
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "chat_models": ["gemini-2.0-flash"],
        "default_chat": "gemini-2.0-flash",
    }
    provider = GeminiProvider(cfg)
    response = {"candidates": [{"content": {"parts": [{"text": "AI works via patterns."}]}}]}
    with patch("namm.llm.providers.http_json", return_value=response):
        with patch("namm.llm.providers.resolve_env_key", return_value="AIza-test"):
            text = provider.chat([{"role": "user", "content": "Explain AI briefly"}])
    assert "patterns" in text


def test_provider_status_structure(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "AIza-test")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    status = provider_status()
    assert "providers" in status
    assert any(p["id"] == "gemini" for p in status["providers"])


def test_resolve_provider_with_key(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "gsk-test")
    monkeypatch.delenv("NAMM_CHAT_PROVIDER", raising=False)
    name = resolve_provider("chat", "auto")
    assert name == "groq"


def test_http_json_error():
    import urllib.error

    def _raise(*_a, **_k):
        raise urllib.error.HTTPError("http://x", 401, "Unauthorized", {}, None)

    with patch("urllib.request.urlopen", side_effect=_raise):
        with pytest.raises(LLMHTTPError):
            http_json("GET", "http://x")
