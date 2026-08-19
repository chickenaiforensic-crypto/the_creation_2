"""Phase 0 — match rating core (sport-agnostic).

Director spec (2026-08-19):

  pA vs pB, per-set game scores.
  1. Normalise each set: -1 on both sides until the higher side has
     `max_winner_games` (6) games (7-5 resolves to 6-4). Orientation preserved.
  2. Points per player per set, from games won after normalisation
     (config `rating_rules.json`: 0-2 -> 2 (1x) ; 3-4 -> 4 (2x) ; 5 -> 7 (3x) ;
     6 -> 10 (4x)).
  3. Match totals = sum of per-set points.
  4. Rating: pA = totalA - totalB ; pB = totalB - totalA.

Worked example (verified): sets 6-2, 6-4 -> totals 20 / 6 -> pA +14, pB -14.

ZERO-HARDCODING: every value below is loaded from engine/config/rating_rules.json
at import. There is no rating value in this code.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from sport_engine.config import load_config

_RULES = load_config("rating_rules")

MAX_WINNER_GAMES: int = int(_RULES["max_winner_games"])
GAMES_TO_POINTS: Dict[int, int] = {int(k): int(v) for k, v in _RULES["points_by_games"].items()}
TIER_LABEL: Dict[int, str] = {int(k): str(v) for k, v in _RULES["tier_by_games"].items()}


def _validate_rules() -> None:
    """Config must fully cover 0..MAX_WINNER_GAMES in both tables — fail loudly."""
    for games in range(0, MAX_WINNER_GAMES + 1):
        if games not in GAMES_TO_POINTS:
            raise ValueError(f"rating_rules.json missing points for {games} games")
        if games not in TIER_LABEL:
            raise ValueError(f"rating_rules.json missing tier for {games} games")
    for games, points in GAMES_TO_POINTS.items():
        if points < 0:
            raise ValueError(f"rating_rules.json: negative points {points} for {games} games")


_validate_rules()


class RatingError(ValueError):
    """A set score that cannot exist or cannot be rated under the Phase 0 rules."""


def points_for_games(games: int) -> int:
    if games < 0 or games > MAX_WINNER_GAMES:
        raise RatingError(f"games {games} outside 0..{MAX_WINNER_GAMES}")
    return GAMES_TO_POINTS[games]


def tier_for_games(games: int) -> str:
    if games < 0 or games > MAX_WINNER_GAMES:
        raise RatingError(f"games {games} outside 0..{MAX_WINNER_GAMES}")
    return TIER_LABEL[games]


def normalize_set(a: int, b: int) -> Tuple[int, int]:
    """Apply -1 to BOTH sides until the higher side has max_winner_games (6) games.

    Orientation is preserved (the higher side stays on its original side) so the
    caller can assign points to the correct player.
    """
    if a < 0 or b < 0:
        raise RatingError(f"negative games in set {a}-{b}")
    if a == b:
        raise RatingError(f"set cannot be tied {a}-{b} (unfinished or invalid)")
    dec = max(0, max(a, b) - MAX_WINNER_GAMES)
    na, nb = a - dec, b - dec
    if na < 0 or nb < 0:
        raise RatingError(f"set score cannot normalise to {MAX_WINNER_GAMES} games: {a}-{b}")
    return na, nb


@dataclass
class SetRating:
    games_a: int
    games_b: int
    points_a: int
    points_b: int
    tier_a: str
    tier_b: str


@dataclass
class RatingResult:
    total_a: int
    total_b: int
    sets: List[SetRating] = field(default_factory=list)

    @property
    def delta_a(self) -> int:
        return self.total_a - self.total_b

    @property
    def delta_b(self) -> int:
        return self.total_b - self.total_a


def rate_sets(sets: List[Tuple[int, int]]) -> RatingResult:
    """Rate a match from per-set (gamesA, gamesB). Raises RatingError on invalid sets."""
    if not sets:
        raise RatingError("no sets to rate")
    total_a, total_b = 0, 0
    rated: List[SetRating] = []
    for a, b in sets:
        na, nb = normalize_set(a, b)
        pa, pb = points_for_games(na), points_for_games(nb)
        total_a += pa
        total_b += pb
        rated.append(
            SetRating(
                games_a=na,
                games_b=nb,
                points_a=pa,
                points_b=pb,
                tier_a=tier_for_games(na),
                tier_b=tier_for_games(nb),
            )
        )
    return RatingResult(total_a=total_a, total_b=total_b, sets=rated)
