# Chess Endgame Reasoning System - Rook & King vs King

## Overview

This module demonstrates how the `advice_logic_3` knowledge representation system can be used to reason about chess endgames, specifically Rook & King vs King (RKK) - one of the most fundamental endgames in chess.

**File:** `chess_rkk_endgame.py`  
**Lines of Code:** 535  
**Purpose:** Encode and reason about RKK endgame strategy using Horn clauses

## What It Does

The system models RKK endgame knowledge as:

1. **Board Representation** - 8x8 chessboard with files (a-h) and ranks (1-8)
2. **Piece Placement** - Position of white rook, white king, and black king
3. **Legal Moves** - Rules for rook and king movement
4. **Endgame Principles** - Strategic concepts encoded as Horn clauses:
   - Opposition (who has the advantage to move)
   - Cutting off the king (rook's role in restricting escape)
   - Key squares (corner/edge zones for checkmate)
   - Zugzwang (positions where moving worsens your situation)

5. **Position Evaluation** - Classify positions as winning/losing
6. **Example Positions** - Concrete board positions demonstrating principles

## Key Endgame Principles Demonstrated

```
1. Opposition
   Kings facing each other with one square between forces the 
   player to move into a worse position.

2. Rook Activity  
   Keep the rook active on open files/ranks to cut off escape squares.

3. King Confinement
   Gradually drive the black king toward the edge and corners 
   where checkmate is possible.

4. Checkmate Patterns
   Back-rank mate and corner mates are the most common finishes.

5. Zugzwang
   Create positions where the opponent must make a move that 
   worsens their position.

6. Key Squares
   Certain squares are critical for either side - white for 
   delivering mate, black for escaping confinement.

7. Support
   The white king must support the rook's efforts. Distant support 
   is usually preferable to maintain flexibility.

8. Gradual Progress
   Methodically reduce the opponent's options through a sequence 
   of accurate moves.
```

## Usage

Run the demonstration:

```bash
cd /work/TPmeta_interpreter
python advice_logic_3/chess_rkk_endgame.py
```

### Output Structure

The demo runs 8 demonstrations:

1. **Board Representation** - Squares and board features
2. **Opposition** - Kings facing with advantage to move
3. **Cutting Off** - Rook's strategic role
4. **Corner Squares** - Checkmate zones
5. **Example Position 1** - Winning setup (king in corner)
6. **Example Position 2** - Opposition advantage
7. **Strategic Recommendations** - Key principles summary
8. **Endgame Principles** - Complete principle list

## Code Structure

### Main Components

```python
create_rkk_endgame_kb()    # Create knowledge base with endgame rules
    ├─ Board representation (files, ranks, squares)
    ├─ Legal moves (rook horizontal/vertical, king one square)
    ├─ Endgame principles (opposition, cutting off, zugzwang)
    ├─ Position evaluation (winning/losing indicators)
    ├─ Example positions (3 concrete positions)
    └─ Strategic recommendations

demonstrate_rkk_endgame()  # Run the demonstration queries
```

### Example Positions Encoded

**Position 1 (Winning Setup):**
- White: Rook e4, King d5
- Black: King h8 (corner)
- Result: Winning for white

**Position 2 (Opposition):**
- White: Rook e5, King e3
- Black: King e7
- Result: White has opposition advantage

**Position 3 (Confinement):**
- White: Rook f5, King e4
- Black: King g7
- Result: Black confined

## Horn Clause Knowledge Representation

The system uses Horn clauses like:

```prolog
% Opposition rule
opposition(WKF, WKR, BKF, BKR) :- direct_opposition(WKF, WKR, BKF, BKR).

% Rook cutting off king
rook_cuts_off_king(RF, RR, BKF) :- file(RF), file(BKF).

% Corner piece
corner_square(1, 1).  % a1
corner_square(8, 8).  % h8

% Position evaluation
winning_for_white(Position) :- 
    position(Position), 
    black_king_confined(BKF, BKR).
```

## Learning Outcomes

This module demonstrates:

- **Knowledge Representation** - Encoding chess strategy in logic
- **Symbolic Reasoning** - Using logical inference to evaluate positions
- **Domain Modeling** - Reducing complex domain (chess) to logical facts/rules
- **Pattern Recognition** - Identifying endgame patterns (opposition, zugzwang)
- **Decision Support** - Reasoning about "should we do X?" questions
- **Educational Value** - Understanding chess principles through logic

## Running Custom Queries

You can extend the knowledge base and run custom queries:

```python
from advice_logic_3 import AdviceLogic3

al3 = AdviceLogic3()

# Add facts about a position
al3.add_fact("piece(white_rook, e4)")
al3.add_fact("piece(white_king, d5)")
al3.add_fact("piece(black_king, h8)")

# Add strategic rules
al3.add_rule("winning", ["piece(white_rook, e4)", "piece(black_king, h8)"])

# Query
if al3.recommend("winning"):
    print("Position is winning!")
```

## Limitations & Future Enhancements

**Current Limitations:**
- Simplified legal move generation (doesn't check for piece blocking)
- No move search algorithm (would require additional logic)
- No efficiency optimizations (would need indexing)
- Limited to 8x8 board (easily extended)

**Future Enhancements:**
- Full chess position evaluation
- Endgame tablebase integration
- Move search engine (minimax on top of logic engine)
- Multi-piece endgames (RKK, RKPK, etc.)
- Interactive chess analyzer
- Training mode with feedback

## References

**Chess Endgame Theory:**
- Silman, J. *The Endgame Manual*
- Fine, R. *Basic Chess Endings*
- Dvoretsky, M. *Dvoretsky's Endgame Manual*

**Horn Clause Logic:**
- See `logical_engine/README.md` for core engine documentation
- See `README.md` in parent directory for AdviceLogic3 overview

## File Statistics

| Component | Lines | Purpose |
|-----------|-------|---------|
| Board representation | 50 | Squares, files, ranks |
| Legal moves | 60 | Rook and king movement rules |
| Endgame principles | 80 | Opposition, zugzwang, cutting off |
| Position evaluation | 40 | Winning/losing assessment |
| Example positions | 60 | Concrete board setups |
| Demonstrations | 150 | Query examples and output |
| **TOTAL** | **535** | **Complete RKK reasoning system** |

## Summary

The `chess_rkk_endgame.py` module demonstrates advanced knowledge representation by encoding a sophisticated board game (chess) alongside its strategic principles using Horn clause logic. This makes it an excellent educational tool for understanding both chess strategy and symbolic AI reasoning.
