# 🚀 Flight Track Viewer - Complete Setup Instructions

## What You've Got

A complete desktop application for visualizing flight trajectories with:

✅ **Python FastAPI Backend** - Processes CSV files, calculates headings & distances
✅ **Electron Desktop App** - Beautiful UI with map, charts, and animations
✅ **Real-time Animation** - Watch flights replay with adjustable speed
✅ **Interactive Charts** - Altitude, Speed, and Distance visualizations
✅ **Export Features** - Save maps and charts as images

## 📁 Project Structure

```
flight-track-viewer/
├── backend/
│   ├── main.py              ← Python FastAPI server
│   └── requirements.txt      ← Python dependencies
├── main.js                   ← Electron main process
├── renderer.js               ← Frontend logic
├── index.html                ← UI layout
├── styles.css                ← Styling
├── package.json              ← Node.js config
├── sample_flight.csv         ← Test data
├── README.md                 ← Main docs
├── QUICKSTART.md             ← Quick setup guide
├── PROJECT_STRUCTURE.md      ← Technical details
├── DEPLOYMENT.md             ← Build & distribute
└── .gitignore                ← Git ignore rules
```

## 🏃 Quick Start (5 Minutes)

### Step 1: Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
cd ..
```

**Frontend:**
```bash
npm install
```

### Step 2: Run the App

```bash
npm start
```

The app will:
1. Start Python backend (port 8000)
2. Launch Electron window
3. Be ready to use in ~3 seconds

### Step 3: Test with Sample Data

1. Click **"Browse CSV File"**
2. Select `sample_flight.csv`
3. Click **"Process Flight Data"**
4. Watch the magic happen! ✨

## 🎨 Customization

### Replace Airplane Icon

In `renderer.js`, find this line:
```javascript
const AIRPLANE_ICON = 'data:image/png;base64,...';
```

Replace with your own base64-encoded airplane image.

**How to get base64:**
```bash
# Linux/Mac
base64 -i your-airplane.png

# Windows (PowerShell)
[convert]::ToBase64String((Get-Content -Path "your-airplane.png" -Encoding Byte))
```

### Change Colors

Edit `styles.css`:
- Primary blue: `#3498db`
- Success green: `#27ae60`
- Dark background: `#1a1a1a`

### Customize Map Tiles

In `renderer.js`, change the tile server:
```javascript
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);
```

Try these alternatives:
- **Satellite**: Mapbox, ESRI
- **Dark Mode**: CartoDB Dark Matter
- **Terrain**: OpenTopoMap

## 📊 CSV Format

Your FlightRadar24 CSV should look like this (tab-separated):

```
Timestamp	UTC	Callsign	Position	Altitude	Speed	Direction
1768060778	2026-01-10T15:59:38Z	N503SP	42.187,-71.176	0	0	61
```

**Required Columns:**
- `Timestamp` - Unix timestamp
- `UTC` - ISO 8601 datetime
- `Callsign` - Aircraft identifier
- `Position` - Latitude,Longitude (comma-separated)
- `Altitude` - Feet
- `Speed` - Knots
- `Direction` - Degrees (0-360)

## 🛠️ Development

### Run with DevTools
```bash
npm run dev
```

### Build for Distribution
```bash
npm run build
```

Creates installer in `dist/`:
- Windows: `.exe`
- macOS: `.dmg`
- Linux: `.AppImage`

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check Python version (needs 3.8+)
python --version

# Reinstall dependencies
cd backend
pip install -r requirements.txt --upgrade
```

### Port 8000 Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Animation is Laggy
- Lower speed multiplier
- Close other applications
- Check system resources

## 📚 Documentation

- **README.md** - Comprehensive guide
- **QUICKSTART.md** - Fast setup
- **PROJECT_STRUCTURE.md** - Architecture details
- **DEPLOYMENT.md** - Build & distribute

## 🎯 Key Features

### Map Visualization
- ✅ Interactive Leaflet.js map
- ✅ Flight path overlay
- ✅ Rotating airplane marker
- ✅ Zoom and pan controls
- ✅ Progress path highlighting

### Charts
- ✅ Altitude vs Time
- ✅ Speed vs Time
- ✅ Distance from Reference Point
- ✅ Export as PNG images

### Animation
- ✅ Play/Pause controls
- ✅ Speed: 0.25x to 10x
- ✅ Progress slider
- ✅ Reset to start

### Data Export
- ✅ Save charts as images
- ✅ Flight statistics display
- ✅ Duration and distance metrics

## 🔮 Future Ideas

Want to contribute? Here are some ideas:
- [ ] Video export of animation
- [ ] 3D visualization mode
- [ ] Multiple flight comparison
- [ ] GPX/KML file support
- [ ] Weather overlay
- [ ] Airport database
- [ ] Real-time tracking

## 🤝 Need Help?

1. Check the documentation files
2. Look at sample_flight.csv for format reference
3. Review console for error messages
4. Make sure Python and Node.js are installed

## 🎉 You're Ready!

Everything is set up and ready to go. Just run:

```bash
npm start
```

And start exploring flight tracks! ✈️

---

**Enjoy your Flight Track Viewer!**

*Built with Python FastAPI + Electron + Leaflet.js + Chart.js*
