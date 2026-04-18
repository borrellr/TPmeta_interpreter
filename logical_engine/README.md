# Logical Engine

A Python implementation of a **deductive reasoning system** based on Horn clause logic. It provides backward-chaining inference, unification, term rewriting, and meta-interpretation capabilities.

## Overview

The Logical Engine is a Prolog-like system that reasons over logical rules and facts to derive conclusions. It's ideal for educational purposes, expert systems, knowledge representation, and as a foundation for inductive logic programming (ILP).

## Features

✅ **Horn clause reasoning** — Facts, rules, and backward chaining  
✅ **Unification** — First-order unification with occurs-check  
✅ **Backward chaining** — Depth-first search with backtracking  
✅ **Term rewriting** — Pattern-based term transformation  
✅ **Parsing** — Natural syntax for predicates and terms  
✅ **Proof trees** — Trace derivations and proofs  
✅ **Type-safe** — Clean OOP design with Variable, Constant, Function classes  

## Installation

```bash
# Python 3.12+
cd /work/TPmeta_interpreter

# Set PYTHONPATH
export PYTHONPATH=/work/TPmeta_interpreter
```

## Quick Start

### 1. Basic Facts and Rules

```python
from logical_engine.horn_clauses import KnowledgeBase, Fact, Rule
from logical_engine.meta_interpreter import solve

# Create knowledge base
kb = KnowledgeBase()

# Add facts
kb.add_fact(Fact("parent(john, mary)"))
kb.add_fact(Fact("parent(mary, alice)"))

# Add rules
kb.add_rule(Rule("child(X, Y)", ["parent(Y, X)"]))
kb.add_rule(Rule("ancestor(X, Y)", ["parent(X, Y)"]))
kb.add_rule(Rule("ancestor(X, Y)", ["parent(X, Z)", "ancestor(Z, Y)"]))

# Display knowledge base contents
kb.display_kb_contents()

# Query
solutions = list(solve("ancestor(john, alice)", kb))
print(f"Found {len(solutions)} solution(s)")
```

### 2. Unification and Substitution

```python
from logical_engine.unification import unify, Substitution
from logical_engine.terms import Variable, Constant, Function

x = Variable("X")
y = Variable("Y")
a = Constant("a")

# Unify X with 'a'
subst = unify(x, a)
print(subst)  # {X: a}

# Unify compound terms
f_x = Function("f", [x])
f_a = Function("f", [a])
subst = unify(f_x, f_a)
print(subst)  # {X: a}
```

### 3. Term Parsing and Composition

```python
from logical_engine.parser import parse_term

# Parse string representation
term = parse_term("ancestor(john, X)")
print(term)  # Function with name='ancestor', args=[Constant('john'), Variable('X')]

# Rewriting
from logical_engine.rewriting import RewriteRule, rewrite_once
rule = RewriteRule("f(X, X)", "g(X)")
result = rewrite_once("f(a, a)", [rule])
print(result)  # "g(a)"
```

### 4. Proof Trees

```python
from logical_engine.meta_interpreter import prove

proofs = prove("ancestor(john, alice)", kb)
for proof in proofs:
    print(f"Source: {proof.get('source')}")
    print(f"Goal: {proof.get('goal')}")
    print(f"Substitution: {proof.get('substitution')}")
```

## Architecture

```
logical_engine/
├── terms.py              — Term data structures
│   ├── Term
│   ├── Variable
│   ├── Constant
│   ├── Function
│   ├── Predicate
│   └── Equation
│
├── unification.py        — Unification algorithm
│   ├── unify()
│   ├── deref()
│   ├── occurs_check()
│   └── Substitution (dict subclass)
│
├── parser.py             — String → Term parsing
│   ├── parse_term()
│   ├── parse_formula()
│   └── parse_arguments()
│
├── horn_clauses.py       — Knowledge representation
│   ├── Fact
│   ├── Rule
│   └── KnowledgeBase
│
├── meta_interpreter.py   — Inference engine
│   ├── solve()           — Backward chaining
│   ├── solve_goals()     — Solve conjunctions
│   ├── prove()           — Build proof tree
│   └── apply_substitution()
│
├── inference.py          — Classical inference rules
│   ├── modus_ponens()
│   ├── modus_tollens()
│   └── syllogism()
│
├── rewriting.py          — Term rewriting
│   ├── RewriteRule
│   ├── rewrite_once()
│   ├── normalize()
│   └── apply_substitution_to_term()
│
└── kb.py                 — Knowledge base utilities
```

