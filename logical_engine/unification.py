"""
Unification Algorithm
Provides unification with occurs-check and substitution objects.
"""

from .terms import Variable, Constant, Function


class Substitution(dict):
    """
    A substitution is a mapping from variables to terms.
    
    Extends dict to represent variable bindings created during unification.
    Keys are variable names (strings), values are terms.
    """

    def copy(self):
        """Return a shallow copy preserving the Substitution subclass."""
        return Substitution(self)

    def __copy__(self):
        return self.copy()

    def apply(self, term):
        """Apply this substitution to a term."""
        from .rewriting import apply_substitution_to_term
        return apply_substitution_to_term(term, self)

    def compose(self, other):
        """
        Compose two substitutions.
        
        Returns a new substitution where bindings from both are combined.
        If the same variable appears in both, 'other' takes precedence.
        """
        result = Substitution(self)
        for var, term in other.items():
            result[var] = result.apply(term)
        return result

    def rename(self, old_var, new_var):
        """Rename a variable throughout the substitution."""
        if old_var in self:
            self[new_var] = self.pop(old_var)

    def __repr__(self):
        """Return a readable representation."""
        items = [f"{k}: {v}" for k, v in self.items()]
        return "{" + ", ".join(items) + "}"

def unify(t1, t2, subst=None):
    """
    Unify two terms and return a substitution or None.
    
    Implements the Robinson unification algorithm with occurs-check.
    Finds a substitution that makes t1 and t2 structurally equal.
    
    Args:
        t1: First term (Variable, Constant, Function, or string)
        t2: Second term (Variable, Constant, Function, or string)
        subst: Optional initial substitution (Substitution object)
    
    Returns:
        A Substitution object if unification succeeds, None otherwise
    
    Examples:
        >>> unify(Variable('X'), Constant('a'))
        {'X': Constant('a')}
        >>> unify(Function('f', [Variable('X')]), Function('f', [Constant('a')]))
        {'X': Constant('a')}
        >>> unify(Constant('a'), Constant('b'))
        None
    """
    if subst is None:
        subst = Substitution()
    else:
        subst = subst.copy()
    
    # Dereference terms by applying current substitution
    t1 = deref(t1, subst)
    t2 = deref(t2, subst)
    
    # Case 1: Same term (after dereferencing)
    if terms_equal(t1, t2):
        return subst
    
# Case 2: Both are variables
    if isinstance(t1, Variable) and isinstance(t2, Variable):
        if t1.name == t2.name:
            return subst
        if occurs_check(t2.name, t1, subst):
            return None
        subst[t2.name] = t1
        return subst

    # Case 3: t1 is a variable
    if isinstance(t1, Variable):
        # Occurs-check: prevent X = f(X)
        if occurs_check(t1.name, t2, subst):
            return None
        subst[t1.name] = t2
        return subst

    # Case 4: t2 is a variable
    if isinstance(t2, Variable):
        # Occurs-check: prevent X = f(X)
        if occurs_check(t2.name, t1, subst):
            return None
        subst[t2.name] = t1
        return subst
    
    # Case 4: Both are strings (for simple string-based representation)
    if isinstance(t1, str) and isinstance(t2, str):
        if t1 == t2:
            return subst
        # Try to parse as variables
        if t1[0].isupper():
            if occurs_check(t1, t2, subst):
                return None
            subst[t1] = t2
            return subst
        if t2[0].isupper():
            if occurs_check(t2, t1, subst):
                return None
            subst[t2] = t1
            return subst
        return None
    
    # Case 5: Both are constants
    if isinstance(t1, Constant) and isinstance(t2, Constant):
        if t1.value == t2.value:
            return subst
        return None
    
    # Case 6: Both are functions
    if isinstance(t1, Function) and isinstance(t2, Function):
        # Must have same name and arity
        if t1.name != t2.name or len(t1.args) != len(t2.args):
            return None
        
        # Unify arguments pairwise
        for arg1, arg2 in zip(t1.args, t2.args):
            subst = unify(arg1, arg2, subst)
            if subst is None:
                return None
        
        return subst
    
    # Case 7: No unification possible
    return None


def deref(term, subst):
    """
    Dereference a term by following substitution chains.
    
    If term is a variable bound in the substitution, returns the
    binding. Recursively dereferences to handle chains of bindings.
    """
    if isinstance(term, Variable):
        if term.name in subst:
            # Recursively dereference the binding
            return deref(subst[term.name], subst)
        return term
    
    elif isinstance(term, str) and term and term[0].isupper():
        # Handle string-based variables
        if term in subst:
            return deref(subst[term], subst)
        return term
    
    elif isinstance(term, Function):
        return Function(term.name, [deref(arg, subst) for arg in term.args])

    return term


def occurs_check(var_name, term, subst):
    """
    Check if a variable occurs in a term (with dereferencing).
    
    Prevents creating cyclic structures like X = f(X).
    
    Args:
        var_name: The variable name to check for
        term: The term to search in
        subst: The current substitution
    
    Returns:
        True if var_name occurs in term, False otherwise
    """
    term = deref(term, subst)
    
    if isinstance(term, Variable):
        return var_name == term.name
    
    elif isinstance(term, str) and term[0].isupper():
        return var_name == term
    
    elif isinstance(term, Constant):
        return False
    
    elif isinstance(term, Function):
        # Check if variable occurs in any argument
        return any(occurs_check(var_name, arg, subst) for arg in term.args)
    
    return False


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
