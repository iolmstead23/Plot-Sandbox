"""Slider callbacks: mutate live physics config and reseed the simulation.

Sliders fire on `<ButtonRelease-1>`, write the new value into `config.physics`,
and trigger a fresh seed so the user sees the new force regime from a clean
initial layout. The tick reads the live config each step, so the change
propagates without any further plumbing.
"""

from packages.config import config

from .reseed import reseed


def make_force_slider_callback(key: str):
    def callback(app, value: float) -> None:
        setattr(config.physics, key, value)
        reseed(app)

    return callback