## Core Classes

### Term Hierarchy

```python
class Term:
    """Base class for all terms."""
    pass

class Variable(Term):
    """Represents a logical variable (e.g., X, Y, Z)."""
    def __init__(self, name: str)

class Constant(Term):
    """Represents a constant value (e.g., 'john', 123)."""
    def __init__(self, value: str)

class Function(Term):
    """Represents a compound term (e.g., f(a, b))."""
    def __init__(self, name: str, args: list)
```

### Knowledge Representation

```python
class Fact:
    """Represents a ground fact."""
    def __init__(self, head: str)

class Rule:
    """Represents a Horn clause rule (head :- body)."""
    def __init__(self, head: str, body: list)

class KnowledgeBase:
    """Container for facts and rules."""
    def __init__(self)
    def add_fact(self, fact: Fact)
    def add_rule(self, rule: Rule)
    def display_kb_contents(self)
```

### Substitution

```python
class Substitution(dict):
    """Maps variables to terms."""
    def copy() -> Substitution
    def apply(self, term) -> term
    def compose(self, other) -> Substitution
    def rename(self, old_var: str, new_var: str)
```

## Key Functions

### Inference

| Function | Purpose |
|----------|---------|
| `solve(goal, kb, subst=None)` | Find all solutions via backward chaining |
| `solve_goals(goals, kb, subst)` | Solve conjunctions (AND) of goals |
| `prove(goal, kb)` | Build proof tree showing derivation |

### Unification

| Function | Purpose |
|----------|---------|
| `unify(t1, t2, subst=None)` | Unify two terms |
| `deref(term, subst)` | Dereference term by following substitution |
| `occurs_check(var, term, subst)` | Check if variable occurs in term |

### Term Processing

| Function | Purpose |
|----------|---------|
| `parse_term(text)` | Parse string to Term |
| `parse_formula(text)` | Parse string to Predicate/Equation |
| `rewrite_once(term, rules)` | Apply one rewrite rule |
| `normalize(term, rules)` | Iteratively rewrite to normal form |

## Examples

### Example 1: Family Relationships

```python
from logical_engine.horn_clauses import KnowledgeBase, Fact, Rule
from logical_engine.meta_interpreter import solve

kb = KnowledgeBase()

# Facts
kb.add_fact(Fact("parent(tom, bob)"))
kb.add_fact(Fact("parent(tom, liz)"))
kb.add_fact(Fact("parent(bob, ann)"))
kb.add_fact(Fact("parent(bob, pat)"))
kb.add_fact(Fact("parent(pat, jim)"))

# Rules
kb.add_rule(Rule("grandparent(X, Z)", ["parent(X, Y)", "parent(Y, Z)"]))
kb.add_rule(Rule("ancestor(X, Y)", ["parent(X, Y)"]))
kb.add_rule(Rule("ancestor(X, Y)", ["parent(X, Z)", "ancestor(Z, Y)"]))

# Queries
solutions = list(solve("grandparent(tom, ann)", kb))
print(f"tom is grandparent of ann: {len(solutions) > 0}")

solutions = list(solve("ancestor(tom, jim)", kb))
print(f"tom is ancestor of jim: {len(solutions) > 0}")

# Query with variables
solutions = list(solve("ancestor(tom, X)", kb))
print(f"tom's descendants: {[sol.get('X', '?') for sol in solutions]}")
```

### Example 2: Logic Puzzle

```python
kb = KnowledgeBase()

# Facts about who likes what
kb.add_fact(Fact("likes(mary, food)"))
kb.add_fact(Fact("likes(mary, wine)"))
kb.add_fact(Fact("likes(john, wine)"))
kb.add_fact(Fact("likes(john, mary)"))

# Rule: if X likes Y and Y likes Z, then X is interested in Z
kb.add_rule(Rule("interested(X, Z)", 
                  ["likes(X, Y)", "likes(Y, Z)"]))

# Find all things john is interested in
solutions = list(solve("interested(john, X)", kb))
print(f"John is interested in: {solutions}")
```

