# User Guide - Flight Track Viewer GUI

Complete guide to using the Flight Track Viewer graphical interface.

---

## 🚀 Launching the Application

After installation with `setup_with_ui`, you can launch the app:

**Windows:**
```batch
python flight_track_viewer.py
```

**Mac/Linux:**
```bash
python3 flight_track_viewer.py
```

---

## 🖥️ Interface Overview

```
┌──────────────────────────────────────────────────────────────┐
│ Controls                                                     │
│ ┌──────────────────────────────────────────────────────────┐ │
│ │ CSV File: [sample_flight.csv]        [📁 Browse]        │ │
│ │ Options: ☑ Save Figures  ☑ Save Video  ☑ Live Animation│ │
│ │ [🚀 Process Flight Data]                                 │ │
│ └──────────────────────────────────────────────────────────┘ │
├───────────────────────────┬──────────────────────────────────┤
│ Flight Track Animation    │ Altitude vs Time                 │
│                           │ ┌──────────────────────────────┐ │
│ ┌───────────────────────┐ │ │                              │ │
│ │                       │ │ │   [Altitude Chart]           │ │
│ │   [Map Display with   │ │ │                              │ │
│ │    Flight Path]       │ │ └──────────────────────────────┘ │
│ │                       │ │                                  │
│ └───────────────────────┘ │ Speed vs Time                    │
│                           │ ┌──────────────────────────────┐ │
│ [▶ Play] [⏸ Pause] [⟲]   │ │   [Speed Chart]              │ │
│                           │ └──────────────────────────────┘ │
│                           │                                  │
│                           │ Flight Information               │
│                           │ ┌──────────────────────────────┐ │
│                           │ │ Callsign: N503SP             │ │
│                           │ │ Max Altitude: 10,000 ft      │ │
│                           │ │ Max Speed: 155 knots         │ │
│                           │ │ Distance: 25.3 nm            │ │
│                           │ └──────────────────────────────┘ │
└───────────────────────────┴──────────────────────────────────┘
```

---

## 📋 Step-by-Step Guide

### Step 1: Select a CSV File

1. Click the **"📁 Browse"** button
2. Navigate to your FlightRadar24 CSV export
3. Select the file
4. The filename will appear in the interface

**Quick Test:** Use `examples/sample_flight.csv` to try the application

### Step 2: Configure Options

#### ☑ Live Animation (Default: On)
- Shows real-time playback of the flight path
- Recommended for most users
- Can be disabled for faster processing of large files

#### ☑ Save Figures (Default: Off)
Saves static plots as PNG files:
- `flight_track_map.png` - Full flight path map
- `altitude_plot.png` - Altitude vs time chart
- `speed_plot.png` - Speed vs time chart

Files are saved in the same directory as your CSV.

#### ☑ Save Animation (Default: Off)
- Creates an MP4 video of the animated flight path
- Saved as `flight_animation.mp4`
- Useful for presentations or sharing

### Step 3: Process the Flight

1. Click **"🚀 Process Flight Data"**
2. Wait for the progress bar to complete
3. View results in the interface

**Processing Time:**
- Small files (<1,000 points): ~5-10 seconds
- Medium files (1,000-5,000 points): ~15-30 seconds
- Large files (>5,000 points): ~30-60 seconds

### Step 4: View Results

#### Left Panel: Flight Animation
- **Gray line:** Complete flight path
- **Blue line:** Current progress
- **Red dot:** Current aircraft position
- Updates in real-time during playback

#### Right Panel: Charts & Info

**Altitude Chart:**
- X-axis: Time (data point index)
- Y-axis: Altitude in feet
- Shows climb, cruise, and descent phases

**Speed Chart:**
- X-axis: Time (data point index)
- Y-axis: Speed in knots
- Highlights acceleration and deceleration

**Flight Information:**
- Callsign
- Total data points
- Maximum/minimum altitude
- Maximum/average speed
- Maximum distance from origin
- Takeoff/landing indices (if detected)

### Step 5: Control Animation

#### ▶ Play
- Starts the flight animation
- Changes to "⏸ Pause" during playback
- Animation loops automatically when complete

#### ⏸ Pause
- Pauses animation at current position
- Click again to resume

#### ⟲ Reset
- Returns animation to the beginning
- Stops playback if running

---

## 📊 Understanding Your Flight Data

### CSV Format Requirements

**Required Columns:**
```csv
Position, UTC (or Timestamp UTC)
```

**Optional Columns:**
```csv
Altitude, Speed, Direction, Callsign
```

**Example:**
```csv
Timestamp UTC,Callsign,Position,Altitude,Speed,Direction
2026-01-15T14:30:00Z,N503SP,"42.1900,-71.1720",0,0,0
2026-01-15T14:31:00Z,N503SP,"42.1950,-71.1680",500,80,45
```

### Data Quality Tips

**For best results:**
- ✅ Consistent time intervals
- ✅ Valid lat/lon coordinates
- ✅ Continuous data (minimal gaps)
- ✅ Reasonable altitude/speed values

