from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Config:
    # Data selection
    csv_file: str = ""
    callsign: str = ""

    # Reference point
    ref_lat: float = 42.1900
    ref_lon: float = -71.1720

    # Smart zoom
    smart_zoom: bool = True
    zoom_quantiles: tuple[float, float] = (0.01, 0.99)
    pad_frac: float = 0.05
    min_pad_deg: float = 0.01

    # Plot/output
    show_plots: bool = True
    save_figures: bool = True
    save_video: bool = True
    output_folder: str = ""
    output_base_name: str = ""

    # Playback
    animate: bool = True
    animate_step_seconds: float = 30.0

    # Video
    video_fps: int = 30
    video_quality: int = 95  # 0-100


def default_config() -> Config:
    return Config()


def validate_config(cfg: Config) -> Config:
    if cfg.animate_step_seconds <= 0:
        raise ValueError("animate_step_seconds must be > 0")
    if cfg.video_fps <= 0:
        raise ValueError("video_fps must be > 0")

    q0, q1 = cfg.zoom_quantiles
    if not (0 <= q0 < q1 <= 1):
        raise ValueError("zoom_quantiles must be (low, high) with 0 <= low < high <= 1")

    cfg.video_quality = max(0, min(100, int(cfg.video_quality)))
    cfg.csv_file = str(cfg.csv_file)
    cfg.callsign = str(cfg.callsign)
    cfg.output_folder = str(cfg.output_folder)
    cfg.output_base_name = str(cfg.output_base_name)
    return cfg