### Example 3: Using Proof Trees

```python
from logical_engine.meta_interpreter import prove

kb = KnowledgeBase()
kb.add_fact(Fact("bird(tweety)"))
kb.add_rule(Rule("animal(X)", ["bird(X)"]))

proofs = prove("animal(tweety)", kb)
for proof in proofs:
    print(f"Goal: {proof['goal']}")
    print(f"From: {proof['source']}")
    if proof['source'] == 'rule':
        print(f"Rule: {proof['rule_head']}")
        print(f"Body: {proof['subgoals']}")
```

## Testing

```bash
# Run all tests
export PYTHONPATH=/work/TPmeta_interpreter
pytest TPmeta_interpreter/tests/ -v

# Run specific module tests
pytest TPmeta_interpreter/tests/test_unification.py -v
pytest TPmeta_interpreter/tests/test_meta.py -v

# Run with output
pytest -s TPmeta_interpreter/tests/ --tb=short
```

## How It Works

### Backward Chaining

When you call `solve(goal, kb)`:

1. Try to match goal with each **fact** in KB using unification
2. Try to match goal with each **rule head** in KB
   - If match succeeds, recursively solve the **rule body** (subgoals)
   - Collect all solutions from subgoals
3. Return all solutions (as generators for memory efficiency)

**Example:**
```
Query: ancestor(tom, jim)

Step 1: Check facts → no direct match
Step 2: Try rule "ancestor(X,Y) :- parent(X,Y)"
        Match: {X=tom, Y=jim}
        Solve body: parent(tom, jim) → NO
Step 3: Try rule "ancestor(X,Y) :- parent(X,Z), ancestor(Z,Y)"
        Match: {X=tom, Y=jim}
        Solve body: 
          - parent(tom, Z) → Z=bob (found in facts)
          - ancestor(bob, jim) → YES (recursive call finds it)
        SUCCESS: {X=tom, Y=jim, Z=bob}
```

### Unification

The unification algorithm (Robinson 1965):

```
unify(X, a) → {X: a}              (variable matches constant)
unify(f(X), f(a)) → {X: a}        (decompose function)
unify(f(X,X), f(a,b)) → None      (occurs-check prevents X=a and X=b)
unify(X, Y) → {Y: X}              (variable matches variable)
```

## Limitations

- **String-based predicates** — Goals and facts are strings, not objects
- **No constraint solving** — CLP(FD) constraints not supported
- **No tabling** — Recursive predicates may recompute
- **Limited debugging** — No trace/debug mode like SWI-Prolog
- **No modules** — Single global namespace
- **No DCG (grammar) support**

## Extending the Engine

### Adding Custom Inference Rules

```python
# Implement your own inference as a function
def my_inference(goal, kb):
    """Custom inference procedure."""
    # Generate solutions somehow
    yield solution1
    yield solution2
```

### Adding Constraint Solving

```python
# Extend meta_interpreter to handle constraints
class ConstrainedSolver(MetaInterpreter):
    def solve_constraint(self, constraint):
        # Use CLP(FD) or similar
        pass
```

### Building an ILP System

See the `foil/` directory for an example Inductive Logic Programming system built on logical_engine.

## References

- **Robinson, J.A.** (1965). "A machine-oriented logic based on the resolution principle". *Journal of the ACM*, 12(1), 23-41.
- **Quinlan, J.R.** (1990). "Learning logical definitions from relations". *Machine Learning*, 5, 239-266.
- **Muggleton, S.H. & De Raedt, L.** (1994). "Inductive logic programming: Theory and methods". *Journal of Logic Programming*, 19/20, 629-679.
- **Prolog Documentation** — https://www.swi-prolog.org/
- **Logic Programming** — https://en.wikipedia.org/wiki/Logic_programming

## License

This project is provided as-is for educational purposes.

## Contributing

Contributions are welcome. Please ensure:
- Unit tests pass: `pytest TPmeta_interpreter/tests/ -v`
- Code follows existing style
- Docstrings are updated
- Examples demonstrate new features

## Support

For issues, questions, or suggestions, refer to the test suite and examples in:
- `TPmeta_interpreter/tests/` — Test cases
- `foil/examples.py` — FOIL learner examples
- `logical_engine/parser.py` — Term syntax examples
