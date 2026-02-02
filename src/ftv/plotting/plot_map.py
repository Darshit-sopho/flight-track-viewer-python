import matplotlib.pyplot as plt
import contextily as cx


def plot_map(d: dict, cfg):
    """
    Plot flight track on lon/lat axes (simple, works everywhere).
    """
    vis = cfg.show_plots
    fig = plt.figure(figsize=(8, 6))
    if not vis:
        plt.close(fig)

    ax = fig.add_subplot(111)
    ax.plot(d["lon"], d["lat"], linewidth=2.5, color="black", label="Track")
    # ax.plot(cfg.ref_lon, cfg.ref_lat, marker="o", markersize=8, label="Ref")

    if d.get("i_liftoff") is not None and d.get("i_touchdown") is not None and len(d.get("alt", [])) > 0:
        i0 = d["i_liftoff"]
        i1 = d["i_touchdown"]
        ax.plot(d["lon"][i0], d["lat"][i0], marker="o", markersize=8, label="Liftoff")
        ax.plot(d["lon"][i1], d["lat"][i1], marker="o", markersize=8, label="Touchdown")

    lat_lim = d["lat_lim"]
    lon_lim = d["lon_lim"]
    ax.set_xlim(lon_lim)
    ax.set_ylim(lat_lim)

    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Flight track")
    ax.grid(True)
    ax.legend(loc="best")
    try:
        # 'crs' tells contextily your data is in Latitude/Longitude (WGS84)
        # It will automatically fetch map tiles and match them to your track.
        cx.add_basemap(ax, crs='EPSG:4326', source=cx.providers.OpenStreetMap.Mapnik)
    except Exception as e:
        print(f"Could not load map background: {e}")

    return fig
