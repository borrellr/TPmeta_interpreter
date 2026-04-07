"""
Meta-Interpreter
Coordinates unification, Horn clause evaluation, rewriting, and inference rules.
"""

import itertools

from .unification import unify, Substitution
from .horn_clauses import Rule, Fact
from .parser import parse_term
from .terms import Variable, Constant, Function

_fresh_var_counter = itertools.count()


def parse_or_term(term):
    if isinstance(term, str):
        try:
            return parse_term(term)
        except ValueError:
            return term
    return term


def freshen_term(term, var_map=None):
    if var_map is None:
        var_map = {}

    if isinstance(term, str):
        return freshen_term(parse_term(term), var_map)

    if isinstance(term, Variable):
        if term.name not in var_map:
            var_map[term.name] = f"{term.name}_fresh_{next(_fresh_var_counter)}"
        return Variable(var_map[term.name])

    if isinstance(term, Function):
        return Function(term.name, [freshen_term(arg, var_map) for arg in term.args])

    return term


def freshen_rule(rule):
    var_map = {}
    fresh_head = freshen_term(rule.head, var_map)
    fresh_body = [freshen_term(goal, var_map) for goal in rule.body]
    return fresh_head, fresh_body


def solve(goal, kb, subst=None):
    """
    Attempt to solve a goal using the knowledge base via backward chaining.
    
    Uses depth-first search with backtracking to find all solutions to a goal.
    Unifies the goal with facts and rule heads in the knowledge base, recursively
    solving rule bodies as needed.
    
    Args:
        goal: The goal to solve (a predicate/term string)
        kb: KnowledgeBase instance containing facts and rules
        subst: Optional Substitution object for tracking variable bindings
    
    Returns:
        Generator of Substitution objects representing all solutions to the goal.
        Each substitution contains variable assignments that satisfy the goal.
    
    Example:
        >>> kb = KnowledgeBase()
        >>> kb.add_fact(Fact("parent(john, mary)"))
        >>> kb.add_rule(Rule("ancestor(X, Y)", ["parent(X, Y)"]))
        >>> solutions = list(solve("ancestor(X, mary)", kb))
        >>> # solutions will contain {X: john}
    """
    if subst is None:
        subst = Substitution()
    
    goal_term = parse_or_term(goal)
    
    # Try to match goal with facts in the knowledge base
    for fact in kb.facts:
        # Apply current substitution to the fact head
        fact_head = apply_substitution(fact.head, subst)
        
        # Try to unify the goal with the fact
        new_subst = unify(goal_term, parse_or_term(fact_head), subst.copy())
        if new_subst is not None:
            yield new_subst
    
    # Try to match goal with rule heads and solve rule bodies
    for rule in kb.rules:
        fresh_head, fresh_body = freshen_rule(rule)

        # Try to unify the goal with the fresh rule head
        new_subst = unify(goal_term, fresh_head, subst.copy())
        if new_subst is not None:
            # Recursively solve all goals in the fresh rule body
            for solution in solve_goals(fresh_body, kb, new_subst):
                yield solution


def solve_goals(goals, kb, subst):
    """
    Solve a list of goals (conjunction) using the knowledge base.
    
    Args:
        goals: List of goal strings to solve
        kb: KnowledgeBase instance
        subst: Current substitution
    
    Returns:
        Generator of Substitution objects representing all solutions
    """
    if not goals:
        # Base case: all goals solved
        yield subst
        return
    
    # Solve the first goal and recurse on remaining goals
    first_goal = goals[0]
    remaining_goals = goals[1:]
    
    for solution in solve(first_goal, kb, subst):
        for final_solution in solve_goals(remaining_goals, kb, solution):
            yield final_solution


def term_to_string(term):
    if isinstance(term, Variable):
        return term.name
    if isinstance(term, Constant):
        return term.value
    if isinstance(term, Function):
        return f"{term.name}({', '.join(term_to_string(arg) for arg in term.args)})"
    return str(term)


def apply_substitution(term, subst):
    """
    Apply a substitution to a term.
    
    Args:
        term: A term (string) potentially containing variables
        subst: Substitution mapping variables to values
    
    Returns:
        The term with substitutions applied
    """
    if isinstance(term, str):
        # Simple string-based substitution (naive approach)
        result = term
        for var, value in subst.items():
            replacement = term_to_string(value) if isinstance(value, (Variable, Constant, Function)) else str(value)
            result = result.replace(var, replacement)
        return result
    return term


def prove(goal, kb):
    """
    Return a proof tree for the goal showing how it was derived.
    
    Constructs a tree structure that documents the derivation of the goal,
    showing which facts and rules were used at each step.
    
    Args:
        goal: The goal to prove
        kb: KnowledgeBase instance
    
    Returns:
        A list of proof tree dictionaries. Each dictionary has:
        - 'goal': the goal that was proven
        - 'source': 'fact' or 'rule'
        - 'subgoals': list of subgoals (if from a rule)
        - 'proofs': proofs of the subgoals (if from a rule)
        - 'substitution': the substitution that proved the goal
    
    Example:
        >>> kb.add_fact(Fact("parent(john, mary)"))
        >>> proof = prove("parent(john, mary)", kb)
        >>> # proof contains [{goal: "parent(john, mary)", source: "fact", ...}]
    """
    proofs = []
    
    goal_term = parse_or_term(goal)
    # Try to match goal with facts
    for fact in kb.facts:
        fact_head = fact.head
        subst = unify(goal_term, parse_or_term(fact_head))
        if subst is not None:
            proofs.append({
                'goal': goal,
                'source': 'fact',
                'fact': fact_head,
                'substitution': subst
            })
    
    # Try to match goal with rule heads
    for rule in kb.rules:
        rule_head = rule.head
        subst = unify(goal_term, parse_or_term(rule_head))
        if subst is not None:
            # Recursively prove all subgoals in the rule body
            subgoal_proofs = []
            all_proved = True
            
            for subgoal in rule.body:
                subgoal_proof = prove(subgoal, kb)
                if subgoal_proof:
                    subgoal_proofs.append(subgoal_proof)
                else:
                    all_proved = False
                    break
            
            if all_proved or not rule.body:
                # All subgoals proved (or rule body is empty)
                proofs.append({
                    'goal': goal,
                    'source': 'rule',
                    'rule_head': rule_head,
                    'subgoals': rule.body,
                    'subgoal_proofs': subgoal_proofs,
                    'substitution': subst
                })
    
    return proofs
