"""
Ivan Bratko's Advice Logic 3 System

A classic knowledge representation system using Horn clauses that provides
recommendations based on factual conditions. This implementation follows the
educational example from "Programming in Prolog" and demonstrates:

- Factual knowledge representation
- Rule-based inference
- Backward chaining reasoning
- Meta-interpretation over logical rules

Typical application: Recommending whether to play tennis based on weather
and court conditions, or similar decision-making scenarios.
"""

from .advice_logic_3 import AdviceLogic3, create_default_kb

__all__ = ['AdviceLogic3', 'create_default_kb']
