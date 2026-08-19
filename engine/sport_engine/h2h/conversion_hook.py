"""Future per-tournament calibration hook — abstraction for a conversion
subsystem that will normalize separate raw tournament ratings.

When the Director specifies the conversion subsystem, this hook executes
mathematical conversions on per-tournament raw ratings so that two matching
players arriving from entirely different tournament data pools can be compared
cross-tournament. Until then it is a placeholder: `available` reports the hook
exists but is not configured; `convert` raises NotImplementedError rather than
inventing a conversion (zero-hardcoding, nothing guessed).
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from sport_engine.config import load_config


def _hook_cfg() -> dict:
    return load_config("h2h_tournament")["conversion_hook"]


def available() -> bool:
    """True once the Director configures the conversion subsystem."""
    cfg = _hook_cfg()
    return bool(cfg.get("enabled")) and cfg.get("method") != "not_specified"


def convert(player_context: Dict[str, Any]) -> Dict[str, Any]:
    """Apply the configured conversion to one player's per-tournament context.

    Not implemented until the Director specifies the conversion method. Raises
    NotImplementedError — no conversion may be invented.
    """
    cfg = _hook_cfg()
    if not cfg.get("enabled") or cfg.get("method") == "not_specified":
        raise NotImplementedError(
            "Per-tournament conversion hook is not yet configured by the Director; "
            "no conversion may be invented."
        )
    method = cfg.get("method")
    raise NotImplementedError(f"Conversion method {method!r} not implemented")
