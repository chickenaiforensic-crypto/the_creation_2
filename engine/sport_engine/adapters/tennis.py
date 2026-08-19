"""Tennis adapter — match record (new-data-branch schema) -> per-set game scores.

Consumes rows of the shape built by data/tennis/build.py (arena/01a015bb-the-creation-2):
  score: "6-4 7-6(4)"  status: "completed"  retired/walkover/defaulted: bool
  setsA/setsB: int     gamesA/gamesB: int   winner: "A"

Rating guard: only completed, non-void matches with every set having a winner are
rateable. Everything else returns None (refused, never guessed).
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from sport_engine.adapters.base import SportAdapter


class TennisAdapter(SportAdapter):
    sport = "tennis"

    def extract_sets(self, match: dict) -> Optional[List[Tuple[int, int]]]:
        # Void / incomplete matches are not rateable.
        if match.get("status") != "completed":
            return None
        if match.get("retired") or match.get("walkover") or match.get("defaulted"):
            return None

        score = match.get("score")
        if not isinstance(score, str) or not score.strip():
            return None

        sets: List[Tuple[int, int]] = []
        for token in score.split():
            token = token.split("(")[0]  # drop tiebreak detail: 7-6(4) -> 7-6
            parts = token.split("-")
            if len(parts) != 2 or not (parts[0].isdigit() and parts[1].isdigit()):
                return None
            a, b = int(parts[0]), int(parts[1])
            if a < 0 or b < 0 or a == b:
                return None  # tied/unfinished set is not a final set score
            sets.append((a, b))

        if not sets:
            return None

        # A dropped set is legitimate (e.g. 6-3 3-6 6-4). The correct consistency
        # checks are against the stored fields: set count and sets won by A.
        a_won = sum(1 for a, b in sets if a > b)
        sets_a, sets_b = match.get("setsA"), match.get("setsB")
        if sets_a is not None and sets_b is not None and (sets_a + sets_b != len(sets)):
            return None
        if sets_a is not None and a_won != sets_a:
            return None
        return sets
