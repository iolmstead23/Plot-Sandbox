from dataclasses import dataclass


@dataclass
class VelocimetryConfig:
    enabled: bool
    output_path: str
    save_csv: bool
    save_npz: bool
    plot_on_convergence: bool
    max_frames: int = 20000
