from .haversine_nm import haversine_nm


def compute_metrics(d: dict, ref_lat: float, ref_lon: float) -> dict:
    """
    Compute distance from reference point and max radius.
    """
    dist = haversine_nm(d["lat"], d["lon"], ref_lat, ref_lon)
    d["dist_nm"] = dist
    d["max_radius_nm"] = float(dist.max())
    d["i_max_radius"] = int(dist.argmax())
    return d
