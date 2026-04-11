# Ivan Bratko's Advice Logic 3 System

A classic knowledge representation system implementing **Horn clause reasoning** for decision support and recommendations. This is an educational implementation of concepts from Ivan Bratko's "Programming in Prolog" and "Prolog Programming for Artificial Intelligence."

## Overview

The Advice Logic 3 system demonstrates:
- **Factual knowledge representation** using Horn clauses
- **Rule-based inference** through backward chaining
- **Meta-interpretation** over logical rules
- **Decision-support capabilities** for real-world scenarios

### Historical Context

Ivan Bratko's work in the 1980s and 1990s introduced the "Advice Logic" systems as educational examples of Prolog-based knowledge representation. The system exemplifies how logical programming can encode expert knowledge in a declarative, reasoning-friendly format.

## Architecture

The system consists of several key files:

```
advice_logic_3/
├── __init__.py           # Package exports
├── advice_logic_3.py     # Core implementation
├── examples.py           # Usage examples
├── chess_rkk_endgame.py  # Rook and King vs King chess reasoning example
├── chess_rkkn_endgame.py # Rook and King vs Knight and King chess reasoning example
├── tests.py              # Unit tests
└── README.md             # This file
```

### Core Classes

#### `AdviceLogic3`
The main class for building and querying a decision-support system.

**Methods:**
- `add_fact(fact_string)` — Add a factual statement
- `add_rule(head, body)` — Add an inference rule
- `query(goal)` — Query the knowledge base
- `recommend(goal)` — Get yes/no recommendation
- `print_kb()` — Display knowledge base contents

#### `create_default_kb()`
Creates a pre-built knowledge base with tennis decision-making rules and facts.

## Quick Start

### Basic Usage

```python
from advice_logic_3 import AdviceLogic3

# Create system
al3 = AdviceLogic3()

# Add facts
al3.add_fact("weather(sunny)")
al3.add_fact("temperature(mild)")

# Add rules
al3.add_rule("good_day", ["weather(sunny)", "temperature(mild)"])

# Query
solution = al3.query("good_day")
print(solution)  # Returns list of solutions
```

### Using Default Knowledge Base

```python
from advice_logic_3 import create_default_kb

# Create pre-built system
kb = create_default_kb()

# Query
if kb.recommend("good_weather(sunny)"):
    print("Sunny weather is good!")
```

## Example: Tennis Recommendation System

The default knowledge base encodes rules for recommending whether to play tennis:

### Facts
```
weather(sunny)
weather(rainy)
weather(overcast)

temperature(hot)
temperature(mild)
temperature(cold)

wind(strong)
wind(moderate)
wind(calm)

player_strength(weak)
player_strength(medium)
player_strength(strong)
```

### Rules
```prolog
% Good weather conditions
good_weather(sunny).
good_weather(overcast).

% Temperature comfort
comfortable_temp(T) :- 
    temperature(T), 
    not_too_hot(T), 
    not_too_cold(T).

not_too_hot(mild).
not_too_hot(cold).

not_too_cold(mild).
not_too_cold(hot).

% Playable wind
playable_wind(W) :- 
    wind(W), 
    acceptable_wind_strength(W).

acceptable_wind_strength(calm).
acceptable_wind_strength(moderate).

% Overall recommendation
recommend_play :- 
    weather(W), 
    good_weather(W), 
    playable_wind(calm).
```

## Domain Applications

### 1. Tennis Decision Support
```python
al3 = create_default_kb()
if al3.recommend("recommend_play"):
    print("Go play tennis!")
```

### 2. Medical Diagnosis
```python
al3 = AdviceLogic3()

# Patient facts
al3.add_fact("symptom(fever)")
al3.add_fact("symptom(cough)")

# Diagnostic rules
al3.add_rule("possible_cold", ["symptom(fever)", "symptom(cough)"])
al3.add_rule("consult_doctor", ["possible_cold"])

if al3.recommend("consult_doctor"):
    print("Please consult a doctor")
```

### 3. Activity Recommendation
```python
al3 = AdviceLogic3()

al3.add_fact("time(morning)")
al3.add_fact("weather(sunny)")
al3.add_fact("energy_level(high)")

al3.add_rule("good_for_exercise", 
             ["time(morning)", "energy_level(high)"])

if al3.recommend("good_for_exercise"):
    print("Good time for exercise!")
```

