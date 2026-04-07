"""
Term and Formula Definitions
Defines the core data structures for algebraic terms and logical formulas.
"""

class Term:
    pass

class Variable(Term):
    def __init__(self, name):
        self.name = name

class Constant(Term):
    def __init__(self, value):
        self.value = value

class Function(Term):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Predicate:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Equation:
    def __init__(self, left, right):
        self.left = left
        self.right = right
