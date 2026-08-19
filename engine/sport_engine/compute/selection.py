"""Filter and mute selection — pure selection logic.

Filters choose which matches to include; mutes remove designated years/tournaments
from the selected set before computation ("mute remove from computation any
designated year or tournament we want from the systems output results" — Director,
2026-08-19). All names come from the caller or from config — no literals here.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping, Tuple


@dataclass(frozen=True)
class Filters:
    tournaments: Tuple[str, ...] = ()
    years: Tuple[str, ...] = ()
    players: Tuple[str, ...] = ()
    tiers: Tuple[str, ...] = ()

    def __init__(
        self,
        tournaments: Iterable[str] = (),
        years: Iterable[str] = (),
        players: Iterable[str] = (),
        tiers: Iterable[str] = (),
    ):
        object.__setattr__(self, "tournaments", tuple(tournaments))
        object.__setattr__(self, "years", tuple(years))
        object.__setattr__(self, "players", tuple(players))
        object.__setattr__(self, "tiers", tuple(tiers))

    @classmethod
    def from_config(cls, cfg: Mapping) -> "Filters":
        return cls(
            tournaments=cfg.get("tournaments", ()),
            years=cfg.get("years", ()),
            players=cfg.get("players", ()),
            tiers=cfg.get("tiers", ()),
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
