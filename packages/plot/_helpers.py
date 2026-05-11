"""Private scene-building helpers: color generation and axis visuals."""

from __future__ import annotations

import numpy as np

from vispy.scene.visuals import Line  # type: ignore[attr-defined]

from .theme import (
    _AXIS_WIDTH,
    _AXIS_X_COLOR,
    _AXIS_Y_COLOR,
    _AXIS_Z_COLOR,
    _NODE_HUE_STEP,
    _NODE_SATURATION,
    _NODE_VALUE,
)


def generate_node_colors(n: int) -> np.ndarray:
    """Return (N, 4) RGBA float32 array with maximally-distinct hues.

    Uses golden-angle hue spacing so consecutive node indices get very
    different colours — this maximises perceptual contrast between nearby
    nodes without knowing their spatial positions.
    """
    if n == 0:
        return np.zeros((0, 4), dtype=np.float32)

    hues = (np.arange(n, dtype=np.float32) * _NODE_HUE_STEP) % 1.0

    s = _NODE_SATURATION
    v = _NODE_VALUE
    h6 = hues * 6.0
    i = np.floor(h6).astype(np.int32) % 6
    f = (h6 - np.floor(h6)).astype(np.float32)
    p = np.float32(v * (1.0 - s))
    q = (v * (1.0 - s * f)).astype(np.float32)
    t = (v * (1.0 - s * (1.0 - f))).astype(np.float32)
    vv = np.float32(v)

    r = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [vv, q, p, p, t, vv])
    g = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [t, vv, vv, q, p, p])
    b = np.select([i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [p, p, t, vv, vv, q])

    return np.stack([r, g, b, np.ones(n, np.float32)], axis=1)


def axis_visual(focus: tuple[float, float, float], length: float) -> Line:
    fx, fy, fz = focus
    pts = np.array(
        [
            [fx, fy, fz], [fx + length, fy, fz],
            [fx, fy, fz], [fx, fy + length, fz],
            [fx, fy, fz], [fx, fy, fz + length],
        ],
        dtype=np.float32,
    )
    clrs = np.array(
        [
            _AXIS_X_COLOR, _AXIS_X_COLOR,
            _AXIS_Y_COLOR, _AXIS_Y_COLOR,
            _AXIS_Z_COLOR, _AXIS_Z_COLOR,
        ],
        dtype=np.float32,
    )
    return Line(pos=pts, color=clrs, connect="segments", width=int(_AXIS_WIDTH), antialias=False)
