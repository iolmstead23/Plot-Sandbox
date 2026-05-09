"""Mutation queue: button clicks enqueue here; the physics tick drains and
applies between integrator steps so array reshape never happens during a
force computation.
"""

from typing import Any, Callable, Optional

import numpy as np

from packages.dom import dom

_pending: list[Callable[[], None]] = []

# Wired by handlers/tick.py to restart the physics tick when mutations are
# enqueued while the tick is paused at equilibrium.
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
    """Apply all pending mutations. Returns True if any were applied."""
    if not _pending:
        return False
    actions = _pending[:]
    _pending.clear()
    for fn in actions:
        fn()
    return True
