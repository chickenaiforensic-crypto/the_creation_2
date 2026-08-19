"""Phase 1 — Head-to-Head (H2H) computation module.

Direct game score difference between pA and pB (the margin), decoupled from the
Phase 0 absolute-point rating. Runs as a stand-alone subsystem.
"""

from sport_engine.h2h.h2h import match_game_difference, match_region_points, run_h2h
