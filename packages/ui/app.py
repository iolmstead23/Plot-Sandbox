"""Tkinter window with a sidebar of injectable buttons and an embedded matplotlib Figure."""

import tkinter as tk
from typing import Callable, Optional

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# A button handler is any callable that accepts the App instance.
# The App is the only context handed to a handler; handlers interact with the
# UI exclusively through App's public methods (e.g. set_figure).
ButtonHandler = Callable[["App"], None]
ButtonSpec = tuple[str, ButtonHandler]


class App(tk.Tk):
    def __init__(
        self,
        figure: Figure,
        buttons: Optional[list[ButtonSpec]] = None,
        *,
        sample_size: int,
    ):
        super().__init__()
        self.title("3D Plot")
        self.geometry("900x600")

        # Bottom overlay packed first so it reserves a full-width strip; never re-rendered.
        # RGB legend: X=Red, Y=Green, Z=Blue vectors anchored at origin (0,0,0).
        overlay_text = f"n={sample_size}  |  X (Red)  Y (Green)  Z (Blue)"
        self._overlay = tk.Label(self, text=overlay_text)
        self._overlay.pack(side="bottom", fill="x")

        sidebar = tk.Frame(self)
        sidebar.pack(side="left", fill="y")
        for label, handler in buttons or []:
            tk.Button(
                sidebar,
                text=label,
                width=14,
                command=lambda h=handler: h(self),
            ).pack(padx=8, pady=6)

        self._canvas_area = tk.Frame(self)
        self._canvas_area.pack(side="right", fill="both", expand=True)

        self._canvas: FigureCanvasTkAgg = self._mount_canvas(figure)

    def _mount_canvas(self, figure: Figure) -> FigureCanvasTkAgg:
        canvas = FigureCanvasTkAgg(figure, master=self._canvas_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return canvas

    def set_figure(self, figure: Figure) -> None:
        """Replace the embedded figure. The only UI hook a handler should need."""
        self._canvas.get_tk_widget().destroy()
        self._canvas = self._mount_canvas(figure)


def launch(
    figure: Figure,
    buttons: Optional[list[ButtonSpec]] = None,
    *,
    sample_size: int,
) -> None:
    App(figure, buttons=buttons, sample_size=sample_size).mainloop()
