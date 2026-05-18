import contextlib
import time

import numpy as np

from packages.config import config
from packages.dom import dom
from packages.physics import cool, relax_step, to_device, to_numpy

from ..state import temperature
from . import _params
from . import _thread_state as _state


def loop() -> None:
    steps = 0
    t0 = time.perf_counter()
    _state._current_temperature = temperature.get()

    try:
        import cupy as cp
        cp.cuda.Device(config.tick.cuda_device).use()
    except Exception:
        pass

    while not _state._stop_event.is_set():
        if dom.n == 0:
            time.sleep(0.001)
            continue

        if _state._converged.is_set():
            time.sleep(0.01)
            continue

        substeps = max(1, config.tick.physics_substeps)
        params   = _params.build()
        dt       = config.tick.dt

        # ------------------------------------------------------------------
        # Conditional upload: re-upload only when DOM structure has changed.
        # Lock is held only for CPU array copies; GPU ops run outside lock.
        # ------------------------------------------------------------------
        pos_np: np.ndarray = np.empty(0)
        w_np:   np.ndarray = np.empty(0)
        pin_np: np.ndarray = np.empty(0)
        e_np:   np.ndarray = np.empty(0)
        with _state.positions_lock:
            n = dom.n
            if n != _state._gpu_n:
                pos_np = dom.positions.copy()
                w_np   = dom.weights.copy()
                pin_np = dom.pinned.copy()
                e_np   = dom.edges.copy()

        stream_ctx = _state._physics_stream if _state._physics_stream is not None else contextlib.nullcontext()
        with stream_ctx:
            if n != _state._gpu_n:
                _state._pos_gpu = to_device(pos_np.astype(np.float32))
                _state._w_gpu   = to_device(w_np.astype(np.float32))
                _state._pin_gpu = to_device(pin_np.astype(np.uint8))
                _state._e_gpu   = to_device(e_np.astype(np.int32))
                _state._gpu_n   = n

            # GPU-to-GPU copy (~60 KB for N=5000); no PCIe traffic.
            prev_pos_gpu = _state._pos_gpu.copy()

            T = temperature.get()
            for _ in range(substeps):
                _state._pos_gpu = relax_step(
                    _state._pos_gpu, _state._w_gpu, _state._pin_gpu,
                    edges=_state._e_gpu,
                    dt=dt,
                    temperature=T,
                    params=params,
                )
                T = cool(T, cooling_factor=config.physics.cooling_factor,
                         min_temperature=config.physics.min_temperature)

        # Single sync point: covers all kernel launches in the batch.
        if _state._physics_stream is not None:
            _state._physics_stream.synchronize()

        # ------------------------------------------------------------------
        # On-GPU convergence check: one scalar download (~4 bytes).
        # ------------------------------------------------------------------
        try:
            import cupy as cp
            disp     = _state._pos_gpu - prev_pos_gpu
            max_disp = float(cp.max(cp.linalg.norm(disp, axis=1)).get())
        except Exception:
            new_pos_np = to_numpy(_state._pos_gpu).astype(np.float64)
            prev_np    = to_numpy(prev_pos_gpu).astype(np.float64)
            max_disp   = float(np.linalg.norm(new_pos_np - prev_np, axis=1).max())

        new_pos = to_numpy(_state._pos_gpu).astype(np.float64)

        for _ in range(substeps):
            temperature.step()
        _state._current_temperature = T

        with _state.positions_lock:
            if dom.n == n:
                dom._set_positions(new_pos)

        steps += substeps
        elapsed = time.perf_counter() - t0
        if elapsed >= 1.0:
            _state._steps_per_sec = steps / elapsed
            steps = 0
            t0 = time.perf_counter()

        if max_disp < config.tick.equilibrium_threshold * substeps:
            elapsed = time.perf_counter() - t0
            if elapsed > 0 and steps > 0:
                _state._steps_per_sec = steps / elapsed
            _state._converged.set()
