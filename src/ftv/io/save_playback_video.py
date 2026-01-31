# src/ftv/io/save_playback_video.py

import imageio.v2 as imageio

def save_playback_video(video_path: str, cfg):
    """
    Create and return an imageio video writer.
    cfg.video_quality is expected as 0-100 (MATLAB-like). We convert to 1-10 for imageio-ffmpeg.
    """
    q100 = int(getattr(cfg, "video_quality", 95))
    q100 = max(0, min(100, q100))

    # Map 0..100 -> 1..10 (ffmpeg plugin requirement)
    q10 = max(1, min(10, int(round(q100 / 10))))

    writer = imageio.get_writer(
        video_path,
        fps=int(getattr(cfg, "video_fps", 30)),
        quality=q10
    )
    return writer
