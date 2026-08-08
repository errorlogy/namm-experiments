"""Known confluent rewriting systems vs random baselines."""

from __future__ import annotations

from namm.domains.rewriting.evaluator import confluence_score
from namm.domains.rewriting.rules import RewriteRule, RewritingSystem


def known_confluent_systems(max_length: int = 6) -> list[RewritingSystem]:
    """
    Catalog of confluent systems on {a,b} strings.

    ba->ab sorts binary strings; confluent on bounded length.
    """
    return [
        RewritingSystem(
            rules=[RewriteRule("ba", "ab")],
            max_length=max_length,
            system_id="sort-ba-ab",
        ),
        RewritingSystem(
            rules=[RewriteRule("ba", "ab"), RewriteRule("b", "")],
            max_length=max_length,
            system_id="sort-with-truncate-b",
        ),
    ]


def baseline_confluence_scores(max_length: int = 6) -> dict[str, float]:
    """Confluence scores for known baselines."""
    return {
        sys.system_id: confluence_score(sys, max_length).score
        for sys in known_confluent_systems(max_length)
    }


def exceeds_random_baseline(score: float, random_scores: list[float]) -> bool:
    """True if score beats best random baseline in the sample."""
    if not random_scores:
        return score >= 1.0
    return score > max(random_scores)
