from dataclasses import dataclass


@dataclass
class SliderRangeConfig:
    min: float
    max: float
    step: float


@dataclass
class SlidersConfig:
    gravity_ratio: SliderRangeConfig
    repel_ratio: SliderRangeConfig
    k_edge: SliderRangeConfig
