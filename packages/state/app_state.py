"""Plain-data app state.

This module owns:
  - The seed data (SAMPLE_ELEMENT_RECORDS) and sample-point generation.
  - The AppState class, which holds the points currently being displayed.
  - A module-level `state` singleton — the one source of truth other layers mutate.

No imports from sibling packages. Element records are stored as plain tuples so this
package never depends on spatial.Element. Handlers convert records -> Element when
they need to apply a formula.
"""

import random
from typing import Optional


sample_size: int = 5


def generate_sample_points(n: int = sample_size) -> list[tuple[str, float, float, float]]:
    return [
        (chr(65 + i), random.uniform(-5, 5), random.uniform(-5, 5), random.uniform(-5, 5))
        for i in range(n)
    ]


def edges_from_points(
    points: list[tuple[str, float, float, float]],
) -> list[tuple[str, str]]:
    labels = [p[0] for p in points]
    return [
        (labels[i], labels[j])
        for i in range(len(labels))
        for j in range(i + 1, len(labels))
    ]


# (label, weight, token_count, backlink_count)
SAMPLE_ELEMENT_RECORDS: list[tuple[str, float, int, int]] = [
    ("A", 1.0, 10, 2),
    ("B", 2.5, 42, 5),
    ("C", 0.7, 8,  1),
    ("D", 3.1, 27, 4),
    ("E", 0.0, 0,  0),
]


class AppState:
    """Mutable runtime state — the points currently being displayed and the plot title."""

    def __init__(self) -> None:
        self.points: list[tuple[str, float, float, float]] = generate_sample_points()
        self.edges: list[tuple[str, str]] = edges_from_points(self.points)
        self.title: str = "3D Plot of Elements"
        # Fixed look-at target. The plot centers this point on screen.
        self.camera_focus: tuple[float, float, float] = (0.0, 0.0, 0.0)
        # Placeholder — reserved for future camera-position control. Currently
        # the view direction is driven by config.view elev/azim; this slot
        # exists so a later change can swap in a position-based camera mode.
        self.camera_position: tuple[float, float, float] = (5.0, 5.0, 5.0)

    def set_points(
        self,
        points: list[tuple[str, float, float, float]],
        title: Optional[str] = None,
    ) -> None:
        self.points = list(points)
        self.edges = edges_from_points(self.points)
        if title is not None:
            self.title = title


# Module-level singleton — the app's one true state.
state = AppState()
