"""Tennis adapter — match record -> per-set game scores.

Consumes rows of the shape built by data/tennis/build.py (arena/01a015bb-the-creation-2).
All schema field names and score grammar come from engine/config/tennis_schema.json —
this module contains no schema literals (zero-hardcoding rule).

Rating guard: only completed, non-void matches with every set having a winner are
rateable. Everything else returns None (refused, never guessed).
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from sport_engine.adapters.base import SportAdapter
from sport_engine.config import load_config

_SCHEMA = load_config("tennis_schema")
_FIELDS = _SCHEMA["fields"]
_GRAMMAR = _SCHEMA["score_grammar"]

_STATUS = _FIELDS["status"]
_COMPLETED = _FIELDS["status_value_completed"]
_VOID_FLAGS = tuple(_FIELDS["void_flags"])
_SCORE = _FIELDS["score"]
_SETS_A = _FIELDS["sets_a"]
_SETS_B = _FIELDS["sets_b"]
_SET_SEP = _GRAMMAR["set_separator"]
_TIEBREAK_OPEN = _GRAMMAR["tiebreak_open"]


class TennisAdapter(SportAdapter):
    sport = _SCHEMA["sport"]

    def extract_sets(self, match: dict) -> Optional[List[Tuple[int, int]]]:
        # Void / incomplete matches are not rateable.
        if match.get(_STATUS) != _COMPLETED:
            return None
        if any(match.get(flag) for flag in _VOID_FLAGS):
            return None

        score = match.get(_SCORE)
        if not isinstance(score, str) or not score.strip():
            return None

        sets: List[Tuple[int, int]] = []
        for token in score.split():
            token = token.split(_TIEBREAK_OPEN)[0]  # drop tiebreak detail: 7-6(4) -> 7-6
            parts = token.split(_SET_SEP)
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
        sets_a, sets_b = match.get(_SETS_A), match.get(_SETS_B)
        if sets_a is not None and sets_b is not None and (sets_a + sets_b != len(sets)):
            return None
        if sets_a is not None and a_won != sets_a:
            return None
        return sets
