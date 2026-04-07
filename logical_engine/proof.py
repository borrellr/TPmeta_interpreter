"""
Proof Tree Structures
Defines nodes and utilities for constructing and printing proof trees.
"""

class ProofNode:
    def __init__(self, conclusion, rule=None, premises=None):
        self.conclusion = conclusion
        self.rule = rule
        self.premises = premises or []
