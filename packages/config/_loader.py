"""Config file loading, validation, and construction."""

import json
import os

from ._defaults import _DEFAULT_CONFIG, _SCHEMA
from ._models import (
    Config,
    DomConfig,
    PhysicsConfig,
    PlotConfig,
    SimulationConfig,
    TickConfig,
    UiConfig,
    ViewConfig,
)


def _type_name(t) -> str:
    if isinstance(t, tuple):
        return " | ".join(x.__name__ for x in t)
    return t.__name__


def _validate(data: dict) -> None:
    """Raise TypeError or KeyError with a descriptive path on any mismatch."""
    for section, fields in _SCHEMA.items():
        if section not in data:
            raise KeyError(f"Missing config section: '{section}'")
        sec = data[section]
        for key, expected in fields.items():
            if key not in sec:
                raise KeyError(f"Missing config key: '{section}.{key}'")
            value = sec[key]
            if not isinstance(value, expected):
                raise TypeError(
                    f"config.{section}.{key}: expected {_type_name(expected)}, "
                    f"got {type(value).__name__} ({value!r})"
                )

    focus = data["physics"]["focus"]
    if len(focus) != 3 or not all(isinstance(v, (int, float)) for v in focus):
        raise TypeError("config.physics.focus must be a list of 3 numbers")

    if data["simulation"]["dims"] < 1:
        raise ValueError("config.simulation.dims must be >= 1")


def _deep_merge(base: dict, override: dict) -> dict:
    """Merge override into a copy of base, section by section."""
    result = {k: dict(v) for k, v in base.items()}
    for section, fields in override.items():
        if section in result and isinstance(fields, dict):
            result[section].update(fields)
        else:
            result[section] = fields
    return result


def _dict_to_config(d: dict) -> Config:
    return Config(
        physics=PhysicsConfig(**d["physics"]),
        simulation=SimulationConfig(**d["simulation"]),
        tick=TickConfig(**d["tick"]),
        view=ViewConfig(**d["view"]),
        plot=PlotConfig(**d["plot"]),
        dom=DomConfig(**d["dom"]),
        ui=UiConfig(**d["ui"]),
    )


def load_config(path: str = "config.json") -> Config:
    """Load config from *path*, auto-generating it with defaults if absent.

    Deep-merges the file over defaults so new keys added in future versions
    of the app are always present even when the user's file is older.
    Raises TypeError or KeyError on type mismatches.
    """
    if not os.path.exists(path):
        data = _DEFAULT_CONFIG
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
    else:
        with open(path, "r", encoding="utf-8") as fh:
            user_data = json.load(fh)
        data = _deep_merge(_DEFAULT_CONFIG, user_data)

    _validate(data)
    return _dict_to_config(data)
