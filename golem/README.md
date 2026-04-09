# Golem: Generalisation Of Natural Language Descriptions

**Muggleton and Feng's Inductive Logic Programming System**

A bottom-up inductive logic programming (ILP) learner built on `logical_engine`, implementing the Golem algorithm for learning Horn clauses from positive examples only.

## Overview

Golem is a classic ILP system that learns Horn clause rules using a **least-general generalization (LGG)** approach. Unlike systems that require negative examples, Golem learns from positive examples alone, making it ideal for scenarios where negative examples are unavailable or expensive to obtain.

### Key Features

✅ **Positive-only learning** — Learns from positive examples without negative examples  
✅ **Relative LGG** — Uses least general generalization under background theory  
✅ **Bottom-up search** — Builds rules from example pairs  
✅ **Greedy refinement** — Iteratively selects best-coverage rules  
✅ **Logical engine integration** — Leverages the core deductive reasoning system  
✅ **Tractable** — Restricts clause length for practical learning  

## Algorithm

### Golem Learning Process

1. **Seed Selection**: Choose a positive example not yet covered
2. **Pair Generalization**: Compute LGG with other positive examples
3. **Coverage Evaluation**: Measure how many examples the candidate rule covers
4. **Rule Selection**: Keep the rule with highest coverage
5. **Removal**: Remove covered examples from the set
6. **Iteration**: Repeat until all examples are covered or maximum iterations reached

### Mathematical Foundation

Golem uses **Relative Least General Generalization (LGG)** to compute the most specific generalization of two examples that is logically consistent with the background theory:

$$\text{lgg}(t_1, t_2) = \text{most specific } g \text{ such that } \text{BG} \models t_1 \theta_1, \text{BG} \models t_2 \theta_2 \text{ and } g \theta = t_i$$

Where:
- BG = Background knowledge
- θ = Substitution mapping
- g = Generalized term

## Project Structure

```
logical_engine/
├── terms.py              (Term, Variable, Function, Constant)
├── unification.py        (Unification algorithm)
├── parser.py             (Parse term strings)
├── meta_interpreter.py   (solve/prove - backward chaining)
├── horn_clauses.py       (Rule, Fact, KnowledgeBase)
└── ...
        ↓
golem/
├── golem_learner.py      (Golem learner implementation)
├── examples.py           (Usage examples)
├── test_golem.py         (Unit tests)
└── README.md             (This file)
```

## Installation & Usage

### Basic Setup

```bash
cd /work/TPmeta_interpreter
export PYTHONPATH=/work/TPmeta_interpreter
```

### Simple Example: Learning Ancestor Relations

```python
from logical_engine.horn_clauses import KnowledgeBase, Fact
from golem.golem_learner import GolemLearner, Example

# Create knowledge base with background facts
kb = KnowledgeBase()
kb.add_fact(Fact("parent(john, mary)"))
kb.add_fact(Fact("parent(mary, alice)"))
kb.add_fact(Fact("parent(alice, bob)"))

# Define positive training examples
positive_examples = [
    Example("ancestor(john, mary)"),
    Example("ancestor(john, alice)"),
    Example("ancestor(john, bob)"),
    Example("ancestor(mary, alice)"),
    Example("ancestor(mary, bob)"),
    Example("ancestor(alice, bob)"),
]

# Create learner (no negative examples needed!)
learner = GolemLearner(kb, max_clause_length=2, verbose=True)

# Learn rules
learned_rules = learner.learn(positive_examples, predicate_name="ancestor")

# Display learned rules
learner.print_learned_rules()

# Use learned rules for inference
from logical_engine.meta_interpreter import solve
learned_kb = learner.get_learned_knowledge_base()
kb.add_rule(learned_rules[0].to_horn_clause())

solutions = list(solve("ancestor(john, bob)", kb))
print(f"ancestor(john, bob): {bool(solutions)}")
```

### Advanced Usage

#### Custom Max Clause Length

```python
# Learn rules with up to 3 body literals
learner = GolemLearner(kb, max_clause_length=3, verbose=True)
```

#### Verbose Output

```python
# Enable detailed learning trace
learner = GolemLearner(kb, verbose=True)
learned_rules = learner.learn(positive_examples)
# [Golem] Starting learning with 6 positive examples
# [Iteration 0] Uncovered examples: {0, 1, 2, 3, 4, 5}
# [Iteration 0] Learned rule: ancestor(john, X0) :- parent(john, X0).
# ...
```

#### Rule Specialization

