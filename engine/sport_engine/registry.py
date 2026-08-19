"""Pluggable sport registry.

Register a SportAdapter subclass once; the engine then resolves sports by name.
Adding a new sport = one adapter class + one register() call. No engine changes.
"""

from __future__ import annotations

from typing import Dict, Type

from sport_engine.adapters.base import SportAdapter

_REGISTRY: Dict[str, Type[SportAdapter]] = {}


def register(adapter_cls: Type[SportAdapter]) -> Type[SportAdapter]:
    """Register an adapter class under its ``sport`` name (idempotent per name)."""
    if not adapter_cls.sport:
        raise ValueError(f"{adapter_cls.__name__} must declare a non-empty sport name")
    if adapter_cls.sport in _REGISTRY and _REGISTRY[adapter_cls.sport] is not adapter_cls:
        raise ValueError(f"sport {adapter_cls.sport!r} already registered")
    _REGISTRY[adapter_cls.sport] = adapter_cls
    return adapter_cls


def get_sport(name: str) -> Type[SportAdapter]:
    if name not in _REGISTRY:
        raise KeyError(f"sport {name!r} not registered; known: {sorted(_REGISTRY)}")
    return _REGISTRY[name]


def sports() -> tuple:
    return tuple(sorted(_REGISTRY))
