"""
Inductive Logic Programming (ILP) Module
Implements FOIL (First-Order Inductive Learner) algorithm.
"""

import sys
sys.path.insert(0, '/work/TPmeta_interpreter')

from logical_engine.meta_interpreter import solve
from logical_engine.horn_clauses import KnowledgeBase, Rule, Fact
from logical_engine.parser import parse_term
from logical_engine.terms import Variable, Function


class Example:
    """Represents a training example for ILP."""
    
    def __init__(self, goal, label=True):
        """
        Args:
            goal: Goal string (e.g., "ancestor(john, alice)")
            label: True for positive example, False for negative
        """
        self.goal = goal
        self.label = label
    
    def __repr__(self):
        label_str = "+" if self.label else "-"
        return f"Example({label_str} {self.goal})"


def solves(rule, example, kb=None):
    """
    Check if a rule covers (explains) an example.
    
    Args:
        rule: Rule object
        example: Example object
        kb: Optional KnowledgeBase with additional facts
    
    Returns:
        True if the rule covers the example, False otherwise
    """
    if kb is None:
        kb = KnowledgeBase()
    
    # Create a temporary KB with the rule added
    temp_kb = KnowledgeBase()
    temp_kb.facts = kb.facts.copy()
    temp_kb.rules = kb.rules + [rule]
    
    # Try to solve the example goal with the temporary KB
    try:
        solutions = list(solve(example.goal, temp_kb))
        return len(solutions) > 0
    except:
        return False


def covers_negatives(rule, negatives, kb=None):
    """
    Check if a rule covers any negative examples (bad).
    
    Args:
        rule: Rule object
        negatives: List of negative Example objects
        kb: Optional KnowledgeBase
    
    Returns:
        True if rule covers any negative example, False otherwise
    """
    if kb is None:
        kb = KnowledgeBase()
    
    for negative_example in negatives:
        if solves(rule, negative_example, kb):
            return True
    return False


def recall(rule, positive_examples, kb=None):
    """
    Calculate recall: fraction of positive examples covered by rule.
    
    Args:
        rule: Rule object
        positive_examples: List of positive Example objects
        kb: Optional KnowledgeBase
    
    Returns:
        Float in [0, 1]
    """
    if kb is None:
        kb = KnowledgeBase()
    
    if not positive_examples:
        return 0.0
    
    covered = sum(1 for ex in positive_examples if solves(rule, ex, kb))
    return covered / len(positive_examples)


def precision(rule, positive_examples, negative_examples, kb=None):
    """
    Calculate precision: fraction of covered examples that are positive.
    
    Args:
        rule: Rule object
        positive_examples: List of positive Example objects
        negative_examples: List of negative Example objects
        kb: Optional KnowledgeBase
    
    Returns:
        Float in [0, 1]
    """
    if kb is None:
        kb = KnowledgeBase()
    
    all_examples = positive_examples + negative_examples
    if not all_examples:
        return 0.0
    
    covered_positives = sum(1 for ex in positive_examples if solves(rule, ex, kb))
    covered_total = sum(1 for ex in all_examples if solves(rule, ex, kb))
    
    if covered_total == 0:
        return 0.0
    
    return covered_positives / covered_total


def information_gain(rule, positive_examples, negative_examples, kb=None):
    """
    Calculate information gain (fitness score) for a rule.
    
    Measures how well the rule discriminates positives from negatives.
    
    Args:
        rule: Rule object
        positive_examples: List of positive Example objects
        negative_examples: List of negative Example objects
        kb: Optional KnowledgeBase
    
    Returns:
        Float (higher is better)
    """
    if kb is None:
        kb = KnowledgeBase()
    
    pos_covered = sum(1 for ex in positive_examples if solves(rule, ex, kb))
    neg_covered = sum(1 for ex in negative_examples if solves(rule, ex, kb))
    
    # Prefer rules covering many positives, few negatives
    # Avoid division by zero
    return pos_covered / (neg_covered + 1)


def specialize_clause(rule, new_literal):
    """
    Create a specialized version of a rule by adding a literal to its body.
    
    Args:
        rule: Original Rule object
        new_literal: String representation of the new literal (e.g., "parent(X, Z)")
    
    Returns:
        New Rule object with extended body
    """
    new_body = rule.body + [new_literal]
    return Rule(rule.head, new_body)


