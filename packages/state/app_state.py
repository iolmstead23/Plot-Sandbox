"""Plain-data app state.

This module owns:
  - The AppState class, which holds view configuration for the active plot.
  - A module-level `state` singleton — the one source of truth other layers mutate.

No imports from sibling packages.
"""


class AppState:
    """Mutable runtime state — the title and camera focus for the active plot."""

    def __init__(self) -> None:
        self.title: str = "3D Plot of Elements"
        # Fixed look-at target. The plot centers this point on screen.
        self.camera_focus: tuple[float, float, float] = (0.0, 0.0, 0.0)


# Module-level singleton — the app's one true state.
state = AppState()
