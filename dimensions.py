import chess

piece_order = [
    # PieceType,   Colour       ValidTargets
    (chess.PAWN,   chess.WHITE,  6),
    (chess.PAWN,   chess.BLACK,  6),
    (chess.KNIGHT, chess.WHITE, 12),
    (chess.KNIGHT, chess.BLACK, 12),
    (chess.BISHOP, chess.WHITE, 10),
    (chess.BISHOP, chess.BLACK, 10),
    (chess.ROOK,   chess.WHITE, 10),
    (chess.ROOK,   chess.BLACK, 10),
    (chess.QUEEN,  chess.WHITE, 12),
    (chess.QUEEN,  chess.BLACK, 12),
    (chess.KING,   chess.WHITE,  8),
    (chess.KING,   chess.BLACK,  8),
]

def total_pseudo_attacks(piece_type: chess.PieceType, color: chess.Color) -> int:
    b = chess.Board(None)  # empty board
    total = 0
    for sq in chess.SQUARES:
        # pawns only from a2..h7
        if piece_type == chess.PAWN:
            r = chess.square_rank(sq)
            if r == 0 or r == 7:
                continue

        b.set_piece_at(sq, chess.Piece(piece_type, color))
        total += len(b.attacks(sq))
        b.remove_piece_at(sq)
    return total


total = 0
for piece_type, colour, valid_targets in piece_order:
    squareoffset = total_pseudo_attacks(piece_type, colour)
    total += valid_targets * squareoffset

print("array size", total) # 79856
