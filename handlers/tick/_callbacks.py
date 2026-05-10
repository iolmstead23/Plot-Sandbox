from packages.config import config
from packages.dom import dom

from ..dom import mutate
from ..state import app as app_state, momentum, temperature


def _on_dom_change(_dom) -> None:
    temperature.reset()
    momentum.reset()


def _on_mutation_enqueued() -> None:
    # Lazy import avoids circular reference with __init__.py at load time.
    if app_state.app is not None and not app_state.app.is_ticking:
        from . import physics_tick
        app_state.app.start_tick(physics_tick, interval_ms=config.tick.interval_ms)


def wire() -> None:
    dom.on_change = _on_dom_change
    mutate.on_enqueue = _on_mutation_enqueued
