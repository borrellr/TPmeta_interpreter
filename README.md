# TPmeta_interpreter

`TPmeta_interpreter` is a Python project for symbolic reasoning and inductive logic programming. It contains a core logical engine for Horn clause reasoning together with a FOIL-style inductive learner built on top of that engine.

## Project structure

- `logical_engine/` — Core logic engine implementation
  - Includes term representation, first-order unification, parsing, Horn clause knowledge bases, backward chaining, proof construction, and rewriting.
  - See `logical_engine/README.md` for architecture details, examples, and usage.

- `foil/` — First-Order Inductive Learner
  - Implements the FOIL algorithm for learning Horn clause rules from positive and negative examples.
  - See `foil/README.md` for the ILP overview, example usage, and tests.

- `rlgg_ilp/` — Relative Least General Generalization (RLGG) ILP System
  - Implements the RLGG algorithm for learning Horn clause rules from positive examples.
  - Computes generalizations relative to background theory using the logical engine.
  - See `rlgg_ilp/README.md` for algorithm details, examples, and usage.

- `golem/` — Golem ILP System (Muggleton & Feng)
  - Implements the Golem algorithm for learning Horn clause rules from positive examples only.
  - Uses relative least-general generalization (LGG) under background theory.
  - Built on the logical engine for deductive inference.
  - See `golem/README.md` for algorithm details, examples, and usage.

- `tests/` — Project tests
  - Contains test cases for the interpreter and learner.

- `.gitignore` — Git ignore rules for this project.
- `.pytest_cache/` — Local pytest cache (generated during test runs).

## Purpose

This repository is intended to support experiments in logic programming, knowledge representation, and inductive learning:

- Build and query Horn clause knowledge bases using a Prolog-like deductive engine.
- Perform unification and backward chaining with explicit substitutions.
- Learn logical rules from examples using FOIL-style ILP.
- Explore symbolic reasoning algorithms in Python.

## Getting started

```bash
cd /work/TPmeta_interpreter
export PYTHONPATH=/work/TPmeta_interpreter
```

Activate the workspace Python environment if required, then run tests or examples.

## Useful links

- `logical_engine/README.md`
- `foil/README.md`
- `rlgg_ilp/README.md`
- `golem/README.md`

## Running tests

```bash
cd /work
source venv_312/bin/activate
PYTHONPATH=/work/TPmeta_interpreter pytest -q
```

## Notes

For the best project-level overview, start with this file and then read the directory-specific READMEs in `logical_engine/`, `foil/`, and `rlgg_ilp/`.
