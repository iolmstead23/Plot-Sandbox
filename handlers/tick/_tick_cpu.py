"""CPU tick path — inline physics, no background thread."""

from typing import Any

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import relax_step, to_device, to_numpy
from packages.plot import project_to_3d, update_vispy_scene

from . import _params
from ..state import temperature
from ..velocimetry import on_converged as _vel_converged, record_tick as _vel_record


def tick(app: Any, render_counter: int) -> bool:
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
        _vel_record(dom.positions, temperature.get())
        if converged:
            _vel_converged()

    render_every = max(1, config.tick.render_every)
    if app.artists is not None and (render_counter % render_every == 0):
        update_vispy_scene(
            app.artists,
            project_to_3d(dom.positions),
            dom.sizes,
            dom.edges,
            size_scale=config.render.size_scale,
            node_size_min=config.render.node_size_min,
            node_size_max=config.render.node_size_max,
        )
        app.canvas.update()

    if converged:
        app.stop_tick()

    return converged
