"""
Example usage of FOIL learner with logical_engine.
"""

import sys
sys.path.insert(0, '/work/TPmeta_interpreter')

from foil.ilp import (
    Example,
    foil_learn,
    information_gain,
    covers_negatives,
    solves,
)
from logical_engine.horn_clauses import KnowledgeBase, Fact, Rule


def example_ancestor_learning():
    """
    Learn ancestor rules from parent examples.
    """
    print("=" * 60)
    print("Learning Ancestor Rules with FOIL")
    print("=" * 60)
    
    # Create knowledge base with facts
    kb = KnowledgeBase()
    kb.add_fact(Fact("parent(john, mary)"))
    kb.add_fact(Fact("parent(mary, alice)"))
    kb.add_fact(Fact("parent(john, bob)"))
    kb.add_fact(Fact("parent(bob, charlie)"))
    
    # Create training examples
    positive_examples = [
        Example("ancestor(john, mary)", True),
        Example("ancestor(john, alice)", True),
        Example("ancestor(john, bob)", True),
        Example("ancestor(john, charlie)", True),
        Example("ancestor(mary, alice)", True),
        Example("ancestor(bob, charlie)", True),
    ]
    
    negative_examples = [
        Example("ancestor(mary, john)", False),
        Example("ancestor(alice, john)", False),
        Example("ancestor(charlie, bob)", False),
    ]
    
    # Define available predicates for learning
    predicates = [
        "parent(X, Y)",
        "parent(X, Z)",
        "parent(Y, Z)",
        "ancestor(X, Z)",
        "ancestor(Z, Y)",
    ]
    
    print(f"\nKnowledge Base Facts:")
    for fact in kb.facts:
        print(f"  {fact.head}")
    
    print(f"\nPositive Examples (+):")
    for ex in positive_examples:
        print(f"  {ex.goal}")
    
    print(f"\nNegative Examples (-):")
    for ex in negative_examples:
        print(f"  {ex.goal}")
    
    # Learn rules
    learned_rules = foil_learn(
        "ancestor",
        positive_examples,
        negative_examples,
        available_predicates=predicates,
        kb=kb,
        max_specializations=10
    )
    
    print(f"\nLearned Rules:")
    for i, rule in enumerate(learned_rules, 1):
        body_str = ", ".join(rule.body) if rule.body else "true"
        print(f"  {i}. {rule.head} :- {body_str}")
    
    # Verify rules against examples
    print(f"\nVerification:")
    print(f"  Positive examples covered:")
    for ex in positive_examples:
        covered = any(solves(rule, ex, kb) for rule in learned_rules)
        status = "✓" if covered else "✗"
        print(f"    {status} {ex.goal}")
    
    print(f"  Negative examples covered:")
    for ex in negative_examples:
        covered = any(solves(rule, ex, kb) for rule in learned_rules)
        status = "✗" if covered else "✓"
        print(f"    {status} {ex.goal}")


def example_simple_learning():
    """
    Learn simple rules from basic facts.
    """
    print("\n" + "=" * 60)
    print("Learning Simple Rules")
    print("=" * 60)
    
    kb = KnowledgeBase()
    kb.add_fact(Fact("bird(tweety)"))
    kb.add_fact(Fact("bird(polly)"))
    kb.add_fact(Fact("bird(rover)"))
    kb.add_fact(Fact("fly(tweety)"))
    kb.add_fact(Fact("fly(polly)"))
    kb.add_fact(Fact("fly(rover)"))
    
    positive_examples = [
        Example("fly(tweety)", True),
        Example("fly(polly)", True),
        Example("fly(rover)", True),
    ]
    
    negative_examples = [
        Example("fly(fido)", False),
    ]
    
    predicates = [
        "bird(X)",
        "bird(Y)",
    ]
    
    print(f"\nKnowledge Base:")
    for fact in kb.facts:
        print(f"  {fact.head}")
    
    print(f"\nExamples:")
    for ex in positive_examples:
        print(f"  + {ex.goal}")
    for ex in negative_examples:
        print(f"  - {ex.goal}")
    
    learned_rules = foil_learn(
        "fly",
        positive_examples,
        negative_examples,
        available_predicates=predicates,
        kb=kb
    )
    
    print(f"\nLearned Rules:")
    for i, rule in enumerate(learned_rules, 1):
        body_str = ", ".join(rule.body) if rule.body else "true"
        print(f"  {i}. {rule.head} :- {body_str}")


if __name__ == "__main__":
    example_ancestor_learning()
    example_simple_learning()
    print("\n" + "=" * 60)
    print("FOIL Learning Examples Complete")
    print("=" * 60)
