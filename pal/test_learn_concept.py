"""
Tests for the PAL (Perturbation-based Active Learning) system.
"""

import pytest
from pal.learn_concept import PALSystem, learn_concept, Clause
from logical_engine.horn_clauses import KnowledgeBase, Fact


def test_construct_initial_clause():
    """Test initial clause construction."""
    pal_system = PALSystem()
    initial_example = Clause("parent(john, mary)")
    clause = pal_system.construct_initial_clause(initial_example)
    assert clause.head == "parent(john, mary)"
    assert clause.body == []


def test_initial_perturbation_level():
    """Test initial perturbation level."""
    pal_system = PALSystem()
    level = pal_system.initial_perturbation_level()
    assert level == 1


def test_perturbation_method():
    """Test perturbation method generates examples."""
    pal_system = PALSystem()
    clause = Clause("parent(john, mary)")

    # First perturbation
    example1 = pal_system.perturbation_method(clause, 1)
    assert example1 is not None
    assert example1.head == "parent(mary, alice)"

    # Second perturbation should be None
    example2 = pal_system.perturbation_method(clause, 1)
    assert example2 is None


def test_is_positive():
    """Test positive example checking."""
    pal_system = PALSystem()
    example = Clause("parent(john, mary)")
    assert pal_system.is_positive(example) == True


def test_learn_concept_basic():
    """Test basic learning functionality."""
    bk = KnowledgeBase()
    pal_system = PALSystem(background_kb=bk)
    initial_example = Clause("parent(john, mary)")

    learned_clause = learn_concept(initial_example, pal_system)

    # Should learn a generalized clause
    assert learned_clause is not None
    assert "parent" in learned_clause.head

    # Should be added to background knowledge
    assert len(pal_system.background_kb.facts) > 0 or len(pal_system.background_kb.rules) > 0


def test_covers_negative_example():
    """Test negative example coverage checking."""
    negative_examples = [Clause("parent(alice, john)")]
    pal_system = PALSystem(negative_examples=negative_examples)

    # Clause that might cover negative example
    clause = Clause("parent(X, Y)")
    assert pal_system.covers_negative_example(clause) == True

    # Clause that doesn't cover
    clause2 = Clause("ancestor(X, Y)")
    assert pal_system.covers_negative_example(clause2) == False


if __name__ == "__main__":
    pytest.main([__file__])