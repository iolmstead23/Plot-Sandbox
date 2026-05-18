import numpy as np

from ._frame import VelocimetryFrame


class Recorder:
    def __init__(self, max_frames: int = 20000) -> None:
        self._frames: list[VelocimetryFrame] = []
        self._max_frames = max_frames

    def record(self, temperature: float, distances: np.ndarray) -> None:
        if len(self._frames) < self._max_frames:
            self._frames.append(VelocimetryFrame(temperature, distances.copy()))

    def is_empty(self) -> bool:
        return not self._frames

    def clear(self) -> None:
        self._frames.clear()

    def as_arrays(self) -> tuple[np.ndarray, np.ndarray]:
        """Return (temperatures: shape (T,), distances: shape (T, N))."""
        temperatures = np.array([f.temperature for f in self._frames])
        distances = np.stack([f.distances for f in self._frames], axis=0)
        return temperatures, distances
