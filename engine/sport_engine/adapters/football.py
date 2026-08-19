"""Football adapter — STUB.

Phase 0 spec (2026-08-19) is game/set-based (tennis-shaped). The Director has not yet
specified how football matches map to rateable periods (e.g. goals -> the points table,
per-half, per-match). Registering the adapter now makes the plug point visible; using it
fails loudly rather than inventing a mapping.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from sport_engine.adapters.base import SportAdapter


class FootballAdapter(SportAdapter):
    sport = "football"

    def extract_sets(self, match: dict) -> Optional[List[Tuple[int, int]]]:
        raise NotImplementedError(
            "Football rating mapping not yet specified by the Director (Phase 0 is "
            "game/set-based). No mapping may be invented."
        )
