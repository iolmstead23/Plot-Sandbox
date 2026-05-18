"""Config file loading, validation, and construction."""

import dataclasses
import json
import os

from ._defaults import _DEFAULT_CONFIG
from ._schema import _SCHEMA
from ._model_physics import PhysicsConfig
from ._model_render import RenderConfig
from ._model_root import Config
from ._model_simulation import SimulationConfig
from ._model_sliders import SliderRangeConfig, SlidersConfig
from ._model_tick import TickConfig
from ._model_ui import UiConfig
from ._model_velocimetry import VelocimetryConfig


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
            if isinstance(expected, dict):
                # Nested sub-object (e.g. sliders.gravity_ratio -> {min, max, step}).
                if not isinstance(value, dict):
                    raise TypeError(
                        f"config.{section}.{key}: expected dict, "
                        f"got {type(value).__name__}"
                    )
                for sub_key, sub_type in expected.items():
                    if sub_key not in value:
                        raise KeyError(
                            f"Missing config key: '{section}.{key}.{sub_key}'"
                        )
                    sub_val = value[sub_key]
                    if not isinstance(sub_val, sub_type):
                        raise TypeError(
                            f"config.{section}.{key}.{sub_key}: "
                            f"expected {_type_name(sub_type)}, "
                            f"got {type(sub_val).__name__} ({sub_val!r})"
                        )
            elif not isinstance(value, expected):
                raise TypeError(
                    f"config.{section}.{key}: expected {_type_name(expected)}, "
                    f"got {type(value).__name__} ({value!r})"
                )

    focus = data["physics"]["focus"]
    if len(focus) != 3 or not all(isinstance(v, (int, float)) for v in focus):
        raise TypeError("config.physics.focus must be a list of 3 numbers")

    if data["simulation"]["dims"] < 1:
        raise ValueError("config.simulation.dims must be >= 1")


def _migrate_legacy_sections(data: dict) -> dict:
    """Convert pre-render config.json files (view+plot+dom) to the render section."""
    if "render" in data:
        return data
    render: dict = {}
    if "view" in data:
        v = data["view"]
        render["camera_elev"]     = v.get("elev", 25.0)
        render["camera_azim"]     = v.get("azim", -60.0)
        render["view_range"]      = v.get("view_range", 10.0)
        render["camera_distance"] = v.get("camera_distance", 30.0)
    if "plot" in data:
        p = data["plot"]
        render["title"]         = p.get("title", "Knowledge Graph Simulation")
        render["size_scale"]    = p.get("size_scale", 1.0)
        render["node_size_min"] = p.get("node_size_min", 2.0)
        render["node_size_max"] = p.get("node_size_max", 20.0)
    if "dom" in data:
        render["weight_to_size"] = data["dom"].get("weight_to_size", 3.0)
    if render:
        data = dict(data)
        data["render"] = render
        for old in ("view", "plot", "dom"):
            data.pop(old, None)
    return data


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
    s = d["sliders"]
    return Config(
        physics=PhysicsConfig(**d["physics"]),
        simulation=SimulationConfig(**d["simulation"]),
        tick=TickConfig(**d["tick"]),
        render=RenderConfig(**d["render"]),
        ui=UiConfig(**d["ui"]),
        velocimetry=VelocimetryConfig(**d["velocimetry"]),
        sliders=SlidersConfig(
            gravity_ratio=SliderRangeConfig(**s["gravity_ratio"]),
            repel_ratio=SliderRangeConfig(**s["repel_ratio"]),
            k_edge=SliderRangeConfig(**s["k_edge"]),
        ),
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

    data = _migrate_legacy_sections(data)
    _validate(data)
    return _dict_to_config(data)


def save_config(cfg: Config, path: str = "config.json") -> None:
    """Persist the in-memory config back to *path* as formatted JSON."""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(dataclasses.asdict(cfg), fh, indent=2)
