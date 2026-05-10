"""GPU-accelerated 3D rendering via VisPy + OpenGL.

All VBO uploads are O(N) GPU memory copies — orders of magnitude faster
than matplotlib's per-frame CPU software rasterisation.

build_vispy_scene()  — one-time scene setup
update_vispy_scene() — hot path called every render frame (~16 ms)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

import vispy

vispy.use("pyqt6")

from vispy import scene
from vispy.scene.visuals import Line, Markers  # type: ignore[attr-defined]

import packages.theme as theme

# ---------------------------------------------------------------------------
# Color generation
# ---------------------------------------------------------------------------


def _generate_node_colors(n: int) -> np.ndarray:
    """Return (N, 4) RGBA float32 array with maximally-distinct hues.

    Uses golden-angle hue spacing so consecutive node indices get very
    different colours — this maximises perceptual contrast between nearby
    nodes without knowing their spatial positions.

    Saturation=0.80, Value=0.88 keeps colours vivid but not glaring.
    """
    if n == 0:
        return np.zeros((0, 4), dtype=np.float32)

    # Golden angle in [0, 1] hue space — maximally spreads N hues.
    hues = (np.arange(n, dtype=np.float32) * theme.NODE_HUE_STEP) % 1.0

    # Vectorised HSV → RGB (s=0.80, v=0.88 fixed).
    s = theme.NODE_SATURATION
    v = theme.NODE_VALUE
    h6 = hues * 6.0
    i = np.floor(h6).astype(np.int32) % 6
    f = (h6 - np.floor(h6)).astype(np.float32)
    p = np.float32(v * (1.0 - s))
    q = (v * (1.0 - s * f)).astype(np.float32)
    t = (v * (1.0 - s * (1.0 - f))).astype(np.float32)
    vv = np.float32(v)

    r = np.select(
        [i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [vv, q, p, p, t, vv]
    )
    g = np.select(
        [i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [t, vv, vv, q, p, p]
    )
    b = np.select(
        [i == 0, i == 1, i == 2, i == 3, i == 4, i == 5], [p, p, t, vv, vv, q]
    )

    rgba = np.stack([r, g, b, np.ones(n, np.float32)], axis=1)
    return rgba


# ---------------------------------------------------------------------------
# Scene dataclass
# ---------------------------------------------------------------------------


@dataclass
class SceneObjects:
    canvas: scene.SceneCanvas
    view: scene.widgets.ViewBox
    markers: Markers
    lines: Line
    axes: Line
    node_colors: np.ndarray = field(
        default_factory=lambda: np.zeros((0, 4), dtype=np.float32)
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _axis_visual(focus: tuple[float, float, float], length: float) -> Line:
    fx, fy, fz = focus
    pts = np.array(
        [
            [fx, fy, fz],
            [fx + length, fy, fz],
            [fx, fy, fz],
            [fx, fy + length, fz],
            [fx, fy, fz],
            [fx, fy, fz + length],
        ],
        dtype=np.float32,
    )
    clrs = np.array(
        [
            theme.AXIS_X_COLOR,
            theme.AXIS_X_COLOR,
            theme.AXIS_Y_COLOR,
            theme.AXIS_Y_COLOR,
            theme.AXIS_Z_COLOR,
            theme.AXIS_Z_COLOR,
        ],
        dtype=np.float32,
    )
    return Line(
        pos=pts,
        color=clrs,
        connect="segments",
        width=int(theme.AXIS_WIDTH),
        antialias=False,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_vispy_scene(
    positions: np.ndarray,
    sizes: np.ndarray,
    labels: list[str],
    edges: np.ndarray,
    *,
    title: str = "3D Plot",
    focus: tuple = (0.0, 0.0, 0.0),
    bg_color: str = theme.BG,
    edge_color: tuple = theme.EDGE_COLOR,
    edge_width: float = theme.EDGE_WIDTH,
    size_scale: float = 1.0,
    axis_length: float = 5.0,
    elev: float = 25.0,
    azim: float = -60.0,
) -> SceneObjects:
    canvas = scene.SceneCanvas(
        title=title,
        keys="interactive",
        show=False,
        bgcolor=bg_color,
    )

    view = canvas.central_widget.add_view()
    view.camera = scene.cameras.TurntableCamera(
        fov=0,
        elevation=elev,
        azimuth=azim,
        distance=30,
    )

    axes = _axis_visual(focus, axis_length)
    view.add(axes)

    n = positions.shape[0]
    node_colors = _generate_node_colors(n)
    pos_f32 = positions.astype(np.float32) if n > 0 else np.zeros((1, 3), np.float32)
    sz_f32 = (
        np.clip(sizes * size_scale, theme.NODE_SIZE_MIN, theme.NODE_SIZE_MAX).astype(
            np.float32
        )
        if n > 0
        else np.ones(1, np.float32) * 4.0
    )

    markers = Markers(antialias=0)
    markers.set_data(
        pos_f32,
        face_color=node_colors if n > 0 else "steelblue",  # type: ignore[arg-type]
        size=sz_f32,
        edge_width=0,
    )
    view.add(markers)

    if edges.shape[0] > 0 and n > 0:
        edge_pts = positions[edges].reshape(-1, 3).astype(np.float32)
    else:
        edge_pts = np.zeros((2, 3), np.float32)
    lines = Line(
        pos=edge_pts,
        connect="segments",
        color=edge_color,
        width=max(1, round(edge_width)),
        antialias=False,
    )
    view.add(lines)

    return SceneObjects(
        canvas=canvas,
        view=view,
        markers=markers,
        lines=lines,
        axes=axes,
        node_colors=node_colors,
    )


def update_vispy_scene(
    so: SceneObjects,
    positions: np.ndarray,
    sizes: np.ndarray,
    edges: np.ndarray,
    labels: Optional[list[str]] = None,
    *,
    size_scale: float = 1.0,
) -> None:
    """Upload fresh positions/sizes/edges to the GPU VBOs each render frame."""
    n = positions.shape[0]
    if n == 0:
        return

    # Regenerate colours only when node count changes (structural mutation).
    if len(so.node_colors) != n:
        so.node_colors = _generate_node_colors(n)

    pos_f32 = positions.astype(np.float32)
    sz_f32 = np.clip(
        sizes * size_scale, theme.NODE_SIZE_MIN, theme.NODE_SIZE_MAX
    ).astype(np.float32)

    so.markers.set_data(
        pos_f32,
        face_color=so.node_colors,  # type: ignore[arg-type]
        size=sz_f32,
        edge_width=0,
    )

    if edges.shape[0] > 0:
        edge_pts = positions[edges].reshape(-1, 3).astype(np.float32)
        so.lines.set_data(pos=edge_pts, connect="segments")
