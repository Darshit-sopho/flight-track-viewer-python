import matplotlib.pyplot as plt


def plot_distance(d: dict, cfg):
    fig = plt.figure(figsize=(8, 4))
    if not cfg.show_plots:
        plt.close(fig)

    ax = fig.add_subplot(111)
    ax.plot(d["t"], d["dist_nm"], linewidth=1.2)
    ax.set_title("Radius from reference over time")
    ax.set_ylabel("Distance (NM)")
    ax.set_xlabel("Time")
    ax.grid(True)
    return fig
