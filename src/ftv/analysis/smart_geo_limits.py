import numpy as np


def smart_geo_limits(lat, lon, q=(0.01, 0.99), pad_frac=0.05, min_pad_deg=0.01):
    """
    Robust bounds using quantiles (ignore outliers for framing).
    """
    lat = np.asarray(lat).ravel()
    lon = np.asarray(lon).ravel()

    m = np.isfinite(lat) & np.isfinite(lon)
    latf = lat[m]
    lonf = lon[m]
    if len(latf) < 2:
        raise ValueError("Not enough finite points to compute limits.")

    lo, hi = q
    lat_lo, lat_hi = np.quantile(latf, [lo, hi])
    lon_lo, lon_hi = np.quantile(lonf, [lo, hi])

    if not (lat_hi > lat_lo):
        lat_lo, lat_hi = latf.min(), latf.max()
    if not (lon_hi > lon_lo):
        lon_lo, lon_hi = lonf.min(), lonf.max()

    lat_span = lat_hi - lat_lo
    lon_span = lon_hi - lon_lo

    lat_pad = max(lat_span * pad_frac, min_pad_deg)
    lon_pad = max(lon_span * pad_frac, min_pad_deg)

    return (lat_lo - lat_pad, lat_hi + lat_pad), (lon_lo - lon_pad, lon_hi + lon_pad)
