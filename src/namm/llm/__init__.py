"""Unified LLM + embedding access for NAMM experiments (API and local)."""

from namm.llm.client import (
    LLMClient,
    chat,
    embed,
    embed_batch,
    get_client,
    list_providers,
    provider_status,
)

__all__ = [
    "LLMClient",
    "chat",
    "embed",
    "embed_batch",
    "get_client",
    "list_providers",
    "provider_status",
]
