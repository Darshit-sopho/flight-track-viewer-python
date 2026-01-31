from .smart_geo_limits import smart_geo_limits


def compute_geo_limits(lat, lon, cfg):
    """
    Compute lat/lon limits for plotting (smart quantile zoom or min/max).
    """
    if cfg.smart_zoom:
        return smart_geo_limits(lat, lon, cfg.zoom_quantiles, cfg.pad_frac, cfg.min_pad_deg)

    lat_min, lat_max = float(min(lat)), float(max(lat))
    lon_min, lon_max = float(min(lon)), float(max(lon))

    lat_pad = max((lat_max - lat_min) * cfg.pad_frac, cfg.min_pad_deg)
    lon_pad = max((lon_max - lon_min) * cfg.pad_frac, cfg.min_pad_deg)

    return (lat_min - lat_pad, lat_max + lat_pad), (lon_min - lon_pad, lon_max + lon_pad)
