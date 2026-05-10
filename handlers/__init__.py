from .dom import add_random_node, remove_random_node, seed_physics_dom
from .reseed import reseed
from .state import make_force_slider_callback
from .tick import physics_tick


BUTTON_HANDLERS = [
    ("New Sim",   reseed),
    ("Add Node",  add_random_node),
    ("Remove",    remove_random_node),
]

__all__ = [
    "BUTTON_HANDLERS",
    "add_random_node",
    "make_force_slider_callback",
    "physics_tick",
    "remove_random_node",
    "reseed",
    "seed_physics_dom",
]
