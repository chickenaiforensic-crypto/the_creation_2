"""Filter and mute selection — pure selection logic.

Filters choose which matches to include; mutes remove designated years/tournaments
from the selected set before computation ("mute remove from computation any
designated year or tournament we want from the systems output results" — Director,
2026-08-19). All names come from the caller or from config — no literals here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Mapping, Optional, Tuple


def year_range(
    years_from: Optional[str] = None,
    years_to: Optional[str] = None,
) -> List[str]:
    """Resolve a (from, to) year period into an inclusive year list.

    - Neither bound given -> [] (the caller then means "all years").
    - A single bound -> [that year] (selecting one year means ONE year, not a
      range silently extended to the data's edge).
    - Both bounds -> inclusive range [from..to] (swapped if reversed).
    """
    if not years_from and not years_to:
        return []
    if not years_from:
        return [str(int(years_to))]
    if not years_to:
        return [str(int(years_from))]
    lo, hi = int(years_from), int(years_to)
    if hi < lo:
        lo, hi = hi, lo
    return [str(y) for y in range(lo, hi + 1)]


@dataclass(frozen=True)
class Filters:
    tournaments: Tuple[str, ...] = ()
    years: Tuple[str, ...] = ()
    players: Tuple[str, ...] = ()
    tiers: Tuple[str, ...] = ()
    tours: Tuple[str, ...] = ()

    def __init__(
        self,
        tournaments: Iterable[str] = (),
        years: Iterable[str] = (),
        players: Iterable[str] = (),
        tiers: Iterable[str] = (),
        tours: Iterable[str] = (),
    ):
        object.__setattr__(self, "tournaments", tuple(tournaments))
        object.__setattr__(self, "years", tuple(years))
        object.__setattr__(self, "players", tuple(players))
        object.__setattr__(self, "tiers", tuple(tiers))
        object.__setattr__(self, "tours", tuple(tours))

    @classmethod
    def from_config(cls, cfg: Mapping) -> "Filters":
        return cls(
            tournaments=cfg.get("tournaments", ()),
            years=cfg.get("years", ()),
            players=cfg.get("players", ()),
            tiers=cfg.get("tiers", ()),
            tours=cfg.get("tours", ()),
        )

    def allows(self, match: Mapping, field_names: Mapping) -> bool:
        """A match passes the filter when it matches every non-empty category (OR
        within a category). Empty category = no restriction."""
        if self.tournaments and match.get(field_names["tournament"]) not in self.tournaments:
            return False
        if self.years and match.get(field_names["edition_year"]) not in self.years:
            return False
        if self.tiers and match.get(field_names["tier"]) not in self.tiers:
            return False
        if self.tours and match.get(field_names["tour"]) not in self.tours:
            return False
        if self.players:
            pair = (match.get(field_names["player_a"]), match.get(field_names["player_b"]))
            if not any(name in pair for name in self.players):
                return False
        return True

    def as_dict(self) -> dict:
        return {
            "tournaments": list(self.tournaments),
            "years": list(self.years),
            "players": list(self.players),
            "tiers": list(self.tiers),
            "tours": list(self.tours),
        }


@dataclass(frozen=True)
class Mutes:
    mute_years: Tuple[str, ...] = ()
    mute_tournaments: Tuple[str, ...] = ()

    def __init__(
        self,
        mute_years: Iterable[str] = (),
        mute_tournaments: Iterable[str] = (),
    ):
        object.__setattr__(self, "mute_years", tuple(mute_years))
        object.__setattr__(self, "mute_tournaments", tuple(mute_tournaments))

    @classmethod
    def from_config(cls, cfg: Mapping) -> "Mutes":
        return cls(
            mute_years=cfg.get("mute_years", ()),
            mute_tournaments=cfg.get("mute_tournaments", ()),
        )

    def applies(self, match: Mapping, field_names: Mapping) -> bool:
        if match.get(field_names["edition_year"]) in self.mute_years:
            return True
        if match.get(field_names["tournament"]) in self.mute_tournaments:
            return True
        return False

    def as_dict(self) -> dict:
        return {
            "mute_years": list(self.mute_years),
            "mute_tournaments": list(self.mute_tournaments),
        }
