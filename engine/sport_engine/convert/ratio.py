"""Standalone conversion layer — ratio (percentage) computation.

Every section that needs a percentage output (H2H, ratings, future sections)
plugs into this layer; each call is independent and returns that section's own
answer (no shared state between sections).

Region point mapping (per Director theory table, 2026-08-19):
  a set's games are normalised by subtracting 1 from BOTH sides until the higher
  side has at most 6 games (7-6 -> 6-5, 7-5 -> 6-4, 8-6 -> 7-5 -> 6-4), then the
  Phase 0 points table (config rating_rules.json) is applied per side.
  Example 7-6 7-6 -> per set 10/7 -> totals 20/14 -> 58.8%/41.2%.

Ratio lock:
  %A = pointsA / (pointsA + pointsB) · %B = 100 − %A (computed as the remainder
  so the two sides always sum to 100.0).
  Inputs must be non-negative RAW region point totals. The differential rating
  (e.g. +12/-12) is a separate metric and is rejected as an input.

Zero-hardcoding: the points table, max games, and scaling come from config.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from sport_engine.config import load_config
from sport_engine.rating.phase0 import MAX_WINNER_GAMES, points_for_games


def region_points_for_set(a: int, b: int) -> Tuple[int, int]:
    """Raw region points for one set (gamesA, gamesB) -> (pointsA, pointsB).

    Normalises by subtracting 1 from BOTH sides until the higher side is at most
    max_winner_games (6): 7-6 -> 6-5, 7-5 -> 6-4, 8-6 -> 6-4. Orientation is
    preserved. Then maps each side's games to the Phase 0 points table.
    """
    if a < 0 or b < 0:
        raise ValueError(f"negative games in set {a}-{b}")
    if a == b:
        raise ValueError(f"set cannot be tied {a}-{b} (unfinished or invalid)")
    na, nb = a, b
    while max(na, nb) > MAX_WINNER_GAMES:
        na -= 1
        nb -= 1
        if na < 0 or nb < 0:
            raise ValueError(f"set score cannot normalise to {MAX_WINNER_GAMES} games: {a}-{b}")
    return points_for_games(na), points_for_games(nb)


def region_points(sets: List[Tuple[int, int]]) -> dict:
    """Raw region point totals for a match from per-set (gamesA, gamesB)."""
    points_a = points_b = 0
    details = []
    for a, b in sets:
        pa, pb = region_points_for_set(a, b)
        points_a += pa
        points_b += pb
        details.append({"games_a": a, "games_b": b, "points_a": pa, "points_b": pb})
    return {"region_points_a": points_a, "region_points_b": points_b, "sets": details}


def ratio_lock(points_a: float, points_b: float) -> dict:
    """Relative balance out of 100% from two raw region point totals.

    Inputs must be non-negative raw point totals. The differential rating is NOT
    a valid input (rejected). Linear scaling for this iteration; the exponential
    expansion factor (config convert.json) remains disabled.
    """
    cfg = load_config("convert")
    if points_a < 0 or points_b < 0:
        raise ValueError(
            "ratio_lock inputs must be non-negative raw region point totals "
            f"(got {points_a}, {points_b}); the differential rating is not an input "
            "to the percentage layer."
        )
    total = points_a + points_b
    if total == 0:
        pA_pct = pB_pct = None
    else:
        pA_pct = round(points_a / total * 100, 2)
        pB_pct = round(100 - pA_pct, 2)
    return {
        "points_a": round(points_a, 2),
        "points_b": round(points_b, 2),
        "pA_pct": pA_pct,
        "pB_pct": pB_pct,
        "scaling": cfg.get("scaling", "linear"),
        "exponential_enabled": bool(cfg.get("exponential_enabled", False)),
    }
