from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Callable, Optional

from PyQt6.QtWidgets import QApplication

from ._app import App
from ._types import ButtonSpec, SliderSpec

if TYPE_CHECKING:
    from packages.plot import SceneObjects


def launch(
    scene_objects: SceneObjects,
    buttons: Optional[list[ButtonSpec]] = None,
    *,
    sample_size: int = 0,
    sliders: Optional[list[SliderSpec]] = None,
    on_ready: Optional[Callable[[App], None]] = None,
    window_title: str = "3D Plot",
    geometry: str = "900x600",
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
