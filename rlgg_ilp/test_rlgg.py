"""
Test cases for RLGG ILP System
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rlgg_ilp import RLGGSystem, Clause


def test_basic_lgg():
    """Test basic LGG computation."""
    system = RLGGSystem()

    # Test LGG of two facts
    fact1 = Clause("p(a)")
    fact2 = Clause("p(b)")

    lgg = system.lgg(fact1, fact2)
    print(f"LGG of {fact1} and {fact2}: {lgg}")

    # Test LGG with variables
    fact3 = Clause("p(X)")
    fact4 = Clause("p(a)")

    lgg2 = system.lgg(fact3, fact4)
    print(f"LGG of {fact3} and {fact4}: {lgg2}")

    # Test LGG that should work
    fact5 = Clause("parent(john, mary)")
    fact6 = Clause("parent(mary, alice)")

    lgg3 = system.lgg(fact5, fact6)
    print(f"LGG of {fact5} and {fact6}: {lgg3}")


def test_rule_learning():
    """Test learning rules from examples."""
    system = RLGGSystem()

    # Learn parent relationship - these should generalize to parent(X, Y)
    examples = [
        Clause("parent(john, mary)"),
        Clause("parent(alice, bob)")  # Different constants that can unify
    ]

    rule = system.learn_rule(examples)
    print(f"Learned rule: {rule}")
    if rule:
        print(f"  Head: {rule.head}")
        print(f"  Body: {rule.body}")


def test_complex_example():
    """Test with more complex examples."""
    system = RLGGSystem()

    # Examples for ancestor relationship
    # These should generalize to ancestor(X, Y) :- parent(X, Y)
    examples = [
        Clause("ancestor(john, mary)", ["parent(john, mary)"]),
        Clause("ancestor(alice, bob)", ["parent(alice, bob)"])
    ]

    rule = system.learn_rule(examples)
    print(f"Learned ancestor rule: {rule}")
    if rule:
        print(f"  Head: {rule.head}")
        print(f"  Body: {rule.body}")


if __name__ == "__main__":
    print("Testing RLGG ILP System")
    print("=" * 30)

    test_basic_lgg()
    print()
    test_rule_learning()
    print()
    test_complex_example()