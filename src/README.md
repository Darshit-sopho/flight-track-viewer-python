# Flight Track Viewer (Python)

A Python toolkit for visualizing and analyzing flight tracks from CSV data. Designed for general aviation pilots, flight instructors, and aviation enthusiasts.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)

---

## Features

- 📍 Static flight track map visualization (latitude/longitude)
- 📊 Altitude and speed time-series plots
- 🎯 Distance calculations from a reference point (e.g., airport)
- ✈️ Automatic takeoff and landing detection (altitude-based heuristic)
- 🎬 Flight playback animation with optional MP4 export
- 🔍 Smart zoom that ignores GPS outliers
- 💾 Saves figures as `.png`
- 🧩 Modular design (data / analysis / plotting / io)
- 🆓 Free and open-source

---

## Quick Start

### Prerequisites

- Python **3.10 or 3.11** (recommended)
- Git (optional, for cloning the repository)

> ⚠️ Python 3.14 is not yet supported by scientific libraries such as NumPy, Matplotlib, and ImageIO.

---

### Installation

Clone or download the repository:

```bash
git clone https://github.com/Darshit-sopho/flight-track-viewer-python.git
cd flight-track-viewer-python
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS / Linux:
```bash
source .venv/bin/activate
```

Install the package and dependencies (from `pyproject.toml`):

```bash
pip install -e .
```

---

## Basic Usage

Run with file picker:

```python
from ftv import run

R = run()
```

Run with a specific CSV file:

```python
R = run(csv_file="myFlight.csv")
```

With options:

```python
R = run(
    csv_file="myFlight.csv",
    callsign="N503SP",
    animate=True,
    animate_step_seconds=30,
    save_figures_enabled=True,
    save_video_enabled=True
)
```

---

## CSV Format

### Required columns
- `Position` – format: "lat,lon"
- `UTC` or `Timestamp`

### Optional columns
- `Altitude`
- `Speed`
- `Direction`
- `Callsign`

Example:

```csv
Timestamp UTC,Callsign,Position,Altitude,Speed,Direction
2026-01-15T14:30:00Z,N503SP,"42.1900,-71.1720",0,0,0
2026-01-15T14:31:00Z,N503SP,"42.1950,-71.1680",500,80,45
```

---

## Programmatic Analysis

```python
R = run(csv_file="myFlight.csv", animate=False)

R["data"]["max_radius_nm"]
R["data"]["i_liftoff"]
R["data"]["i_touchdown"]
R["outputs"]
```

Returned dictionary contains:

- `config`
- `data`
- `figures`
- `outputs`

---

## Folder Structure

```
src/ftv/
  data/
  analysis/
  plotting/
  io/
  run.py
  config.py
examples/
  example_usage.py
```

---

## Dependency Management

This project uses **pyproject.toml** for dependency management.

Main dependencies:
- numpy
- pandas
- matplotlib
- imageio
- imageio-ffmpeg

They are installed automatically when you run:

```bash
pip install -e .
```

---

## License

MIT License

---

## Disclaimer

This tool is for visualization and educational purposes only.  
Not approved for navigation or flight safety use.

---

**Happy Flying!** ✈️
