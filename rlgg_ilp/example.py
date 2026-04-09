#!/usr/bin/env python3
"""
Example usage of the RLGG ILP System
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from rlgg_ilp import RLGGSystem, Clause
from logical_engine.horn_clauses import KnowledgeBase, Fact, Rule

def main():
    print("RLGG ILP System Demo")
    print("=" * 30)

    # Example 1: Learning the parent relationship
    print("\n1. Learning the parent relationship:")
    ilp = RLGGSystem()

    examples = [
        Clause("parent(john, mary)"),
        Clause("parent(alice, bob)")
    ]

    rule = ilp.learn_rule(examples)
    print(f"Examples: {[str(ex) for ex in examples]}")
    print(f"Learned rule: {rule.head} :- {', '.join(rule.body) if rule.body else 'true'}")

    # Example 2: Learning ancestor relationship with background knowledge
    print("\n2. Learning ancestor relationship:")
    bk = KnowledgeBase()
    bk.add_fact(Fact("parent(john, mary)"))
    bk.add_fact(Fact("parent(mary, alice)"))

    ilp_with_bk = RLGGSystem(bk)

    examples = [
        Clause("ancestor(john, mary)", ["parent(john, mary)"]),
        Clause("ancestor(mary, alice)", ["parent(mary, alice)"])
    ]

    rule = ilp_with_bk.learn_rule(examples)
    print(f"Examples: {[str(ex) for ex in examples]}")
    print(f"Background knowledge: {[str(f.head) for f in bk.facts]}")
    print(f"Learned rule: {rule.head} :- {', '.join(rule.body)}")

    # Example 3: Learning a more complex rule
    print("\n3. Learning a complex relationship:")
    examples = [
        Clause("grandparent(X, Y)", ["parent(X, Z)", "parent(Z, Y)"]),
        Clause("grandparent(A, B)", ["parent(A, C)", "parent(C, B)"])
    ]

    rule = ilp.learn_rule(examples)
    print(f"Examples: {[str(ex) for ex in examples]}")
    print(f"Learned rule: {rule.head} :- {', '.join(rule.body)}")

if __name__ == "__main__":
    main()
