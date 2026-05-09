"""Button handlers + tick orchestrator — the only layer that bridges packages.

Each button handler has signature `(app) -> None`. The Tk button calls
`handler(app_instance)` on click. Handlers either mutate DOM directly
(synchronous, instant) or enqueue mutations (drained between physics steps).
"""

from .add_random_node import add_random_node
from .randomize_weights import randomize_weights
from .remove_random_node import remove_random_node
from .reseed import reseed, seed_physics_dom
from .tick import physics_tick


BUTTON_HANDLERS = [
    ("New Sim",   reseed),
    ("Add Node",  add_random_node),
    ("Remove",    remove_random_node),
    ("Randomize", randomize_weights),
]

__all__ = [
    "BUTTON_HANDLERS",
    "add_random_node",
    "physics_tick",
    "randomize_weights",
    "remove_random_node",
    "reseed",
    "seed_physics_dom",
]
