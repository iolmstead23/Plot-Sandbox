from typing import Any, Callable, Optional

from packages.dom import dom

_pending: list[Callable[[], None]] = []

on_enqueue: Optional[Callable[[], None]] = None


def queue(action: Callable[[], Any]) -> None:
    _pending.append(action)
    if on_enqueue is not None:
        on_enqueue()


def drain() -> bool:
    if not _pending:
        return False
    actions = _pending[:]
    _pending.clear()
    for fn in actions:
        fn()
    return True
