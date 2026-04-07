"""
Unit tests for FOIL inductive learner.
"""

import sys
sys.path.insert(0, '/work/TPmeta_interpreter')

import pytest
from foil.ilp import (
    Example,
    foil_learn,
    information_gain,
    covers_negatives,
    solves,
    specialize_clause,
    generate_specializations,
    recall,
    precision,
    extract_variables,
)
from logical_engine.horn_clauses import KnowledgeBase, Fact, Rule


class TestExample:
    """Tests for Example class."""
    
    def test_example_creation_positive(self):
        ex = Example("parent(john, mary)", True)
        assert ex.goal == "parent(john, mary)"
        assert ex.label is True
    
    def test_example_creation_negative(self):
        ex = Example("parent(alice, john)", False)
        assert ex.goal == "parent(alice, john)"
        assert ex.label is False
    
    def test_example_repr(self):
        ex_pos = Example("fact(a)", True)
        ex_neg = Example("fact(b)", False)
        assert "+" in repr(ex_pos)
        assert "-" in repr(ex_neg)


class TestSolves:
    """Tests for solves function."""
    
    def test_solves_simple_fact(self):
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        rule = Rule("parent(X, Y)", [])
        ex = Example("parent(john, mary)", True)
        
        assert solves(rule, ex, kb)
    
    def test_solves_with_rule(self):
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        rule = Rule("child(X, Y)", ["parent(Y, X)"])
        ex = Example("child(mary, john)", True)
        
        assert solves(rule, ex, kb)
    
    def test_solves_nonmatching(self):
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        rule = Rule("parent(john, mary)", [])
        ex = Example("parent(alice, bob)", False)
        
        assert not solves(rule, ex, kb)


class TestCoversNegatives:
    """Tests for covers_negatives function."""
    
    def test_covers_negatives_true(self):
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        kb.add_fact(Fact("parent(alice, bob)"))
        rule = Rule("parent(X, Y)", [])  # Too general, covers negative
        negatives = [Example("parent(alice, bob)", False)]
        
        assert covers_negatives(rule, negatives, kb)
    
    def test_covers_negatives_false(self):
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        rule = Rule("parent(john, Y)", [])  # More specific
        negatives = [Example("parent(alice, bob)", False)]
        
        assert not covers_negatives(rule, negatives, kb)


class TestInformationGain:
    """Tests for information_gain function."""
    
    def test_information_gain_perfect(self):
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        kb.add_fact(Fact("parent(mary, alice)"))
        rule = Rule("parent(john, mary)", [])
        positives = [Example("parent(john, mary)", True)]
        negatives = [Example("parent(mary, alice)", False)]
        
        gain = information_gain(rule, positives, negatives, kb)
        assert gain > 0
    
    def test_information_gain_covers_negative(self):
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        kb.add_fact(Fact("parent(mary, alice)"))
        
        rule_general = Rule("parent(X, Y)", [])  # Covers both
        rule_specific = Rule("parent(john, Y)", [])  # Only covers john
        
        positives = [Example("parent(john, mary)", True)]
        negatives = [Example("parent(mary, alice)", False)]
        
        gain_general = information_gain(rule_general, positives, negatives, kb)
        gain_specific = information_gain(rule_specific, positives, negatives, kb)
        
        # Specific rule should have higher gain (covers positive, avoids negative)
        assert gain_specific >= gain_general


class TestSpecializeClause:
    """Tests for specialize_clause function."""
    
    def test_specialize_adds_literal(self):
        rule = Rule("ancestor(X, Y)", [])
        specialized = specialize_clause(rule, "parent(X, Z)")
        
        assert len(specialized.body) == 1
        assert specialized.body[0] == "parent(X, Z)"
        assert specialized.head == rule.head
    
    def test_specialize_chain(self):
        rule = Rule("ancestor(X, Y)", [])
        spec1 = specialize_clause(rule, "parent(X, Z)")
        spec2 = specialize_clause(spec1, "ancestor(Z, Y)")
        
        assert len(spec2.body) == 2
        assert spec2.body == ["parent(X, Z)", "ancestor(Z, Y)"]


class TestGenerateSpecializations:
    """Tests for generate_specializations function."""
    
    def test_generate_specializations(self):
        rule = Rule("ancestor(X, Y)", [])
        predicates = ["parent(X, Z)", "ancestor(X, Z)"]
        candidates = generate_specializations(rule, predicates)
        
        assert len(candidates) == 2
        assert all(len(c.body) == 1 for c in candidates)
    
    def test_generate_specializations_empty(self):
        rule = Rule("ancestor(X, Y)", [])
        candidates = generate_specializations(rule, [])
        
        assert len(candidates) == 0


class TestFoilLearn:
    """Tests for foil_learn function."""
    
    def test_foil_learn_simple(self):
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        
        positives = [Example("parent(john, mary)", True)]
        negatives = [Example("parent(alice, bob)", False)]
        
        rules = foil_learn("parent", positives, negatives, kb=kb)
        
        assert len(rules) > 0
        assert all(isinstance(r, Rule) for r in rules)
    
    def test_foil_learn_ancestor(self):
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        kb.add_fact(Fact("parent(mary, alice)"))
        kb.add_fact(Fact("parent(john, bob)"))
        
        positives = [
            Example("ancestor(john, mary)", True),
            Example("ancestor(john, alice)", True),
            Example("ancestor(mary, alice)", True),
        ]
        negatives = [
            Example("ancestor(mary, john)", False),
            Example("ancestor(alice, john)", False),
        ]
        
        predicates = [
            "parent(X, Y)",
            "parent(X, Z)",
            "ancestor(X, Z)",
            "ancestor(Z, Y)",
        ]
        
        rules = foil_learn(
            "ancestor",
            positives,
            negatives,
            available_predicates=predicates,
            kb=kb,
            max_specializations=5
        )
        
        assert len(rules) > 0


class TestRecall:
    """Tests for recall metric."""
    
    def test_recall_perfect(self):
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        kb.add_fact(Fact("parent(mary, alice)"))
        rule = Rule("parent(X, Y)", [])
        positives = [
            Example("parent(john, mary)", True),
            Example("parent(mary, alice)", True),
        ]
        
        r = recall(rule, positives, kb)
        assert r == 1.0
    
    def test_recall_partial(self):
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        rule = Rule("parent(john, Y)", [])
        positives = [
            Example("parent(john, mary)", True),
            Example("parent(mary, alice)", True),
        ]
        
        r = recall(rule, positives, kb)
        assert 0 < r < 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
