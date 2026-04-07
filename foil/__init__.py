"""
FOIL: First-Order Inductive Learner
A top-down refinement learner for learning Horn clauses from examples.

Based on Quinlan's FOIL algorithm, adapted to use logical_engine components.
"""

from .ilp import (
    Example,
    foil_learn,
    information_gain,
    covers_negatives,
    solves,
    specialize_clause,
    generate_specializations,
)

__all__ = [
    "Example",
    "foil_learn",
    "information_gain",
    "covers_negatives",
    "solves",
    "specialize_clause",
    "generate_specializations",
]
