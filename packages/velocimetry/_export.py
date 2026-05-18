import csv
from pathlib import Path

import numpy as np

from ._recorder import Recorder


def to_npz(
    recorder: Recorder,
    weights: np.ndarray,
    path: Path,
    *,
    duration_seconds: float | None = None,
) -> None:
    temperatures, distances = recorder.as_arrays()
    extra = {} if duration_seconds is None else {"duration_seconds": np.array(duration_seconds)}
    np.savez_compressed(
        path, temperatures=temperatures, distances=distances, weights=weights, **extra
    )


def to_csv(recorder: Recorder, weights: np.ndarray, path: Path) -> None:
    temperatures, distances = recorder.as_arrays()
    header = ["temperature"] + [f"dist_{i}" for i in range(distances.shape[1])]
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for t, row in zip(temperatures, distances):
            writer.writerow([t, *row])
