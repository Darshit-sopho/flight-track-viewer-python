import numpy as np
import pandas as pd

from .find_col import find_col
from .parse_time import parse_time
from .parse_position import parse_position
from .sort_and_clean import sort_and_clean


def parse_and_extract(df: pd.DataFrame) -> dict:
    """
    Parse DataFrame into normalized dict with cleaned vectors.
    """
    col_utc = find_col(df, "utc")
    col_ts = find_col(df, "timestamp")
    col_call = find_col(df, "callsign")
    col_pos = find_col(df, "position")
    col_alt = find_col(df, "altitude")
    col_spd = find_col(df, "speed")

    if not col_pos:
        raise ValueError("Could not find Position column.")

    t = parse_time(df, col_utc, col_ts)
    lat, lon = parse_position(df[col_pos])

    alt = None
    spd = None
    if col_alt:
        alt = pd.to_numeric(df[col_alt], errors="coerce").to_numpy()
    if col_spd:
        spd = pd.to_numeric(df[col_spd], errors="coerce").to_numpy()

    t_arr, lat, lon, alt, spd, idx, valid = sort_and_clean(t.to_numpy(), lat, lon, alt, spd)

    callsign = ""
    if col_call:
        cs = df[col_call].astype(str).str.replace('"', "", regex=False).str.strip().to_numpy()
        cs = cs[idx][valid]
        if len(cs) > 0:
            callsign = cs[0]

    if len(lat) < 2:
        raise ValueError("Not enough valid lat/lon points after filtering.")

    return {
        "t": t_arr,
        "lat": lat,
        "lon": lon,
        "alt": alt if alt is not None else np.array([]),
        "spd": spd if spd is not None else np.array([]),
        "callsign": callsign,
    }
