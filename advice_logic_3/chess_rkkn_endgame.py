"""
Chess RKKN Endgame Reasoning System

Advanced endgame knowledge base for Rook & King vs Knight & King (RKKN).
This module encodes board representation, movement rules, and strategic
principles for the RKKN endgame using Horn clause reasoning.

It is intended as a companion example to `chess_rkk_endgame.py` and demonstrates:
  - Chessboard modeling with files and ranks
  - Knight and rook move reasoning
  - Endgame concepts such as knight forks, escape squares, and defensive zones
  - Position evaluation and example RKKN positions
"""

from advice_logic_3 import AdviceLogic3


def create_rkkn_endgame_kb():
    """Create the RKKN endgame knowledge base."""
    al3 = AdviceLogic3()

    # ------------------------------------------------------------------
    # board representation
    # ------------------------------------------------------------------
    for file in range(1, 9):
        al3.add_fact(f"file({file})")
    for rank in range(1, 9):
        al3.add_fact(f"rank({rank})")

    al3.add_rule("edge_file(1)", [])
    al3.add_rule("edge_file(8)", [])
    al3.add_rule("edge_rank(1)", [])
    al3.add_rule("edge_rank(8)", [])

    # ------------------------------------------------------------------
    # rook move rules
    # ------------------------------------------------------------------
    al3.add_rule(
        "legal_rook_move(F1, R, F2, R)",
        ["file(F1)", "file(F2)", "rank(R)", "different_files(F1, F2)"]
    )
    al3.add_rule(
        "legal_rook_move(F, R1, F, R2)",
        ["file(F)", "rank(R1)", "rank(R2)", "different_ranks(R1, R2)"]
    )

    # ------------------------------------------------------------------
    # knight move rules
    # ------------------------------------------------------------------
    # Knight moves are two squares in one direction and one square in the other.
    for i in range(1, 7):
        al3.add_fact(f"two_files({i}, {i+2})")
        al3.add_fact(f"two_files({i+2}, {i})")
        al3.add_fact(f"two_ranks({i}, {i+2})")
        al3.add_fact(f"two_ranks({i+2}, {i})")

    al3.add_rule(
        "knight_move(F1, R1, F2, R2)",
        ["file(F1)", "file(F2)", "rank(R1)", "rank(R2)",
         "two_files(F1, F2)", "adjacent_ranks(R1, R2)"]
    )
    al3.add_rule(
        "knight_move(F1, R1, F2, R2)",
        ["file(F1)", "file(F2)", "rank(R1)", "rank(R2)",
         "adjacent_files(F1, F2)", "two_ranks(R1, R2)"]
    )

    # ------------------------------------------------------------------
    # adjacency helpers
    # ------------------------------------------------------------------
    for i in range(1, 8):
        al3.add_fact(f"adjacent_file({i}, {i+1})")
        al3.add_fact(f"adjacent_rank({i}, {i+1})")

    al3.add_rule("adjacent_files(F1, F2)", ["adjacent_file(F1, F2)"])
    al3.add_rule("adjacent_files(F1, F2)", ["adjacent_file(F2, F1)"])
    al3.add_rule("adjacent_ranks(R1, R2)", ["adjacent_rank(R1, R2)"])
    al3.add_rule("adjacent_ranks(R1, R2)", ["adjacent_rank(R2, R1)"])

    al3.add_rule("different_files(F1, F2)", ["file(F1)", "file(F2)"])
    al3.add_rule("different_ranks(R1, R2)", ["rank(R1)", "rank(R2)"])

    # ------------------------------------------------------------------
    # defensive and tactical concepts
    # ------------------------------------------------------------------
    al3.add_rule("rook_protects_king(FR, RR, FK, RK)", ["file(FR)", "rank(RR)", "file(FK)", "rank(RK)", "same_rank(RR, RK)"])
    al3.add_rule("rook_protects_king(FR, RR, FK, RK)", ["file(FR)", "rank(RR)", "file(FK)", "rank(RK)", "same_file(FR, FK)"])

    al3.add_rule("knight_fork_threat(NF, NR, RF, RR, KF, KR)",
        ["knight_move(NF, NR, RF, RR)", "knight_move(NF, NR, KF, KR)"]
    )

    al3.add_rule("rook_on_open_file(FR, RR)", ["file(FR)", "rank(RR)"])
    al3.add_rule("king_near_rook(FK, RK, FR, RR)", ["file(FK)", "rank(RK)", "file(FR)", "rank(RR)"])

    al3.add_rule("active_rook(FR, RR)", ["rook_on_open_file(FR, RR)"])
    al3.add_rule("king_supports_rook(FK, RK, FR, RR)", ["king_near_rook(FK, RK, FR, RR)"])

    # ------------------------------------------------------------------
    # endgame principles
    # ------------------------------------------------------------------
    al3.add_rule("avoid_knight_fork", ["rook_protects_king(FR, RR, FK, KR)"])
    al3.add_rule("use_rook_to_cut_off(FR, RR, BKF)", ["file(FR)", "file(BKF)", "different_files(FR, BKF)"])
    al3.add_rule("restrict_knight(NF, NR)", ["file(NF)", "rank(NR)"])
    al3.add_rule("keep_rook_active", ["active_rook(FR, RR)"])
    al3.add_rule("keep_king_close", ["king_supports_rook(FK, RK, FR, RR)"])

    al3.add_rule("white_safe_position", ["keep_rook_active", "avoid_knight_fork", "keep_king_close"])
    al3.add_rule("black_drawish_position", ["knight_fork_threat(NF, NR, RF, RR, KF, KR)"])

    # ------------------------------------------------------------------
    # example positions
    # ------------------------------------------------------------------
    def add_position_1():
        al3.add_fact("position(rkkn1)")
        al3.add_fact("pos_white_rook(rkkn1, 5, 4)")
        al3.add_fact("pos_white_king(rkkn1, 4, 4)")
        al3.add_fact("pos_black_knight(rkkn1, 6, 6)")
        al3.add_fact("pos_black_king(rkkn1, 8, 8)")
        al3.add_fact("position_safe(rkkn1)")
        al3.add_rule("rook_protects_king(5, 4, 4, 4)", ["position(rkkn1)"])
        al3.add_rule("active_rook(5, 4)", ["position(rkkn1)"])
        al3.add_rule("king_supports_rook(4, 4, 5, 4)", ["position(rkkn1)"])
    add_position_1()

    def add_position_2():
        al3.add_fact("position(rkkn2)")
        al3.add_fact("pos_white_rook(rkkn2, 4, 4)")
        al3.add_fact("pos_white_king(rkkn2, 5, 2)")
        al3.add_fact("pos_black_knight(rkkn2, 6, 4)")
        al3.add_fact("pos_black_king(rkkn2, 7, 6)")
        al3.add_fact("position_drawish(rkkn2)")
        al3.add_rule("knight_fork_threat(6, 4, 4, 4, 5, 2)", ["position(rkkn2)"])
    add_position_2()

    def add_position_3():
        al3.add_fact("position(rkkn3)")
        al3.add_fact("pos_white_rook(rkkn3, 2, 5)")
        al3.add_fact("pos_white_king(rkkn3, 3, 4)")
        al3.add_fact("pos_black_knight(rkkn3, 4, 6)")
        al3.add_fact("pos_black_king(rkkn3, 7, 8)")
        al3.add_rule("rook_protects_king(2, 5, 3, 4)", ["position(rkkn3)"])
        al3.add_rule("active_rook(2, 5)", ["position(rkkn3)"])
        al3.add_rule("keep_rook_active", ["position(rkkn3)"])
    add_position_3()

    return al3


