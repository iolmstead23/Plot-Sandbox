"""Memoized DOM — single source of truth for node data.

NumPy arrays are the source of truth; Node (see node.py) is a thin view that
reads/writes rows on demand. The integrator writes via the underscore-prefixed
bulk API (`_set_positions`); all other mutation flows through the public
methods. Each mutator bumps `_revision`, which is used to invalidate the
`pairs_within_radius` cache and (optionally) notify the `on_change` seam.
"""

from typing import Callable, Optional

import numpy as np


class DOM:
    def __init__(self) -> None:
        # Configurable at startup by main.py via dom.weight_to_size = config.dom.weight_to_size.
        self.weight_to_size: float = 40.0
        self.positions: np.ndarray = np.zeros((0, 3), dtype=np.float64)
        self.weights:   np.ndarray = np.zeros((0,),   dtype=np.float64)
        self.pinned:    np.ndarray = np.zeros((0,),   dtype=bool)
        self.labels:    list[str] = []

        self._id_to_index: dict[int, int] = {}
        self._index_to_id: list[int] = []
        self._next_id: int = 0
        self._revision: int = 0
        # Bumps only when positions/topology change; weight/size mutations
        # leave it untouched so the pairs cache survives them.
        self._position_revision: int = 0

        # Single optional seam (no list, no pub/sub framework). Wired by
        # handlers.tick to reheat the integrator on user/structural
        # mutations. Integrator-driven position writes pass notify=False.
        self.on_change: Optional[Callable[["DOM"], None]] = None

        # (position_revision, radius, pairs) — keyed on position revision so
        # weight/size changes don't invalidate it.
        self._pairs_cache: Optional[tuple[int, float, np.ndarray]] = None

    @property
    def n(self) -> int:
        return self.positions.shape[0]

    @property
    def sizes(self) -> np.ndarray:
        return self.weights * self.weight_to_size

    @property
    def revision(self) -> int:
        return self._revision

    def _bump(self, *, positions_changed: bool, notify: bool = True) -> None:
        self._revision += 1
        if positions_changed:
            self._position_revision += 1
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

        pos_row = np.asarray(position, dtype=np.float64).reshape(1, 3)
        self.positions = np.concatenate([self.positions, pos_row], axis=0)
        self.weights   = np.concatenate([self.weights,   np.array([weight], dtype=np.float64)])
        self.pinned    = np.concatenate([self.pinned,    np.array([False],  dtype=bool)])
        self.labels.append(label if label is not None else _default_label(node_id))

        self._id_to_index[node_id] = idx
        self._index_to_id.append(node_id)

        self._bump(positions_changed=True)
        return node_id

    def remove_node(self, node_id: int) -> None:
        idx = self._id_to_index.pop(node_id)
        last = self.n - 1

        if idx != last:
            # Swap-with-last across all parallel arrays so the truncate at
            # the end leaves a contiguous, valid table.
            self.positions[idx] = self.positions[last]
            self.weights[idx]   = self.weights[last]
            self.pinned[idx]    = self.pinned[last]
            self.labels[idx]    = self.labels[last]
            moved_id = self._index_to_id[last]
            self._index_to_id[idx] = moved_id
            self._id_to_index[moved_id] = idx

        self.positions = self.positions[:last].copy()
        self.weights   = self.weights[:last].copy()
        self.pinned    = self.pinned[:last].copy()
        self.labels.pop()
        self._index_to_id.pop()

        self._bump(positions_changed=True)

    def set_weight(self, node_id: int, weight: float) -> None:
        self.weights[self._id_to_index[node_id]] = weight
        self._bump(positions_changed=False)

    def pin_position(self, node_id: int, position: np.ndarray) -> None:
        idx = self._id_to_index[node_id]
        self.positions[idx] = np.asarray(position, dtype=np.float64).reshape(3,)
        self.pinned[idx] = True
        self._bump(positions_changed=True)

    def unpin(self, node_id: int) -> None:
        self.pinned[self._id_to_index[node_id]] = False
        self._bump(positions_changed=False)

    def clear(self) -> None:
        """Reset all node data and the ID counter to initial state."""
        self.positions = np.zeros((0, 3), dtype=np.float64)
        self.weights   = np.zeros((0,),   dtype=np.float64)
        self.pinned    = np.zeros((0,),   dtype=bool)
        self.labels    = []
        self._id_to_index = {}
        self._index_to_id = []
        self._next_id = 0
        self._revision += 1
        self._position_revision += 1
        self._pairs_cache = None

    def _set_positions(self, positions: np.ndarray) -> None:
        # Bulk write from the integrator. Bumps position revision so the
        # pairs cache invalidates, but suppresses on_change — the cascade
        # is for user/structural mutations, not the per-tick relax step.
        self.positions = positions
        self._bump(positions_changed=True, notify=False)

    # --- Derived queries -------------------------------------------------
    def center_of_mass(self) -> np.ndarray:
        if self.n == 0:
            return np.zeros(3, dtype=np.float64)
        total = self.weights.sum()
        if total == 0.0:
            return self.positions.mean(axis=0)
        return (self.positions * self.weights[:, None]).sum(axis=0) / total

    def pairs_within_radius(self, radius: float) -> np.ndarray:
        if self._pairs_cache is not None:
            cached_rev, cached_r, cached_pairs = self._pairs_cache
            if cached_rev == self._position_revision and cached_r == radius:
                return cached_pairs

        if self.n < 2:
            pairs = np.zeros((0, 2), dtype=np.int64)
        else:
            diff = self.positions[:, None, :] - self.positions[None, :, :]
            dist = np.linalg.norm(diff, axis=-1)
            i_idx, j_idx = np.triu_indices(self.n, k=1)
            mask = dist[i_idx, j_idx] <= radius
            pairs = np.stack([i_idx[mask], j_idx[mask]], axis=1).astype(np.int64)

        self._pairs_cache = (self._position_revision, radius, pairs)
        return pairs

    # --- Lookup ----------------------------------------------------------
    def get_node(self, node_id: int):
        from .node import Node
        return Node(self, node_id)

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
