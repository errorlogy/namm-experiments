"""Provider registry loaded from data/llm_registry.yaml."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

WORKSPACE = Path(__file__).resolve().parents[3]
REGISTRY_PATH = WORKSPACE / "data" / "llm_registry.yaml"


@lru_cache(maxsize=1)
def load_registry() -> dict[str, Any]:
    with REGISTRY_PATH.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def provider_config(name: str) -> dict[str, Any]:
    providers = load_registry().get("providers", {})
    if name not in providers:
        raise KeyError(f"Unknown LLM provider: {name}")
    return {"id": name, **providers[name]}


def list_provider_ids() -> list[str]:
    return list(load_registry().get("providers", {}).keys())


def auto_priority(kind: str) -> list[str]:
    return list(load_registry().get("auto_priority", {}).get(kind, []))


def default_timeout() -> float:
    return float(load_registry().get("defaults", {}).get("timeout_s", 120))


def resolve_env_key(cfg: dict[str, Any]) -> str | None:
    from namm.llm.env import get_secret

    if cfg.get("optional_key"):
        key = cfg.get("env_key")
        return get_secret(key) if key else None
    for alias in cfg.get("env_keys", []):
        val = get_secret(alias)
        if val:
            return val
    env_key = cfg.get("env_key")
    if env_key:
        return get_secret(env_key)
    return None


def is_provider_configured(name: str) -> bool:
    cfg = provider_config(name)
    kind = cfg.get("kind")
    if kind == "local_sentence_transformers":
        return _local_st_available()
    if cfg.get("optional_key"):
        health = cfg.get("health_url")
        if health:
            return _health_ok(health)
        return False
    return resolve_env_key(cfg) is not None


def _health_ok(url: str) -> bool:
    import urllib.error
    import urllib.request

    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=2) as resp:
            return 200 <= resp.status < 300
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def _local_st_available() -> bool:
    try:
        import sentence_transformers  # noqa: F401

        return True
    except ImportError:
        return False


def resolve_provider(kind: str, explicit: str | None = None) -> str:
    if explicit and explicit != "auto":
        if not is_provider_configured(explicit):
            raise RuntimeError(f"Provider '{explicit}' is not configured (missing key or local backend).")
        return explicit
    env_override = os.environ.get(f"NAMM_{kind.upper()}_PROVIDER", "").strip()
    if env_override and env_override != "auto":
        if not is_provider_configured(env_override):
            raise RuntimeError(f"NAMM_{kind.upper()}_PROVIDER={env_override} is not configured.")
        return env_override
    for name in auto_priority(kind):
        if is_provider_configured(name):
            return name
    raise RuntimeError(
        f"No configured {kind} provider. Set keys in .env.local or install [llm-local]. "
        f"Run: namm llm status"
    )