### 4. Business Decision Making
```python
al3 = AdviceLogic3()

al3.add_fact("budget_available(true)")
al3.add_fact("market_demand(high)")
al3.add_fact("resource_availability(sufficient)")

al3.add_rule("launch_product", 
             ["budget_available(true)", "market_demand(high)"])

if al3.recommend("launch_product"):
    print("Launch the product!")
```

## Horn Clauses and Logic

The system is built on **Horn clauses**, which are logical rules of the form:

$$A \leftarrow B_1, B_2, \ldots, B_n$$

Where:
- $A$ is the head (conclusion)
- $B_1, B_2, \ldots, B_n$ are the body (premises)

### Example
```prolog
% Rule: Recommend play IF good weather AND calm wind
recommend_play :- good_weather(X), playable_wind(calm).

% Fact: This is a special case with empty body
good_weather(sunny).
```

## Inference Process

The system uses **backward chaining**:

1. **Goal:** `recommend_play`
2. **Search:** Find rules that conclude `recommend_play`
3. **Subgoals:** Prove each premise in the rule body
4. **Recursion:** Continue until all subgoals are proven or fail
5. **Success:** All premises proven → goal is true

Example trace:
```
Goal: recommend_play
├─ Subgoal: weather(W) ∧ good_weather(W) ∧ playable_wind(calm)
│  ├─ Subgoal: weather(W) → [sunny, rainy, overcast]
│  ├─ Subgoal: good_weather(sunny) → TRUE
│  └─ Subgoal: playable_wind(calm) → TRUE
└─ Result: SUCCESS
```

## Running Examples

Execute the example suite:

```bash
cd /work/TPmeta_interpreter
export PYTHONPATH=/work/TPmeta_interpreter

python -m advice_logic_3.examples
```

This runs five comprehensive examples:
1. **Basic Queries** — Simple fact checking
2. **Rule Inference** — Deriving conclusions from rules
3. **Custom Scenario** — Tennis court recommendations
4. **Domain-Specific** — Medical diagnosis advice
5. **Multi-Choice** — Multiple recommendation pathways

## Integration with Logical Engine

The Advice Logic 3 system leverages the broader Logical Engine:

- **`logical_engine.horn_clauses`** — Fact and Rule representation
- **`logical_engine.meta_interpreter`** — Backward chaining inference
- **`logical_engine.unification`** — Pattern matching
- **`logical_engine.parser`** — Predicate parsing

## Key Concepts

### Facts
Atomic statements that are unconditionally true:
```python
al3.add_fact("weather(sunny)")
```

### Rules
Conditional statements with premises and conclusions:
```python
al3.add_rule("recommend_play", ["good_weather(W)", "calm_wind"])
```

### Queries
Goals to prove against the knowledge base:
```python
solutions = al3.query("recommend_play")
```

### Solutions
Variable bindings that satisfy a query:
```python
# Query: is_parent(X, mary)
# Solution: X = john
```

## Design Principles

1. **Declarative** — Specify what is true, not how to compute
2. **Modular** — Facts and rules are independent units
3. **Compositional** — Complex rules built from simple predicates
4. **Transparent** — Rules are human-readable logical statements
5. **Extensible** — Easy to add new facts and rules

## Historical References

- **Bratko, I.** (1990). *Prolog Programming for Artificial Intelligence* (2nd ed.). Addison-Wesley.
- **Bratko, I.** (1986). "Advice-giving systems as expert systems." In *Developments in Expert Systems*
- **Clocksin, W. F., & Mellish, C. S.** (1987). *Programming in Prolog* (3rd ed.). Springer-Verlag.

## Educational Value

This implementation demonstrates:
- ✅ Declarative knowledge representation
- ✅ Logical inference through unification
- ✅ Backward chaining search strategies
- ✅ Meta-interpretation over logical rules
- ✅ Real-world application of symbolic AI
- ✅ Bridge between theory and practice

## Future Extensions

Potential enhancements:
- Negation as failure (NAF)
- Constraint solving
- Cuts and pruning strategies
- Tabling/memoization
- Explanation generation
- Confidence scores for non-monotonic reasoning

## License

Educational implementation following the Logical Engine framework.
