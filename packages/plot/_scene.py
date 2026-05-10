"""SceneObjects dataclass — container for all live VisPy scene handles."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from vispy import scene
from vispy.scene.visuals import Line, Markers  # type: ignore[attr-defined]


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
