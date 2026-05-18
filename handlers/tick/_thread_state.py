import threading
from typing import Any

positions_lock: threading.Lock = threading.Lock()

_thread: threading.Thread | None = None
_stop_event: threading.Event = threading.Event()
_converged: threading.Event = threading.Event()
_steps_per_sec: float = 0.0
_current_temperature: float = 1.0
_physics_stream = None

# Persistent GPU arrays — survive across batches when DOM structure is stable.
# None until first loop iteration; freed in stop().
_pos_gpu: Any = None
_w_gpu:   Any = None
_pin_gpu: Any = None
_e_gpu:   Any = None
_gpu_n:   int = 0
