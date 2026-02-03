from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, Optional

from .config import Config, default_config, validate_config
from .io.select_csv_file import select_csv_file
from .io.save_figures import save_figures
from .data.read_flight_csv import read_flight_csv
from .data.apply_callsign_filter import apply_callsign_filter
from .data.parse_and_extract import parse_and_extract
from .data.build_frame_idx import build_frame_idx
from .analysis.detect_takeoff_landing import detect_takeoff_landing
from .analysis.compute_metrics import compute_metrics
from .analysis.compute_geo_limits import compute_geo_limits
from .plotting.plot_map import plot_map
from .plotting.plot_time_series import plot_time_series
from .plotting.plot_distance import plot_distance
from .plotting.animate_playback import animate_playback


def run(
    *,
    csv_file: str | Path = "",
    callsign: str = "",
    # reference point
    ref_lat: float = 42.1900,
    ref_lon: float = -71.1720,
    # zoom
    smart_zoom: bool = True,
    zoom_quantiles=(0.01, 0.99),
    pad_frac: float = 0.05,
    min_pad_deg: float = 0.01,
    # output / plotting
    show_plots: bool = True,
    save_figures_enabled: bool = True,
    save_video_enabled: bool = True,
    output_folder: str | Path = "",
    output_base_name: str = "",
    # playback
    animate: bool = True,
    animate_step_seconds: float = 30.0,
    # video settings
    video_fps: int = 30,
    video_quality: int = 95,
) -> Dict[str, Any]:
    """
    Load a flight CSV, plot map/time-series/distance, and optionally export a playback MP4.

    Returns a dict containing config, parsed data, matplotlib figures, and output paths.
    """

    cfg = default_config()
    cfg.csv_file = str(csv_file)
    cfg.callsign = callsign
    cfg.ref_lat = ref_lat
    cfg.ref_lon = ref_lon
    cfg.smart_zoom = smart_zoom
    cfg.zoom_quantiles = tuple(zoom_quantiles)
    cfg.pad_frac = pad_frac
    cfg.min_pad_deg = min_pad_deg
    cfg.show_plots = show_plots
    cfg.save_figures = save_figures_enabled
    cfg.save_video = save_video_enabled
    cfg.output_folder = str(output_folder)
    cfg.output_base_name = output_base_name
    cfg.animate = animate
    cfg.animate_step_seconds = float(animate_step_seconds)
    cfg.video_fps = int(video_fps)
    cfg.video_quality = int(video_quality)

    cfg = validate_config(cfg)

    # ----- choose file -----
    if not cfg.csv_file:
        picked = select_csv_file()
        if picked is None:
            return {}  # user cancelled
        csv_path = Path(picked)
    else:
        csv_path = Path(cfg.csv_file)
        if not csv_path.is_file():
            raise FileNotFoundError(f"CSV not found: {csv_path}")

    # output paths
    if not cfg.output_folder:
        out_dir = csv_path.parent
    else:
        out_dir = Path(cfg.output_folder)
        out_dir.mkdir(parents=True, exist_ok=True)

    base_name = cfg.output_base_name or csv_path.stem

    # ----- load & parse -----
    T = read_flight_csv(csv_path)
    T = apply_callsign_filter(T, cfg.callsign)
    d = parse_and_extract(T)

    if d["lat"][0] and d["lon"][0]:
        cfg.ref_lat = d["lat"][0]
        cfg.ref_lon = d["lon"][0]

    # derived
    d["frame_idx"] = build_frame_idx(d["t"], cfg.animate_step_seconds)
    d["i_liftoff"], d["i_touchdown"] = detect_takeoff_landing(d.get("alt"))

    d = compute_metrics(d, cfg.ref_lat, cfg.ref_lon)
    d["lat_lim"], d["lon_lim"] = compute_geo_limits(d["lat"], d["lon"], cfg)

    # ----- plotting -----
    figs: Dict[str, Any] = {"map": None, "time_series": None, "distance": None, "playback": None}
    figs["map"] = plot_map(d, cfg)
    figs["time_series"] = plot_time_series(d, cfg)
    figs["distance"] = plot_distance(d, cfg)

    outs: Dict[str, str] = {}

    if cfg.save_figures:
        outs = save_figures(figs, out_dir, base_name, outs)

    if cfg.animate:
        figs["playback"], outs = animate_playback(d, cfg, out_dir, base_name, outs)

    return {
        "config": asdict(cfg),
        "csv_file": str(csv_path),
        "output_folder": str(out_dir),
        "base_name": base_name,
        "data": d,
        "figures": figs,
        "outputs": outs,
    }


def main() -> None:
    """CLI entry point: `ftv` opens file picker and runs with defaults."""
    run()
