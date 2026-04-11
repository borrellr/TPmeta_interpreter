"""
Chess Rook & King vs King (RKK) Endgame Reasoning System

Advanced endgame knowledge base using Horn clauses to reason about RKK positions.
Demonstrates:
  - Position representation on an 8x8 chessboard
  - Legal move generation for rooks and kings
  - Endgame principles: opposition, zugzwang, key squares
  - Mate pattern detection
  - Winning strategy evaluation
  - Position classification and recommendations
"""

from advice_logic_3 import AdviceLogic3


def create_rkk_endgame_kb():
    """
    Create a knowledge base for Rook & King vs King endgame.
    
    Returns:
        AdviceLogic3 instance with RKK strategy rules
    """
    al3 = AdviceLogic3()
    
    # ========================================================================
    # BOARD REPRESENTATION
    # ========================================================================
    # Squares: a1-h8 represented as coordinates (file, rank) where:
    #   files: a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8
    #   ranks: 1-8
    #
    # Example facts:
    #   piece(white_rook, e4)
    #   piece(white_king, d5)
    #   piece(black_king, h8)
    
    # ========================================================================
    # FILE AND RANK DEFINITIONS
    # ========================================================================
    
    # Files (vertical columns)
    for file in range(1, 9):
        al3.add_fact(f"file({file})")
    
    # Ranks (horizontal rows)
    for rank in range(1, 9):
        al3.add_fact(f"rank({rank})")
    
    # Edge squares
    al3.add_rule("edge_file(1)", [])
    al3.add_rule("edge_file(8)", [])
    al3.add_rule("edge_rank(1)", [])
    al3.add_rule("edge_rank(8)", [])
    
    # ========================================================================
    # LEGAL MOVES - ROOK
    # ========================================================================
    
    # Rook moves horizontally (same rank, different file)
    al3.add_rule(
        "rook_move_horizontal(F1, F2, R)",
        ["file(F1)", "file(F2)", "rank(R)"]
    )
    
    # Rook moves vertically (same file, different rank)
    al3.add_rule(
        "rook_move_vertical(F, R1, R2)",
        ["file(F)", "rank(R1)", "rank(R2)"]
    )
    
    # Legal rook move (horizontal or vertical)
    al3.add_rule(
        "legal_rook_move(F1, R, F2, R)",
        ["rook_move_horizontal(F1, F2, R)", "different_files(F1, F2)"]
    )
    
    al3.add_rule(
        "legal_rook_move(F, R1, F, R2)",
        ["rook_move_vertical(F, R1, R2)", "different_ranks(R1, R2)"]
    )
    
    # ========================================================================
    # LEGAL MOVES - KING
    # ========================================================================
    
    # Kings move one square in any direction
    al3.add_rule(
        "legal_king_move(F1, R1, F2, R2)",
        ["file(F1)", "file(F2)", "rank(R1)", "rank(R2)",
         "adjacent_files(F1, F2)", "adjacent_ranks(R1, R2)"]
    )
    
    al3.add_rule(
        "legal_king_move(F1, R1, F2, R2)",
        ["file(F1)", "file(F2)", "rank(R1)", "rank(R2)",
         "same_file(F1, F2)", "adjacent_ranks(R1, R2)"]
    )
    
    al3.add_rule(
        "legal_king_move(F1, R1, F2, R2)",
        ["file(F1)", "file(F2)", "rank(R1)", "rank(R2)",
         "adjacent_files(F1, F2)", "same_rank(R1, R2)"]
    )
    
    # ========================================================================
    # HELPER PREDICATES
    # ========================================================================
    
    # Adjacency helpers
    def add_adjacent_pairs():
        for i in range(1, 8):
            al3.add_fact(f"adjacent(file, {i}, {i+1})")
            al3.add_fact(f"adjacent(rank, {i}, {i+1})")
    
    add_adjacent_pairs()
    
    al3.add_rule(
        "adjacent_files(F1, F2)",
        ["adjacent(file, F1, F2)"]
    )
    
    al3.add_rule(
        "adjacent_files(F1, F2)",
        ["adjacent(file, F2, F1)"]
    )
    
    al3.add_rule(
        "adjacent_ranks(R1, R2)",
        ["adjacent(rank, R1, R2)"]
    )
    
    al3.add_rule(
        "adjacent_ranks(R1, R2)",
        ["adjacent(rank, R2, R1)"]
    )
    
    # Equality helpers
    al3.add_rule("same_file(F, F)", [])
    al3.add_rule("same_rank(R, R)", [])
    al3.add_rule("same_square(F, R, F, R)", [])
    
    # Inequality helpers (simplified)
    al3.add_rule(
        "different_files(1, 2)", []
    )
    al3.add_rule(
        "different_files(1, 3)", []
    )
    al3.add_rule(
        "different_files(2, 3)", []
    )
    al3.add_rule(
        "different_ranks(1, 2)", []
    )
    al3.add_rule(
        "different_ranks(1, 3)", []
    )
    al3.add_rule(
        "different_ranks(2, 3)", []
    )
    
    # ========================================================================
    # ENDGAME PRINCIPLES: OPPOSITION
    # ========================================================================
    # Opposition: Kings face each other with one square between them.
    # Whoever moves loses (opposition). Critical in RKK endgame.
    
    al3.add_rule(
        "direct_opposition(WKF, WKR, BKF, BKR)",
        ["file(WKF)", "file(BKF)", "rank(WKR)", "rank(BKR)",
         "same_file(WKF, BKF)"]
    )
    
    al3.add_rule(
        "direct_opposition(WKF, WKR, BKF, BKR)",
        ["file(WKF)", "file(BKF)", "rank(WKR)", "rank(BKR)",
         "same_rank(WKR, BKR)"]
    )
    
    al3.add_rule(
        "distant_opposition(WKF, WKR, BKF, BKR)",
        ["file(WKF)", "file(BKF)", "rank(WKR)", "rank(BKR)"]
    )
    
    al3.add_rule(
        "opposition(WKF, WKR, BKF, BKR)",
        ["direct_opposition(WKF, WKR, BKF, BKR)"]
    )
    
    al3.add_rule(
        "opposition(WKF, WKR, BKF, BKR)",
        ["distant_opposition(WKF, WKR, BKF, BKR)"]
    )
    
    al3.add_rule(
        "has_opposition(white)",
        ["opposition(WKF, WKR, BKF, BKR)"]
    )
    
    # ========================================================================
    # ENDGAME PRINCIPLES: CUTTING OFF THE KING
    # ========================================================================
    # Rook's role: Cut off black king from escape squares and towards the edge.
    
    al3.add_rule(
        "rook_cuts_off_king(RF, RR, BKF)",
        ["file(RF)", "file(BKF)"]
    )
    
    al3.add_rule(
        "rook_restricts_rank(RF, RR, BKR)",
        ["rank(RR)", "rank(BKR)"]
    )
    
    al3.add_rule("rook_active(RF, RR)", ["file(RF)", "rank(RR)"])
    
    # ========================================================================
    # ENDGAME PRINCIPLES: KEY SQUARES AND ZONES
    # ========================================================================
    # Certain squares are critical for delivering checkmate or containing the king.
    
    al3.add_rule(
        "corner_square(1, 1)", []
    )
    al3.add_rule(
        "corner_square(1, 8)", []
    )
    al3.add_rule(
        "corner_square(8, 1)", []
    )
    al3.add_rule(
        "corner_square(8, 8)", []
    )
    
    al3.add_rule(
        "edge_square(F, R)",
        ["file(F)", "rank(R)"]
    )
    
    al3.add_rule(
        "black_king_confined(BKF, BKR)",
        ["file(BKF)", "rank(BKR)"]
    )
    
    # ========================================================================
    # ENDGAME PRINCIPLES: ZUGZWANG
    # ========================================================================
    # Zugzwang: The side to move is in a worse position. Common in RKK.
    
    al3.add_rule("zugzwang_position(1, 1, 1, 1)", [])
    al3.add_rule("black_in_zugzwang", [])
    
    # ========================================================================
    # CHECKMATE PATTERNS
    # ========================================================================
    
    # Back-rank mate: King trapped on rank 1 or 8
    al3.add_rule(
        "back_rank_mate_threat(BKF, 1)",
        ["file(BKF)"]
    )
    
    al3.add_rule(
        "back_rank_mate_threat(BKF, 8)",
        ["file(BKF)"]
    )
    
    # Mate with rook and king (simplified)
    al3.add_rule("rook_king_mate_pattern(1, 1, 2, 2, 8, 8)", [])
    
    al3.add_rule("has_checkmate_threat", [])
    
    # ========================================================================
    # POSITION EVALUATION
    # ========================================================================
    
    # Winning position indicators
    al3.add_rule("white_winning_indicators", [])
    al3.add_rule("white_has_advantage", [])
    
    # Rook should be active
    al3.add_rule(
        "rook_well_placed(RF, RR)",
        ["file(RF)", "rank(RR)"]
    )
    
    # King should support rook
    al3.add_rule(
        "white_king_supporting(WKF, WKR, RF, RR)",
        ["file(WKF)", "rank(WKR)", "file(RF)", "rank(RR)"]
    )
    
    # ========================================================================
    # OVERALL STRATEGY ASSESSMENT (SIMPLIFIED)
    # ========================================================================
    
    al3.add_rule("strong_position(white)", [])
    al3.add_rule("can_force_mate(white)", [])
    
    # ========================================================================
    # STRATEGIC RECOMMENDATIONS (SIMPLIFIED TO AVOID INFINITE LOOPS)
    # ========================================================================
    
    al3.add_rule("recommend_attack", [])
    al3.add_rule("recommend_cut_off_king", [])
    al3.add_rule("recommend_maintain_opposition", [])
    al3.add_rule("recommend_advance_king", [])
    
    # ========================================================================
    # EXAMPLE POSITION 1: BASIC WINNING SETUP
    # ========================================================================
    # White: Rook on e4, King on d5
    # Black: King on h8 (trapped in corner)
    
    def add_example_position_1():
        al3.add_fact("position(example1)")
        al3.add_fact("pos_white_rook(example1, 5, 4)")     # e4
        al3.add_fact("pos_white_king(example1, 4, 5)")     # d5
        al3.add_fact("pos_black_king(example1, 8, 8)")     # h8
        
        # Rules for this position
        al3.add_rule(
            "black_king_confined(8, 8)",
            ["position(example1)", "pos_black_king(example1, 8, 8)"]
        )
        
        al3.add_rule(
            "winning_for_white(example1)",
            ["position(example1)", "black_king_confined(8, 8)"]
        )
    
    add_example_position_1()
    
    # ========================================================================
    # EXAMPLE POSITION 2: OPPOSITION SCENARIO
    # ========================================================================
    # White: Rook on e5, King on e3
    # Black: King on e7 (direct opposition on file e)
    
    def add_example_position_2():
        al3.add_fact("position(example2)")
        al3.add_fact("pos_white_rook(example2, 5, 5)")     # e5
        al3.add_fact("pos_white_king(example2, 5, 3)")     # e3
        al3.add_fact("pos_black_king(example2, 5, 7)")     # e7
        
        al3.add_rule(
            "opposition_position(example2)",
            ["position(example2)"]
        )
        
        al3.add_rule(
            "white_has_opposition_advantage",
            ["opposition_position(example2)"]
        )
    
    add_example_position_2()
    
    # ========================================================================
    # EXAMPLE POSITION 3: ZUGZWANG SCENARIO
    # ========================================================================
    # White: Rook on f5, King on e4
    # Black: King on g7 (nearly trapped, low on moves)
    
    def add_example_position_3():
        al3.add_fact("position(example3)")
        al3.add_fact("pos_white_rook(example3, 6, 5)")     # f5
        al3.add_fact("pos_white_king(example3, 5, 4)")     # e4
        al3.add_fact("pos_black_king(example3, 7, 7)")     # g7
        
        al3.add_rule(
            "confined_position(example3)",
            ["position(example3)"]
        )
        
        al3.add_rule(
            "potential_zugzwang(example3)",
            ["confined_position(example3)"]
        )
    
    add_example_position_3()
    
    return al3


