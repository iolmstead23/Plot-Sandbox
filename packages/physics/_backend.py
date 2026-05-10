"""GPU/CPU array backend for physics computation.

Call `setup(use_gpu)` once at startup (from main.py via packages.physics.setup_backend).
After that all physics arrays live on the active device and cross-device
copies are handled by `to_device` / `to_numpy`.

  is_gpu()          → True when GPU is active
  get_module(arr)   → cupy if arr is a CuPy ndarray, else numpy
  to_device(arr)    → numpy → GPU (no-op on CPU path)
  to_numpy(arr)     → GPU → numpy (no-op if already numpy)
"""

import numpy as _np

_cupy = None
_cupy_import_error: str = ""
try:
    import cupy as _cp
    _cupy = _cp
except Exception as _e:
    _cupy_import_error = f"{type(_e).__name__}: {_e}"

_gpu_enabled: bool = False
_pool = None   # CuPy MemoryPool, set by setup(); exposed for diagnostics


def setup(use_gpu: bool) -> bool:
    """Attempt to initialise a CUDA device. Returns True when GPU is active."""
    import sys
    global _gpu_enabled, _pool
    if not use_gpu:
        _gpu_enabled = False
        return False
    if _cupy is None:
        _gpu_enabled = False
        reason = _cupy_import_error or "cupy not found"
        print(f"[GPU] CuPy unavailable ({reason})")
        print(f"[GPU] Python: {sys.executable}")
        print("[GPU] Fix: run with the project venv — '.venv\\Scripts\\python.exe main.py'")
        print("[GPU] Falling back to CPU")
        return False
    try:
        _cupy.cuda.Device(0).use()
        _cupy.zeros(1)  # force CUDA context initialisation
        props = _cupy.cuda.runtime.getDeviceProperties(0)
        name = props.get("name", b"unknown")
        if isinstance(name, bytes):
            name = name.decode()
        mem = _cupy.cuda.Device(0).mem_info
        free_mb  = mem[0] // 1024 ** 2
        total_mb = mem[1] // 1024 ** 2
        _gpu_enabled = True

        # Memory pool: recycles freed VRAM instead of calling cudaMalloc each
        # tick.  Cap at 4 GB so the pool does not silently consume all VRAM
        # from intermediate physics arrays that were freed but not yet GC'd.
        _pool = _cupy.cuda.MemoryPool()
        _pool.set_limit(size=4 * 1024 ** 3)
        _cupy.cuda.set_allocator(_pool.malloc)

        print(f"[GPU] CUDA device 0: {name}  ({free_mb} / {total_mb} MB free)")
        return True
    except Exception as exc:
        _gpu_enabled = False
        print(f"[GPU] CUDA unavailable, using CPU ({exc})")
        return False


def is_gpu() -> bool:
    return _gpu_enabled


def get_module(arr=None):
    """Return the array module appropriate for arr.

    Passing arr lets callers write xp-agnostic code by calling
    get_module(positions) at the top of each physics function.
    Passing no argument returns the default backend.
    """
    if _cupy is not None and arr is not None:
        return _cupy.get_array_module(arr)
    if _gpu_enabled and _cupy is not None:
        return _cupy
    return _np


def to_device(arr: _np.ndarray):
    """Upload a numpy array to GPU if GPU is enabled; no-op otherwise."""
    if _gpu_enabled and _cupy is not None:
        return _cupy.asarray(arr)
    return arr


def to_numpy(arr) -> _np.ndarray:
    """Download a GPU array to CPU numpy; no-op if arr is already numpy."""
    if _cupy is not None and isinstance(arr, _cupy.ndarray):
        return _np.asarray(arr.get())
    return _np.asarray(arr)
