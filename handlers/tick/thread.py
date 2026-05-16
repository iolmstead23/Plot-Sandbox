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
from typing import Any

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
_current_temperature: float = 1.0
_physics_stream = None  # cp.cuda.Stream, created in start()

# Persistent GPU arrays — survive across batches when DOM structure is stable.
# None until first loop iteration; freed in stop().
_pos_gpu: Any = None   # cp.ndarray (N, 3) float32
_w_gpu:   Any = None   # cp.ndarray (N,)   float32
_pin_gpu: Any = None   # cp.ndarray (N,)   uint8
_e_gpu:   Any = None   # cp.ndarray (E, 2) int32
_gpu_n: int = 0        # node count at last upload; 0 forces re-upload on first batch


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def is_running() -> bool:
    return _thread is not None and _thread.is_alive() and not _stop_event.is_set()


def has_converged() -> bool:
    return _converged.is_set()


def steps_per_sec() -> float:
    return _steps_per_sec


def get_temperature() -> float:
    return _current_temperature


def start() -> None:
    global _thread, _physics_stream, _gpu_n
    if is_running():
        return
    _gpu_n = 0  # force full re-upload on first loop iteration
    _stop_event.clear()
    _converged.clear()
    try:
        import cupy as cp
        cp.cuda.Device(config.tick.cuda_device).use()
        _physics_stream = cp.cuda.Stream(non_blocking=True)
    except Exception:
        _physics_stream = None
    _thread = threading.Thread(target=_loop, daemon=True, name="gpu-physics")
    _thread.start()


def stop() -> None:
    global _pos_gpu, _w_gpu, _pin_gpu, _e_gpu, _gpu_n
    _stop_event.set()
    if _thread is not None:
        _thread.join(timeout=1.0)
    # Release VRAM; _gpu_n=0 ensures re-upload on next start().
    _pos_gpu = _w_gpu = _pin_gpu = _e_gpu = None
    _gpu_n = 0


def reheat() -> None:
    """Clear the converged flag so the thread resumes computation."""
    _converged.clear()


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------

class _NullCtx:
    """No-op context manager used when no CUDA stream is available."""
    def __enter__(self): return self
    def __exit__(self, *_): pass


def _loop() -> None:
    global _steps_per_sec, _current_temperature
    global _pos_gpu, _w_gpu, _pin_gpu, _e_gpu, _gpu_n

    steps = 0
    t0 = time.perf_counter()
    _current_temperature = temperature.get()

    try:
        import cupy as cp
        cp.cuda.Device(config.tick.cuda_device).use()
    except Exception:
        pass

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

        # ------------------------------------------------------------------
        # Conditional upload: re-upload only when DOM structure has changed.
        # Lock is held only for CPU array copies; GPU ops run outside lock.
        # ------------------------------------------------------------------
        with positions_lock:
            n = dom.n
            if n != _gpu_n:
                # Structural change (reseed / add / remove node): full re-upload.
                pos_np = dom.positions.copy()
                w_np   = dom.weights.copy()
                pin_np = dom.pinned.copy()
                e_np   = dom.edges.copy()
            # If n == _gpu_n, skip all CPU copies — GPU already has latest positions.

        stream_ctx = _physics_stream if _physics_stream is not None else _NullCtx()
        with stream_ctx:
            if n != _gpu_n:
                _pos_gpu = to_device(pos_np.astype(np.float32))
                _w_gpu   = to_device(w_np.astype(np.float32))
                _pin_gpu = to_device(pin_np.astype(np.uint8))
                _e_gpu   = to_device(e_np.astype(np.int32))
                _gpu_n   = n

            # GPU-to-GPU copy (~60 KB for N=5000); no PCIe traffic.
            # .copy() is required so prev holds the start-of-batch snapshot
            # while _pos_gpu accumulates substep results.
            prev_pos_gpu = _pos_gpu.copy()

            T = temperature.get()
            for _ in range(substeps):
                _pos_gpu = relax_step(
                    _pos_gpu, _w_gpu, _pin_gpu,
                    edges=_e_gpu,
                    dt=dt,
                    temperature=T,
                    params=params,
                )
                T = cool(T, cooling_factor=config.physics.cooling_factor,
                         min_temperature=config.physics.min_temperature)

        # Single sync point: covers all kernel launches in the batch.
        if _physics_stream is not None:
            _physics_stream.synchronize()

        # ------------------------------------------------------------------
        # On-GPU convergence check: one scalar download (~4 bytes) rather
        # than a full float64 array download just to compute a max-norm.
        # ------------------------------------------------------------------
        try:
            import cupy as cp
            disp     = _pos_gpu - prev_pos_gpu
            max_disp = float(cp.max(cp.linalg.norm(disp, axis=1)).get())
        except Exception:
            new_pos_np = to_numpy(_pos_gpu).astype(np.float64)
            prev_np    = to_numpy(prev_pos_gpu).astype(np.float64)
            max_disp   = float(np.linalg.norm(new_pos_np - prev_np, axis=1).max())

        # Download for CPU DOM write-back (render loop reads dom.positions).
        new_pos = to_numpy(_pos_gpu).astype(np.float64)

        # Advance shared temperature to the batch end point.
        for _ in range(substeps):
            temperature.step()
        _current_temperature = T

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
