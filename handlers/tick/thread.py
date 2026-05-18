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

from packages.config import config

from . import _thread_state as _state
from ._worker import loop as _loop

# Re-export so callers can do `thread.positions_lock` without knowing _thread_state.
positions_lock = _state.positions_lock


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def is_running() -> bool:
    return (
        _state._thread is not None
        and _state._thread.is_alive()
        and not _state._stop_event.is_set()
    )


def has_converged() -> bool:
    return _state._converged.is_set()


def steps_per_sec() -> float:
    return _state._steps_per_sec


def get_temperature() -> float:
    return _state._current_temperature


def start() -> None:
    if is_running():
        return
    _state._gpu_n = 0
    _state._stop_event.clear()
    _state._converged.clear()
    try:
        import cupy as cp
        cp.cuda.Device(config.tick.cuda_device).use()
        _state._physics_stream = cp.cuda.Stream(non_blocking=True)
    except Exception:
        _state._physics_stream = None
    _state._thread = threading.Thread(target=_loop, daemon=True, name="gpu-physics")
    _state._thread.start()


def stop() -> None:
    _state._stop_event.set()
    if _state._thread is not None:
        _state._thread.join(timeout=1.0)
    _state._pos_gpu = _state._w_gpu = _state._pin_gpu = _state._e_gpu = None
    _state._gpu_n = 0


def reheat() -> None:
    """Clear the converged flag so the thread resumes computation."""
    _state._converged.clear()
