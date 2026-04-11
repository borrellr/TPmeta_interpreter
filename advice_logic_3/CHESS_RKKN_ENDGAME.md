# Chess Endgame Reasoning System - Rook & King vs Knight & King

## Overview

This module demonstrates how the `advice_logic_3` knowledge representation system can reason about the RKKN (Rook & King vs Knight & King) endgame.

**File:** `chess_rkkn_endgame.py`  
**Purpose:** Encode RKKN endgame principles using Horn clauses and show example position reasoning.

## What It Does

The RKKN example models:

1. **Board Representation** - Standard 8x8 chessboard with files and ranks.
2. **Piece Placement** - White rook, white king, black knight, and black king positions.
3. **Legal Moves** - Rules for rook movement and knight moves.
4. **Tactical Concepts** - Principles like knight fork threats, rook protection, and king support.
5. **Position Evaluation** - Identify safe white setups and drawish knight tactics.
6. **Example Positions** - Concrete RKKN snapshots demonstrating strategy.

## Key RKKN Concepts Demonstrated

```
1. Rook Activity
   Keep the rook active on open files and ranks to limit the knight.

2. King Support
   Use the white king to support the rook and control escape squares.

3. Knight Fork Threats
   Beware of knight jumps that attack both rook and king.

4. Rook Protection
   Position the rook to cover the white king and reduce tactical risk.

5. Drawish Knight Tactics
   Recognize positions where the knight creates counterplay or draws.

6. Escape Control
   Restrict the black king’s mobility while avoiding knight forks.

7. Tactical Awareness
   Avoid placing the rook where a knight can fork it and the king.

8. Position Safety
   Prefer structurally safe positions that preserve the material advantage.
```

## Usage

Run the demonstration:

```bash
cd /work/TPmeta_interpreter
python advice_logic_3/chess_rkkn_endgame.py
```

### Demo Output

The script runs these checks:

1. **Knight movement pattern** - Validates a knight jump.
2. **Rook safety** - Checks whether the rook protects the white king.
3. **Knight fork threat** - Detects a tactical threat in a sample position.
4. **Example positions** - Verifies explicit safe/drawish RKKN setups.
5. **Strategic principles** - Prints practical guidance for RKKN play.

## Code Structure

### Main Functions

```python
create_rkkn_endgame_kb()    # Build the RKKN knowledge base
    ├─ Board representation (files, ranks, adjacency)
    ├─ Rook move rules
    ├─ Knight move rules
    ├─ Tactical reasoning rules
    ├─ Position facts for examples
    └─ Explicit example labels for safety/drawish analysis

demonstrate_rkkn_endgame()  # Run example queries and print results
```

### Example Positions Encoded

**Position 1 (Safe White Setup):**
- White rook on e4, white king on d4
- Black knight on f6, black king on h8
- Classified as structurally safe for white

**Position 2 (Knight Fork Threat):**
- White rook on d4, white king on e2
- Black knight on f4, black king on g6
- Classified as drawish due to knight tactics

**Position 3 (Active Rook Support):**
- White rook on b5, white king on c4
- Black knight on d6, black king on g8
- Demonstrates rook activity and king support

## Horn Clause Knowledge Representation

The code uses Horn clauses like:

```prolog
knight_move(F1, R1, F2, R2) :-
    file(F1), file(F2), rank(R1), rank(R2),
    two_files(F1, F2), adjacent_ranks(R1, R2).

rook_protects_king(FR, RR, FK, RK) :-
    same_file(FR, FK).

knight_fork_threat(NF, NR, RF, RR, KF, KR) :-
    knight_move(NF, NR, RF, RR),
    knight_move(NF, NR, KF, KR).
```

## Learning Outcomes

This RKKN module teaches:

- **Domain encoding** of chess principles in logical rules.
- **Tactical reasoning** for fork threats, rook safety, and positional play.
- **Symbolic inference** using Horn clauses over a chessboard model.
- **Educational value** for combining game strategy with AI reasoning.

## Limitations & Future Enhancements

**Current limitations:**
- Simplified move logic without full board obstruction checks.
- No search algorithm for move sequences.
- Abstracted position evaluation rather than full game analysis.

**Possible enhancements:**
- Add a knight escape-zone evaluator.
- Encode more concrete RKKN tactical motifs.
- Build a search layer to examine move options.
- Expand to related endgames like RKN and RPKN.

## Summary

The `chess_rkkn_endgame.py` module is a focused RKKN reasoning example for the `advice_logic_3` package. It shows how to use Horn clauses to encode tactical chess ideas, making it a useful educational bridge between chess strategy and logical inference.
