# RLGG ILP System

An implementation of the Relative Least General Generalization (RLGG) algorithm for Inductive Logic Programming, based on the work of Stephen Muggleton and collaborators.

## Overview

This system implements ILP (Inductive Logic Programming) using the RLGG algorithm to learn Horn clause rules from positive examples. The RLGG algorithm computes the most specific generalization of examples that is consistent with background knowledge.

## Features

- **Relative Least General Generalization**: Computes generalizations relative to background theory
- **Horn Clause Learning**: Learns rules in the form `head :- body`
- **Background Knowledge Integration**: Uses background knowledge to constrain generalizations
- **Built on Logical Engine**: Uses the existing logical engine for unification and inference

## Installation

```bash
# Navigate to the TPmeta_interpreter directory
cd /work/TPmeta_interpreter

# Set PYTHONPATH to include the current directory
export PYTHONPATH=/work/TPmeta_interpreter:$PYTHONPATH
```

## Usage

### Basic Example

```python
from rlgg_ilp import RLGGSystem, Clause

# Create the ILP system
ilp = RLGGSystem()

# Define positive examples for learning the parent relationship
examples = [
    Clause("parent(john, mary)"),
    Clause("parent(alice, bob)")
]

# Learn a rule
rule = ilp.learn_rule(examples)
print(f"Learned: {rule.head} :- {', '.join(rule.body) if rule.body else 'true'}")
# Output: Learned: parent(X1, X2) :- true
```

### With Background Knowledge

```python
from logical_engine.horn_clauses import KnowledgeBase, Fact, Rule

# Create background knowledge
bk = KnowledgeBase()
bk.add_fact(Fact("male(john)"))
bk.add_fact(Fact("female(mary)"))

# Create ILP system with background knowledge
ilp = RLGGSystem(bk)

# Learn rules that respect the background knowledge
examples = [
    Clause("ancestor(john, mary)", ["parent(john, mary)"]),
    Clause("ancestor(alice, bob)", ["parent(alice, bob)"])
]

rule = ilp.learn_rule(examples)
print(f"Learned: {rule.head} :- {', '.join(rule.body)}")
# Output: Learned: ancestor(X1, X2) :- parent(X3, X4)
```

# Create background knowledge
bk = KnowledgeBase()
bk.add_fact(Fact("male(john)"))
bk.add_fact(Fact("female(mary)"))

# Create ILP system with background knowledge
ilp = RLGGSystem(bk)

# Learn rules that respect the background knowledge
examples = [
    Clause(Predicate("father", [Constant("john"), Constant("mary")]), [Predicate("male", [Constant("john")])])
]
```

## Algorithm Overview

The RLGG algorithm works by:

1. **Computing LGG**: Finding the least general generalization of two clauses
2. **Relative Generalization**: Ensuring the generalization is entailed by background knowledge
3. **Iterative Learning**: Applying RLGG successively to multiple examples

## Running Tests

```bash
python test_rlgg.py
```

## Dependencies

- Python 3.12+
- Logical Engine (`/work/TPmeta_interpreter/logical_engine/`)

## References

- Muggleton, S. (1995). Inverse entailment and progol. New Generation Computing, 13(3-4), 245-286.
- Muggleton, S., & De Raedt, L. (1994). Inductive logic programming: Theory and methods. The Journal of Logic Programming, 19, 629-679.

## License

MIT License
