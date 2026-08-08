"""Rewrite rule and system definitions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RewriteRule:
    """Single rewrite rule lhs -> rhs over a fixed alphabet."""

    left: str
    right: str


@dataclass
class RewritingSystem:
    """String rewriting system with bounded string length."""

    rules: list[RewriteRule]
    alphabet: tuple[str, ...] = ("a", "b")
    max_length: int = 6
    system_id: str = ""

    def canonical_rules(self) -> list[RewriteRule]:
        """Stable sort order for rules."""
        return sorted(self.rules, key=lambda r: (r.left, r.right))

    def to_dict(self) -> dict[str, Any]:
        return rules_to_dict(self)


def rules_to_dict(system: RewritingSystem) -> dict[str, Any]:
    """Serialize rewriting system to JSON-friendly dict."""
    return {
        "alphabet": list(system.alphabet),
        "max_length": system.max_length,
        "rules": [{"left": r.left, "right": r.right} for r in system.canonical_rules()],
        "system_id": system.system_id,
    }


def parse_rules_dict(data: dict[str, Any]) -> RewritingSystem:
    """Parse rewriting system from dict."""
    rules = [RewriteRule(left=r["left"], right=r["right"]) for r in data["rules"]]
    return RewritingSystem(
        rules=rules,
        alphabet=tuple(data.get("alphabet", ["a", "b"])),
        max_length=int(data.get("max_length", 6)),
        system_id=str(data.get("system_id", "")),
    )


def system_hash(system: RewritingSystem) -> str:
    """Stable hash of canonical rule set."""
    payload = json.dumps(rules_to_dict(system), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()[:16]
