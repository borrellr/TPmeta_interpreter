"""
Golem ILP System - Muggleton and Feng's Inductive Logic Programming System

A bottom-up inductive logic programming learner using relative least-general
generalization (LGG) under background theory.
"""

from .golem_learner import (
    GolemLearner,
    Example,
    GolemRule,
)

__all__ = [
    "GolemLearner",
    "Example",
    "GolemRule",
]
