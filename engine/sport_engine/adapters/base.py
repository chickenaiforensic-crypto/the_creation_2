"""SportAdapter contract — how a sport's raw match record becomes rateable periods.

A "period" is one set of games (tennis) — the Phase 0 rating unit. For football this
adapter will define the equivalent period mapping when the Director specifies the phase.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple


class SportAdapter(ABC):
    sport: str = ""

    @abstractmethod
    def extract_sets(self, match: dict) -> Optional[List[Tuple[int, int]]]:
        """Return per-period game scores as [(gamesA, gamesB), ...].

        Must return None when the match is NOT rateable (void, incomplete, unfinished
        sets, contradictory data). Never fabricate or infer a score.
        """
