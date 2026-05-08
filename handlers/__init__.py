"""Button handlers — orchestration glue between UI events, state, spatial, and plot.

Each handler has signature `(app) -> None`. The UI calls `handler(app_instance)` when its
button is clicked. Handlers read/write app state via the `state` singleton, then call
`app.set_figure(...)` to update the view.
"""

from ._compute import points_from_formula, records_to_elements
from .show_linear import show_linear
from .show_sample import show_sample
from .show_weighted import show_weighted


BUTTON_HANDLERS = [
    ("Sample", show_sample),
    ("Linear", show_linear),
    ("Weighted", show_weighted),
]

__all__ = [
    "BUTTON_HANDLERS",
    "points_from_formula",
    "records_to_elements",
    "show_linear",
    "show_sample",
    "show_weighted",
]
