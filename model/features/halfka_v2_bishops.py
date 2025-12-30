import chess

from .feature_block import FeatureBlock
from collections import OrderedDict

import typing
from typing import Dict, List
if typing.TYPE_CHECKING:
  from typing_extensions import Self, TypeAlias

SQUARE_NB = 64

FeatureOffset: TypeAlias = int
PS_W_PAWN: FeatureOffset     =  0 
PS_B_PAWN: FeatureOffset     =  1 * SQUARE_NB
PS_W_KNIGHT: FeatureOffset   =  2 * SQUARE_NB
PS_B_KNIGHT: FeatureOffset   =  3 * SQUARE_NB
PS_W_L_BISHOP: FeatureOffset =  4 * SQUARE_NB
PS_W_D_BISHOP: FeatureOffset =  5 * SQUARE_NB
PS_B_L_BISHOP: FeatureOffset =  6 * SQUARE_NB
PS_B_D_BISHOP: FeatureOffset =  7 * SQUARE_NB
PS_W_ROOK: FeatureOffset     =  8 * SQUARE_NB
PS_B_ROOK: FeatureOffset     =  9 * SQUARE_NB
PS_W_QUEEN: FeatureOffset    = 10 * SQUARE_NB
PS_B_QUEEN: FeatureOffset    = 11 * SQUARE_NB
PS_KING: FeatureOffset       = 12 * SQUARE_NB
PS_NB: int                   = 13 * SQUARE_NB
PS_VIRTUAL_NB: int           = 14 * SQUARE_NB

DIMENSIONS = SQUARE_NB * PS_NB // 2

KB_IDX = lambda x: x * PS_NB

KING_BUCKETS: List[int] = [
  KB_IDX(28), KB_IDX(29), KB_IDX(30), KB_IDX(31), KB_IDX(31), KB_IDX(30), KB_IDX(29), KB_IDX(28),
  KB_IDX(24), KB_IDX(25), KB_IDX(26), KB_IDX(27), KB_IDX(27), KB_IDX(26), KB_IDX(25), KB_IDX(24),
  KB_IDX(20), KB_IDX(21), KB_IDX(22), KB_IDX(23), KB_IDX(23), KB_IDX(22), KB_IDX(21), KB_IDX(20),
  KB_IDX(16), KB_IDX(17), KB_IDX(18), KB_IDX(19), KB_IDX(19), KB_IDX(18), KB_IDX(17), KB_IDX(16),
  KB_IDX(12), KB_IDX(13), KB_IDX(14), KB_IDX(15), KB_IDX(15), KB_IDX(14), KB_IDX(13), KB_IDX(12),
  KB_IDX( 8), KB_IDX( 9), KB_IDX(10), KB_IDX(11), KB_IDX(11), KB_IDX(10), KB_IDX( 9), KB_IDX( 8),
  KB_IDX( 4), KB_IDX( 5), KB_IDX( 6), KB_IDX( 7), KB_IDX( 7), KB_IDX( 6), KB_IDX( 5), KB_IDX( 4),
  KB_IDX( 0), KB_IDX( 1), KB_IDX( 2), KB_IDX( 3), KB_IDX( 3), KB_IDX( 2), KB_IDX( 1), KB_IDX( 0),
]

IS_BLACK_SQUARE: List[bool] = [
  True, False, True, False, True, False, True, False,
  False, True, False, True, False, True, False, True,
  True, False, True, False, True, False, True, False,
  False, True, False, True, False, True, False, True,
  True, False, True, False, True, False, True, False,
  False, True, False, True, False, True, False, True,
  True, False, True, False, True, False, True, False,
  False, True, False, True, False, True, False, True,
]

OrientTBL: List[] = [
  chess.H1, chess.H1, chess.H1, chess.H1, chess.A1, chess.A1, chess.A1, chess.A1,
  chess.H1, chess.H1, chess.H1, chess.H1, chess.A1, chess.A1, chess.A1, chess.A1,
  chess.H1, chess.H1, chess.H1, chess.H1, chess.A1, chess.A1, chess.A1, chess.A1,
  chess.H1, chess.H1, chess.H1, chess.H1, chess.A1, chess.A1, chess.A1, chess.A1,
  chess.H1, chess.H1, chess.H1, chess.H1, chess.A1, chess.A1, chess.A1, chess.A1,
  chess.H1, chess.H1, chess.H1, chess.H1, chess.A1, chess.A1, chess.A1, chess.A1,
  chess.H1, chess.H1, chess.H1, chess.H1, chess.A1, chess.A1, chess.A1, chess.A1,
  chess.H1, chess.H1, chess.H1, chess.H1, chess.A1, chess.A1, chess.A1, chess.A1,
];

