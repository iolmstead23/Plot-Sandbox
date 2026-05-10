from packages.config import config
from packages.physics import cool

_value: float = config.physics.initial_temperature


def get() -> float:
    return _value


def reset() -> None:
    global _value
    _value = config.physics.initial_temperature


def step() -> float:
    global _value
    _value = cool(
        _value,
        cooling_factor=config.physics.cooling_factor,
        min_temperature=config.physics.min_temperature,
    )
    return _value
