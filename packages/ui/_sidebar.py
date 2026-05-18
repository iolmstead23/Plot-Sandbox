"""Sidebar widget builder — extracted from App._build_sidebar."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from .theme import (
    _BG,
    _BORDER,
    _BUTTON_BG,
    _BUTTON_HOVER,
    _BUTTON_WIDTH,
    _SIDEBAR_WIDTH,
    _SLIDER_MARGIN,
    _SLIDER_PADDING,
    _TEXT,
)

if TYPE_CHECKING:
    from ._app import App
    from ._types import ButtonSpec, SliderSpec


def build_sidebar(
    app: "App",
    buttons: list["ButtonSpec"],
    sliders: list["SliderSpec"],
    padx: int,
    pady: int,
) -> tuple[QWidget, list[QPushButton]]:
    sidebar = QWidget()
    sidebar.setFixedWidth(_SIDEBAR_WIDTH)
    layout = QVBoxLayout(sidebar)
    layout.setContentsMargins(padx, pady, padx, pady)
    layout.setSpacing(pady)

    gated_buttons: list[QPushButton] = []
    for spec in buttons:
        label, handler = spec[0], spec[1]
        gated = len(spec) > 2 and bool(spec[2])
        btn = QPushButton(label)
        btn.setFixedWidth(_BUTTON_WIDTH)
        btn.clicked.connect(lambda _checked, h=handler: h(app))
        if gated:
            btn.setEnabled(False)
            gated_buttons.append(btn)
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
                cb(app, fval)

            slider.valueChanged.connect(_on_change)
            frame_layout.addWidget(slider)

        layout.addWidget(frame)

    sidebar.setObjectName("sidebar_container")
    sidebar.setStyleSheet(f"""
        QWidget#sidebar_container {{ background-color: {_BG}; }}
        QWidget#sidebar_container QPushButton {{
            background-color: {_BUTTON_BG};
            color: {_TEXT};
            border: 1px solid {_BORDER};
            padding: {_SLIDER_PADDING};
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
            margin: {_SLIDER_MARGIN};
        }}
    """)

    return sidebar, gated_buttons
