"""Score Calibrator — CENTRAL (cross-year) regional analysis.

Pools every player across all selected years into one cluster, analyzes the raw
Phase 0 rating distribution from 1st position to last, and derives central region
targets/adjustments. Per Director decision (2026-08-19) the calibration is NOT
applied — the engine uses the raw Phase 0 points.
"""

from sport_engine.calibrator.calibrate import run_score_calibrator