PIECE_SQUARE_INDEX: Dict[bool, Dict[chess.Color, Dict[chess.PieceType, int]]] = {
  # white pov
  True: {
    chess.WHITE: {
      chess.PAWN:   PS_W_PAWN,
      chess.KNIGHT: PS_W_KNIGHT,
      chess.BISHOP: PS_W_L_BISHOP,
      chess.ROOK:   PS_W_ROOK,
      chess.QUEEN:  PS_W_QUEEN,
      chess.KING:   PS_KING,
    },
    chess.BLACK: {
      chess.PAWN:   PS_B_PAWN,
      chess.KNIGHT: PS_B_KNIGHT,
      chess.BISHOP: PS_B_L_BISHOP,
      chess.ROOK:   PS_B_ROOK,
      chess.QUEEN:  PS_B_QUEEN,
      chess.KING:   PS_KING,
    },
  },
  # black pov
  False: {
    chess.WHITE: {
      chess.PAWN:   PS_B_PAWN,
      chess.KNIGHT: PS_B_KNIGHT,
      chess.BISHOP: PS_B_L_BISHOP,
      chess.ROOK:   PS_B_ROOK,
      chess.QUEEN:  PS_B_QUEEN,
      chess.KING:   PS_KING,
    },
    chess.BLACK: {
      chess.PAWN:   PS_W_PAWN,
      chess.KNIGHT: PS_W_KNIGHT,
      chess.BISHOP: PS_W_L_BISHOP,
      chess.ROOK:   PS_W_ROOK,
      chess.QUEEN:  PS_W_QUEEN,
      chess.KING:   PS_KING,
    },
  }
}

def halfka_idx(is_white_pov: bool, king_sq: int, sq: int, p: chess.Piece) -> int:
  perspective = 1 - is_white_pov
  flip = 56 * perspective
  orient_s = sq ^ OrientTBL[king_sq] ^ flip

  offset = PIECE_SQUARE_INDEX[is_white_pov][p.color][p.type]
  offset += ((p.type == chess.BISHOP) & IS_BLACK_SQUARE[sq]) << 6;

  return orient_s + offset + KING_BUCKETS[king_sq ^ flip]


def halfka_psqts() -> list[int]:
  # values copied from stockfish, in stockfish internal units
  piece_values = {
    chess.PAWN:    208,
    chess.KNIGHT:  781,
    chess.BISHOP:  825,
    chess.ROOK:   1276,
    chess.QUEEN:  2538,
  }

  values = [0] * DIMENSIONS

  for ksq in range(64):
    for s in range(64):
      for pt, val in piece_values.items():
        idxw = halfka_idx(True, ksq, s, chess.Piece(pt, chess.WHITE))
        idxb = halfka_idx(True, ksq, s, chess.Piece(pt, chess.BLACK))
        values[idxw] = val
        values[idxb] = -val

    return values

class Features(FeatureBlock):
  def __init__(self):
    super().__init__(
      "HalfKAv2_hm_bishops", 0x40809277, OrderedDict([("HalfKAv2_hm_bishops", DIMENSIONS)])
    )

    def get_active_features(self, board: chess.Board):
      raise Exception(
        "Not supported yet, you must use the c++ data loader for support during training"
      )

    def get_initial_psqt_features(self) -> list[int]:
      return halfka_psqts()

class FactorizedFeatures(FeatureBlock):
  def __init__(self):
    super().__init__(
      "HalfKAv2_hm_bishops^",
      0x40809277,
      OrderedDict([("HalfKAv2_hm_bishops", DIMENSIONS), ("A", PS_VIRTUAL_NB)]),
    )

    def get_active_features(self, board: chess.Board):
      raise Exception(
        "Not supported yet, you must use the c++ data loader for factorizer support during training"
      )

    def get_feature_factors(self, idx: int) -> list[int]:
      if idx >= self.num_real_features:
        raise Exception("Feature must be real")

        a_idx = idx % PS_NB
        k_idx = idx // PS_NB

        is_king = a_idx // SQUARE_NB == 12
        king_sq = KING_BUCKETS[a_idx % SQUARE_NB]  // PS_NB

        if is_king and k_idx != king_sq:
          a_idx += SQUARE_NB

        return [idx, self.get_factor_base_feature("A") + a_idx]

    def get_initial_psqt_features(self) -> list[int]:
      return halfka_psqts() + [0] * PS_VIRTUAL_NB


"""
This is used by the features module for discovery of feature blocks.
"""


def get_feature_block_clss() -> list[type[FeatureBlock]]:
  return [Features, FactorizedFeatures]
