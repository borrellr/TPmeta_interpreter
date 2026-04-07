"""
Parser for Terms and Formulas
Optional: parse user-friendly syntax into internal term structures.
"""

import re
from .terms import Term, Variable, Constant, Function, Predicate, Equation


def parse_term(text):
    """
    Parse a term from text.
    
    Supports:
    - Variables: X, Y, Var (identifiers starting with uppercase)
    - Constants: abc, 123, "string" (lowercase identifiers, numbers, quoted strings)
    - Functions: f(a, b), parent(john, mary) (name with parenthesized arguments)
    
    Args:
        text: String representation of a term
    
    Returns:
        A Term object (Variable, Constant, or Function)
    
    Raises:
        ValueError: If the text cannot be parsed as a term
    
    Examples:
        >>> parse_term("X")
        Variable(name='X')
        >>> parse_term("123")
        Constant(value='123')
        >>> parse_term("f(a, b)")
        Function(name='f', args=[Constant('a'), Constant('b')])
    """
    text = text.strip()
    
    # Check for function/predicate with arguments: name(...)
    match = re.match(r'^([a-zA-Z_]\w*)\((.*)\)$', text)
    if match:
        name = match.group(1)
        args_text = match.group(2).strip()
        
        if not args_text:
            # Empty arguments
            args = []
        else:
            # Parse comma-separated arguments
            args = parse_arguments(args_text)
        
        return Function(name, args)
    
    # Check for variable: uppercase identifier
    if re.match(r'^[A-Z_]\w*$', text):
        return Variable(text)
    
    # Check for quoted string
    if (text.startswith('"') and text.endswith('"')) or \
       (text.startswith("'") and text.endswith("'")):
        return Constant(text[1:-1])
    
    # Check for number
    if re.match(r'^-?\d+(\.\d+)?$', text):
        return Constant(text)
    
    # Check for lowercase identifier (constant)
    if re.match(r'^[a-z_]\w*$', text):
        return Constant(text)
    
    raise ValueError(f"Cannot parse term: {text}")


def parse_arguments(args_text):
    """
    Parse comma-separated arguments, handling nested parentheses.
    
    Args:
        args_text: String containing comma-separated argument list
    
    Returns:
        List of parsed Term objects
    """
    args = []
    current_arg = ""
    paren_depth = 0
    
    for char in args_text:
        if char == '(' :
            paren_depth += 1
            current_arg += char
        elif char == ')':
            paren_depth -= 1
            current_arg += char
        elif char == ',' and paren_depth == 0:
            # Found argument separator
            if current_arg.strip():
                args.append(parse_term(current_arg.strip()))
            current_arg = ""
        else:
            current_arg += char
    
    # Don't forget the last argument
    if current_arg.strip():
        args.append(parse_term(current_arg.strip()))
    
    return args


def parse_formula(text):
    """
    Parse a formula from text.
    
    Supports:
    - Predicates: parent(john, mary), likes(X, Y)
    - Equations: X = Y, length(L) = 5
    
    Args:
        text: String representation of a formula
    
    Returns:
        A Predicate or Equation object
    
    Raises:
        ValueError: If the text cannot be parsed as a formula
    
    Examples:
        >>> parse_formula("parent(john, mary)")
        Predicate(name='parent', args=[Constant('john'), Constant('mary')])
        >>> parse_formula("X = Y")
        Equation(left=Variable('X'), right=Variable('Y'))
    """
    text = text.strip()
    
    # Check for equation: term = term
    if '=' in text:
        # Find the '=' that's not inside parentheses
        paren_depth = 0
        eq_pos = -1
        
        for i, char in enumerate(text):
            if char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            elif char == '=' and paren_depth == 0:
                eq_pos = i
                break
        
        if eq_pos != -1:
            left_text = text[:eq_pos].strip()
            right_text = text[eq_pos + 1:].strip()
            
            left_term = parse_term(left_text)
            right_term = parse_term(right_text)
            
            return Equation(left_term, right_term)
    
    # Otherwise, try to parse as a predicate
    match = re.match(r'^([a-zA-Z_]\w*)\((.*)\)$', text)
    if match:
        name = match.group(1)
        args_text = match.group(2).strip()
        
        if not args_text:
            args = []
        else:
            args = parse_arguments(args_text)
        
        return Predicate(name, args)
    
    raise ValueError(f"Cannot parse formula: {text}")
