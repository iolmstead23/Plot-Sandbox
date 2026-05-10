"""plot: 3D scene builders. VisPy (GPU/OpenGL) is the primary renderer."""

from .projection import project_to_3d
from .vispy_3d import SceneObjects, build_vispy_scene, update_vispy_scene

__all__ = [
    "SceneObjects",
    "build_vispy_scene",
    "project_to_3d",
    "update_vispy_scene",
]
