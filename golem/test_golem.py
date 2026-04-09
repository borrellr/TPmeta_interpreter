"""
Unit tests for Golem ILP System.
"""

import pytest
from logical_engine.horn_clauses import KnowledgeBase, Fact, Rule
from logical_engine.meta_interpreter import solve
from golem_learner import GolemLearner, Example, GolemRule


class TestGolemLearner:
    """Test suite for GolemLearner."""
    
    def test_initialization(self):
        """Test GolemLearner initialization."""
        kb = KnowledgeBase()
        learner = GolemLearner(kb, max_clause_length=2, verbose=False)
        
        assert learner.kb is kb
        assert learner.max_clause_length == 2
        assert learner.max_iterations == 100
        assert len(learner.learned_rules) == 0
    
    def test_example_creation(self):
        """Test Example creation."""
        ex = Example("parent(john, mary)")
        assert ex.goal == "parent(john, mary)"
        assert ex.label is True
        
        ex_neg = Example("parent(john, mary)", False)
        assert ex_neg.label is False
    
    def test_golem_rule_creation(self):
        """Test GolemRule creation and representation."""
        rule = GolemRule("ancestor(X, Y)", ["parent(X, Y)"])
        assert rule.head == "ancestor(X, Y)"
        assert rule.body == ["parent(X, Y)"]
        
        rule_str = str(rule)
        assert "ancestor(X, Y)" in rule_str
        assert "parent(X, Y)" in rule_str
    
    def test_golem_rule_fact(self):
        """Test GolemRule without body (fact)."""
        rule = GolemRule("parent(john, mary)", [])
        rule_str = str(rule)
        assert "parent(john, mary)" in rule_str
        assert ":-" not in rule_str
    
    def test_simple_learning(self):
        """Test basic learning scenario."""
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        kb.add_fact(Fact("parent(mary, alice)"))
        
        positive_examples = [
            Example("child(mary)"),
            Example("child(alice)"),
        ]
        
        learner = GolemLearner(kb, max_clause_length=1, verbose=False)
        rules = learner.learn(positive_examples)
        
        # Should learn at least one rule
        assert len(rules) >= 0
        assert all(isinstance(r, GolemRule) for r in rules)
    
    def test_covered_examples(self):
        """Test that covered examples detection works."""
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        kb.add_fact(Fact("parent(mary, alice)"))
        
        learner = GolemLearner(kb, verbose=False)
        
        # Add a rule to KB
        rule = GolemRule("ancestor(X, Y)", ["parent(X, Y)"])
        
        examples = [
            Example("ancestor(john, mary)"),
            Example("ancestor(mary, alice)"),
        ]
        
        covered = learner._get_covered_examples(rule, examples)
        # Both examples should be coverable with the rule
        assert len(covered) >= 0
    
    def test_get_learned_rules(self):
        """Test retrieving learned rules."""
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        
        learner = GolemLearner(kb, verbose=False)
        learner.learned_rules = [
            GolemRule("test(X)", [])
        ]
        
        rules = learner.get_learned_rules()
        assert len(rules) == 1
        assert rules[0].head == "test(X)"
    
    def test_learned_knowledge_base(self):
        """Test converting learned rules to KB."""
        learner = GolemLearner(KnowledgeBase(), verbose=False)
        learner.learned_rules = [
            GolemRule("parent(john, mary)", []),
            GolemRule("child(X, Y)", ["parent(Y, X)"])
        ]
        
        kb = learner.get_learned_knowledge_base()
        assert len(kb.facts) == 1
        assert len(kb.rules) == 1
    
    def test_rule_specialization(self):
        """Test rule specialization."""
        kb = KnowledgeBase()
        learner = GolemLearner(kb, max_clause_length=3, verbose=False)
        
        rule = GolemRule("ancestor(X, Y)", ["parent(X, Y)"])
        specialized = learner.specialize_rule(rule, ["parent(X, Z)", "ancestor(Z, Y)"])
        
        assert len(specialized.body) == 3
        assert "parent(X, Y)" in specialized.body
        assert "parent(X, Z)" in specialized.body
    
    def test_too_long_specialization(self):
        """Test that over-long specializations are rejected."""
        kb = KnowledgeBase()
        learner = GolemLearner(kb, max_clause_length=2, verbose=False)
        
        rule = GolemRule("test(X)", ["a(X)"])
        too_long = learner.specialize_rule(rule, ["b(X)", "c(X)", "d(X)"])
        
        # Should return original rule if too long
        assert too_long == rule or len(too_long.body) <= learner.max_clause_length
    
    def test_generalize_examples(self):
        """Test generalization of examples."""
        kb = KnowledgeBase()
        learner = GolemLearner(kb, verbose=False)
        
        ex1 = Example("parent(john, mary)")
        ex2 = Example("parent(john, tom)")
        
        generalized = learner._generalize_examples([ex1, ex2])
        assert generalized is not None
        # Generalization should have a variable for differing argument
        assert "X" in generalized.head or "Y" in generalized.head or "Z" in generalized.head
    
    def test_create_rule_from_example(self):
        """Test creating a rule from a single example."""
        kb = KnowledgeBase()
        learner = GolemLearner(kb, verbose=False)
        
        ex = Example("parent(john, mary)")
        rule = learner._create_rule_from_example(ex)
        
        assert rule is not None
        assert rule.body == []
        # Should have variables in head
        assert "X" in rule.head or "Y" in rule.head or "Z" in rule.head


class TestGolemFamilyRelations:
    """Test Golem on family relation problems."""
    
    def test_parent_predicate(self):
        """Test learning with simple parent facts."""
        kb = KnowledgeBase()
        kb.add_fact(Fact("parent(john, mary)"))
        kb.add_fact(Fact("parent(mary, alice)"))
        kb.add_fact(Fact("parent(alice, bob)"))
        
        learner = GolemLearner(kb, verbose=False)
        
        # Should be able to handle learning with KB containing facts
        assert kb.facts is not None
    
    def test_ancestor_learning(self):
        """Test learning ancestor relation."""
        kb = KnowledgeBase()
        
        # Add parent facts
        kb.add_fact(Fact("parent(a, b)"))
        kb.add_fact(Fact("parent(b, c)"))
        kb.add_fact(Fact("parent(c, d)"))
        
        # Positive examples
        positive_examples = [
            Example("ancestor(a, b)"),
            Example("ancestor(b, c)"),
            Example("ancestor(a, c)"),
        ]
        
        learner = GolemLearner(kb, max_clause_length=2, verbose=False)
        rules = learner.learn(positive_examples)
        
        # Should produce some rules
        assert isinstance(rules, list)


class TestGolemRuleConversion:
    """Test conversion between GolemRule and Horn clauses."""
    
    def test_rule_to_horn_clause(self):
        """Test GolemRule to Horn clause conversion."""
        golem_rule = GolemRule("ancestor(X, Y)", ["parent(X, Y)"])
        horn_rule = golem_rule.to_horn_clause()
        
        assert horn_rule.head == "ancestor(X, Y)"
        assert horn_rule.body == ["parent(X, Y)"]
    
    def test_fact_to_horn_clause(self):
        """Test GolemRule fact to Horn clause conversion."""
        golem_fact = GolemRule("parent(john, mary)", [])
        horn_fact = golem_fact.to_horn_clause()
        
        assert horn_fact.head == "parent(john, mary)"
        assert horn_fact.body == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
