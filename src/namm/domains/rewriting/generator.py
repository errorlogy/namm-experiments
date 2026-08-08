"""Random rewriting system generation."""

from __future__ import annotations

import random
import uuid

from namm.domains.rewriting.rules import RewriteRule, RewritingSystem


def random_rewriting_system(
    seed: int | None = None,
    *,
    num_rules: int = 3,
    max_length: int = 6,
    alphabet: tuple[str, ...] = ("a", "b"),
    max_pattern_len: int = 3,
) -> tuple[RewritingSystem, str]:
    """Generate a random rewriting system. Returns (system, candidate_id)."""
    rng = random.Random(seed)
    candidate_id = f"rew-{uuid.uuid4().hex[:8]}"
    rules: list[RewriteRule] = []
    seen: set[tuple[str, str]] = set()

    for _ in range(num_rules * 3):
        if len(rules) >= num_rules:
            break
        plen = rng.randint(1, max_pattern_len)
        left = "".join(rng.choice(alphabet) for _ in range(plen))
        rlen = rng.randint(0, max_pattern_len)
        right = "".join(rng.choice(alphabet) for _ in range(rlen))
        if left == right:
            continue
        key = (left, right)
        if key in seen:
            continue
        seen.add(key)
        rules.append(RewriteRule(left=left, right=right))

    while len(rules) < num_rules:
        left = rng.choice(alphabet) + rng.choice(alphabet)
        right = rng.choice(alphabet)
        if (left, right) not in seen and left != right:
            seen.add((left, right))
            rules.append(RewriteRule(left=left, right=right))

    system = RewritingSystem(
        rules=rules,
        alphabet=alphabet,
        max_length=max_length,
        system_id=candidate_id,
    )
    return system, candidate_id


def mutate_rewriting_system(
    base: RewritingSystem,
    seed: int,
    *,
    max_pattern_len: int = 3,
) -> tuple[RewritingSystem, str]:
    """Mutate an existing system (add/replace one rule)."""
    rng = random.Random(seed)
    candidate_id = f"rew-{uuid.uuid4().hex[:8]}"
    rules = list(base.rules)
    if rules and rng.random() < 0.5:
        idx = rng.randrange(len(rules))
        plen = rng.randint(1, max_pattern_len)
        left = "".join(rng.choice(base.alphabet) for _ in range(plen))
        rlen = rng.randint(0, max_pattern_len)
        right = "".join(rng.choice(base.alphabet) for _ in range(rlen))
        if left != right:
            rules[idx] = RewriteRule(left=left, right=right)
    else:
        plen = rng.randint(1, max_pattern_len)
        left = "".join(rng.choice(base.alphabet) for _ in range(plen))
        right = "".join(rng.choice(base.alphabet) for _ in range(max(0, plen - 1)))
        if left != right:
            rules.append(RewriteRule(left=left, right=right))
    system = RewritingSystem(
        rules=rules[:4],
        alphabet=base.alphabet,
        max_length=base.max_length,
        system_id=candidate_id,
    )
    return system, candidate_id
