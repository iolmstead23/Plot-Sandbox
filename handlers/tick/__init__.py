import time

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import relax_step
from packages.physics._backend import is_gpu, to_device, to_numpy
from packages.plot import project_to_3d, update_vispy_scene

from ..dom import mutate
from ..state import app as app_state, temperature
from . import _callbacks, _params, thread

_callbacks.wire()

_last_tick_time: float = 0.0
_fps: float = 0.0
_tick_ms: float = 0.0
_render_counter: int = 0
_last_render_structure: tuple = (-1, -1)


def physics_tick(app) -> None:
    global _last_tick_time, _fps, _tick_ms, _render_counter, _last_render_structure

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

        _render_counter += 1
        render_every = max(1, config.tick.render_every)
        if app.artists is not None and (_render_counter % render_every == 0):
            with thread.positions_lock:
                pos_snap    = project_to_3d(dom.positions)
                sizes_snap  = dom.sizes.copy()
                edges_snap  = dom.edges.copy()
                n_snap      = dom.n
                labels_snap = list(dom.labels)

            current_structure = (n_snap, edges_snap.shape[0])
            structure_changed = current_structure != _last_render_structure
            _last_render_structure = current_structure

            update_vispy_scene(
                app.artists,
                pos_snap,
                sizes_snap,
                edges_snap,
                labels=labels_snap if structure_changed else None,
                size_scale=config.plot.size_scale,
            )
            app.canvas.update()

        if converged:
            thread.stop()
            app.stop_tick()

    # ------------------------------------------------------------------
    # CPU path: inline physics (no background thread).
    # ------------------------------------------------------------------
    else:
        converged = False
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
            dom._set_positions(new_positions)
            temperature.step()

        _render_counter += 1
        render_every = max(1, config.tick.render_every)
        if app.artists is not None and (_render_counter % render_every == 0):
            current_structure = (dom.n, dom.edges.shape[0])
            structure_changed = current_structure != _last_render_structure
            _last_render_structure = current_structure

            update_vispy_scene(
                app.artists,
                project_to_3d(dom.positions),
                dom.sizes,
                dom.edges,
                labels=list(dom.labels) if structure_changed else None,
                size_scale=config.plot.size_scale,
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
