"""Certificate and representation metrics for rewriting systems."""

from __future__ import annotations

import gzip
import hashlib
from typing import Any

import orjson

from namm.domains.rewriting.evaluator import confluence_score, normalize
from namm.domains.rewriting.rules import RewritingSystem, rules_to_dict, system_hash


def eval_hash(system: RewritingSystem, test_strings: list[str]) -> str:
    """Digest of normal forms on reference strings."""
    rules = system.canonical_rules()
    parts = [f"{s}->{normalize(s, rules)[0]}" for s in test_strings]
    payload = "|".join(parts)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def human_projection_from_system(system: RewritingSystem, *, candidate_id: str) -> str:
    """Lossy human-readable description of a rewriting system."""
    lines = [
        f"**Candidate:** `{candidate_id}`",
        f"**Alphabet:** {', '.join(system.alphabet)}",
        f"**Max string length:** {system.max_length}",
        "**Rules:**",
    ]
    for r in system.canonical_rules():
        lines.append(f"- `{r.left}` → `{r.right}`")
    lines.append(
        "\n> Trust certificate; full object in certificate.json. "
        "Projection omits witness strings and confluence counterexamples."
    )
    return "\n".join(lines)


def compute_rewriting_representation_metrics(
    system: RewritingSystem,
) -> dict[str, Any]:
    """K_A proxies for rewriting certificate payload."""
    payload = rules_to_dict(system)
    raw = orjson.dumps(payload)
    json_bytes = len(raw)
    gzip_bytes = len(gzip.compress(raw))
    projection = human_projection_from_system(system, candidate_id=system.system_id)
    projection_token_estimate = max(1, len(projection.split()))
    return {
        "json_bytes": json_bytes,
        "gzip_bytes": gzip_bytes,
        "eval_time_ms": 0.0,
        "projection_token_estimate": projection_token_estimate,
        "token_count_estimate": projection_token_estimate,
    }


def build_rewriting_certificate(
    *,
    candidate_id: str,
    system: RewritingSystem,
    seed: int,
    test_strings: list[str],
    confluence: dict[str, Any],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build primary certificate.json payload for rewriting domain."""
    cert: dict[str, Any] = {
        "candidate_id": candidate_id,
        "rewriting_system": rules_to_dict(system),
        "system_hash": system_hash(system),
        "eval_hash": eval_hash(system, test_strings),
        "confluence_witness": confluence,
        "witness_bounds": {
            "max_string_length": system.max_length,
            "test_string_count": len(test_strings),
            "alphabet": list(system.alphabet),
        },
        "seeds": {"experiment": seed, "generator": seed},
        "representation_metrics": compute_rewriting_representation_metrics(system),
    }
    if extra:
        cert.update(extra)
    return cert
