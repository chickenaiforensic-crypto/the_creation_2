"""Computational layer — filterable live computation over the data files with a mute
feature. Computes Phase 0 ratings on demand from the edition files (verified against
the manifest before use); never writes to the data tree.
"""

from sport_engine.compute.compute import compute_ratings
from sport_engine.compute.ratings_table import build_ratings_table, render_table_text
from sport_engine.compute.selection import Filters, Mutes
