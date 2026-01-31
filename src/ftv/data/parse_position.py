import numpy as np
import pandas as pd


def parse_position(pos_col: pd.Series) -> tuple[np.ndarray, np.ndarray]:
    """
    Parse "lat,lon" strings into numeric arrays.
    """
    s = pos_col.astype(str).str.replace('"', "", regex=False).str.replace(" ", "", regex=False)
    parts = s.str.split(",", n=1, expand=True)
    if parts.shape[1] < 2:
        raise ValueError('Position column does not look like "lat,lon".')
    lat = pd.to_numeric(parts[0], errors="coerce").to_numpy()
    lon = pd.to_numeric(parts[1], errors="coerce").to_numpy()
    return lat, lon
