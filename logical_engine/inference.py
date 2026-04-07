"""
Logical Inference Rules
Implements Modus Ponens, Modus Tollens, Universal Instantiation, and Resolution.
"""

def modus_ponens(p, implies_p_q):
    """
    Modus Ponens: If p is true and p→q is true, then q is true.
    
    Args:
        p: A proposition (premise)
        implies_p_q: An implication rule in the form {'premise': p, 'conclusion': q}
    
    Returns:
        The conclusion q if the implication matches p, otherwise None
    """
    if isinstance(implies_p_q, dict) and implies_p_q.get('premise') == p:
        return implies_p_q.get('conclusion')
    return None

def modus_tollens(not_q, implies_p_q):
    """
    Modus Tollens: If ¬q is true and p→q is true, then ¬p is true.
    
    Args:
        not_q: A negated proposition (the negation of the conclusion)
        implies_p_q: An implication rule in the form {'premise': p, 'conclusion': q}
    
    Returns:
        The negation of the premise if the implication's conclusion matches q, otherwise None
    """
    if isinstance(implies_p_q, dict):
        conclusion = implies_p_q.get('conclusion')
        premise = implies_p_q.get('premise')
        # Check if not_q matches the negation of the conclusion
        if conclusion == not_q or (isinstance(not_q, str) and not_q == f"¬{conclusion}"):
            # Return negation of premise
            if isinstance(premise, str):
                return f"¬{premise}" if not premise.startswith('¬') else premise[1:]
            return f"¬{premise}"
    return None

def universal_instantiation(forall_formula, constant):
    """
    Universal Instantiation: From ∀x P(x), we can derive P(c) for any constant c.
    
    Args:
        forall_formula: A universally quantified formula in the form {'type': 'forall', 'variable': 'x', 'formula': 'P(x)'}
        constant: A constant to instantiate the variable with
    
    Returns:
        The instantiated formula with the constant replacing the variable, or None if invalid
    """
    if isinstance(forall_formula, dict) and forall_formula.get('type') == 'forall':
        variable = forall_formula.get('variable')
        formula = forall_formula.get('formula')
        
        if isinstance(formula, str) and variable:
            # Replace the variable with the constant in the formula
            instantiated = formula.replace(variable, str(constant))
            return instantiated
    return None

def resolve(clause1, clause2):
    """
    Resolution: If clause1 contains literal L and clause2 contains ¬L, 
    we can derive a new clause by removing L and ¬L and combining the rest.
    
    Args:
        clause1: A clause represented as a set or list of literals
        clause2: Another clause represented as a set or list of literals
    
    Returns:
        A new clause (set) resulting from resolving the two clauses, 
        or None if they don't have complementary literals
    """
    # Convert to sets if needed
    c1 = set(clause1) if not isinstance(clause1, set) else clause1.copy()
    c2 = set(clause2) if not isinstance(clause2, set) else clause2.copy()
    
    # Find complementary literals
    complementary_pairs = []
    for lit1 in c1:
        for lit2 in c2:
            # Check if lit2 is the negation of lit1
            lit1_str = str(lit1)
            lit2_str = str(lit2)
            
            # Handle different negation formats
            if ((lit1_str.startswith('¬') and lit2_str == lit1_str[1:]) or
                (lit2_str.startswith('¬') and lit1_str == lit2_str[1:]) or
                (lit1_str.startswith('~') and lit2_str == lit1_str[1:]) or
                (lit2_str.startswith('~') and lit1_str == lit2_str[1:]) or
                (lit1_str.startswith('not_') and lit2_str == lit1_str[4:]) or
                (lit2_str.startswith('not_') and lit1_str == lit2_str[4:])):
                complementary_pairs.append((lit1, lit2))
    
    # If complementary literals found, perform resolution
    if complementary_pairs:
        lit1, lit2 = complementary_pairs[0]
        resolved = (c1 - {lit1}) | (c2 - {lit2})
        return resolved if resolved else set()  # Return empty set if resolvent is empty clause
    
    return None
