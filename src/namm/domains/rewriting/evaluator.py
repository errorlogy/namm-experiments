"""Evaluate confluence and normalization on bounded strings."""

from __future__ import annotations

from dataclasses import dataclass

from namm.domains.rewriting.rules import RewriteRule, RewritingSystem


def _all_strings(alphabet: tuple[str, ...], max_length: int) -> list[str]:
    """All non-empty strings up to max_length over alphabet."""
    strings: list[str] = []
    for length in range(1, max_length + 1):
        _extend("", length, alphabet, strings)
    return strings


def _extend(prefix: str, remaining: int, alphabet: tuple[str, ...], out: list[str]) -> None:
    if remaining == 0:
        out.append(prefix)
        return
    for ch in alphabet:
        _extend(prefix + ch, remaining - 1, alphabet, out)


def _apply_one_step(s: str, rules: list[RewriteRule]) -> set[str]:
    """One-step rewrites (leftmost-longest match per rule application)."""
    results: set[str] = set()
    for rule in rules:
        if not rule.left:
            continue
        start = 0
        while True:
            idx = s.find(rule.left, start)
            if idx < 0:
                break
            results.add(s[:idx] + rule.right + s[idx + len(rule.left) :])
            start = idx + 1
    return results


def normalize(
    s: str,
    rules: list[RewriteRule],
    *,
    max_steps: int = 200,
) -> tuple[str, int]:
    """Greedy leftmost-longest normalization; returns (normal_form, steps)."""
    current = s
    steps = 0
    while steps < max_steps:
        rewrites = _apply_one_step(current, rules)
        if not rewrites:
            break
        # Deterministic: pick lexicographically smallest one-step result
        current = min(rewrites)
        steps += 1
    return current, steps


def _reachable_normal_forms(
    s: str,
    rules: list[RewriteRule],
    *,
    max_steps: int = 50,
    max_queue: int = 500,
) -> set[str]:
    """All normal forms reachable from s via bounded BFS."""
    normals: set[str] = set()
    queue = [s]
    seen = {s}
    steps = 0
    while queue and steps < max_steps and len(seen) < max_queue:
        current = queue.pop(0)
        rewrites = _apply_one_step(current, rules)
        if not rewrites:
            normals.add(current)
            continue
        for nxt in sorted(rewrites):
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
        steps += 1
    if not normals and queue:
        normals.add(min(seen, key=len))
    return normals


@dataclass
class ConfluenceResult:
    confluent: bool
    score: float
    counterexample: dict | None = None
    strings_tested: int = 0


def confluence_score(system: RewritingSystem, max_length: int | None = None) -> ConfluenceResult:
    """
    Fraction of test strings with a unique normal form.

    Full confluence requires exactly one normal form per string.
    """
    n = max_length if max_length is not None else system.max_length
    strings = _all_strings(system.alphabet, n)
    rules = system.canonical_rules()
    unique_count = 0
    for s in strings:
        normals = _reachable_normal_forms(s, rules)
        if len(normals) == 1:
            unique_count += 1
        elif len(normals) > 1:
            return ConfluenceResult(
                confluent=False,
                score=unique_count / len(strings) if strings else 0.0,
                counterexample={"string": s, "normal_forms": sorted(normals)[:5]},
                strings_tested=len(strings),
            )
    score = unique_count / len(strings) if strings else 0.0
    return ConfluenceResult(
        confluent=score == 1.0,
        score=score,
        strings_tested=len(strings),
    )


def check_confluence(system: RewritingSystem, max_length: int | None = None) -> bool:
    """Return True if system is confluent on all strings up to max_length."""
    return confluence_score(system, max_length).confluent


def check_normalization(system: RewritingSystem, max_length: int | None = None) -> bool:
    """Every string reduces to some normal form within step bound."""
    n = max_length if max_length is not None else system.max_length
    rules = system.canonical_rules()
    for s in _all_strings(system.alphabet, n):
        _, steps = normalize(s, rules)
        if steps >= 200:
            return False
        rewrites = _apply_one_step(s, rules)
        if rewrites:
            nf, _ = normalize(s, rules)
            if _apply_one_step(nf, rules):
                return False
    return True
