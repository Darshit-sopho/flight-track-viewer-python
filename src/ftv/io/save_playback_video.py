# # src/ftv/io/save_playback_video.py

# import imageio.v2 as imageio

# def save_playback_video(video_path: str, cfg):
#     """
#     Create and return an imageio video writer.
#     cfg.video_quality is expected as 0-100 (MATLAB-like). We convert to 1-10 for imageio-ffmpeg.
#     """
#     q100 = int(getattr(cfg, "video_quality", 95))
#     q100 = max(0, min(100, q100))

#     # Map 0..100 -> 1..10 (ffmpeg plugin requirement)
#     q10 = max(1, min(10, int(round(q100 / 10))))

#     writer = imageio.get_writer(
#         video_path,
#         fps=int(getattr(cfg, "video_fps", 30)),
#         quality=q10
#     )
    
#     return writer

# # src/ftv/io/save_playback_video.py
# FIXED VERSION - Windows Media Player Compatible

import imageio.v2 as imageio


def save_playback_video(video_path: str, cfg):
    """
    Create and return an imageio video writer with Windows Media Player compatibility.
    
    cfg.video_quality is expected as 0-100 (MATLAB-like). We convert to 1-10 for imageio-ffmpeg.
    
    The output MP4 will be compatible with:
    - Windows Media Player
    - VLC Media Player
    - QuickTime
    - Web browsers
    - Mobile devices
    """
    q100 = int(getattr(cfg, "video_quality", 95))
    q100 = max(0, min(100, q100))

    # Map 0..100 -> 1..10 (ffmpeg plugin requirement)
    # q10 = max(1, min(10, int(round(q100 / 10))))
    q10 = max(1, min(9, int(round(q100 / 11))))

    fps = int(getattr(cfg, "video_fps", 30))

    # Windows Media Player compatible settings
    writer = imageio.get_writer(
        video_path,
        fps=fps,
        quality=q10,
        codec='libx264',           # H.264 codec
        pixelformat='yuv420p',     # Standard pixel format
        output_params=[            # FFmpeg parameters for compatibility
            '-profile:v', 'baseline',  # H.264 baseline profile (most compatible)
            '-level', '3.0',           # H.264 level 3.0 (widely supported)
            '-preset', 'medium',       # Encoding speed vs quality
            '-movflags', '+faststart', # Enable seeking/streaming
        ]
    )
    
    return writer
