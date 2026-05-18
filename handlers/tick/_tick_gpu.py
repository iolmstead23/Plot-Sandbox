"""GPU tick path — render-only callback; physics runs in the background thread."""

from typing import Any

from packages.config import config
from packages.dom import dom
from packages.plot import project_to_3d, update_vispy_scene

from . import thread
from ..velocimetry import on_converged as _vel_converged, record_tick as _vel_record


def tick(app: Any, render_counter: int) -> bool:
    if not thread.is_running():
        thread.start()

    converged = thread.has_converged()
    app.set_converged(converged)

    render_every = max(1, config.tick.render_every)
    will_render = app.artists is not None and (render_counter % render_every == 0)

    sizes_snap = dom.sizes
    edges_snap = dom.edges
    with thread.positions_lock:
        raw_pos = dom.positions.copy()
        if will_render:
            sizes_snap = dom.sizes.copy()
            edges_snap = dom.edges.copy()

    _vel_record(raw_pos, thread.get_temperature())

    if will_render:
        update_vispy_scene(
            app.artists,
            project_to_3d(raw_pos),
            sizes_snap,
            edges_snap,
            size_scale=config.render.size_scale,
            node_size_min=config.render.node_size_min,
            node_size_max=config.render.node_size_max,
        )
        app.canvas.update()

    if converged:
        _vel_converged()
        thread.stop()
        app.stop_tick()

    return converged