def generate_specializations(rule, predicates):
    """
    Generate candidate specializations by adding literals to rule body.
    
    Args:
        rule: Rule object to specialize
        predicates: List of callable predicates (strings) to try adding
                   e.g., ["parent(X, Z)", "ancestor(X, Z)", "sibling(X, Y)"]
    
    Returns:
        List of new Rule objects
    """
    candidates = []
    for pred in predicates:
        new_rule = specialize_clause(rule, pred)
        candidates.append(new_rule)
    return candidates


def extract_variables(goal_string):
    """
    Extract variable names from a goal string.
    
    Args:
        goal_string: Goal string like "ancestor(X, Y)"
    
    Returns:
        Set of variable names
    """
    try:
        term = parse_term(goal_string)
        vars_set = set()
        
        def collect_vars(t):
            if isinstance(t, Variable):
                vars_set.add(t.name)
            elif isinstance(t, Function):
                for arg in t.args:
                    collect_vars(arg)
        
        collect_vars(term)
        return vars_set
    except:
        return set()


def foil_learn(target_predicate, positive_examples, negative_examples, 
               available_predicates=None, kb=None, max_specializations=50, beam_width=1):
    """
    Learn rules using FOIL algorithm.
    
    Starts with the most general clause and iteratively specializes it
    by adding body literals until all positives are covered without
    covering negatives.
    
    Args:
        target_predicate: Name of predicate to learn (e.g., "ancestor")
        positive_examples: List of positive Example objects
        negative_examples: List of negative Example objects
        available_predicates: List of predicates to use in specialization.
                            Default: basic arithmetic and structure predicates
        kb: Optional KnowledgeBase with initial facts/rules
        max_specializations: Maximum specialization steps
        beam_width: Beam width for search (1=greedy, >1=beam search)
    
    Returns:
        List of learned Rule objects (clauses)
    """
    if kb is None:
        kb = KnowledgeBase()
    
    if available_predicates is None:
        available_predicates = [
            "parent(X, Z)", "parent(Z, X)", "parent(Y, Z)", "parent(Z, Y)",
            "sibling(X, Z)", "sibling(Z, X)", "sibling(Y, Z)", "sibling(Z, Y)",
            "ancestor(X, Z)", "ancestor(Z, X)", "ancestor(Y, Z)", "ancestor(Z, Y)",
            "equal(X, Y)", "equal(X, Z)", "equal(Y, Z)",
        ]
    
    learned_rules = []
    remaining_positives = positive_examples.copy()
    
    # Generate most general clause
    vars_in_examples = set()
    for ex in positive_examples:
        vars_in_examples.update(extract_variables(ex.goal))
    
    vars_list = sorted(list(vars_in_examples))[:3]  # Limit to reasonable number
    if not vars_list:
        vars_list = ["X", "Y"]
    
    general_head = f"{target_predicate}({', '.join(vars_list)})"
    current_rule = Rule(general_head, [])
    
    # Iteratively specialize
    for iteration in range(max_specializations):
        if not remaining_positives:
            break
        
        # If current rule covers no negatives, we're done specializing this clause
        if not covers_negatives(current_rule, negative_examples, kb):
            learned_rules.append(current_rule)
            # Remove covered positives from remaining
            remaining_positives = [
                ex for ex in remaining_positives 
                if not solves(current_rule, ex, kb)
            ]
            
            if remaining_positives:
                # Start a new clause
                current_rule = Rule(general_head, [])
            else:
                break
        else:
            # Specialize further
            candidates = generate_specializations(current_rule, available_predicates)
            
            # Score each candidate
            scored_candidates = []
            for candidate in candidates:
                gain = information_gain(candidate, remaining_positives, negative_examples, kb)
                scored_candidates.append((gain, candidate))
            
            # Sort by gain and keep beam_width best
            scored_candidates.sort(reverse=True, key=lambda x: x[0])
            
            if scored_candidates:
                _, current_rule = scored_candidates[0]
            else:
                # No improvement possible
                break
    
    # Add final rule if it covers positives without negatives
    if current_rule.body and not covers_negatives(current_rule, negative_examples, kb):
        learned_rules.append(current_rule)
    elif not covers_negatives(current_rule, negative_examples, kb):
        learned_rules.append(current_rule)
    
    return learned_rules
