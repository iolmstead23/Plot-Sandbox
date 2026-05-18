"""DOM — single source of truth for node data.

NumPy arrays are the source of truth. The integrator writes via the underscore-prefixed
bulk API (`_set_positions`); all other mutation flows through the public
methods. Each mutator calls `_bump()` to (optionally) notify the `on_change` seam.
"""

from typing import Callable, Optional

import numpy as np


class DOM:
    def __init__(self) -> None:
        # Configurable at startup by main.py via dom.weight_to_size = config.render.weight_to_size.
        self.weight_to_size: float = 40.0
        # Spatial dimensionality. Set by main.py from config.simulation.dims before any seeding.
        self.dims: int = 3
        self.positions: np.ndarray = np.zeros((0, self.dims), dtype=np.float64)
        self.weights: np.ndarray = np.zeros((0,), dtype=np.float64)
        self.pinned: np.ndarray = np.zeros((0,), dtype=bool)
        self.labels: list[str] = []
        self.edges: np.ndarray = np.zeros((0, 2), dtype=np.int64)

        self._id_to_index: dict[int, int] = {}
        self._index_to_id: list[int] = []
        self._next_id: int = 0

        # Single optional seam (no list, no pub/sub framework). Wired by
        # handlers.tick to reheat the integrator on user/structural
        # mutations. Integrator-driven position writes pass notify=False.
        self.on_change: Optional[Callable[["DOM"], None]] = None

    @property
    def n(self) -> int:
        return self.positions.shape[0]

    @property
    def sizes(self) -> np.ndarray:
        return self.weights * self.weight_to_size

    def _bump(self, *, notify: bool = True) -> None:
        if notify and self.on_change is not None:
            self.on_change(self)

    # --- Mutation API ----------------------------------------------------
    def add_node(
        self,
        weight: float,
        position: np.ndarray,
        label: Optional[str] = None,
    ) -> int:
        node_id = self._next_id
        self._next_id += 1
        idx = self.n

        pos_row = np.asarray(position, dtype=np.float64).reshape(1, self.dims)
        self.positions = np.concatenate([self.positions, pos_row], axis=0)
        self.weights = np.concatenate(
            [self.weights, np.array([weight], dtype=np.float64)]
        )
        self.pinned = np.concatenate([self.pinned, np.array([False], dtype=bool)])
        self.labels.append(label if label is not None else _default_label(node_id))

        self._id_to_index[node_id] = idx
        self._index_to_id.append(node_id)

        self._bump()
        return node_id

    def remove_node(self, node_id: int) -> None:
        idx = self._id_to_index.pop(node_id)
        last = self.n - 1

        # Drop edges that touched the removed node, then remap any reference
        # to the swapped-in `last` index so it points to `idx`.
        if self.edges.shape[0] > 0:
            keep = (self.edges[:, 0] != idx) & (self.edges[:, 1] != idx)
            edges = self.edges[keep]
            if idx != last and edges.shape[0] > 0:
                edges = np.where(edges == last, idx, edges)
                # Re-sort each row to maintain i < j after remap.
                edges = np.sort(edges, axis=1)
            self.edges = edges

        if idx != last:
            # Swap-with-last across all parallel arrays so the truncate at
            # the end leaves a contiguous, valid table.
            self.positions[idx] = self.positions[last]
            self.weights[idx] = self.weights[last]
            self.pinned[idx] = self.pinned[last]
            self.labels[idx] = self.labels[last]
            moved_id = self._index_to_id[last]
            self._index_to_id[idx] = moved_id
            self._id_to_index[moved_id] = idx

        self.positions = self.positions[:last].copy()
        self.weights = self.weights[:last].copy()
        self.pinned = self.pinned[:last].copy()
        self.labels.pop()
        self._index_to_id.pop()

        self._bump()

    def clear(self) -> None:
        """Reset all node data and the ID counter to initial state."""
        self.positions = np.zeros((0, self.dims), dtype=np.float64)
        self.weights = np.zeros((0,), dtype=np.float64)
        self.pinned = np.zeros((0,), dtype=bool)
        self.labels = []
        self.edges = np.zeros((0, 2), dtype=np.int64)
        self._id_to_index = {}
        self._index_to_id = []
        self._next_id = 0

    def add_edge(self, i: int, j: int) -> None:
        if i == j:
            return
        a, b = (i, j) if i < j else (j, i)
        if self.edges.shape[0] > 0:
            existing = (self.edges[:, 0] == a) & (self.edges[:, 1] == b)
            if existing.any():
                return
        new_row = np.array([[a, b]], dtype=np.int64)
        self.edges = np.concatenate([self.edges, new_row], axis=0)
        self._bump()

    def _set_positions(self, positions: np.ndarray) -> None:
        # Bulk write from the integrator. Suppresses on_change — the cascade
        # is for user/structural mutations, not the per-tick relax step.
        self.positions = positions
        self._bump(notify=False)

    # --- Lookup ----------------------------------------------------------
    def ids(self) -> list[int]:
        return list(self._id_to_index.keys())


def _default_label(node_id: int) -> str:
    if node_id < 26:
        return chr(65 + node_id)
    first = chr(65 + (node_id // 26) - 1)
    second = chr(65 + (node_id % 26))
    return first + second


# Module-level singleton — the app's one true DOM.
dom = DOM()
