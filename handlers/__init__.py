from typing import Any

from packages.config import config

from .dom import add_random_node, remove_random_node
from .dom.seed_zettelkasten import seed_from_zettelkasten
from .reseed import reseed
from .state import make_force_slider_callback
from .state import zettelkasten_path as _zk_path
from .tick import physics_tick
from .tick import thread as _tick_thread


def reseed_handler(app: Any) -> None:
    reseed(
        app,
        stop_fn=_tick_thread.stop,
        start_fn=lambda a: a.start_tick(physics_tick, interval_ms=config.tick.interval_ms),
        seed_fn=lambda rng: seed_from_zettelkasten(_zk_path.path, rng),
    )


BUTTON_HANDLERS = [
    ("New Sim",   reseed_handler),
    ("Add Node",  add_random_node,    True),  # gated: disabled until converged
    ("Remove",    remove_random_node, True),  # gated: disabled until converged
]

__all__ = [
    "BUTTON_HANDLERS",
    "add_random_node",
    "make_force_slider_callback",
    "physics_tick",
    "remove_random_node",
    "reseed_handler",
]
