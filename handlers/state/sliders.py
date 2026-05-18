from typing import Any, Callable

from packages.config import config


def make_force_slider_callback(key: str, *, reseed_fn: Callable) -> Callable[[Any, float], None]:
    def callback(app, value: float) -> None:
        setattr(config.physics, key, value)
        reseed_fn(app)

    return callback
