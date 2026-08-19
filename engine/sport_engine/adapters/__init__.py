"""Adapter package — auto-registers the active adapters listed in
engine/config/sports.json. No adapter name is hardcoded here; the config is the
single source of the active list (zero-hardcoding rule). Adding a sport = add an
adapter module under adapters/ and list it in config/sports.json.
"""

from __future__ import annotations

from importlib import import_module

from sport_engine.adapters.base import SportAdapter
from sport_engine.config import load_config
from sport_engine.registry import register

_ACTIVE = load_config("sports")["active_adapters"]


def _import_and_register(name: str) -> None:
    module = import_module(f"sport_engine.adapters.{name}")
    for obj in vars(module).values():
        if (
            isinstance(obj, type)
            and issubclass(obj, SportAdapter)
            and obj is not SportAdapter
            and obj.sport == name
        ):
            register(obj)
            return
    raise ImportError(
        f"adapter module sport_engine.adapters.{name} declares no SportAdapter "
        f"subclass with sport == {name!r}"
    )


for _name in _ACTIVE:
    _import_and_register(_name)
