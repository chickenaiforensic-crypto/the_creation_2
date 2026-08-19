"""Generate the Score Calibrator markdown report from the engine run.

Usage (from engine/):  python3 tools/generate_calibrator_report.py
Writes: reports/score_calibrator_report.md

Structural formatting only — every number comes from the engine run (data + config).
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sport_engine.calibrator.calibrate import run_score_calibrator  # noqa: E402


def _ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def _pct(x) -> str:
    return "—" if x is None else f"{x * 100:.2f}%"


def _render_year(result: dict) -> list:
    year = result["year"]
    dist = result["distribution"]
    cal = result["calibration"]
    lines = [f"## {year} — {result['tournament']}", ""]

    lines.append(f"Matches: selected={dist['summary']['matches_selected']} "
                 f"rated={dist['summary']['matches_rated']} "
                 f"refused={dist['summary']['matches_refused']} "
                 f"players={dist['summary']['players']}")

    lines.append("")
    lines.append("### Distribution — regions (top performer down to last)")
    lines.append("")
    lines.append("| Region (position) | Players | Mean raw rating | Min | Max | Std |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for pos, s in dist["regions"].items():
        lines.append(
            f"| {_ordinal(pos)} | {s['count']} | {s['mean']:.2f} | {s['min']:.1f} "
            f"| {s['max']:.1f} | {s['std']:.2f} |"
        )

    lines.append("")
    lines.append("### Density clusters (rating gaps ≤ cluster_gap)")
    lines.append("")
    if dist["clusters"]:
        lines.append("| Cluster | Players | Rating span | Members (first/last) |")
        lines.append("|---|---:|---:|---|")
        for c in dist["clusters"][:5]:
            span = f"{c['min_rating']} .. {c['max_rating']}"
            members = f"{c['players'][0]} … {c['players'][-1]} ({c['count']} total)"
            lines.append(f"| #{dist['clusters'].index(c) + 1} | {c['count']} | {span} | {members} |")
    else:
        lines.append("No clusters of 2+ players within the gap threshold.")

    lines.append("")
    lines.append("### Regional assignments (added points per region)")
    lines.append("")
    lines.append("| Region | Mean raw | Target | Adjustment |")
    lines.append("|---|---:|---:|---:|")
    for pos in sorted(cal["region_adjustments"]):
        lines.append(
            f"| {_ordinal(pos)} | {dist['regions'][pos]['mean']:.2f} "
            f"| {cal['region_targets'][pos]:.2f} "
            f"| {cal['region_adjustments'][pos]:+.2f} |"
        )

    lines.append("")
    lines.append("### Reflection accuracy")
    lines.append("")
    lines.append("| Metric | Raw | Calibrated |")
    lines.append("|---|---:|---:|")
    lines.append(f"| Cross-region correctly-ordered pairs | {_pct(cal['accuracy_raw'])} "
                 f"| {_pct(cal['accuracy_calibrated'])} |")
    lines.append(f"| Spearman (rating vs position) | {cal['spearman_raw']:.4f} "
                 f"| {cal['spearman_calibrated']:.4f} |")

    lines.append("")
    lines.append("### Calibrated leaderboard (top 10 of "
                 f"{len(result['rows'])}) — rating = raw + region adjustment")
    lines.append("")
    lines.append("| # | Player | Raw | Region adj | Calibrated | Position |")
    lines.append("|---|---:|---:|---:|---:|---|")
    for p in result["rows"][:10]:
        lines.append(
            f"| {p['rank']} | {p['player']} | {p['rating']:+d} "
            f"| {p['region_adjustment']:+.2f} | {p['rating_calibrated']:+.2f} "
            f"| {p['position']} |"
        )
    lines.append("")
    return lines


def main() -> None:
    run = run_score_calibrator()
    out = ["# SCORE CALIBRATOR — Cincinnati Masters 2021–2025", ""]
    out.append("Regional point-assignment layer: each year's raw Phase 0 ratings are "
               "analyzed from the top performer down to the last, density clusters are "
               "detected, and per-region supplemental points (isotonic/PAVA targets, "
               "min-adjustment threshold applied) are added so ratings reflect the "
               "leaderboard hierarchy. 2021 is the baseline; 2022–2025 follow.")
    out.append("")
    out.append("| Year | Raw accuracy | Calibrated accuracy | Spearman raw | Spearman calibrated |")
    out.append("|---|---:|---:|---:|---:|")
    for year, v in run["summary"].items():
        out.append(f"| {year} | {_pct(v['accuracy_raw'])} | {_pct(v['accuracy_calibrated'])} "
                   f"| {v['spearman_raw']:.4f} | {v['spearman_calibrated']:.4f} |")
    o = run["overall"]
    out.append(f"| **Mean** | **{_pct(o['mean_accuracy_raw'])}** "
               f"| **{_pct(o['mean_accuracy_calibrated'])}** | — | — |")
    out.append("")
    out.append(f"Target accuracy: {_pct(o['target_accuracy'])}. "
               "Method: regional_isotonic_pava. Accuracy = fraction of cross-region "
               "player pairs correctly ordered by rating; same-region and equal-rating "
               "pairs are not judged.")
    out.append("")
    for result in run["results"]:
        out.extend(_render_year(result))

    report = Path(__file__).resolve().parents[1] / "reports" / "score_calibrator_report.md"
    report.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {report}")


if __name__ == "__main__":
    main()
