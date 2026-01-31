# Quick Start Guide - Flight Track Viewer UI

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies

Run one of the installation scripts:

**Windows:**
```batch
install_ui.bat
```

**Mac/Linux:**
```bash
chmod +x install_ui.sh
./install_ui.sh
```

**Or manually:**
```bash
pip install PyQt6>=6.6.0
```

### Step 2: Run the Application

```bash
python flight_track_viewer.py
```

### Step 3: Load Your Flight Data

1. Click "📁 Browse" button
2. Select your CSV file (or use `sample_flight.csv` for testing)
3. Check desired options:
   - ✅ Live Animation (recommended)
   - ✅ Save Figures (PNG)
   - ✅ Save Animation (MP4)
4. Click "🚀 Process Flight Data"

## 📋 What You'll See

- **Left Panel**: Animated flight path on a map
  - Use Play/Pause to control animation
  - Reset button to start over

- **Right Panel**: 
  - Altitude vs Time chart
  - Speed vs Time chart
  - Flight statistics (max altitude, speed, distance, etc.)

## 🎯 Test Flight

Use the included `sample_flight.csv` to test the application:
- Simulated flight from Bedford, MA area
- Includes takeoff, cruise, and landing
- Total flight time: ~31 minutes
- Max altitude: 10,000 ft

## 💡 Tips

1. **Large Files**: For CSV files with >10,000 points, consider disabling live animation for faster processing

2. **Animation Speed**: Currently set to ~10 FPS. You can modify this in the code by changing the timer interval in `toggle_animation()`

3. **Saved Files**: Look in the same directory as your CSV for:
   - `flight_track_map.png`
   - `altitude_plot.png`
   - `speed_plot.png`
   - `flight_animation.mp4`

4. **CSV Format**: Ensure your FlightRadar24 export has:
   - `Position` column (format: "lat,lon")
   - `Timestamp UTC` or `UTC` column
   - Optional: `Altitude`, `Speed`, `Direction`, `Callsign`

## 🐛 Troubleshooting

**"ftv module not found"**
→ Install the base package: `pip install -e /path/to/flight-track-viewer-python`

**Animation not showing**
→ Verify your CSV has valid Position data in "lat,lon" format

**Slow performance**
→ Disable "Live Animation" for large files

**Qt errors on Linux**
→ Install: `sudo apt-get install libxcb-xinerama0`

## 📖 Full Documentation

See `README_UI.md` for complete documentation including:
- Detailed feature descriptions
- Architecture overview
- Advanced troubleshooting
- Integration details

---

**Enjoy analyzing your flights!** ✈️
