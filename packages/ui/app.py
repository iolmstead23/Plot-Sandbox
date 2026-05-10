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
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from packages.plot.vispy_3d import SceneObjects

# ── Visual constants (no cross-package import; values mirror packages/theme) ──
_BG           = "#1e1e2e"
_TEXT         = "#cdd6f4"
_BORDER       = "#45475a"
_BUTTON_BG    = "#313244"
_BUTTON_HOVER = "#45475a"
_BANNER_FONT       = "Courier"
_BANNER_FONT_SIZE  = 9
_BANNER_HEIGHT     = 22
_BANNER_PADDING    = "2px 6px"
_SIDEBAR_WIDTH = 160
_BUTTON_WIDTH  = 130

ButtonHandler = Callable[["App"], None]
ButtonSpec = tuple[str, ButtonHandler]
SliderCallback = Callable[["App", float], None]
SliderSpec = tuple[str, float, float, float, float, SliderCallback]


# ---------------------------------------------------------------------------
# Canvas compatibility shim
# ---------------------------------------------------------------------------


class _CanvasWrapper:
    """Thin wrapper so render handlers can call app.canvas.update()."""

    def __init__(self, vispy_canvas) -> None:
        self._c = vispy_canvas

    def update(self) -> None:
        self._c.update()



# ---------------------------------------------------------------------------
# Main window
# ---------------------------------------------------------------------------


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

        # Parse WxH geometry string
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

        # ── root layout ────────────────────────────────────────────────────
        root = QWidget()
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ── main content row (sidebar + canvas) ────────────────────────────
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar — target only the container widget (not child buttons/sliders)
        # so native QPushButton rendering is preserved.
        sidebar = self._build_sidebar(
            buttons or [], sliders or [], button_padx, button_pady
        )
        sidebar.setObjectName("sidebar_container")
        sidebar.setStyleSheet(f"""
            QWidget#sidebar_container {{ background-color: {_BG}; }}
            QWidget#sidebar_container QPushButton {{
                background-color: {_BUTTON_BG};
                color: {_TEXT};
                border: 1px solid {_BORDER};
                padding: 4px 8px;
                border-radius: 3px;
            }}
            QWidget#sidebar_container QPushButton:hover {{
                background-color: {_BUTTON_HOVER};
            }}
            QWidget#sidebar_container QLabel {{
                background-color: transparent;
                color: {_TEXT};
            }}
            QWidget#sidebar_container QFrame {{
                background-color: {_BUTTON_BG};
                border: 1px solid {_BORDER};
                border-radius: 3px;
            }}
            QWidget#sidebar_container QSlider::groove:horizontal {{
                background: {_BORDER};
                height: 4px;
                border-radius: 2px;
            }}
            QWidget#sidebar_container QSlider::handle:horizontal {{
                background: {_TEXT};
                width: 12px;
                height: 12px;
                border-radius: 6px;
                margin: -4px 0;
            }}
        """)
        content_layout.addWidget(sidebar)

        # VisPy OpenGL canvas — zero margins, same background so clipped
        # nodes at the edge blend rather than hard-cut against a white frame.
        canvas_widget = scene_objects.canvas.native
        canvas_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        content_layout.addWidget(canvas_widget)

        root_layout.addWidget(content)

        # ── banner — explicit colours so it reads on any Windows theme ───────
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

    # ── sidebar construction ───────────────────────────────────────────────

    def _build_sidebar(
        self,
        buttons: list[ButtonSpec],
        sliders: list[SliderSpec],
        padx: int,
        pady: int,
    ) -> QWidget:
        sidebar = QWidget()
        sidebar.setFixedWidth(_SIDEBAR_WIDTH)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(padx, pady, padx, pady)
        layout.setSpacing(pady)

        for label, handler in buttons:
            btn = QPushButton(label)
            btn.setFixedWidth(_BUTTON_WIDTH)
            btn.clicked.connect(lambda _checked, h=handler: h(self))
            layout.addWidget(btn)

        layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        )

        if sliders:
            frame = QFrame()
            frame.setFrameShape(QFrame.Shape.StyledPanel)
            frame_layout = QVBoxLayout(frame)
            frame_layout.setContentsMargins(4, 4, 4, 4)
            frame_layout.setSpacing(2)

            for s_label, s_init, s_lo, s_hi, s_step, s_cb in sliders:
                lbl = QLabel(s_label)
                frame_layout.addWidget(lbl)

                val_label = QLabel(f"{s_init:.2f}")
                val_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                frame_layout.addWidget(val_label)

                steps = max(1, round((s_hi - s_lo) / s_step))
                slider = QSlider(Qt.Orientation.Horizontal)
                slider.setRange(0, steps)
                slider.setValue(round((s_init - s_lo) / s_step))

                def _on_change(
                    v: int, lo=s_lo, st=s_step, vl=val_label, cb=s_cb
                ) -> None:
                    fval = lo + v * st
                    vl.setText(f"{fval:.2f}")
                    cb(self, fval)

                slider.valueChanged.connect(_on_change)
                frame_layout.addWidget(slider)

            layout.addWidget(frame)

        return sidebar

    # ── scene management ───────────────────────────────────────────────────

    @property
    def artists(self) -> Optional[SceneObjects]:
        return self._scene

    # ── canvas access ──────────────────────────────────────────────────────

    @property
    def canvas(self) -> _CanvasWrapper:
        return self._canvas_wrapper

    # ── tick / timer ───────────────────────────────────────────────────────

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

    # ── banner ─────────────────────────────────────────────────────────────

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

    # ── window events ──────────────────────────────────────────────────────

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.stop_tick()
        if a0 is not None:
            a0.accept()


# ---------------------------------------------------------------------------
# Launch helper
# ---------------------------------------------------------------------------


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
