"""Tkinter window with a sidebar of injectable buttons and an embedded matplotlib Figure.

Supports two modes of update:
  - `set_figure(fig)`: full canvas teardown + rebuild (legacy / Sample path).
  - `start_tick(cb)` + in-place artist updates: a recurring `after()` callback
    drives the physics tick. The canvas is never destroyed mid-tick.
"""

import tkinter as tk
from typing import Callable, Optional

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


ButtonHandler = Callable[["App"], None]
ButtonSpec = tuple[str, ButtonHandler]


class App(tk.Tk):
    def __init__(
        self,
        figure: Figure,
        buttons: Optional[list[ButtonSpec]] = None,
        *,
        sample_size: int,
        params: Optional[dict] = None,
        window_title: str = "3D Plot",
        geometry: str = "900x600",
        button_width: int = 14,
        button_padx: int = 8,
        button_pady: int = 6,
    ):
        super().__init__()
        self.title(window_title)
        self.geometry(geometry)

        self._params = params
        self._overlay = tk.Label(self, text=self._build_banner(sample_size))
        self._overlay.pack(side="bottom", fill="x")

        sidebar = tk.Frame(self)
        sidebar.pack(side="left", fill="y")
        for label, handler in buttons or []:
            tk.Button(
                sidebar,
                text=label,
                width=button_width,
                command=lambda h=handler: h(self),
            ).pack(padx=button_padx, pady=button_pady)

        self._canvas_area = tk.Frame(self)
        self._canvas_area.pack(side="right", fill="both", expand=True)

        self._canvas: FigureCanvasTkAgg = self._mount_canvas(figure)

        self._artists = None
        self._tick_callback: Optional[Callable[["App"], None]] = None
        self._tick_interval_ms: int = 33
        self._tick_id: Optional[str] = None

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _mount_canvas(self, figure: Figure) -> FigureCanvasTkAgg:
        canvas = FigureCanvasTkAgg(figure, master=self._canvas_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return canvas

    def set_figure(self, figure: Figure) -> None:
        """Replace the embedded figure (full rebuild). Stops any active tick."""
        self.stop_tick()
        self._canvas.get_tk_widget().destroy()
        self._canvas = self._mount_canvas(figure)
        self._artists = None

    def set_artists(self, artists) -> None:
        """Hand the renderer's Artists bundle to the App so the tick can update in place."""
        self._artists = artists

    @property
    def artists(self):
        return self._artists

    @property
    def is_ticking(self) -> bool:
        return self._tick_id is not None

    @property
    def canvas(self) -> FigureCanvasTkAgg:
        return self._canvas

    def _build_banner(self, n: int, temperature: Optional[float] = None) -> str:
        parts: list[str] = [f"n={n}"]
        if temperature is not None:
            parts.append(f"T={temperature:.3f}")
        if self._params:
            p = self._params
            parts.append(
                f"k_g={p['k_g']}  k_r={p['k_r']}  k_a={p['k_a']}"
                f"  r0={p['r0']}  R={p['R']}  dt={p['dt']}"
            )
        parts.append("X (Red)  Y (Green)  Z (Blue)")
        return "  |  ".join(parts)

    def update_banner(self, n: int, temperature: Optional[float] = None) -> None:
        self._overlay.config(text=self._build_banner(n, temperature))

    def start_tick(
        self,
        callback: Callable[["App"], None],
        *,
        interval_ms: int = 33,
    ) -> None:
        self.stop_tick()
        self._tick_callback = callback
        self._tick_interval_ms = interval_ms
        self._schedule_next_tick()

    def stop_tick(self) -> None:
        if self._tick_id is not None:
            try:
                self.after_cancel(self._tick_id)
            except tk.TclError:
                pass
            self._tick_id = None
        self._tick_callback = None

    def _schedule_next_tick(self) -> None:
        if self._tick_callback is None:
            return
        self._tick_id = self.after(self._tick_interval_ms, self._on_tick)

    def _on_tick(self) -> None:
        cb = self._tick_callback
        if cb is None:
            return
        cb(self)
        self._schedule_next_tick()

    def _on_close(self) -> None:
        self.stop_tick()
        self.destroy()


def launch(
    figure: Figure,
    buttons: Optional[list[ButtonSpec]] = None,
    *,
    sample_size: int,
    params: Optional[dict] = None,
    artists=None,
    on_ready: Optional[Callable[["App"], None]] = None,
    window_title: str = "3D Plot",
    geometry: str = "900x600",
    button_width: int = 14,
    button_padx: int = 8,
    button_pady: int = 6,
) -> None:
    app = App(
        figure,
        buttons=buttons,
        sample_size=sample_size,
        params=params,
        window_title=window_title,
        geometry=geometry,
        button_width=button_width,
        button_padx=button_padx,
        button_pady=button_pady,
    )
    if artists is not None:
        app.set_artists(artists)
    if on_ready is not None:
        on_ready(app)
    app.mainloop()
