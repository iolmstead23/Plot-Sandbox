import time
from typing import Any

from packages.config import config
from packages.dom import dom
from packages.physics import is_gpu

from ..dom import mutate
from ..state import app as app_state, temperature
from . import _callbacks, _tick_cpu, _tick_gpu, thread

_callbacks.wire()

_last_tick_time: float = 0.0
_fps: float = 0.0
_tick_ms: float = 0.0
_render_counter: int = 0


def physics_tick(app: Any) -> None:
    global _last_tick_time, _fps, _tick_ms, _render_counter

    tick_start = time.perf_counter()
    app_state.app = app
    mutate.drain()
    _render_counter += 1

    if is_gpu():
        _tick_gpu.tick(app, _render_counter)
    else:
        _tick_cpu.tick(app, _render_counter)

    now = time.perf_counter()
    _tick_ms = (now - tick_start) * 1000.0
    if _last_tick_time > 0.0:
        elapsed = now - _last_tick_time
        _fps = 1.0 / elapsed if elapsed > 0 else 0.0
    _last_tick_time = now

    if is_gpu():
        phys_hz = thread.steps_per_sec()
        accel_label = f"GPU  phys={phys_hz:.0f}Hz" if phys_hz > 0 else "GPU"
    else:
        accel_label = "CPU"

    app.update_banner(dom.n, temperature.get(), fps=_fps, tick_ms=_tick_ms,
                      accel=accel_label)
