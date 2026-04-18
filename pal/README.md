# PAL (Perturbation-based Active Learning)

A functional Python implementation of the LearnConcept algorithm for Inductive Logic Programming (ILP), built on top of the logical_engine.

## Overview

This system implements a perturbation-based active learning approach to concept learning in first-order logic. The algorithm uses Relative Least General Generalization (RLGG) to learn Horn clause rules from examples.

## Algorithm

The `learn_concept` function implements the following algorithm:

1. Start with an initial example
2. Construct an initial clause
3. Iteratively perturb the current clause to generate new examples
4. If a positive example is found, **generalize using the Generalize algorithm** (instead of direct RLGG)
5. Check consistency with negative examples and user feedback
6. Continue until no more perturbations or stopping condition
7. Validate that all stored examples are covered
8. Add the learned clause to background knowledge

## Key Components

- **PALSystem**: Main class managing the learning process
- **learn_concept**: Functional implementation of the learning algorithm
- **GeneralizationSystem**: Implements the Generalize algorithm with domain theory expansion
- **PerturbationSystem**: Implements the PerturbationMethod algorithm for generating examples
- **RLGG Integration**: Uses the rlgg_ilp system for clause generalization
- **Perturbation Methods**: Generate new examples from current hypotheses

## Generalize Algorithm

The `generalize` function implements:

1. Expand domain theory with new example
2. Derive atoms from domain and example
3. Construct head from input predicates
4. Build new clause with derived body
5. Compute LGG with current concept
6. Clean up unused variables and isolated literals

## Perturbation Algorithm

The `perturbation_method` function implements:

1. For each perturbation class (add_constraint, remove_constraint, modify_predicate)
2. Generate an example that fails at least one literal
3. Identify failed literals
4. Generate an example that succeeds on at least one failed literal
5. Return the succeeding example if found
6. Try next class if not found

## Usage

```python
from pal.learn_concept import PALSystem, learn_concept, Clause
from logical_engine.horn_clauses import KnowledgeBase

# Create background knowledge
bk = KnowledgeBase()
bk.add_fact(Fact("parent(john, mary)"))

# Create PAL system
pal_system = PALSystem(background_kb=bk)

# Learn from initial example
initial_example = Clause("parent(john, mary)")
learned_clause = learn_concept(initial_example, pal_system)

print(f"Learned: {learned_clause}")
```

## Files

- `learn_concept.py`: Main learning algorithm with integrated generalization and perturbation
- `generalize.py`: Generalization algorithm implementation
- `perturbation.py`: Perturbation method for example generation
- `test_learn_concept.py`: Unit tests

## Dependencies

- logical_engine (parent directory)
- rlgg_ilp (sibling directory)

## Running Tests

```bash
cd /work/TPmeta_interpreter
python -m pytest pal/ -v
```

## References

- Morales, Eduardo. Learning Chess Patterns. pp. 517–537 in *Inductive Logic Programming*, Stephen Muggleton (ed.), 1992.
