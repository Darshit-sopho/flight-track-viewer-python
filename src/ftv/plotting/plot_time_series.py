import matplotlib.pyplot as plt
import numpy as np


def plot_time_series(d: dict, cfg):
    alt = d.get("alt", np.array([]))
    spd = d.get("spd", np.array([]))
    if (alt is None or len(alt) == 0) and (spd is None or len(spd) == 0):
        return None

    fig = plt.figure(figsize=(8, 6))
    if not cfg.show_plots:
        plt.close(fig)

    ax1 = fig.add_subplot(211)
    if alt is not None and len(alt) > 0:
        ax1.plot(d["t"], alt, linewidth=1.2)
        ax1.set_ylabel("Altitude (feet)")
        ax1.set_title("Altitude vs time")
        ax1.grid(True)
    else:
        ax1.text(0.1, 0.5, "No altitude column found", transform=ax1.transAxes)
        ax1.axis("off")

    ax2 = fig.add_subplot(212)
    if spd is not None and len(spd) > 0:
        ax2.plot(d["t"], spd, linewidth=1.2)
        ax2.set_ylabel("Speed (knots)")
        ax2.set_xlabel("Time")
        ax2.set_title("Speed vs time")
        ax2.grid(True)
    else:
        ax2.text(0.1, 0.5, "No speed column found", transform=ax2.transAxes)
        ax2.axis("off")

    fig.tight_layout()
    return fig
