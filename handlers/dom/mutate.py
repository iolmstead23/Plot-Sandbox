from typing import Any, Callable, Optional

import numpy as np

from packages.dom import dom

_pending: list[Callable[[], None]] = []

on_enqueue: Optional[Callable[[], None]] = None


def queue(action: Callable[[], Any]) -> None:
    _pending.append(action)
    if on_enqueue is not None:
        on_enqueue()


def queue_add_node(weight: float, position: np.ndarray) -> None:
    queue(lambda: dom.add_node(weight, position))


def queue_remove_node(node_id: int) -> None:
    queue(lambda: dom.remove_node(node_id))


def drain() -> bool:
    if not _pending:
        return False
    actions = _pending[:]
    _pending.clear()
    for fn in actions:
        fn()
    return True
