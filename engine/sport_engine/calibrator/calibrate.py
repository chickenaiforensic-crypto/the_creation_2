"""Score Calibrator — regional point-assignment algorithm.

Ensures the engine's generated ratings reflect the leaderboard hierarchy (1st, 2nd,
3rd, ...) by adding per-region supplemental points.

Method (regional isotonic / PAVA):
  1. per-region mean of raw ratings (regions = leaderboard position bands)
  2. enforce monotone non-increasing region targets (Pool Adjacent Violators)
  3. region adjustment = target - mean, applied to every player in the region
  4. measure reflection accuracy (cross-region correctly-ordered pair ratio +
     Spearman rating vs position) before and after calibration.

Applied per (year, tournament); 2021 is the baseline, then 2022-2025.
Zero-hardcoding: regions, positions and thresholds come from data + config.
"""

from __future__ import annotations

from statistics import mean
from typing import List, Optional

from sport_engine.calibrator.distribution import analyze_distribution, region_stats
from sport_engine.compute.ratings_table import build_ratings_table
from sport_engine.compute.selection import Filters, Mutes
from sport_engine.config import load_config


def _pava_targets(means: List[float]) -> List[float]:
    """Monotone non-increasing targets via Pool Adjacent Violators (PAVA)."""
    blocks: List[List[float]] = [[m] for m in means]
    while True:
        merged = False
        for i in range(len(blocks) - 1):
            if mean(blocks[i]) < mean(blocks[i + 1]):
                blocks[i] = blocks[i] + blocks[i + 1]
                del blocks[i + 1]
                merged = True
                break
        if not merged:
            break
    targets: List[float] = []
    for b in blocks:
        targets.extend([mean(b)] * len(b))
    return targets


def _ranks(values: List[float]) -> List[float]:
    """Average ranks (ties share the average rank)."""
    idx = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    i = 0
    while i < len(idx):
        j = i
        while j + 1 < len(idx) and values[idx[j + 1]] == values[idx[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            out[idx[k]] = avg
        i = j + 1
    return out


def _spearman_rating_vs_position(rows: List[dict], rating_key: str) -> Optional[float]:
    """Spearman correlation between rating and position number. Negative means
    higher position number (worse finish) has lower rating — the correct direction."""
    if len(rows) < 2:
        return None
    x = _ranks([r[rating_key] for r in rows])
    y = _ranks([r["position_number"] for r in rows])
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    vx = sum((a - mx) ** 2 for a in x) ** 0.5
    vy = sum((b - my) ** 2 for b in y) ** 0.5
    if vx == 0 or vy == 0:
        return None
    return cov / (vx * vy)


def _reflection_accuracy(rows: List[dict], rating_key: str) -> Optional[float]:
    """Fraction of cross-region player pairs correctly ordered by rating
    (lower position number -> higher rating). Same-region pairs and equal-rating
    pairs are not judged (regional calibration cannot reorder within a region)."""
    judged = []
    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            if a["position_number"] != b["position_number"] and a[rating_key] != b[rating_key]:
                judged.append((a, b))
    if not judged:
        return None
    correct = sum(
        1
        for a, b in judged
        if (a["position_number"] < b["position_number"])
        == (a[rating_key] > b[rating_key])
    )
    return correct / len(judged)


def calibrate_table(table: dict, min_adjustment: float = 0.0) -> dict:
    """Apply regional calibration to one ratings table. Mutates each row dict with
    region_adjustment and rating_calibrated. Adjustments below min_adjustment are
    dropped (noise-level shifts are not applied). Returns the calibration record."""
    rows = table["rows"]
    stats = region_stats(rows)
    positions = sorted(stats)
    means = [stats[p]["mean"] for p in positions]
    targets = _pava_targets(means)
    proposed = {p: targets[i] - means[i] for i, p in enumerate(positions)}
    adjustments = {
        p: (round(a, 2) if abs(a) >= min_adjustment else 0.0)
        for p, a in proposed.items()
    }
    for r in rows:
        r["region_adjustment"] = adjustments[r["position_number"]]
        r["rating_calibrated"] = round(r["rating"] + r["region_adjustment"], 2)
    return {
        "region_targets": {p: round(t, 2) for p, t in zip(positions, targets)},
        "region_adjustments": {p: round(a, 2) for p, a in adjustments.items()},
        "accuracy_raw": _reflection_accuracy(rows, "rating"),
        "accuracy_calibrated": _reflection_accuracy(rows, "rating_calibrated"),
        "spearman_raw": _spearman_rating_vs_position(rows, "rating"),
        "spearman_calibrated": _spearman_rating_vs_position(rows, "rating_calibrated"),
    }


def run_score_calibrator(
    filters: Optional[Filters] = None,
    mutes: Optional[Mutes] = None,
) -> dict:
    """Run the Score Calibrator over the selected (year, tournament) tables.

    Returns per-year calibration results (distribution, region adjustments,
    calibrated rows, accuracy before/after) plus a summary table.
    """
    cfg = load_config("calibrator")
    tables = build_ratings_table(filters, mutes)["tables"]

    results = []
    for table in tables:
        distribution = analyze_distribution(table, float(cfg["cluster_gap"]))
        calibration = calibrate_table(table, float(cfg["min_adjustment"]))
        # re-rank by calibrated rating (the calibrated leaderboard order)
        table["rows"].sort(key=lambda r: (-r["rating_calibrated"], r["player"]))
        for rank, r in enumerate(table["rows"], 1):
            r["rank"] = rank
        results.append(
            {
                "tournament": table["tournament"],
                "year": table["year"],
                "distribution": distribution,
                "calibration": calibration,
                "rows": table["rows"],
            }
        )

    summary = {}
    for r in results:
        cal = r["calibration"]
        summary[r["year"]] = {
            "accuracy_raw": cal["accuracy_raw"],
            "accuracy_calibrated": cal["accuracy_calibrated"],
            "spearman_raw": cal["spearman_raw"],
            "spearman_calibrated": cal["spearman_calibrated"],
        }

    calibrated_accs = [v["accuracy_calibrated"] for v in summary.values() if v["accuracy_calibrated"] is not None]
    raw_accs = [v["accuracy_raw"] for v in summary.values() if v["accuracy_raw"] is not None]

    return {
        "schema": "score_calibrator.1.0",
        "method": cfg["method"],
        "summary": summary,
        "overall": {
            "mean_accuracy_raw": mean(raw_accs) if raw_accs else None,
            "mean_accuracy_calibrated": mean(calibrated_accs) if calibrated_accs else None,
            "target_accuracy": float(cfg["accuracy_target"]),
        },
        "results": results,
    }
