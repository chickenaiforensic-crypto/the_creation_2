"""Score Calibrator — regional point-assignment layer.

Analyzes each (year, tournament) Phase 0 rating distribution from top performer to
last, detects density clusters, and assigns per-region supplemental points so the
generated ratings reflect the leaderboard hierarchy. 2021 baseline, then 2022-2025.
"""

from sport_engine.calibrator.calibrate import calibrate_table, run_score_calibrator
from sport_engine.calibrator.distribution import analyze_distribution
