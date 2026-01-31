# Flight Track Viewer - Graphical User Interface

A modern, user-friendly GUI for the Flight Track Viewer Python toolkit. This interface makes it easy to visualize and analyze flight tracks from CSV data exported from FlightRadar24.

## Features

✨ **Modern GUI Interface**
- Clean, intuitive design with PyQt6
- Real-time flight track animation
- Interactive controls for playback

📊 **Comprehensive Visualization**
- Live animated flight path on map
- Altitude vs Time plot
- Speed vs Time plot
- Flight statistics and information panel

⚙️ **Flexible Options**
- Browse and select CSV files easily
- Toggle animation on/off
- Optional PNG figure export
- Optional MP4 video export
- Play/Pause/Reset animation controls

## Installation

### Prerequisites

- Python 3.10 or 3.11 (recommended)
- The `ftv` (Flight Track Viewer) package installed
- Git (optional)

### Step 1: Install the Flight Track Viewer Package

First, make sure you have the base `ftv` package installed:

```bash
cd /path/to/flight-track-viewer-python
pip install -e .
```

### Step 2: Install UI Dependencies

Install the additional dependencies required for the GUI:

```bash
pip install -r requirements_ui.txt
```

Or install manually:

```bash
pip install PyQt6>=6.6.0
```

## Usage

### Running the Application

Simply run the Python script:

```bash
python flight_track_viewer.py
```

### Using the Interface

1. **Select a CSV File**
   - Click the "📁 Browse" button
   - Navigate to your FlightRadar24 CSV export file
   - Select the file

2. **Configure Options** (Optional)
   - ✅ **Live Animation**: Check to enable real-time playback (enabled by default)
   - ✅ **Save Figures (PNG)**: Check to save static plots as PNG files
   - ✅ **Save Animation (MP4)**: Check to export the animation as an MP4 video

3. **Process the Flight Data**
   - Click the "🚀 Process Flight Data" button
   - Wait for processing to complete (progress bar will show status)

4. **View Results**
   - **Left Panel**: Animated flight track with play/pause controls
   - **Right Panel**: 
     - Altitude vs Time plot
     - Speed vs Time plot
     - Flight information summary

5. **Animation Controls**
   - ▶ **Play/Pause**: Start or pause the flight animation
   - ⟲ **Reset**: Reset animation to the beginning

## Screenshots

### Main Interface
```
┌─────────────────────────────────────────────────────────────┐
│  Controls                                                   │
│  CSV File: [your_flight.csv]              [📁 Browse]      │
│  Options: ☑ Save Figures  ☑ Save Video  ☑ Live Animation │
│  [🚀 Process Flight Data]                                  │
├──────────────────────┬──────────────────────────────────────┤
│ Flight Track         │ Altitude vs Time                     │
│ Animation            │ [Altitude Plot]                      │
│                      │                                      │
│ [Map Display]        │ Speed vs Time                        │
│                      │ [Speed Plot]                         │
│ [▶ Play] [⟲ Reset]  │                                      │
│                      │ Flight Information                   │
│                      │ [Statistics & Details]               │
└──────────────────────┴──────────────────────────────────────┘
```

## CSV File Format

The application expects CSV files in the FlightRadar24 export format:

### Required Columns
- `Position` – format: "lat,lon"
- `UTC` or `Timestamp UTC`

### Optional Columns
- `Altitude` (in feet)
- `Speed` (in knots)
- `Direction` (heading)
- `Callsign` (aircraft identifier)

### Example CSV
```csv
Timestamp UTC,Callsign,Position,Altitude,Speed,Direction
2026-01-15T14:30:00Z,N503SP,"42.1900,-71.1720",0,0,0
2026-01-15T14:31:00Z,N503SP,"42.1950,-71.1680",500,80,45
2026-01-15T14:32:00Z,N503SP,"42.2000,-71.1640",1000,95,45
```

## Output Files

When enabled, the application saves files to the same directory as your CSV:

- **PNG Figures**: 
  - `flight_track_map.png`
  - `altitude_plot.png`
  - `speed_plot.png`

- **MP4 Video**:
  - `flight_animation.mp4`

## Troubleshooting

### "ftv module not found"
Make sure you've installed the base Flight Track Viewer package:
```bash
cd /path/to/flight-track-viewer-python
pip install -e .
```

### Animation not displaying
- Ensure your CSV file has valid Position data
- Check that the file format matches the expected structure
- Verify latitude/longitude values are valid

### "Qt platform plugin could not be initialized"
This usually happens on Linux systems. Install the required Qt dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install libxcb-xinerama0

# Or use a different Qt platform
export QT_QPA_PLATFORM=xcb
```

### Slow performance
- For large CSV files (>10,000 points), consider:
  - Disabling live animation
  - Reducing animation frame rate
  - Using data downsampling

## Technical Details

### Architecture
- **GUI Framework**: PyQt6 (cross-platform)
- **Plotting**: Matplotlib with Qt5Agg backend
- **Data Processing**: Pandas, NumPy
- **Threading**: QThread for non-blocking processing

### Performance
- Background processing prevents UI freezing
- Efficient matplotlib canvas updates
- Configurable animation frame rate

## Integration with ftv Package

This UI is designed to work seamlessly with your existing `ftv` package:

```python
from ftv import run

# The UI essentially calls:
result = run(
    csv_file="path/to/file.csv",
    animate=True,
    save_figures=True,
    save_video=True
)
```

All the core functionality from your original package is preserved.

## License

This UI follows the same MIT License as the Flight Track Viewer package.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## Acknowledgments

- Built on top of the excellent Flight Track Viewer Python toolkit
- Uses PyQt6 for cross-platform GUI
- Matplotlib for scientific visualization

---

**Happy Flying!** ✈️

For issues or questions, please refer to the main Flight Track Viewer repository.
