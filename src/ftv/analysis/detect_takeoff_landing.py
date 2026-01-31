import numpy as np


def detect_takeoff_landing(alt):
    """
    Simple heuristic: first and last index where alt > 0.
    Returns (i_liftoff, i_touchdown) or (None, None).
    """
    if alt is None or len(alt) == 0:
        return None, None
    alt = np.asarray(alt)
    idx = np.where(alt > 0)[0]
    if len(idx) == 0:
        return None, None
    return int(idx[0]), int(idx[-1])
