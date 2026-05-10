"""Qt + VisPy application window.

Preserves the same public API as the old Tkinter version so all handlers
work without changes:

  App(scene_objects, buttons, *, sliders, window_title, geometry, ...)
  app.artists          — SceneObjects bundle
  app.canvas           — CanvasWrapper with .update()
  app.is_ticking       — bool
  app.start_tick(cb, interval_ms)
  app.stop_tick()
  app.update_banner(n, temperature, fps, tick_ms, accel)

Threading model
---------------
  Main thread (Qt event loop)  — renders at 60 FPS via QTimer
  Background thread (thread.py) — GPU physics runs continuously
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Callable, Optional

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCloseEvent, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from packages.plot.vispy_3d import SceneObjects

from .theme import _BG, _BANNER_FONT, _BANNER_FONT_SIZE, _BANNER_HEIGHT, _BANNER_PADDING, _BORDER, _TEXT
from ._canvas import _CanvasWrapper
from ._sidebar import build_sidebar
from ._types import ButtonSpec, SliderSpec


class App(QMainWindow):
    def __init__(
        self,
        scene_objects: SceneObjects,
        buttons: Optional[list[ButtonSpec]] = None,
        *,
        sample_size: int = 0,
        sliders: Optional[list[SliderSpec]] = None,
        window_title: str = "3D Plot",
        geometry: str = "900x640",
        button_padx: int = 8,
        button_pady: int = 6,
    ) -> None:
        super().__init__()
        self.setWindowTitle(window_title)

        try:
            w, h = (int(v) for v in geometry.split("x"))
        except ValueError:
            w, h = 900, 640
        self.resize(w, h)

        self._scene: SceneObjects = scene_objects
        self._canvas_wrapper = _CanvasWrapper(scene_objects.canvas)

        self._tick_callback: Optional[Callable[["App"], None]] = None
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._on_tick)

        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        sidebar = build_sidebar(self, buttons or [], sliders or [], button_padx, button_pady)
        content_layout.addWidget(sidebar)

        canvas_widget = scene_objects.canvas.native
        canvas_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        content_layout.addWidget(canvas_widget)

        root_layout.addWidget(content)

        self._banner = QLabel(self._format_banner(sample_size))
        self._banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._banner.setFont(QFont(_BANNER_FONT, _BANNER_FONT_SIZE))
        self._banner.setFixedHeight(_BANNER_HEIGHT)
        self._banner.setStyleSheet(
            f"background-color:{_BG};"
            f"color:{_TEXT};"
            f"padding:{_BANNER_PADDING};"
            f"border-top:1px solid {_BORDER};"
            "font-weight:bold;"
        )
        root_layout.addWidget(self._banner)

    @property
    def artists(self) -> Optional[SceneObjects]:
        return self._scene

    @property
    def canvas(self) -> _CanvasWrapper:
        return self._canvas_wrapper

    @property
    def is_ticking(self) -> bool:
        return self._timer.isActive()

    def start_tick(
        self,
        callback: Callable[["App"], None],
        *,
        interval_ms: int = 16,
    ) -> None:
        self.stop_tick()
        self._tick_callback = callback
        self._timer.start(interval_ms)

    def stop_tick(self) -> None:
        self._timer.stop()
        self._tick_callback = None

    def _on_tick(self) -> None:
        if self._tick_callback is not None:
            self._tick_callback(self)

    @staticmethod
    def _format_banner(
        n: int,
        temperature: Optional[float] = None,
        fps: Optional[float] = None,
        tick_ms: Optional[float] = None,
        accel: str = "",
    ) -> str:
        parts = [f"n={n}"]
        if temperature is not None:
            parts.append(f"T={temperature:.3f}")
        if fps is not None:
            parts.append(f"FPS={fps:.1f}")
        if tick_ms is not None:
            parts.append(f"tick={tick_ms:.1f}ms")
        if accel:
            parts.append(accel)
        parts.append("X (Red)  Y (Green)  Z (Blue)")
        return "  |  ".join(parts)

    def update_banner(
        self,
        n: int,
        temperature: Optional[float] = None,
        fps: Optional[float] = None,
        tick_ms: Optional[float] = None,
        accel: str = "",
    ) -> None:
        self._banner.setText(self._format_banner(n, temperature, fps, tick_ms, accel))

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.stop_tick()
        if a0 is not None:
            a0.accept()


def launch(
    scene_objects: SceneObjects,
    buttons: Optional[list[ButtonSpec]] = None,
    *,
    sample_size: int = 0,
    sliders: Optional[list[SliderSpec]] = None,
    on_ready: Optional[Callable[[App], None]] = None,
    window_title: str = "3D Plot",
    geometry: str = "900x640",
    button_padx: int = 8,
    button_pady: int = 6,
) -> None:
    qt_app = QApplication.instance() or QApplication(sys.argv)

    app = App(
        scene_objects,
        buttons=buttons,
        sample_size=sample_size,
        sliders=sliders,
        window_title=window_title,
        geometry=geometry,
        button_padx=button_padx,
        button_pady=button_pady,
    )
    if on_ready is not None:
        on_ready(app)
    app.show()
    qt_app.exec()