**Common issues:**
- ❌ GPS signal loss (causes jumps)
- ❌ Incorrect position format
- ❌ Missing required columns
- ❌ Corrupted CSV file

---

## 💡 Tips & Tricks

### Performance Optimization

**Large Files (>10,000 points):**
1. Disable "Live Animation" during processing
2. Enable animation after processing completes
3. Use the saved MP4 video instead of live playback

**Slow Animation:**
- Reduce window size
- Close other applications
- Use faster computer/more RAM

### Best Practices

**Before Processing:**
- Preview CSV in spreadsheet software
- Check for data errors
- Verify position format

**During Processing:**
- Don't minimize the window
- Wait for progress bar to complete
- Don't interrupt the process

**After Processing:**
- Review flight statistics
- Check for anomalies in charts
- Save outputs before loading new file

### Keyboard Shortcuts

Currently not implemented, but coming soon:
- `Space` - Play/Pause
- `R` - Reset
- `Ctrl+O` - Open file
- `Ctrl+S` - Save figures

---

## 🎯 Common Workflows

### Workflow 1: Quick Flight Review
1. Browse → Select CSV
2. Process (with Live Animation on)
3. Watch animation
4. Review statistics

### Workflow 2: Professional Report
1. Browse → Select CSV
2. Enable "Save Figures" and "Save Animation"
3. Process
4. Collect PNG files and MP4 video
5. Include in presentation/report

### Workflow 3: Batch Processing
For multiple flights, use the Python API instead:
```python
from ftv import run

for csv_file in flight_files:
    run(csv_file=csv_file, save_figures=True)
```

---

## 🐛 Troubleshooting

### Animation Not Showing
**Problem:** Map is blank or not updating

**Solutions:**
1. Check CSV has valid Position data
2. Verify lat/lon format: "42.1900,-71.1720"
3. Ensure coordinates are reasonable values
4. Try the sample CSV to verify installation

### Charts Are Empty
**Problem:** Altitude or speed charts are blank

**Solutions:**
1. Check CSV has Altitude/Speed columns
2. Verify values are numeric (not text)
3. Look for missing data or NULL values

### "Processing Error" Message
**Problem:** Error during flight data processing

**Solutions:**
1. Verify CSV format matches requirements
2. Check for corrupted file (re-export from source)
3. Look at error details in status bar
4. Try with sample_flight.csv to isolate issue

### Saved Files Not Found
**Problem:** Can't find PNG or MP4 files

**Solutions:**
1. Check same directory as your CSV file
2. Verify you enabled the save options
3. Check for permission errors (write access)
4. Look in the application status messages

### Application Won't Start
**Problem:** Error when launching

**Solutions:**
1. Verify PyQt6 is installed: `pip list | grep PyQt6`
2. Reinstall UI dependencies: `pip install -e ".[ui]"`
3. Check Python version (must be 3.10 or 3.11)
4. Try running from command line to see errors

---

## 📁 Output Files

### Location
All output files are saved in the **same directory as your input CSV file**.

Example:
```
C:\Users\YourName\Documents\Flights\
├── my_flight.csv              ← Input
├── flight_track_map.png       ← Output
├── altitude_plot.png          ← Output
├── speed_plot.png             ← Output
└── flight_animation.mp4       ← Output
```

### File Descriptions

**flight_track_map.png**
- Resolution: 800x600 pixels
- Format: PNG
- Contents: Full flight path on map
- Use: Reports, presentations

**altitude_plot.png**
- Resolution: 600x300 pixels
- Format: PNG
- Contents: Altitude vs time chart
- Use: Performance analysis

**speed_plot.png**
- Resolution: 600x300 pixels
- Format: PNG
- Contents: Speed vs time chart
- Use: Performance analysis

**flight_animation.mp4**
- Format: MP4 (H.264)
- Frame rate: ~10 FPS
- Duration: Varies based on flight length
- Use: Presentations, social media

---

## 🎓 Advanced Features

### Flight Statistics

The information panel shows:

**Basic Info:**
- Callsign (if available)
- Total data points

**Altitude:**
- Maximum altitude reached
- Minimum altitude (typically ground level)

**Speed:**
- Maximum speed
- Average speed during flight

**Distance:**
- Maximum distance from origin point
- Calculated using haversine formula

**Flight Events:**
- Liftoff index (when altitude first exceeds threshold)
- Touchdown index (when altitude drops below threshold)

### Animation Details

**How It Works:**
1. Parses CSV data
2. Extracts lat/lon coordinates
3. Creates matplotlib figure
4. Updates frame-by-frame
5. Shows progress with blue line and red marker

**Customization:**
Currently fixed, but future versions may allow:
- Adjustable playback speed
- Custom color schemes
- Different map projections
- Zoom controls

---

## 📚 Next Steps

- **Learn the API:** See [API Documentation](API.md)
- **View Examples:** Check [examples folder](../examples/)
- **Report Issues:** [GitHub Issues](https://github.com/yourusername/flight-track-viewer/issues)
- **Contribute:** See project README

---

**Happy Flight Tracking!** ✈️
