from pathlib import Path
from typing import Any, Dict


def save_figures(figs: Dict[str, Any], folder: Path, base_name: str, outs: Dict[str, str]) -> Dict[str, str]:
    """
    Save key figures as PNG (and optionally other formats).
    Python doesn't have MATLAB .fig; we save PNG + optionally PDF.
    """
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)

    pairs = [
        ("Map", figs.get("map")),
        ("TimeSeries", figs.get("time_series")),
        ("Distance", figs.get("distance")),
    ]

    for tag, fig in pairs:
        if fig is None:
            continue
        png_path = folder / f"{base_name}_{tag}.png"
        fig.savefig(png_path, dpi=300, bbox_inches="tight")
        outs[f"{tag.lower()}_png"] = str(png_path)

    return outs
