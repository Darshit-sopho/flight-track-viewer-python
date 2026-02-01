# Flight Track Viewer

> A Python toolkit with graphical interface for visualizing and analyzing flight tracks from CSV data.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

**Designed for general aviation pilots, flight instructors, and aviation enthusiasts.**

---

## ✨ Features

- 🖥️ **Modern GUI** - Easy-to-use PyQt6 interface with live animation
- 📊 **Interactive Charts** - Altitude and speed visualizations  
- 🎬 **Flight Playback** - Watch your flight path animate in real-time
- 💾 **Export Options** - Save figures (PNG) and animations (MP4)
- 🎯 **Smart Analysis** - Automatic takeoff/landing detection, distance calculations
- 🧩 **Flexible Usage** - GUI application OR Python API

---

## 🚀 Quick Start

### Option 1: GUI Application (Recommended)

**Windows:**
```batch
scripts\setup_with_ui.bat
```

**Mac/Linux:**
```bash
chmod +x scripts/setup_with_ui.sh
./scripts/setup_with_ui.sh
```

This installs everything and launches the GUI automatically!

### Option 2: Python API Only

For programmatic use without the GUI:

**Windows:**
```batch
scripts\setup_core.bat
```

**Mac/Linux:**
```bash
chmod +x scripts/setup_core.sh
./scripts/setup_core.sh
```

Then use it in your code:
```python
from ftv import run

result = run(csv_file="flight.csv", animate=True, save_figures=True)
print(f"Max altitude: {result['data']['max_altitude_ft']} ft")
```

---

## 📖 What's Included

### GUI Application
![Flight Track Viewer Interface](docs/screenshot_placeholder.png)

**Left Panel:**
- Animated flight path on map
- Play/pause/reset controls

**Right Panel:**
- Altitude vs Time chart
- Speed vs Time chart  
- Flight statistics

### Python API
```python
from ftv import run

# With file picker
result = run()

# Or specify options
result = run(
    csv_file="myFlight.csv",
    callsign="N503SP",
    animate=True,
    save_figures=True,
    save_video=True
)
```

---

## 📊 CSV File Format

Your CSV file should have these columns:

**Required:**
- `Position` - format: "lat,lon"  
- `UTC` or `Timestamp UTC`

**Optional:**
- `Altitude` (feet)
- `Speed` (knots)
- `Direction` (degrees)
- `Callsign` (aircraft ID)

**Example:**
```csv
Timestamp UTC,Callsign,Position,Altitude,Speed,Direction
2026-01-15T14:30:00Z,N503SP,"42.1900,-71.1720",0,0,0
2026-01-15T14:31:00Z,N503SP,"42.1950,-71.1680",500,80,45
```

See `examples/sample_flight.csv` for a complete example.

---

## 📚 Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed installation options
- **[User Guide](docs/USER_GUIDE.md)** - How to use the GUI
- **[API Reference](docs/API.md)** - Python API documentation
- **[Examples](examples/)** - Sample files and usage examples

---

## 🛠️ Project Structure

```
flight-track-viewer/
├── README.md                    # You are here
├── flight_track_viewer.py       # GUI application
├── pyproject.toml              # Package configuration
├── scripts/                    # Installation scripts
│   ├── setup_with_ui.bat       # GUI setup (Windows)
│   ├── setup_with_ui.sh        # GUI setup (Mac/Linux)
│   ├── setup_core.bat          # Core setup (Windows)
│   └── setup_core.sh           # Core setup (Mac/Linux)
├── docs/                       # Documentation
│   ├── INSTALLATION.md         # Installation guide
│   ├── USER_GUIDE.md           # GUI user guide
│   └── API.md                  # API documentation
├── examples/                   # Examples & sample data
│   ├── sample_flight.csv       # Test CSV file
│   └── example_usage.py        # API examples
└── src/ftv/                    # Core package
    ├── run.py                  # Main entry point
    ├── data/                   # Data processing
    ├── analysis/               # Flight analysis
    ├── plotting/               # Visualization
    └── io/                     # File operations
```

---

## 💡 Use Cases

- **Flight Training** - Review student flights and maneuvers
- **Personal Flying** - Analyze your flight patterns
- **Flight Schools** - Create reports and documentation  
- **Aviation Enthusiasts** - Visualize interesting flights

---

## 🤝 Contributing

Contributions welcome! Please feel free to:
- Report bugs via [GitHub Issues](https://github.com/yourusername/flight-track-viewer/issues)
- Suggest features
- Submit pull requests

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

**For visualization and educational purposes only.**  
Not approved for navigation or flight safety use.

---

## 🙏 Acknowledgments

Built with Python, NumPy, Pandas, Matplotlib, and PyQt6.

---

**Happy Flying!** ✈️

*For detailed documentation, see the [docs](docs/) folder.*
