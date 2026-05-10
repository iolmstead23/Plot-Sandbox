from packages.config import config

from .dom import add_random_node, remove_random_node, seed_physics_dom
from .reseed import reseed
from .state import make_force_slider_callback
from .tick import physics_tick
from .tick import thread as _tick_thread


def reseed_handler(app) -> None:
    reseed(
        app,
        stop_fn=_tick_thread.stop,
        start_fn=lambda a: a.start_tick(physics_tick, interval_ms=config.tick.interval_ms),
    )


BUTTON_HANDLERS = [
    ("New Sim",   reseed_handler),
    ("Add Node",  add_random_node),
    ("Remove",    remove_random_node),
]

__all__ = [
    "BUTTON_HANDLERS",
    "add_random_node",
    "make_force_slider_callback",
    "physics_tick",
    "remove_random_node",
    "reseed_handler",
    "seed_physics_dom",
]
