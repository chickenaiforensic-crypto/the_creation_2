"""Compute orchestrator — live computation with filters and mutes.

Pipeline: load data (manifest-verified) -> apply feed default + caller filters ->
apply mutes -> rate each selected match with Phase 0 -> aggregate per player.
Never writes to the data tree; output is computed live on every call.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from sport_engine.adapters.tennis import TennisAdapter
from sport_engine.config import load_config
from sport_engine.compute.data_source import DataIntegrityError, edition_identity, load_editions
from sport_engine.compute.selection import Filters, Mutes
from sport_engine.rating.phase0 import rate_sets

REPO_ROOT = Path(__file__).resolve().parents[3]


def _field_names() -> dict:
    """Tennis match-row field names from config, merged with computed accessors."""
    t = load_config("tennis_schema")["fields"]
    return {
        "date": t["date"],
        "tournament": t["tournament"],
        "tier": t["tier"],
        "round": t["round"],
        "edition_year": t["edition_year"],
        "player_a": t["player_a"],
        "player_b": t["player_b"],
        "score": t["score"],
        "status": t["status"],
        "status_completed": t["status_value_completed"],
        "void_flags": tuple(t["void_flags"]),
        "sets_a": t["sets_a"],
        "sets_b": t["sets_b"],
    }


def _refusal_reason(match: Mapping, f: dict) -> str:
    """Why a selected match is not rateable — mirrors the adapter's refusal logic
    using config names. Never invents a score; refuses and says why."""
    if match.get(f["status"]) != f["status_completed"]:
        return f"status is {match.get(f['status'])!r} (not {f['status_completed']!r})"
    for flag in f["void_flags"]:
        if match.get(flag):
            return f"marked {flag}"
    return "score cannot be parsed to final sets (empty, tied, or malformed)"


def _rate_match(match: Mapping, adapter, f: dict) -> dict:
    """Build the report row for one selected match (rated or refused)."""
    sets = adapter.extract_sets(match)
    base = {
        "date": match.get("date"),
        "tournament": match.get(f["tournament"]),
        "year": match.get(f["edition_year"]),
        "round": match.get("round"),
        "player_a": match.get(f["player_a"]),
        "player_b": match.get(f["player_b"]),
        "score": match.get(f["score"]),
    }
    if sets is None:
        base.update(
            {
                "rateable": False,
                "reason": _refusal_reason(match, f),
                "rating_a": None,
                "rating_b": None,
                "points_a": None,
                "points_b": None,
                "sections_a": None,
                "sections_b": None,
            }
        )
        return base
    r = rate_sets(sets)
    base.update(
        {
            "rateable": True,
            "reason": None,
            "rating_a": r.delta_a,
            "rating_b": r.delta_b,
            "points_a": r.total_a,
            "points_b": r.total_b,
            "sections_a": [s.section_a for s in r.sets],
            "sections_b": [s.section_b for s in r.sets],
        }
    )
    return base


def _aggregate(rows: List[dict]) -> List[dict]:
    """Per-player aggregates over the report rows. rating = sum of match ratings;
    average = rating / rated matches; refused = count of refused appearances."""
    acc: dict = {}
    for row in rows:
        for side in ("player_a", "player_b"):
            name = row[side]
            entry = acc.setdefault(
                name, {"player": name, "rating": 0, "matches": 0, "average": None, "refused": 0}
            )
            if row["rateable"]:
                entry["rating"] += row["rating_a"] if side == "player_a" else row["rating_b"]
                entry["matches"] += 1
                entry["average"] = entry["rating"] / entry["matches"]
            else:
                entry["refused"] += 1
    players = sorted(acc.values(), key=lambda p: (-p["rating"], p["player"]))
    return players


def _edition_in_scope(edition: Mapping, filters: Filters, mschema: Mapping) -> bool:
    """Is this loaded edition eligible under the effective filters? (Match-level
    filters like players cannot be judged at edition level.)"""
    identity = edition_identity(edition, mschema)
    if filters.tournaments and identity["tournament"] not in filters.tournaments:
        return False
    if filters.years and identity["year"] not in filters.years:
        return False
    tier = edition.get(mschema["edition_file_tier"]) if mschema["edition_file_tier"] else None
    if filters.tiers and tier not in filters.tiers:
        return False
    return True


def _effective_filters(caller: Filters, feed_cfg: Mapping) -> Filters:
    """Feed scope (config) composes with caller filters: a category the caller left
    empty falls back to the feed's value; a category the caller set overrides it.
    This keeps the configured feed scope true for every query."""
    feed = Filters.from_config(feed_cfg)
    return Filters(
        tournaments=caller.tournaments or feed.tournaments,
        years=caller.years or feed.years,
        players=caller.players or feed.players,
        tiers=caller.tiers or feed.tiers,
    )


def _effective_mutes(caller: Mutes, mutes_cfg: Mapping) -> Mutes:
    """Caller mutes union config-default mutes."""
    defaults = Mutes.from_config(mutes_cfg)
    return Mutes(
        mute_years=tuple(dict.fromkeys(defaults.mute_years + caller.mute_years)),
        mute_tournaments=tuple(
            dict.fromkeys(defaults.mute_tournaments + caller.mute_tournaments)
        ),
    )


def compute_ratings(
    filters: Optional[Filters] = None,
    mutes: Optional[Mutes] = None,
) -> dict:
    """Compute Phase 0 ratings live over the configured data tree.

    filters/mutes omitted -> defaults from engine/config/compute.json (the configured
    feed scope; no default mutes). Explicit filters compose with the feed scope;
    explicit mutes union the configured defaults.
    """
    cfg = load_config("compute")
    mschema = load_config("manifest_schema")
    f = _field_names()

    if filters is None:
        filters = Filters.from_config(cfg["feed"])
    else:
        filters = _effective_filters(filters, cfg["feed"])
    if mutes is None:
        mutes = Mutes.from_config(cfg["mutes"])
    else:
        mutes = _effective_mutes(mutes, cfg["mutes"])

    data_root = REPO_ROOT / cfg["data_root_relative_to_repo"]
    editions = load_editions(data_root, cfg["manifest_file"], mschema)

    adapter = TennisAdapter()
    rows: List[dict] = []
    for edition in editions:
        if not _edition_in_scope(edition, filters, mschema):
            continue
        for match in edition[mschema["edition_file_matches"]]:
            if not filters.allows(match, f):
                continue
            if mutes.applies(match, f):
                continue
            rows.append(_rate_match(match, adapter, f))

    rows.sort(key=lambda r: (r["date"] or "", r["player_a"] or "", r["player_b"] or ""))
    players = _aggregate(rows)

    rated = sum(1 for r in rows if r["rateable"])
    refused = len(rows) - rated

    return {
        "report_schema": "1.0",
        "scope": {
            "filters": filters.as_dict(),
            "mutes": mutes.as_dict(),
            "loaded_editions": sorted(
                (edition_identity(e, mschema) for e in editions),
                key=lambda e: (e["tournament"], e["year"]),
            ),
            "feed_editions": sorted(
                (
                    edition_identity(e, mschema)
                    for e in editions
                    if _edition_in_scope(e, filters, mschema)
                ),
                key=lambda e: (e["tournament"], e["year"]),
            ),
            "data_root": str(data_root),
        },
        "summary": {
            "matches_selected": len(rows),
            "matches_rated": rated,
            "matches_refused": refused,
            "players_rated": sum(1 for p in players if p["matches"] > 0),
        },
        "matches": rows,
        "players": players,
    }
