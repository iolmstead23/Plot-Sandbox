import time

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import relax_step
from packages.physics import is_gpu, to_device, to_numpy
from packages.plot import project_to_3d, update_vispy_scene

from ..dom import mutate
from ..state import app as app_state, temperature
from . import _callbacks, _params, thread

_callbacks.wire()

_last_tick_time: float = 0.0
_fps: float = 0.0
_tick_ms: float = 0.0
_render_counter: int = 0


def physics_tick(app) -> None:
    global _last_tick_time, _fps, _tick_ms, _render_counter

    tick_start = time.perf_counter()
    app_state.app = app
    mutate.drain()

    # ------------------------------------------------------------------
    # GPU path: physics runs in background thread; this callback is
    # render-only. Positions are snapshotted under the lock so we never
    # read a half-written array.
    # ------------------------------------------------------------------
    if is_gpu():
        if not thread.is_running():
            thread.start()

        converged = thread.has_converged()
        app.set_converged(converged)

        _render_counter += 1
        render_every = max(1, config.tick.render_every)
        will_render = app.artists is not None and (_render_counter % render_every == 0)

        # Always snapshot positions for velocimetry; only copy sizes/edges on
        # render ticks — they are stable between mutations and copying the
        # edge array (up to ~400 KB) every tick wastes lock time.
        with thread.positions_lock:
            raw_pos = dom.positions.copy()
            if will_render:
                sizes_snap = dom.sizes.copy()
                edges_snap = dom.edges.copy()

        from ..velocimetry import record_tick as _vel_record, on_converged as _vel_converged
        _vel_record(raw_pos, thread.get_temperature())

        if will_render:
            update_vispy_scene(
                app.artists,
                project_to_3d(raw_pos),
                sizes_snap,
                edges_snap,
                size_scale=config.plot.size_scale,
                node_size_min=config.plot.node_size_min,
                node_size_max=config.plot.node_size_max,
            )
            app.canvas.update()

        if converged:
            _vel_record(raw_pos, thread.get_temperature())  # capture equilibrium frame
            _vel_converged()
            thread.stop()
            app.stop_tick()

    # ------------------------------------------------------------------
    # CPU path: inline physics (no background thread).
    # ------------------------------------------------------------------
    else:
        converged = False
        app.set_converged(False)
        if dom.n > 0:
            positions = to_device(dom.positions)
            weights   = to_device(dom.weights)
            pinned    = to_device(dom.pinned)
            edges     = to_device(dom.edges)

            proposed = relax_step(
                positions, weights, pinned,
                edges=edges,
                dt=config.tick.dt,
                temperature=temperature.get(),
                params=_params.build(),
            )

            new_positions = to_numpy(proposed)
            step = new_positions - dom.positions
            max_disp = float(np.linalg.norm(step, axis=1).max())
            converged = max_disp < config.tick.equilibrium_threshold
            app.set_converged(converged)
            dom._set_positions(new_positions)
            temperature.step()
            from ..velocimetry import record_tick as _vel_record, on_converged as _vel_converged
            _vel_record(dom.positions, temperature.get())
            if converged:
                _vel_converged()

        _render_counter += 1
        render_every = max(1, config.tick.render_every)
        if app.artists is not None and (_render_counter % render_every == 0):
            update_vispy_scene(
                app.artists,
                project_to_3d(dom.positions),
                dom.sizes,
                dom.edges,
                size_scale=config.plot.size_scale,
                node_size_min=config.plot.node_size_min,
                node_size_max=config.plot.node_size_max,
            )
            app.canvas.update()

        if converged:
            app.stop_tick()

    # ------------------------------------------------------------------
    # Banner (both paths)
    # ------------------------------------------------------------------
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
