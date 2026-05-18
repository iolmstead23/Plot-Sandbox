"""Resource-usage progress reporter for physics loops.

Two modes:
  live=True  — in-place overwrite via \\r (interactive terminal, one updating line)
  live=False — newline-terminated (headless / log-friendly)

GPU and CPU paths emit the same column layout.
"""

import sys
import time
from typing import Any

_start: float = 0.0
_last_print: float = 0.0
_has_live_line: bool = False
_nvml_handles: dict[int, Any] = {}

_LINE_WIDTH = 140


def reset() -> None:
    global _start, _last_print, _has_live_line
    if _has_live_line:
        print(file=sys.stderr, flush=True)
        _has_live_line = False
    _start = time.perf_counter()
    _last_print = _start


def finalize() -> None:
    """Commit the current in-place line with a newline (call at convergence/stop)."""
    global _has_live_line
    if _has_live_line:
        print(file=sys.stderr, flush=True)
        _has_live_line = False


def _due(interval: float) -> bool:
    global _last_print
    now = time.perf_counter()
    if now - _last_print >= interval:
        _last_print = now
        return True
    return False


def _elapsed() -> float:
    return time.perf_counter() - _start


def _nvml_handle(device: int) -> Any:
    if device not in _nvml_handles:
        try:
            import pynvml  # type: ignore[import-untyped]
            pynvml.nvmlInit()
            _nvml_handles[device] = pynvml.nvmlDeviceGetHandleByIndex(device)
        except Exception:
            _nvml_handles[device] = None
    return _nvml_handles[device]


def _gpu_fields(device: int) -> tuple[str, str]:
    """(util_str, vram_str) — pynvml first, CuPy VRAM-only as fallback."""
    handle = _nvml_handle(device)
    if handle is not None:
        try:
            import pynvml  # type: ignore[import-untyped]
            util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            return f"{util:3d}%", f"{mem.used/1024**3:5.2f}/{mem.total/1024**3:.2f} GB"
        except Exception:
            pass
    try:
        import cupy as cp  # type: ignore[import-untyped]
        free, total = cp.cuda.Device(device).mem_info
        used_gb = (total - free) / 1024**3
        return " N/A", f"{used_gb:5.2f}/{total/1024**3:.2f} GB"
    except Exception:
        return " N/A", "           N/A"


def _cpu_fields() -> tuple[str, str]:
    """(util_str, ram_str)."""
    try:
        import psutil  # type: ignore[import-untyped]
        util = psutil.cpu_percent(interval=None)
        vm = psutil.virtual_memory()
        return f"{util:3.0f}%", f"{vm.used/1024**3:5.2f}/{vm.total/1024**3:.2f} GB"
    except Exception:
        return " N/A", "           N/A"


def _progress(steps_done: int, max_steps: int) -> str:
    if max_steps > 0:
        pct = 100.0 * steps_done / max_steps
        return f"step {steps_done:>6}/{max_steps} ({pct:4.1f}%)"
    return f"step {steps_done:>6}"


def _emit(line: str, live: bool) -> None:
    global _has_live_line
    if live:
        print(f"\r{line:<{_LINE_WIDTH}}", end="", file=sys.stderr, flush=True)
        _has_live_line = True
    else:
        print(line, file=sys.stderr, flush=True)


def maybe_gpu(
    device: int,
    steps_per_sec: float,
    temperature: float,
    steps_done: int,
    interval: float,
    max_steps: int = 0,
    live: bool = False,
) -> None:
    if not _due(interval):
        return
    util, vram = _gpu_fields(device)
    line = (
        f"[GPU{device} | util {util} | VRAM {vram}"
        f" | {steps_per_sec:>7.0f} steps/s"
        f" | T={temperature:.4f}"
        f" | {_progress(steps_done, max_steps)}"
        f" | t={_elapsed():>6.1f}s]"
    )
    _emit(line, live)


def maybe_cpu(
    steps_per_sec: float,
    temperature: float,
    steps_done: int,
    interval: float,
    max_steps: int = 0,
    live: bool = False,
) -> None:
    if not _due(interval):
        return
    util, ram = _cpu_fields()
    line = (
        f"[CPU  | util {util} | RAM  {ram}"
        f" | {steps_per_sec:>7.0f} steps/s"
        f" | T={temperature:.4f}"
        f" | {_progress(steps_done, max_steps)}"
        f" | t={_elapsed():>6.1f}s]"
    )
    _emit(line, live)