def demonstrate_rkkn_endgame():
    """Run RKKN endgame demonstration queries."""
    print("\n" + "=" * 70)
    print("ROOK & KING VS KNIGHT & KING ENDGAME")
    print("=" * 70)

    kb = create_rkkn_endgame_kb()

    print("\n" + "-" * 70)
    print("DEMO 1: KNIGHT MOVEMENT PATTERN")
    print("-" * 70)
    knight_move = kb.query("knight_move(5, 4, 6, 6)")
    print(f"\nIs e4 to g6 a legal knight move? {bool(knight_move)}")

    print("\n" + "-" * 70)
    print("DEMO 2: KING AND ROOK SAFETY")
    print("-" * 70)
    protect = kb.query("rook_protects_king(5, 4, 4, 4)")
    print(f"\nDoes rook on e4 protect king on d4? {bool(protect)}")

    print("\n" + "-" * 70)
    print("DEMO 3: KNIGHT FORK THREAT")
    print("-" * 70)
    fork = kb.query("knight_fork_threat(6, 4, 4, 4, 5, 2)")
    print(f"\nIs there a knight fork threat in position 2? {bool(fork)}")

    print("\n" + "-" * 70)
    print("DEMO 4: EXAMPLE POSITIONS")
    print("-" * 70)
    position1_safe = kb.query("position_safe(rkkn1)")
    position2_drawish = kb.query("position_drawish(rkkn2)")
    print(f"\nPosition 1 is structurally safe: {bool(position1_safe)}")
    print(f"Position 2 is drawish due to knight tactics: {bool(position2_drawish)}")

    print("\n" + "-" * 70)
    print("DEMO 5: STRATEGIC PRINCIPLES")
    print("-" * 70)
    principles = [
        "Keep the rook active and away from knight forks.",
        "Use the white king to support the rook and control escape routes.",
        "Avoid knight fork squares when the rook and king are close.",
        "Drive the black king toward the edge while limiting knight activity.",
        "Recognize drawish knight tactics and avoid unnecessary simplifications."
    ]
    for principle in principles:
        print(f"\n{principle}")

    print("\n" + "=" * 70 + "\n")


if __name__ == "__main__":
    demonstrate_rkkn_endgame()
