"""Node view — thin wrapper over DOM-owned NumPy arrays.

A Node holds (dom, id). Attribute access reads/writes the row at
dom._id_to_index[id]. If the underlying node is removed, accessing the view
raises KeyError. Constructed via dom.get_node(id), not directly.
"""

import numpy as np

from .dom import DOM


class Node:
    __slots__ = ("_dom", "_id")

    def __init__(self, dom: DOM, node_id: int) -> None:
        self._dom = dom
        self._id = node_id

    @property
    def id(self) -> int:
        return self._id

    @property
    def label(self) -> str:
        return self._dom.labels[self._dom._id_to_index[self._id]]

    @property
    def weight(self) -> float:
        return float(self._dom.weights[self._dom._id_to_index[self._id]])

    @weight.setter
    def weight(self, value: float) -> None:
        self._dom.set_weight(self._id, value)

    @property
    def size(self) -> float:
        return float(self._dom.sizes[self._dom._id_to_index[self._id]])

    @property
    def position(self) -> np.ndarray:
        return self._dom.positions[self._dom._id_to_index[self._id]].copy()

    @property
    def pinned(self) -> bool:
        return bool(self._dom.pinned[self._dom._id_to_index[self._id]])

    def pin(self, position: np.ndarray) -> None:
        self._dom.pin_position(self._id, position)

    def unpin(self) -> None:
        self._dom.unpin(self._id)
