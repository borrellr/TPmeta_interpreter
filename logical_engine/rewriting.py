"""
Term Rewriting System
Supports rewrite rules, normalization, and rule application.
"""

from .parser import parse_term
from .terms import Term, Variable, Constant, Function
from .unification import unify, Substitution


def parse_or_term(term):
    if isinstance(term, str):
        try:
            return parse_term(term)
        except ValueError:
            return term
    return term


def term_to_string(term):
    if isinstance(term, Variable):
        return term.name
    if isinstance(term, Constant):
        return term.value
    if isinstance(term, Function):
        return f"{term.name}({', '.join(term_to_string(arg) for arg in term.args)})"
    return str(term)


class RewriteRule:
    def __init__(self, lhs, rhs, name=None):
        self.lhs = lhs
        self.rhs = rhs
        self.name = name


def rewrite_once(term, rules):
    """
    Apply one rewrite rule to a term.
    
    Attempts to match the left-hand side of each rewrite rule against the term
    or any subterm. On the first successful match, applies the substitution to
    the right-hand side and returns the rewritten term. If no rules match,
    returns the original term unchanged.
    
    Args:
        term: A term to be rewritten (Variable, Constant, Function, or string)
        rules: List of RewriteRule objects with lhs and rhs attributes
    
    Returns:
        A rewritten term if a rule matched, otherwise the original term unchanged
    
    Examples:
        rule = RewriteRule("f(X, X)", "g(X)")
        rewrite_once("f(a, a)", [rule])  # Returns "g(a)"
        rewrite_once("f(a, b)", [rule])  # Returns "f(a, b)" (no match)
    """
    original_was_string = isinstance(term, str)
    parsed_term = parse_or_term(term)

    # Try to apply each rule
    for rule in rules:
        lhs = parse_or_term(rule.lhs)
        subst = unify(lhs, parsed_term)
        if subst is not None:
            # Successfully unified - apply substitution to RHS
            rewritten = apply_substitution_to_term(parse_or_term(rule.rhs), subst)
            return term_to_string(rewritten) if original_was_string else rewritten
    
    # If parsed_term is a Function, try rewriting subterms
    if isinstance(parsed_term, Function):
        for i, arg in enumerate(parsed_term.args):
            rewritten_arg = rewrite_once(arg, rules)
            if rewritten_arg != arg:
                # One of the arguments was rewritten
                new_args = parsed_term.args[:i] + [rewritten_arg] + parsed_term.args[i+1:]
                rewritten = Function(parsed_term.name, new_args)
                return term_to_string(rewritten) if original_was_string else rewritten
    
    # No rules matched
    return term


def normalize(term, rules, max_iterations=None):
    """
    Normalize a term by repeatedly applying rewrite rules.
    
    Applies rewrite rules until reaching a fixed point (no more rules can be
    applied) or until reaching the maximum number of iterations. This simulates
    term reduction/evaluation using the given rewrite system.
    
    Args:
        term: A term to be normalized
        rules: List of RewriteRule objects
        max_iterations: Optional maximum number of rewriting steps (default: 1000)
    
    Returns:
        The normalized (fully reduced) term
    
    Examples:
        rules = [
            RewriteRule("f(X)", "g(X)"),
            RewriteRule("g(X)", "h(X)")
        ]
        normalize("f(a)", rules)  # Returns "h(a)"
    """
    if max_iterations is None:
        max_iterations = 1000
    
    current = term
    iterations = 0
    
    while iterations < max_iterations:
        # Apply one rewrite step
        next_term = rewrite_once(current, rules)
        
        # Check if we've reached a fixed point (no change)
        if terms_equal(current, next_term):
            break
        
        current = next_term
        iterations += 1
    
    return current


def apply_substitution_to_term(term, subst):
    """
    Apply a substitution to a term.
    
    Args:
        term: A term object
        subst: A Substitution (dict-like) mapping variables to terms
    
    Returns:
        The term with substitutions applied
    """
    if isinstance(term, Variable):
        # Check if variable is in substitution
        if term.name in subst:
            return subst[term.name]
        return term
    
    elif isinstance(term, Constant):
        return term
    
    elif isinstance(term, Function):
        # Recursively apply substitution to arguments
        new_args = [apply_substitution_to_term(arg, subst) for arg in term.args]
        return Function(term.name, new_args)
    
    # Handle string representation
    elif isinstance(term, str):
        result = term
        for var, value in subst.items():
            result = result.replace(var, str(value))
        return result
    
    return term


def terms_equal(t1, t2):
    """
    Check if two terms are structurally equal.
    
    Args:
        t1: First term
        t2: Second term
    
    Returns:
        True if terms are equal, False otherwise
    """
    if type(t1) != type(t2):
        return False
    
    if isinstance(t1, Variable):
        return t1.name == t2.name
    
    elif isinstance(t1, Constant):
        return t1.value == t2.value
    
    elif isinstance(t1, Function):
        return t1.name == t2.name and \
               len(t1.args) == len(t2.args) and \
               all(terms_equal(a1, a2) for a1, a2 in zip(t1.args, t2.args))
    
    elif isinstance(t1, str) and isinstance(t2, str):
        return t1 == t2
    
    return False
