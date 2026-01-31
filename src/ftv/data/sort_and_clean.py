import numpy as np
import pandas as pd


def sort_and_clean(t, lat, lon, alt=None, spd=None):
    """
    Sort by time and remove invalid lat/lon points. Returns cleaned arrays plus indices.
    """
    # sort index
    idx = np.argsort(pd.Series(t).to_numpy())
    t = np.asarray(t)[idx]
    lat = np.asarray(lat)[idx]
    lon = np.asarray(lon)[idx]

    if alt is not None and len(alt) > 0:
        alt = np.asarray(alt)[idx]
    else:
        alt = None

    if spd is not None and len(spd) > 0:
        spd = np.asarray(spd)[idx]
    else:
        spd = None

    valid = np.isfinite(lat) & np.isfinite(lon)
    t = t[valid]
    lat = lat[valid]
    lon = lon[valid]
    if alt is not None:
        alt = alt[valid]
    if spd is not None:
        spd = spd[valid]

    return t, lat, lon, alt, spd, idx, valid
