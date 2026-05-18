"""GPU-accelerated 3D rendering via VisPy + OpenGL.

All VBO uploads are O(N) GPU memory copies — orders of magnitude faster
than matplotlib's per-frame CPU software rasterisation.

build_vispy_scene()  — one-time scene setup
update_vispy_scene() — hot path called every render frame (~16 ms)
"""

from __future__ import annotations

import numpy as np

import vispy

vispy.use("pyqt6")

from vispy import scene
from vispy.scene.visuals import Line, Markers  # type: ignore[attr-defined]

from ._scene import SceneObjects
from ._helpers import generate_node_colors, axis_visual
from .theme import (
    _AXIS_LENGTH, _BG,
    _EDGE_COLOR, _EDGE_WIDTH,
    _NODE_SIZE_DEFAULT,
)


def build_vispy_scene(
    positions: np.ndarray,
    sizes: np.ndarray,
    edges: np.ndarray,
    *,
    title: str = "3D Plot",
    focus: tuple = (0.0, 0.0, 0.0),
    bg_color: str = _BG,
    edge_color: tuple = _EDGE_COLOR,
    edge_width: float = _EDGE_WIDTH,
    size_scale: float = 1.0,
    axis_length: float = _AXIS_LENGTH,
    elev: float,
    azim: float,
    camera_distance: float,
    node_size_min: float,
    node_size_max: float,
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
        distance=camera_distance,
    )

    axes = axis_visual(focus, axis_length)
    view.add(axes)

    n = positions.shape[0]
    node_colors = generate_node_colors(n)
    pos_f32 = positions.astype(np.float32) if n > 0 else np.zeros((1, 3), np.float32)
    sz_f32 = (
        np.clip(sizes * size_scale, node_size_min, node_size_max).astype(np.float32)
        if n > 0
        else np.ones(1, np.float32) * _NODE_SIZE_DEFAULT
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
    *,
    size_scale: float = 1.0,
    node_size_min: float,
    node_size_max: float,
) -> None:
    """Upload fresh positions/sizes/edges to the GPU VBOs each render frame."""
    n = positions.shape[0]
    if n == 0:
        return

    pos_f32 = positions.astype(np.float32)
    sz_f32 = np.clip(sizes * size_scale, node_size_min, node_size_max).astype(np.float32)

    # Regenerate color array only when node count changes; always upload it
    # because VisPy's set_data resets unspecified attributes to defaults.
    if len(so.node_colors) != n:
        so.node_colors = generate_node_colors(n)
    so.markers.set_data(pos_f32, face_color=so.node_colors, size=sz_f32, edge_width=0)  # type: ignore[arg-type]

    if edges.shape[0] > 0:
        edge_pts = positions[edges].reshape(-1, 3).astype(np.float32)
        so.lines.set_data(pos=edge_pts, connect="segments")