```python
base_rule = GolemRule("ancestor(X, Y)", ["parent(X, Y)"])

# Specialize the rule
specialized = learner.specialize_rule(
    base_rule,
    ["parent(X, Z)", "ancestor(Z, Y)"]
)
print(specialized)  # ancestor(X, Y) :- parent(X, Y), parent(X, Z), ancestor(Z, Y).
```

## Examples

The `examples.py` file contains complete worked examples:

### Example 1: Family Relations
Learn grandparent relation from parent facts.

### Example 2: Simple Pattern Learning
Learn patterns like `round(X)` from object properties.

### Example 3: Ancestor Chains
Learn transitive ancestor relationships.

```bash
python examples.py
```

## API Reference

### GolemLearner

```python
class GolemLearner:
    def __init__(self, kb: KnowledgeBase, max_clause_length: int = 2,
                 max_iterations: int = 100, verbose: bool = False) -> None
    
    def learn(self, positive_examples: List[Example],
              predicate_name: Optional[str] = None) -> List[GolemRule]
    
    def get_learned_rules(self) -> List[GolemRule]
    
    def get_learned_knowledge_base(self) -> KnowledgeBase
    
    def print_learned_rules(self) -> None
    
    def specialize_rule(self, rule: GolemRule,
                       literals_to_add: List[str]) -> GolemRule
```

### Example

```python
@dataclass
class Example:
    goal: str           # String representation of goal
    label: bool = True  # Positive (True) or Negative (False)
```

### GolemRule

```python
@dataclass
class GolemRule:
    head: str           # Head of the rule
    body: List[str]     # Body literals
    
    def to_horn_clause(self) -> Rule
    def __repr__(self) -> str
```

## Testing

Run the test suite:

```bash
cd /work/TPmeta_interpreter
pytest golem/test_golem.py -v
```

Test coverage includes:
- Learner initialization
- Example creation
- Rule representation
- Simple learning scenarios
- Example coverage detection
- Rule specialization
- Family relation learning
- Rule conversion to Horn clauses

## Advantages and Limitations

### Advantages

✅ Works with **positive examples only** (no negatives needed)  
✅ **Sound** learning algorithm with logical foundations  
✅ **Tractable** with reasonable clause length restrictions  
✅ Leverages **background knowledge** effectively  
✅ **Bottom-up** search can be more efficient than top-down  

### Limitations

⚠️ May require **many positive examples** for good coverage  
⚠️ **Harder to learn from limited data** without negative examples  
⚠️ Clause length restrictions may limit expressiveness  
⚠️ LGG computation can be expensive with large example sets  
⚠️ Performance depends heavily on background theory quality  

## Comparison with Other ILP Systems

| System | Examples | Approach | Clause Length |
|--------|----------|----------|----------------|
| **Golem** | Positive only | Bottom-up LGG | Limited (default 2) |
| FOIL | Pos + Neg | Top-down greedy | Limited |
| RLGG | Positive only | Generalization | Unlimited |
| Inductive Logic Programming | Both | Covers all | Varies |

## References

1. **Muggleton, S. H., & Feng, C.** (1990). "Efficient induction of logic programs." In Proceedings of the 1st Conference on Algorithmic Learning Theory, Tokyo.

2. **Muggleton, S. H.** (1991). "Inductive logic programming." New Generation Computing, 8(4), 295-318.

3. **Plotkin, G. D.** (1971). "A further note on inductive generalization." In Machine Intelligence 6, pp. 101-124.

## Related Works

- [logical_engine/README.md](../logical_engine/README.md) — Core deductive reasoning
- [foil/README.md](../foil/README.md) — Alternative ILP system (top-down)
- [rlgg_ilp/README.md](../rlgg_ilp/README.md) — Alternative ILP system (generalization)

## Future Enhancements

- [ ] Implement full relative LGG with subsumption checking
- [ ] Add negative example handling for refinement
- [ ] Implement inverse resolution refinement
- [ ] Add performance optimizations for large theories
- [ ] Support for constraint-based specialization
- [ ] Visualization of learned rules

## Contributing

Contributions welcome! Areas for improvement:
- More complete LGG implementation
- Better example coverage heuristics
- Performance optimizations
- Additional test cases
- Support for more complex Horn clause structures

## License

This code is provided as educational material for the TPmeta_interpreter project.

---

**Author**: Muggleton & Feng (1990); Implementation by TPmeta_interpreter  
**Date**: 2024  
**Status**: Educational/Research Implementation
