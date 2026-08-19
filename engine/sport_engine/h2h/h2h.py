"""Phase 1 — Head-to-Head (H2H) computation module.

Hooks into the pre-built game-score-difference engine (the tennis adapter's
per-set extraction + Phase 0 set normalisation) and computes the DIRECT game
score difference between pA and pB — the margin — while the primary Phase 0
rating tracks absolute points gathered without margins.

Point allocation: points are awarded per game of score difference
(config h2h.json, points_per_game_difference). E.g. normalised sets 6-2 6-4
give pA a game difference of +6 -> +6 H2H points, pB -6.

Decoupled, stand-alone layer:
- own data model (no points/rating/calibration fields),
- own pipeline (load -> filter/mute -> extract -> normalise -> difference ->
  aggregate),
- own state; never imports the absolute-point tracking routines
  (rate_sets, GAMES_TO_POINTS, compute_ratings, _aggregate).
Reuses only the pre-built difference machinery: TennisAdapter.extract_sets and
Phase 0 normalize_set, plus the shared manifest-verified data loader and the
pure Filters/Mutes selection logic.

Tournament-aware tracking (Phase 1 extension, 2026-08-19): every player carries
their per-tournament context (matches, games, difference, average per
tournament) in addition to all-tournament totals, so the module traces the
specific tournament context for each player. The tournaments filter supports
multi-tournament ingestion (the UI can select multiple tournaments for H2H).
A future per-tournament calibration hook (conversion_hook) will normalize
separate raw tournament ratings for cross-tournament comparison when players
arrive from different data pools — currently a placeholder, never applied.

Zero-hardcoding: all field names come from config (tennis_schema,
manifest_schema); the per-game difference points from config (h2h.json).
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import List, Optional

from sport_engine.adapters.tennis import TennisAdapter
from sport_engine.compute.data_source import edition_identity, load_editions
from sport_engine.compute.selection import Filters, Mutes
from sport_engine.config import load_config
from sport_engine.convert.ratio import region_points
from sport_engine.h2h import conversion_hook
from sport_engine.rating.phase0 import normalize_set

REPO_ROOT = Path(__file__).resolve().parents[3]


def _fields() -> dict:
    """Tennis match-row field names from config (schema lives in config, not code)."""
    t = load_config("tennis_schema")["fields"]
    return {
        "date": t["date"],
        "tournament": t["tournament"],
        "tour": t["tour"],
        "round": t["round"],
        "edition_year": t["edition_year"],
        "player_a": t["player_a"],
        "player_b": t["player_b"],
        "score": t["score"],
        "status": t["status"],
        "status_completed": t["status_value_completed"],
        "void_flags": tuple(t["void_flags"]),
    }


def _refusal_reason(match: dict, f: dict) -> str:
    """Why a selected match is not rateable — mirrors the adapter's refusal
    logic using config names. Never invents a score; refuses and says why."""
    if match.get(f["status"]) != f["status_completed"]:
        return f"status is {match.get(f['status'])!r} (not {f['status_completed']!r})"
    for flag in f["void_flags"]:
        if match.get(flag):
            return f"marked {flag}"
    return "score cannot be parsed to final sets (empty, tied, or malformed)"


def match_region_points(sets: List[tuple]) -> dict:
    """Raw region point totals for one match — delegated to the standalone
    conversion layer (convert.region_points). The totals are non-negative raw
    points — the input the ratio lock feeds on (NOT the differential rating)."""
    return region_points(sets)


def match_game_difference(sets: List[tuple]) -> dict:
    """Direct game score difference for one match from per-set (gamesA, gamesB).

    Normalises every set with the pre-built Phase 0 engine (7-5 -> 6-4, 7-6 ->
    6-4, orientation preserved), then sums the per-set game differences.
    Points = difference * points_per_game_difference (config).
    """
    ppg = float(load_config("h2h")["points_per_game_difference"])
    games_a = games_b = 0
    set_details = []
    for a, b in sets:
        na, nb = normalize_set(a, b)
        games_a += na
        games_b += nb
        set_details.append({"games_a": na, "games_b": nb, "difference": na - nb})
    difference = games_a - games_b
    return {
        "games_a": games_a,
        "games_b": games_b,
        "game_difference": difference,
        "h2h_a": round(difference * ppg),
        "h2h_b": round(-difference * ppg),
        "sets": set_details,
    }


def _rate_match(match: dict, adapter: TennisAdapter, f: dict) -> dict:
    """Build the H2H report row for one selected match (rated or refused)."""
    sets = adapter.extract_sets(match)
    base = {
        "date": match.get(f["date"]),
        "tournament": match.get(f["tournament"]),
        "year": match.get(f["edition_year"]),
        "round": match.get(f["round"]),
        "player_a": match.get(f["player_a"]),
        "player_b": match.get(f["player_b"]),
        "score": match.get(f["score"]),
    }
    if sets is None:
        base.update(
            {
                "rateable": False,
                "reason": _refusal_reason(match, f),
                "games_a": None,
                "games_b": None,
                "game_difference": None,
                "h2h_a": None,
                "h2h_b": None,
                "region_points_a": None,
                "region_points_b": None,
                "sets": None,
            }
        )
        return base
    diff = match_game_difference(sets)
    points = match_region_points(sets)
    base.update({"rateable": True, "reason": None, **diff, **points})
    return base


def _aggregate(rows: List[dict]) -> List[dict]:
    """Per-player H2H aggregates over the report rows.

    Tournament-aware tracking: each player carries their per-tournament context
    (per-tournament matches, games, difference, average) in addition to their
    all-tournament totals, so the H2H module traces and maintains the specific
    tournament context for each individual player.

    game_difference = games_for - games_against (sum over rated matches);
    average = difference / rated matches; refused = refused appearances.
    """
    acc: dict = {}
    for row in rows:
        tournament = row["tournament"]
        for side in ("player_a", "player_b"):
            name = row[side]
            entry = acc.setdefault(
                name,
                {
                    "player": name,
                    "matches": 0,
                    "games_for": 0,
                    "games_against": 0,
                    "game_difference": 0,
                    "average": None,
                    "refused": 0,
                    "tournaments": {},  # tournament -> per-tournament context
                },
            )
            tctx = entry["tournaments"].setdefault(
                tournament,
                {"tournament": tournament, "matches": 0, "games_for": 0,
                 "games_against": 0, "game_difference": 0, "average": None},
            )
            if row["rateable"]:
                g = row["games_a"] if side == "player_a" else row["games_b"]
                entry["games_for"] += g
                entry["games_against"] += row["games_a"] + row["games_b"] - g
                entry["matches"] += 1
                entry["game_difference"] = entry["games_for"] - entry["games_against"]
                entry["average"] = entry["game_difference"] / entry["matches"]
                tctx["games_for"] += g
                tctx["games_against"] += row["games_a"] + row["games_b"] - g
                tctx["matches"] += 1
                tctx["game_difference"] = tctx["games_for"] - tctx["games_against"]
                tctx["average"] = tctx["game_difference"] / tctx["matches"]
            else:
                entry["refused"] += 1
    for p in acc.values():
        p["tournaments"] = sorted(p["tournaments"].values(),
                                  key=lambda t: (-t["game_difference"], t["tournament"]))
    players = sorted(acc.values(), key=lambda p: (-p["game_difference"], p["player"]))
    return players


def _effective_filters(caller: Filters, feed_cfg: dict) -> Filters:
    """Feed scope (config) composes with caller filters: a category the caller
    left empty falls back to the feed's value; a category the caller set
    overrides it. Same semantics as the primary layer — the H2H subsystem is
    decoupled in state, not in feed scope."""
    feed = Filters.from_config(feed_cfg)
    return Filters(
        tournaments=caller.tournaments or feed.tournaments,
        years=caller.years or feed.years,
        players=caller.players or feed.players,
        tiers=caller.tiers or feed.tiers,
        tours=caller.tours or feed.tours,
    )


def run_h2h(
    filters: Optional[Filters] = None,
    mutes: Optional[Mutes] = None,
) -> dict:
    """Stand-alone H2H computation over the configured data tree.

    Independent subsystem: same feed scope / filters / mutes as the primary
    layer (config compute.json applies underneath), but computes only the
    direct game score difference — never absolute points.
    """
    cfg = load_config("compute")
    mschema = load_config("manifest_schema")
    f = _fields()
    _ = load_config("h2h")  # validate h2h config exists (fails loudly if not)

    if filters is None:
        filters = Filters.from_config(cfg["feed"])
    else:
        filters = _effective_filters(filters, cfg["feed"])
    if mutes is None:
        mutes = Mutes.from_config(cfg["mutes"])

    data_root = REPO_ROOT / cfg["data_root_relative_to_repo"]
    editions = load_editions(data_root, cfg["manifest_file"], mschema)

    adapter = TennisAdapter()
    rows: List[dict] = []
    for edition in editions:
        if filters.tournaments and edition[mschema["edition_file_tournament"]] not in filters.tournaments:
            continue
        if filters.years and str(edition[mschema["edition_file_year"]]) not in filters.years:
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
        "schema": "h2h.1.0",
        "scope": {
            "filters": filters.as_dict(),
            "mutes": mutes.as_dict(),
            "loaded_editions": sorted(
                (edition_identity(e, mschema) for e in editions),
                key=lambda e: (e["tournament"], e["year"]),
            ),
            "data_root": str(data_root),
        },
        "conversion_hook": {
            "available": conversion_hook.available(),
            "configured_method": load_config("h2h_tournament")["conversion_hook"]["method"],
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
