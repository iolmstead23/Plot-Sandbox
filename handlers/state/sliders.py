from packages.config import config


def make_force_slider_callback(key: str):
    def callback(app, value: float) -> None:
        setattr(config.physics, key, value)
        from ..reseed import reseed
        reseed(app)

    return callback
