"""Continuous background physics thread for GPU mode.

When GPU is active, physics runs as fast as the GPU allows in a daemon
thread, fully decoupled from the Qt timer render interval. CuPy releases
the GIL during kernel execution, so GPU computation runs in genuine
parallel with the Qt main thread renderer.

DOM positions are protected by `positions_lock`. The main thread holds
the lock only for the duration of a shallow array copy — typically a few
microseconds — so neither side blocks the other for long.

Life cycle
----------
start()   called when the Qt timer tick starts (on_ready / after reseed)
stop()    called when the Qt timer tick stops (convergence / reseed)
reheat()  called on any structural DOM change to clear the converged flag
"""

import threading
import time

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import cool, relax_step
from packages.physics import to_device, to_numpy

from ..state import temperature
from . import _params

# Shared lock: held briefly for array copies and position writes.
positions_lock = threading.Lock()

_thread: threading.Thread | None = None
_stop_event = threading.Event()
_converged = threading.Event()
_steps_per_sec: float = 0.0


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def is_running() -> bool:
    return _thread is not None and _thread.is_alive() and not _stop_event.is_set()


def has_converged() -> bool:
    return _converged.is_set()


def steps_per_sec() -> float:
    return _steps_per_sec


def start() -> None:
    global _thread
    if is_running():
        return
    _stop_event.clear()
    _converged.clear()
    _thread = threading.Thread(target=_loop, daemon=True, name="gpu-physics")
    _thread.start()


def stop() -> None:
    _stop_event.set()
    if _thread is not None:
        _thread.join(timeout=1.0)


def reheat() -> None:
    """Clear the converged flag so the thread resumes computation."""
    _converged.clear()


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------

def _loop() -> None:
    global _steps_per_sec
    steps = 0
    t0 = time.perf_counter()

    while not _stop_event.is_set():
        if dom.n == 0:
            time.sleep(0.001)
            continue

        if _converged.is_set():
            time.sleep(0.01)
            continue

        substeps = max(1, config.tick.physics_substeps)
        params   = _params.build()
        dt       = config.tick.dt

        # Snapshot arrays — lock held only for the duration of CPU copies.
        with positions_lock:
            n      = dom.n
            pos_np = dom.positions.copy()
            w_np   = dom.weights.copy()
            pin_np = dom.pinned.copy()
            e_np   = dom.edges.copy()

        # Upload once, then run `substeps` relax_step calls back-to-back on
        # the GPU with zero CPU roundtrips between them. CuPy releases the
        # GIL on every kernel launch, so these run in parallel with the main
        # thread's matplotlib renderer. Amortising Python overhead over
        # `substeps` is the key fix for GIL-contention-limited throughput.
        #
        # Cast to float32 before upload: RTX 5070 Ti has 32x more float32
        # throughput than float64, and halves intermediate array sizes.
        pos_gpu = to_device(pos_np.astype(np.float32))
        w_gpu   = to_device(w_np.astype(np.float32))
        pin_gpu = to_device(pin_np)
        e_gpu   = to_device(e_np)

        T = temperature.get()
        for _ in range(substeps):
            pos_gpu = relax_step(
                pos_gpu, w_gpu, pin_gpu,
                edges=e_gpu,
                dt=dt,
                temperature=T,
                params=params,
            )
            T = cool(T, cooling_factor=config.physics.cooling_factor,
                     min_temperature=config.physics.min_temperature)

        # Single sync point: one download for the whole batch.
        # Cast back to float64 so the DOM always stores float64 positions.
        new_pos  = to_numpy(pos_gpu).astype(np.float64)
        step     = new_pos - pos_np
        max_disp = float(np.linalg.norm(step, axis=1).max())

        # Advance shared temperature to the batch end point.
        for _ in range(substeps):
            temperature.step()

        # Write back only if DOM structure is unchanged during the batch.
        with positions_lock:
            if dom.n == n:
                dom._set_positions(new_pos)

        # Count individual physics steps (not batches) for the Hz readout.
        steps += substeps
        elapsed = time.perf_counter() - t0
        if elapsed >= 1.0:
            _steps_per_sec = steps / elapsed
            steps = 0
            t0 = time.perf_counter()

        # Convergence threshold scaled by substeps (aggregate displacement).
        if max_disp < config.tick.equilibrium_threshold * substeps:
            elapsed = time.perf_counter() - t0
            if elapsed > 0 and steps > 0:
                _steps_per_sec = steps / elapsed
            _converged.set()