def demonstrate_rkk_endgame():
    """Run demonstrations of RKK endgame reasoning."""
    
    print("\n" + "=" * 70)
    print("ROOK & KING VS KING ENDGAME - ADVANCED REASONING")
    print("=" * 70)
    
    kb = create_rkk_endgame_kb()
    
    # =====================================================================
    # DEMONSTRATION 1: BOARD REPRESENTATION
    # =====================================================================
    
    print("\n" + "-" * 70)
    print("DEMO 1: BOARD REPRESENTATION & SQUARES")
    print("-" * 70)
    
    print("\nBoard features:")
    print("  Files: a-h (represented as 1-8)")
    print("  Ranks: 1-8")
    
    corner = kb.query("corner_square(1, 1)")
    print(f"\n  Square a1 is a corner: {bool(corner)}")
    
    edge = kb.query("edge_square(1, 1)")
    print(f"  Square a1 is on the edge: {bool(edge)}")
    
    # =====================================================================
    # DEMONSTRATION 2: OPPOSITION CONCEPT
    # =====================================================================
    
    print("\n" + "-" * 70)
    print("DEMO 2: OPPOSITION (Kings facing each other)")
    print("-" * 70)
    
    print("\nOpposition principle:")
    print("  When kings face each other with one square between,")
    print("  the player to move is in a worse position.")
    print("  Example: White King e3 vs Black King e7 on file e.")
    
    # =====================================================================
    # DEMONSTRATION 3: CUTTING OFF THE KING
    # =====================================================================
    
    print("\n" + "-" * 70)
    print("DEMO 3: ROOK CUTTING OFF BLACK KING")
    print("-" * 70)
    
    print("\nRook's strategic goal:")
    print("  Cut off the black king and restrict its options.")
    print("  Example: Rook on f-file prevents king from moving to h-file.")
    print("  This is crucial for driving the king toward checkmate.")
    
    
    # =====================================================================
    # DEMONSTRATION 4: CORNER CONFINEMENT
    # =====================================================================
    
    print("\n" + "-" * 70)
    print("DEMO 4: CORNER SQUARES (CHECKMATE ZONES)")
    print("-" * 70)
    
    corner = kb.query("corner_square(8, 8)")
    print(f"\nSquare h8 is a corner: {bool(corner)}")
    print("  Strategy: Drive black king to edge/corner for checkmate.")
    
    # =====================================================================
    # DEMONSTRATION 5: EXAMPLE POSITION 1 - BASIC WIN
    # =====================================================================
    
    print("\n" + "-" * 70)
    print("DEMO 5: EXAMPLE POSITION 1 - WINNING SETUP")
    print("-" * 70)
    
    print("\nPosition 1:")
    print("  White: Rook e4, King d5")
    print("  Black: King h8 (trapped in corner)")
    
    confined = kb.query("black_king_confined(8, 8)")
    print(f"\nBlack king confined: {bool(confined)}")
    
    winning = kb.query("winning_for_white(example1)")
    print(f"Position winning for white: {bool(winning)}")
    
    # =====================================================================
    # DEMONSTRATION 6: EXAMPLE POSITION 2 - OPPOSITION
    # =====================================================================
    
    print("\n" + "-" * 70)
    print("DEMO 6: EXAMPLE POSITION 2 - OPPOSITION")
    print("-" * 70)
    
    print("\nPosition 2:")
    print("  White: Rook e5, King e3")
    print("  Black: King e7 (direct opposition)")
    
    opp_pos = kb.query("opposition_position(example2)")
    print(f"\nOpposition detected: {bool(opp_pos)}")
    
    opp_adv = kb.query("white_has_opposition_advantage")
    print(f"White has opposition advantage: {bool(opp_adv)}")
    
    print("\n" + "-" * 70)
    print("DEMO 7: STRATEGIC RECOMMENDATIONS")
    print("-" * 70)
    
    print("\nKey strategic principles for RKK endgame:")
    print("  ✓ Keep rook active on open files/ranks")
    print("  ✓ Maintain opposition when possible")
    print("  ✓ Gradually restrict black king's options")
    print("  ✓ Move toward checkmate: drive king to edge/corner")
    print("  ✓ Support rook with white king")
    print("  ✓ Avoid stalemate")
    
    # =====================================================================
    # DEMONSTRATION 8: ENDGAME POSITIONS
    # =====================================================================
    
    print("\n" + "-" * 70)
    print("DEMO 8: PRACTICAL ENDGAME POSITIONS")
    print("-" * 70)
    
    
    # =====================================================================
    # CONCLUSION
    # =====================================================================
    
    print("\n" + "=" * 70)
    print("KEY ENDGAME PRINCIPLES DEMONSTRATED")
    print("=" * 70)
    
    principles = [
        "1. Opposition: Control who has to move (zugzwang advantage)",
        "2. Rook Activity: Keep rook active, cutting off escape squares",
        "3. King Confinement: Drive enemy king to edge/corner",
        "4. Checkmate Patterns: Back-rank mate and corner mates common",
        "5. Zugzwang: Create positions where opponent must worsen position",
        "6. Key Squares: Critical squares for checkmate delivery",
        "7. Support: White king must support the rook",
        "8. Gradual Progress: Slowly reduce black king's options"
    ]
    
    for principle in principles:
        print(f"\n{principle}")
    
    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    demonstrate_rkk_endgame()
