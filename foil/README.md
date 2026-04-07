# FOIL: First-Order Inductive Learner

A top-down inductive logic programming (ILP) system built on `logical_engine`, implementing the FOIL algorithm for learning Horn clauses from examples.

## Overview

FOIL learns Horn clause rules by:
1. Starting with the most general clause (least specific)
2. Iteratively specializing by adding body literals
3. Stopping when all negatives are excluded

This makes it a **greedy top-down refinement learner**.

## Architecture

```
logical_engine/
├── terms.py          (Term, Variable, Function, Constant)
├── unification.py    (Unification algorithm)
├── parser.py         (Parse term strings)
├── meta_interpreter.py (solve/prove - backward chaining)
└── horn_clauses.py   (Rule, Fact, KnowledgeBase)
        ↓
foil/
├── ilp.py           (FOIL learner implementation)
├── examples.py      (Usage examples)
└── test_foil.py     (Unit tests)
```

## Usage

### Basic example

```python
from foil.ilp import Example, foil_learn
from logical_engine.horn_clauses import KnowledgeBase, Fact

# Create knowledge base with facts
kb = KnowledgeBase()
kb.add_fact(Fact("parent(john, mary)"))
kb.add_fact(Fact("parent(mary, alice)"))

# Define training examples
positives = [
    Example("ancestor(john, mary)", True),
    Example("ancestor(john, alice)", True),
    Example("ancestor(mary, alice)", True),
]

negatives = [
    Example("ancestor(mary, john)", False),
    Example("ancestor(alice, john)", False),
]

# Learn rules
rules = foil_learn(
    target_predicate="ancestor",
    positive_examples=positives,
    negative_examples=negatives,
    available_predicates=[
        "parent(X, Y)",
        "parent(X, Z)",
        "ancestor(X, Z)",
        "ancestor(Z, Y)",
    ],
    kb=kb
)

# Print learned rules
for rule in rules:
    print(f"{rule.head} :- {', '.join(rule.body)}")
```

## Key Functions

### Core ILP Functions

- `foil_learn(target, positives, negatives, predicates, kb)` — Main learning function
- `solves(rule, example, kb)` — Check if a rule covers an example
- `covers_negatives(rule, negatives, kb)` — Test if rule covers any negative
- `information_gain(rule, pos, neg, kb)` — Score rule quality
- `specialize_clause(rule, literal)` — Add a literal to rule body
- `generate_specializations(rule, predicates)` — Generate candidate variants

### Metrics

- `recall(rule, positives, kb)` — Fraction of positives covered
- `precision(rule, positives, negatives, kb)` — Fraction of covered examples that are positive

## Data Structures

### Example

```python
Example(goal="ancestor(john, alice)", label=True)
```

- `goal`: Goal string to learn (e.g., "ancestor(X, Y)")
- `label`: True for positive examples, False for negative

### Rule

```python
Rule(head="ancestor(X, Y)", body=["parent(X, Z)", "ancestor(Z, Y)"])
```

- `head`: Head of the clause
- `body`: List of goal strings in the body

## Algorithm

**FOIL (Quinlan 1990) — Simplified version**

```
Input: Target predicate P, examples E+, E-
Output: Set of rules R

R = {}
while E+ not empty:
    Clause = most_general_clause(P)
    
    while Clause covers any E-:
        Candidates = specialize(Clause, available_predicates)
        Clause = argmax(Candidates, information_gain)
    
    R.add(Clause)
    E+ = E+ - {examples covered by Clause}

return R
```

### Information Gain

FOIL uses a simplified information gain metric:

$$\text{gain}(rule) = \frac{\text{positives covered}}{1 + \text{negatives covered}}$$

## Running Tests

```bash
cd /work
source venv_312/bin/activate
PYTHONPATH=/work/TPmeta_interpreter pytest foil/test_foil.py -v
```

## Running Examples

```bash
cd /work
source venv_312/bin/activate
PYTHONPATH=/work/TPmeta_interpreter python foil/examples.py
```

## Limitations

1. **Greedy search** — May not find optimal rules
2. **No recursion handling** — Doesn't automatically discover recursive rules (ancestor calls ancestor)
3. **Limited backtracking** — beam_width=1 uses greedy selection only
4. **Predicate specification required** — Must provide candidate predicates manually

## Future Improvements

- Mode-driven specialization (MODESJ, PROGOL approach)
- Beam search with wider beam_width
- Automatic generation of candidate predicates
- Inverse resolution (for generalization)
- Support for inequality constraints
- Clause compression and optimization

## References

- Quinlan, J.R. (1990). "Learning logical definitions from relations". *Machine Learning*, 5, 239-266.
- Muggleton, S.H. & De Raedt, L. (1994). "Inductive logic programming: Theory and methods". *Journal of Logic Programming*, 19/20, 629-679.
