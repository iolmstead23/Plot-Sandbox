from dataclasses import dataclass


@dataclass
class UiConfig:
    window_title: str
    geometry: str
    button_padx: int
    button_pady: int
