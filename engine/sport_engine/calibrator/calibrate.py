"""Score Calibrator — CENTRAL (cross-year) regional analysis.

Pools every player across all selected years into ONE cluster, analyzes the raw
Phase 0 rating distribution from 1st position to last (all regions), and derives
central region targets (isotonic / PAVA) and adjustments.

Director decision (2026-08-19): the calibration is NOT applied — the engine uses
the raw Phase 0 points. Reason, verified from the bytes: the pooled region means
are already monotonically ordered (1st > 2nd ≥ 3rd > ... > last), so the central
PAVA adjustments are all zero and central raw accuracy equals central calibrated
accuracy. The per-year calibration scope is still reported (per-year adjustments
were year-local noise that cancels out centrally).

Zero-hardcoding: everything comes from data + config — no literals in code.
"""

from __future__ import annotations

from collections import defaultdict
from statistics import mean, pstdev
from typing import List, Optional

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
    (lower position number -> higher rating). Same-region and equal-rating pairs
    are not judged (regional calibration cannot reorder within a region)."""
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


def _per_year_adjustments(tables: List[dict], min_adjustment: float) -> dict:
    """The per-year calibration scope: what each single year would have needed
    locally (for reporting only — not applied)."""
    out: dict = {}
    for table in tables:
        rows = table["rows"]
        groups: dict = defaultdict(list)
        for r in rows:
            groups.setdefault(r["position_number"], []).append(r["rating"])
        positions = sorted(groups)
        means = [mean(groups[p]) for p in positions]
        targets = _pava_targets(means)
        proposed = {p: targets[i] - means[i] for i, p in enumerate(positions)}
        adj = {p: (round(a, 2) if abs(a) >= min_adjustment else 0.0) for p, a in proposed.items()}
        out[table["year"]] = adj
    return out


def run_score_calibrator(
    filters: Optional[Filters] = None,
    mutes: Optional[Mutes] = None,
) -> dict:
    """Central (cross-year) calibration analysis over the selected tables.

    Pools every player across all years into one cluster, computes central region
    stats 1st->last, central PAVA targets and adjustments, and measures raw vs
    calibrated accuracy. Calibration is NOT applied (config: applied=false) — the
    engine uses raw Phase 0 points.
    """
    cfg = load_config("calibrator")
    tables = build_ratings_table(filters, mutes)["tables"]
    years = [t["year"] for t in tables]

    pooled: List[dict] = []
    for table in tables:
        for p in table["rows"]:
            pooled.append(
                {
                    "player": p["player"],
                    "year": table["year"],
                    "position": p["position"],
                    "position_number": p["position_number"],
                    "rating": p["rating"],
                }
            )

    groups: dict = defaultdict(list)
    for p in pooled:
        groups[p["position_number"]].append(p["rating"])

    regions: dict = {}
    for pos in sorted(groups):
        vals = sorted(groups[pos])
        regions[pos] = {
            "count": len(vals),
            "mean": mean(vals),
            "min": vals[0],
            "max": vals[-1],
            "std": pstdev(vals),
        }

    positions = sorted(regions)
    means = [regions[p]["mean"] for p in positions]
    targets = _pava_targets(means)
    proposed = {p: targets[i] - means[i] for i, p in enumerate(positions)}
    adjustments = {
        p: (round(a, 2) if abs(a) >= float(cfg["min_adjustment"]) else 0.0)
        for p, a in proposed.items()
    }

    rows = [dict(p, rating_calibrated=p["rating"] + adjustments[p["position_number"]]) for p in pooled]
    accuracy_raw = _reflection_accuracy(rows, "rating")
    accuracy_calibrated = _reflection_accuracy(rows, "rating_calibrated")
    spearman_raw = _spearman_rating_vs_position(rows, "rating")
    spearman_calibrated = _spearman_rating_vs_position(rows, "rating_calibrated")

    return {
        "schema": "score_calibrator.1.0",
        "method": cfg["method"],
        "scope": cfg["scope"],
        "applied": bool(cfg["applied"]),
        "years": years,
        "pooled_players": len(pooled),
        "regions": regions,
        "targets": {p: round(t, 2) for p, t in zip(positions, targets)},
        "adjustments": adjustments,
        "per_year_adjustments": _per_year_adjustments(tables, float(cfg["min_adjustment"])),
        "accuracy": {
            "raw": accuracy_raw,
            "calibrated": accuracy_calibrated,
            "equal": (
                accuracy_raw == accuracy_calibrated
                if accuracy_raw is not None and accuracy_calibrated is not None
                else None
            ),
        },
        "spearman": {"raw": spearman_raw, "calibrated": spearman_calibrated},
        "target_accuracy": float(cfg["accuracy_target"]),
    }
