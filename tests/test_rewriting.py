"""Tests for string rewriting domain."""

from namm.domains.rewriting.baseline import known_confluent_systems
from namm.domains.rewriting.evaluator import (
    check_confluence,
    check_normalization,
    confluence_score,
    normalize,
)
from namm.domains.rewriting.generator import mutate_rewriting_system, random_rewriting_system
from namm.domains.rewriting.rules import system_hash


def test_sort_system_is_confluent():
    systems = known_confluent_systems(max_length=4)
    sort_sys = systems[0]
    assert check_confluence(sort_sys, max_length=4)
    assert confluence_score(sort_sys, 4).score == 1.0


def test_random_system_usually_not_confluent():
    system, cid = random_rewriting_system(seed=999, num_rules=4, max_length=4)
    assert cid.startswith("rew-")
    score = confluence_score(system, 4)
    assert 0.0 <= score.score <= 1.0


def test_normalize_reduces():
    system = known_confluent_systems(max_length=5)[0]
    rules = system.canonical_rules()
    nf, steps = normalize("baab", rules)
    assert steps >= 1
    assert isinstance(nf, str)


def test_mutate_produces_valid_system():
    base = known_confluent_systems(max_length=5)[0]
    mutated, cid = mutate_rewriting_system(base, seed=42)
    assert mutated.max_length == base.max_length
    assert system_hash(mutated) != system_hash(base) or len(mutated.rules) != len(base.rules)


def test_normalization_on_sort_system():
    system = known_confluent_systems(max_length=5)[0]
    assert check_normalization(system, max_length=5)
