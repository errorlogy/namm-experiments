"""HTTP helpers for LLM providers (stdlib only)."""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from typing import Any


class LLMHTTPError(RuntimeError):
    def __init__(self, status: int, body: str, url: str):
        safe_url = _redact_url(url)
        super().__init__(f"HTTP {status} from {safe_url}: {body[:500]}")
        self.status = status
        self.body = body
        self.url = safe_url


def _redact_url(url: str) -> str:
    return re.sub(r"(key=)[^&]+", r"\1***", url)


def http_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout: float = 120,
) -> dict[str, Any]:
    data = None
    req_headers = {"Content-Type": "application/json", **(headers or {})}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise LLMHTTPError(exc.code, body, url) from exc
