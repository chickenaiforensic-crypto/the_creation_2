"""Generate the CENTRAL Score Calibrator markdown report from the engine run.

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


def main() -> None:
    run = run_score_calibrator()
    out = ["# SCORE CALIBRATOR — CENTRAL (cross-year) analysis, Cincinnati Masters 2021–2025", ""]
    out.append("Every player across all five years is pooled into ONE cluster and analyzed "
               "from 1st position to last. Central targets/adjustments use isotonic (PAVA). "
               "Per Director decision (2026-08-19): the calibration is NOT applied — the "
               "engine uses the raw Phase 0 points.")
    out.append("")
    out.append(f"**Scope:** {run['scope']} · **Applied to ratings:** {run['applied']} "
               f"(raw points used) · **Pooled players:** {run['pooled_players']} "
               f"(years {', '.join(run['years'])})")
    out.append("")
    out.append("### Central region distribution — 1st position to last")
    out.append("")
    out.append("| Region | Players | Mean raw rating | Min | Max | Std |")
    out.append("|---|---:|---:|---:|---:|---:|")
    for pos, s in run["regions"].items():
        out.append(f"| {_ordinal(pos)} | {s['count']} | {s['mean']:.2f} | {s['min']:.1f} "
                   f"| {s['max']:.1f} | {s['std']:.2f} |")
    out.append("")
    out.append("### Central adjustments")
    out.append("")
    out.append("| Region | Mean raw | Target (PAVA) | Adjustment |")
    out.append("|---|---:|---:|---:|")
    for pos in run["adjustments"]:
        out.append(f"| {_ordinal(pos)} | {run['regions'][pos]['mean']:.2f} "
                   f"| {run['targets'][pos]:.2f} | {run['adjustments'][pos]:+.2f} |")
    out.append("")
    out.append("### Per-year calibration scope (reporting only — year-local needs, not applied)")
    out.append("")
    out.append("| Year | 1st | 2nd | 3rd | 5th | 9th | 17th | 33rd | 65th |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    labels = {1: "1st", 2: "2nd", 3: "3rd", 5: "5th", 9: "9th", 17: "17th", 33: "33rd", 65: "65th"}
    for year in run["years"]:
        adj = run["per_year_adjustments"][year]
        cells = [f"{adj.get(pos, 0.0):+.2f}" for pos in (1, 2, 3, 5, 9, 17, 33, 65)]
        out.append(f"| {year} | " + " | ".join(cells) + " |")
    out.append("")
    out.append("### Accuracy (cross-region correctly-ordered pairs)")
    out.append("")
    out.append("| Metric | Raw | Calibrated |")
    out.append("|---|---:|---:|")
    out.append(f"| Accuracy | {_pct(run['accuracy']['raw'])} | {_pct(run['accuracy']['calibrated'])} |")
    out.append(f"| Spearman (rating vs position) | {run['spearman']['raw']:.4f} "
               f"| {run['spearman']['calibrated']:.4f} |")
    out.append("")
    out.append("### Conclusion")
    out.append("")
    if run["adjustments"] and all(a == 0.0 for a in run["adjustments"].values()):
        out.append("Central adjustments are **all 0.00** — the pooled region means are already "
                   "ordered 1st > 2nd ≥ 3rd > … > last, so there is nothing for the calibrator to "
                   "correct. Raw accuracy equals calibrated accuracy exactly. The per-year "
                   "adjustments were year-local inversions that cancel out centrally. **Decision: "
                   "the rating calibration is dropped — the engine uses the raw Phase 0 points.**")
    else:
        out.append("Central adjustments are non-zero (see table); they would be applied only if "
                   "`applied` were true — it is not (raw points are used).")
    out.append("")

    report = Path(__file__).resolve().parents[1] / "reports" / "score_calibrator_report.md"
    report.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {report}")


if __name__ == "__main__":
    main()
