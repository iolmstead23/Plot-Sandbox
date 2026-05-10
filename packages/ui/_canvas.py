"""Canvas compatibility shim."""


class _CanvasWrapper:
    """Thin wrapper so render handlers can call app.canvas.update()."""

    def __init__(self, vispy_canvas) -> None:
        self._c = vispy_canvas

    def update(self) -> None:
        self._c.update()
