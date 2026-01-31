import numpy as np
import pandas as pd


def build_frame_idx(t, step_seconds: float) -> np.ndarray:
    """
    Indices spaced every step_seconds of elapsed time.
    Works with tz-aware pandas datetimes or numeric fallback.
    """
    if len(t) < 2:
        return np.array([0], dtype=int)

    # If datetime-like:
    if isinstance(t[0], (pd.Timestamp,)) or hasattr(t[0], "to_pydatetime"):
        t0 = t[0]
        dt = np.array([(ti - t0).total_seconds() for ti in t])
    else:
        # numeric fallback assumes 1 unit per sample
        dt = np.arange(len(t), dtype=float)

    frame_idx = [0]
    next_time = step_seconds
    for k in range(1, len(dt)):
        if dt[k] >= next_time:
            frame_idx.append(k)
            next_time += step_seconds

    return np.array(frame_idx, dtype=int)
