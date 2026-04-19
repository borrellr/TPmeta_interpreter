Chess vocabulary

contents/3   - contents(Side, Piece, Place)
all_but_K/1  - all_but_K(Piece)
legal_move/4 - legal_move(Side, Piece, Place, NewPlace)
in_check/4   - in_check(Side, Place, OPiece, OPlace)
threat/6     - threat(Side, Piece, Pl, OSide, OPiece, OPl)
other_side/2 - other_side(Side1, Side2)

Example

contents(white, king, square(1,1))
contents(black, king, square(1,8))
contents(white, knight, square(5,6))
other_side(white, black)
all_but_K(pawn)
legal_move(white, king, square(1,1), square(1,2))
legal_move(white, king, square(1,1), square(2,2))
legal_move(white, king, square(1,1), square(2,1))
legal_move(black, king, square(1,8), square(1,7))
legal_move(black, king, square(1,8), square(2,7))
legal_move(black, king, square(1,8), square(2,8))
legal_move(white, knight, square(5,6), square(6,8))
legal_move(white, knight, square(5,6), square(4,8))
legal_move(white, knight, square(5,6), square(3,7))
legal_move(white, knight, square(5,6), square(3,5))
legal_move(white, knight, square(5,6), square(4,4))
legal_move(white, knight, square(5,6), square(6,4))
legal_move(white, knight, square(5,6), square(7,5))
legal_move(white, knight, square(5,6), square(7,7))
in_check(black, square(1,8), knight, square(3,7))

Reference
- Morales, Eduardo. Learning Chess Patterns. pp. 517–537 in *Inductive Logic Programming*, Stephen Muggleton (ed.), 1992.