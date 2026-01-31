# from pathlib import Path
# import numpy as np
# import matplotlib.pyplot as plt
# import imageio.v2 as imageio


# def animate_playback(d: dict, cfg, out_folder: Path, base_name: str, outs: dict):
#     """
#     Animate the track and optionally save MP4 by writing frames.
#     """
#     fig = plt.figure(figsize=(8, 6))
#     if not cfg.show_plots:
#         plt.close(fig)
#     ax = fig.add_subplot(111)

#     ax.set_xlim(d["lon_lim"])
#     ax.set_ylim(d["lat_lim"])
#     ax.set_xlabel("Longitude")
#     ax.set_ylabel("Latitude")
#     ax.set_title("Playback")
#     ax.grid(True)

#     # static ref
#     ax.plot(cfg.ref_lon, cfg.ref_lat, marker="o", markersize=8, label="Ref")

#     # artists
#     (line,) = ax.plot([d["lon"][0]], [d["lat"][0]], linewidth=1.8, label="Track")
#     (pt,) = ax.plot([d["lon"][0]], [d["lat"][0]], marker="o", markersize=6)

#     ax.legend(loc="best")

#     writer = None
#     video_path = None
#     if cfg.save_video:
#         video_path = out_folder / f"{base_name}_Playback.mp4"
#         writer = imageio.get_writer(video_path, fps=cfg.video_fps)

#     try:
#         for k in d["frame_idx"][1:]:
#             line.set_data(d["lon"][: k + 1], d["lat"][: k + 1])
#             pt.set_data([d["lon"][k]], [d["lat"][k]])

#             title = f"{d.get('callsign','')}  {str(d['t'][k])}"
#             ax.set_title(title)

#             fig.canvas.draw()
            
#             if writer is not None:
#                 # grab RGB frame from canvas
#                 w, h = fig.canvas.get_width_height()
#                 # img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8).reshape(h, w, 3)
#                 buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
#                 buf = buf.reshape(h, w, 4)          # ARGB
#                 buf = buf[:, :, [1, 2, 3]]          # -> RGB (drop alpha, reorder)
#                 writer.append_data(buf)
#     finally:
#         if writer is not None:
#             writer.close()

#     if video_path is not None:
#         outs["playback_mp4"] = str(video_path)

#     return fig, outs


# src/ftv/plotting/animate_playback.py

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Tuple, Optional

import numpy as np
import matplotlib.pyplot as plt

from ftv.io.save_playback_video import save_playback_video


def fig_to_rgb_array(fig) -> np.ndarray:
    """
    Render a Matplotlib figure canvas and return an RGB uint8 image array (H, W, 3).

    Works across common Matplotlib backends:
    - Prefer tostring_rgb() when available
    - Fallback to tostring_argb() and reorder channels
    """
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()

    # Preferred: RGB (3 channels)
    if hasattr(fig.canvas, "tostring_rgb"):
        buf = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        return buf.reshape(h, w, 3)

    # Fallback: ARGB (4 channels) -> RGB
    buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8).reshape(h, w, 4)
    return buf[:, :, [1, 2, 3]]  # ARGB -> RGB


def animate_playback(
    d: Dict[str, Any],
    cfg: Any,
    out_dir: str | Path,
    base_name: str,
    outs: Optional[Dict[str, Any]] = None,
) -> Tuple[plt.Figure, Dict[str, Any]]:
    """
    Animate the flight track and optionally export an MP4.

    Parameters
    ----------
    d : dict
        Parsed flight data. Expected keys:
          - lat, lon (arrays)
          - t (datetime-like list/array)
          - frame_idx (list of indices)
          - lat_lim, lon_lim (for framing)
          - alt, spd, callsign (optional)
    cfg : Config-like object
        Expected attrs:
          - show_plots (bool)
          - save_video (bool)
          - video_fps (int)
          - video_quality (int)
    out_dir : str | Path
        Output folder for mp4.
    base_name : str
        Base name for output file.
    outs : dict
        Output registry; updated in-place.

    Returns
    -------
    fig : matplotlib.figure.Figure
    outs : dict
        Updated outputs (e.g., playback_mp4 path).
    """
    if outs is None:
        outs = {}

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # You can keep "visible" behavior by toggling interactive mode.
    # If show_plots is False, we still create the figure, we just don't block.
    if not getattr(cfg, "show_plots", True):
        plt.ioff()

    fig, ax = plt.subplots()
    ax.set_title("Playback")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Frame the full route
    ax.set_xlim(d["lon_lim"])
    ax.set_ylim(d["lat_lim"])
    ax.grid(True)

    # Static elements
    line, = ax.plot([], [], linewidth=2)
    pt, = ax.plot([], [], marker="o")

    writer = None
    video_path = None

    try:
        if getattr(cfg, "save_video", False):
            video_path = str(out_dir / f"{base_name}_Playback.mp4")
            writer = save_playback_video(video_path, cfg)

        # Initial frame
        # k0 = d["frame_idx"][0] if d.get("frame_idx") else 0
        frame_idx = d.get("frame_idx")
        if frame_idx is not None and len(frame_idx) > 0:
            k0 = frame_idx[0]
        else:
            k0 = 0
        line.set_data(d["lon"][: k0 + 1], d["lat"][: k0 + 1])
        pt.set_data([d["lon"][k0]], [d["lat"][k0]])
        fig.canvas.draw()

        if writer is not None:
            writer.append_data(fig_to_rgb_array(fig))

        # Animate frames
        for k in d.get("frame_idx", range(len(d["lat"]))):
            line.set_data(d["lon"][: k + 1], d["lat"][: k + 1])
            pt.set_data([d["lon"][k]], [d["lat"][k]])

            # Optional subtitle-ish text in the title (matplotlib doesn't have subtitle by default)
            callsign = d.get("callsign", "")
            spd = d.get("spd", None)
            alt = d.get("alt", None)
            t = d.get("t", None)

            title_bits = []
            if callsign:
                title_bits.append(str(callsign))
            if spd is not None and len(spd) > k:
                title_bits.append(f"Spd {spd[k]:.0f}")
            if alt is not None and len(alt) > k:
                title_bits.append(f"Alt {alt[k]:.0f}")
            if t is not None and len(t) > k:
                title_bits.append(str(t[k]))

            if title_bits:
                ax.set_title(" | ".join(title_bits))

            fig.canvas.draw()

            if writer is not None:
                writer.append_data(fig_to_rgb_array(fig))

    finally:
        if writer is not None:
            writer.close()

    if video_path:
        outs["playback_mp4"] = video_path

    return fig, outs
