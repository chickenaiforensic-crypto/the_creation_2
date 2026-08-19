"""Ratings-only subsystem — a player's rating is the ACCUMULATION of their own
Phase 0 points per match, WITHOUT subtracting the opponent's points.

This is a distinct metric from the Phase 0 delta rating (pA = totalA - totalB).
Here the rating is totalA alone (or totalB for a B-side match), summed across the
player's rated matches in the selected tournament scope and year period.

Scope is chosen by the caller with tournament / year (or year period) filters —
the same Filters/Mutes selection as the rest of the engine. The metric reuses the
manifest-verified loader and the live compute pipeline (compute_ratings), which
already exposes each selected match's points_a / points_b; it only aggregates the
player's own points and never reads the opponent's points or the delta.

Zero-hardcoding: the metric definition lives in engine/config/ratings.json; field
names come from config (tennis_schema / manifest_schema); no value is in code.
"""

from __future__ import annotations

from collections import defaultdict
from typing import List, Optional

from sport_engine.compute.compute import compute_ratings
from sport_engine.compute.selection import Filters, Mutes, year_range
from sport_engine.config import load_config


def _effective_years(
    years: Optional[List[str]],
    years_from: Optional[str],
    years_to: Optional[str],
) -> List[str]:
    """Year selection: an explicit year period (from/to) wins; otherwise an
    explicit year list; otherwise empty (all years in scope)."""
    if years_from or years_to:
        rp = load_config("ui")["ratings_percentage"]
        return year_range(years_from, years_to, rp["default_from_year"], rp["default_to_year"])
    return list(years or [])


def run_ratings(
    player: str,
    tournaments: Optional[List[str]] = None,
    years: Optional[List[str]] = None,
    tours: Optional[List[str]] = None,
    years_from: Optional[str] = None,
    years_to: Optional[str] = None,
    mutes: Optional[Mutes] = None,
) -> dict:
    """Accumulated-points rating for one player over the selected scope.

    The rating is the sum of the player's own Phase 0 points across every rated
    match in scope — no opponent subtraction. Returns the total plus per-year and
    per-tournament accumulations and a chronological per-match breakdown.
    """
    cfg = load_config("ratings")
    effective_years = _effective_years(years, years_from, years_to)
    filters = Filters(
        players=[player],
        tournaments=tournaments or [],
        years=effective_years,
        tours=tours or [],
    )
    mutes = mutes or Mutes()
    report = compute_ratings(filters=filters, mutes=mutes)

    total = 0
    rated = 0
    per_year = defaultdict(lambda: {"points": 0, "matches": 0})
    per_tournament = defaultdict(lambda: {"points": 0, "matches": 0})
    matches: List[dict] = []
    for m in report["matches"]:
        if not m["rateable"]:
            continue
        if m["player_a"] == player:
            pts = m["points_a"]
            opponent = m["player_b"]
        elif m["player_b"] == player:
            pts = m["points_b"]
            opponent = m["player_a"]
        else:
            continue
        total += pts
        rated += 1
        per_year[m["year"]]["points"] += pts
        per_year[m["year"]]["matches"] += 1
        per_tournament[m["tournament"]]["points"] += pts
        per_tournament[m["tournament"]]["matches"] += 1
        matches.append(
            {
                "date": m["date"],
                "tournament": m["tournament"],
                "year": m["year"],
                "round": m["round"],
                "opponent": opponent,
                "score": m["score"],
                "points": pts,
            }
        )

    matches.sort(key=lambda r: (r["date"] or "", r["tournament"] or ""))

    return {
        "schema": "ratings.1.0",
        "player": player,
        "method": cfg["method"],
        "subtract_opponent": bool(cfg["subtract_opponent"]),
        "basis": cfg["basis"],
        "scope": {
            "tournaments": list(filters.tournaments),
            "years": list(filters.years),
            "tours": list(filters.tours),
            "mutes": mutes.as_dict(),
        },
        "rating": total,
        "matches_rated": rated,
        "per_year": [
            {"year": y, "points": v["points"], "matches": v["matches"]}
            for y, v in sorted(per_year.items())
        ],
        "per_tournament": [
            {"tournament": t, "points": v["points"], "matches": v["matches"]}
            for t, v in sorted(per_tournament.items(), key=lambda kv: -kv[1]["points"])
        ],
        "matches": matches,
    }
