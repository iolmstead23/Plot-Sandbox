import random
import string
import threading
import time
from datetime import datetime
from pathlib import Path

import numpy as np

import packages.velocimetry as vel
from packages.config import config
from packages.dom import dom

_recorder = vel.Recorder(max_frames=config.velocimetry.max_frames)
_converged_fired: bool = False
_start_time: float | None = None


def record_tick(positions: np.ndarray, temperature: float) -> None:
    global _start_time
    if not config.velocimetry.enabled:
        return
    if _recorder.is_empty():
        _start_time = time.time()
    distances = vel.distances_from_focus(positions, config.physics.focus)
    _recorder.record(temperature, distances)


def on_converged() -> None:
    global _converged_fired
    if not config.velocimetry.enabled or _recorder.is_empty() or _converged_fired:
        return
    _converged_fired = True
    threading.Thread(target=_flush, daemon=True, name="vel-flush").start()


def reset() -> None:
    global _converged_fired, _start_time
    _recorder.clear()
    _converged_fired = False
    _start_time = None


def _flush() -> None:
    end_time = time.time()
    duration = end_time - _start_time if _start_time is not None else 0.0

    temperatures, distances = _recorder.as_arrays()
    weights = dom.weights.copy()

    frames = temperatures.shape[0]
    print(
        f"[velocimetry] converged — "
        f"{frames} frames | "
        f"{len(weights)} particles | "
        f"T {temperatures[0]:.4f} → {temperatures[-1]:.4f} | "
        f"duration {duration:.1f}s"
    )

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
    stem = f"{ts}_{run_id}"

    out = Path(config.velocimetry.output_path)
    out.mkdir(parents=True, exist_ok=True)
    if config.velocimetry.save_npz:
        vel.to_npz(_recorder, weights, out / f"velocimetry_{stem}.npz", duration_seconds=duration)
    if config.velocimetry.save_csv:
        vel.to_csv(_recorder, weights, out / f"velocimetry_{stem}.csv")
    if config.velocimetry.plot_on_convergence:
        fig = vel.phase_plot(temperatures, distances, weights)
        fig.savefig(out / f"phase_curves_{stem}.png", dpi=150, bbox_inches="tight")
