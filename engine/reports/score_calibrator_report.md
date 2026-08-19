# SCORE CALIBRATOR — CENTRAL (cross-year) analysis, Cincinnati Masters 2021–2025

Every player across all five years is pooled into ONE cluster and analyzed from 1st position to last. Central targets/adjustments use isotonic (PAVA). Per Director decision (2026-08-19): the calibration is NOT applied — the engine uses the raw Phase 0 points.

**Scope:** central · **Applied to ratings:** False (raw points used) · **Pooled players:** 320 (years 2021, 2022, 2023, 2024, 2025)

### Central region distribution — 1st position to last

| Region | Players | Mean raw rating | Min | Max | Std |
|---|---:|---:|---:|---:|---:|
| 1st | 5 | 53.20 | 38.0 | 70.0 | 11.43 |
| 2nd | 5 | 30.80 | 16.0 | 72.0 | 20.88 |
| 3rd | 10 | 30.80 | 22.0 | 40.0 | 6.27 |
| 5th | 20 | 14.10 | -2.0 | 26.0 | 7.86 |
| 9th | 40 | 10.05 | -6.0 | 24.0 | 7.96 |
| 17th | 80 | 0.15 | -14.0 | 20.0 | 7.02 |
| 33rd | 128 | -8.42 | -16.0 | 12.0 | 5.16 |
| 65th | 32 | -10.81 | -16.0 | -4.0 | 3.12 |

### Central adjustments

| Region | Mean raw | Target (PAVA) | Adjustment |
|---|---:|---:|---:|
| 1st | 53.20 | 53.20 | +0.00 |
| 2nd | 30.80 | 30.80 | +0.00 |
| 3rd | 30.80 | 30.80 | +0.00 |
| 5th | 14.10 | 14.10 | +0.00 |
| 9th | 10.05 | 10.05 | +0.00 |
| 17th | 0.15 | 0.15 | +0.00 |
| 33rd | -8.42 | -8.42 | +0.00 |
| 65th | -10.81 | -10.81 | +0.00 |

### Per-year calibration scope (reporting only — year-local needs, not applied)

| Year | 1st | 2nd | 3rd | 5th | 9th | 17th | 33rd | 65th |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2021 | +0.00 | +6.50 | -6.50 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 2022 | +0.00 | +2.00 | -2.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 2023 | +0.00 | +9.50 | -9.50 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 2024 | +0.00 | +1.00 | -1.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |
| 2025 | +11.00 | -11.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 |

### Accuracy (cross-region correctly-ordered pairs)

| Metric | Raw | Calibrated |
|---|---:|---:|
| Accuracy | 90.31% | 90.31% |
| Spearman (rating vs position) | -0.8060 | -0.8060 |

### Conclusion

Central adjustments are **all 0.00** — the pooled region means are already ordered 1st > 2nd ≥ 3rd > … > last, so there is nothing for the calibrator to correct. Raw accuracy equals calibrated accuracy exactly. The per-year adjustments were year-local inversions that cancel out centrally. **Decision: the rating calibration is dropped — the engine uses the raw Phase 0 points.**

