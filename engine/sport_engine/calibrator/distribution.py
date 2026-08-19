"""Score Calibrator — distribution analysis.

Analyzes the raw Phase 0 rating distribution of a (year, tournament) ratings table
from the top performer down to the last: per-region (position-band) statistics and
density clusters. All numbers come from the data; the cluster gap threshold comes
from config — no literals in code (zero-hardcoding rule).
"""

from __future__ import annotations

from statistics import mean, pstdev
from typing import List


def region_stats(rows: List[dict]) -> dict:
    """Position-band aggregates of raw ratings: count, mean, min, max, std.

    Regions are leaderboard position bands (1, 2, 3, 5, 9, 17, 33, 65) taken from
    each row's position_number (derived from the stored result tree via
    config/position_rules.json).
    """
    groups: dict = {}
    for r in rows:
        groups.setdefault(r["position_number"], []).append(r["rating"])
    out: dict = {}
    for pos in sorted(groups):
        vals = sorted(groups[pos])
        out[pos] = {
            "count": len(vals),
            "mean": mean(vals),
            "min": vals[0],
            "max": vals[-1],
            "std": pstdev(vals) if len(vals) > 1 else 0.0,
        }
    return out


def detect_clusters(rows: List[dict], gap_threshold: float) -> List[dict]:
    """Consecutive players (by rating, descending) whose rating gap is <= threshold
    form a density cluster. Returns clusters with 2+ players, largest first."""
    if not rows:
        return []
    s = sorted(rows, key=lambda r: -r["rating"])
    clusters: List[List[dict]] = []
    cur = [s[0]]
    for a, b in zip(s, s[1:]):
        if a["rating"] - b["rating"] <= gap_threshold:
            cur.append(b)
        else:
            clusters.append(cur)
            cur = [b]
    clusters.append(cur)
    out = []
    for c in clusters:
        if len(c) > 1:
            ratings = [r["rating"] for r in c]
            out.append(
                {
                    "players": [r["player"] for r in c],
                    "count": len(c),
                    "min_rating": min(ratings),
                    "max_rating": max(ratings),
                    "span": max(ratings) - min(ratings),
                }
            )
    out.sort(key=lambda c: -c["count"])
    return out


def analyze_distribution(table: dict, gap_threshold: float) -> dict:
    """Distribution record for one (year, tournament) table."""
    return {
        "tournament": table["tournament"],
        "year": table["year"],
        "summary": table["summary"],
        "regions": region_stats(table["rows"]),
        "clusters": detect_clusters(table["rows"], gap_threshold),
    }
