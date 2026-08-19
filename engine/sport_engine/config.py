"""Configuration loader — the engine's single access point for config JSON.

Zero-hardcoding rule: all spec values and schema names live in engine/config/*.json.
This loader resolves them against the engine config directory and fails loudly at
import time if a config is missing or malformed — never silently defaults.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"


@lru_cache(maxsize=None)
def load_config(name: str) -> Dict[str, Any]:
    """Load and validate one config file. Raises on missing/invalid/empty config."""
    if not name.endswith(".json"):
        name = f"{name}.json"
    path = CONFIG_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"engine config missing: {path}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or not data:
        raise ValueError(f"engine config must be a non-empty object: {path}")
    return data


def config_dir() -> Path:
    return CONFIG_DIR
