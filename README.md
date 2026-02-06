# Flight Track Viewer

A desktop application for visualizing and analyzing flight trajectories from FlightRadar24 CSV data.

![Flight Track Viewer](screenshot.png)

## Features

### 🗺️ Interactive Map Visualization
- Live flight path animation with airplane marker
- Real-time heading calculations and aircraft rotation
- Zoom and pan controls
- OpenStreetMap integration via Leaflet.js

### 📊 Real-time Charts
- **Altitude vs Time** - Track elevation changes throughout the flight
- **Speed vs Time** - Monitor airspeed variations
- **Distance from Reference** - Measure distance from starting point

### 🎮 Animation Controls
- Play/Pause animation
- Speed multipliers (0.25x to 10x)
- Progress slider for scrubbing through the flight
- Reset to beginning

### 💾 Export Capabilities
- Save map view as image
- Export all charts as PNG images
- Preserve flight analysis data

## Architecture

```
Frontend (Electron + React/JavaScript)
├─ Drag & drop CSV upload
├─ Leaflet.js map (60 FPS animation)
├─ Chart.js plots
├─ Animation controls
└─ Responsive design

Backend (Python FastAPI)
├─ POST /api/analyze-flight
├─ Parse CSV (pandas)
├─ Calculate headings
├─ Flight track analysis
└─ Return complete JSON
```

## Installation

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (3.8 or higher)
- **npm** or **yarn**

### Backend Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. The backend will automatically start when you launch the Electron app.

### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Start the application:
```bash
npm start
```

For development with DevTools:
```bash
npm run dev
```

## Building for Distribution

Build executable for your platform:

```bash
npm run build
```

This creates distributable packages in the `dist/` folder:
- **Windows**: `.exe` installer
- **macOS**: `.dmg` installer
- **Linux**: `.AppImage`

## CSV File Format

The application expects FlightRadar24 CSV format with tab-separated values:

```
Timestamp	UTC	Callsign	Position	Altitude	Speed	Direction
1768060778	2026-01-10T15:59:38Z	N503SP	42.187042,-71.176376	0	0	61
1768060922	2026-01-10T16:02:02Z	N503SP	42.187256,-71.176399	0	4	334
...
```

### Required Columns:
- **Timestamp** - Unix timestamp
- **UTC** - ISO 8601 datetime string
- **Callsign** - Aircraft identifier
- **Position** - Latitude,Longitude (comma-separated)
- **Altitude** - Altitude in feet
- **Speed** - Ground speed in knots
- **Direction** - Initial heading in degrees

## Usage

1. **Load CSV File**
   - Click "Browse CSV File" button
   - Select your FlightRadar24 CSV file
   - Click "Process Flight Data"

2. **View Animation**
   - Flight path appears on map
   - Aircraft marker shows current position
   - Press Play to start animation
   - Adjust speed with speed selector

3. **Analyze Data**
   - View altitude and speed charts on the right panel
   - Click "Show Distance from Reference Point" for distance analysis
   - Check Flight Information panel for statistics

4. **Export Results**
   - Click save buttons on charts to export
   - Save map view (screenshot recommended for now)

## Customization

### Airplane Icon
Replace the `AIRPLANE_ICON` constant in `renderer.js` with your base64-encoded airplane image:

```javascript
const AIRPLANE_ICON = 'data:image/png;base64,YOUR_BASE64_IMAGE_HERE';
```

### Map Tiles
Change the tile provider in `renderer.js`:

```javascript
L.tileLayer('https://YOUR_TILE_SERVER/{z}/{x}/{y}.png', {
    attribution: 'Your attribution',
    maxZoom: 19
}).addTo(map);
```

### Color Scheme
Modify colors in `styles.css`:
- Primary color: `#3498db`
- Success color: `#27ae60`
- Background: `#1a1a1a`

## API Endpoints

### Backend API

**POST /api/analyze-flight**
- Accepts: CSV file (multipart/form-data)
- Returns: JSON with flight analysis

```json
{
  "success": true,
  "data": {
    "flightPoints": [...],
    "statistics": {
      "totalPoints": 1212,
      "callsign": "N503SP",
      "maxAltitude": 3575,
      "maxSpeed": 128,
      "totalDistance": 45230.5,
      "duration": 3600,
      ...
    },
    "plots": {
      "altitude": { "x": [...], "y": [...] },
      "speed": { "x": [...], "y": [...] },
      "distance": { "x": [...], "y": [...] }
    }
  }
}
```

**GET /health**
- Returns: Backend health status

## Technical Details

### Heading Calculation
The application calculates bearing/heading between GPS coordinates using the forward azimuth formula:

```python
θ = atan2(sin(Δλ)·cos(φ2), cos(φ1)·sin(φ2) − sin(φ1)·cos(φ2)·cos(Δλ))
```

### Distance Calculation
Haversine formula for great-circle distance:

```python
a = sin²(Δφ/2) + cos(φ1)·cos(φ2)·sin²(Δλ/2)
c = 2·atan2(√a, √(1−a))
d = R·c
```

### Performance
- Map rendering: 60 FPS via Leaflet.js
- Animation: RequestAnimationFrame for smooth updates
- Chart rendering: Chart.js with optimized datasets (pointRadius: 0 for large datasets)

## Troubleshooting

### Backend Connection Issues
- Ensure Python 3.8+ is installed
- Check if port 8000 is available
- Restart the application

### CSV Parsing Errors
- Verify CSV has tab-separated values
- Check for required columns
- Ensure Position format is "latitude,longitude"

### Animation Not Smooth
- Reduce animation speed multiplier
- Close other applications
- Check system resources

## Dependencies

### Frontend
- Electron 28.0.0
- Leaflet.js 1.9.4
- Chart.js 4.4.1
- Axios 1.6.2

### Backend
- FastAPI 0.109.0
- Uvicorn 0.27.0
- Pandas 2.1.4
- NumPy 1.26.3

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For issues or questions:
- Open an issue on GitHub
- Check the documentation
- Review closed issues for similar problems

## Roadmap

- [ ] Video export of flight animation
- [ ] Multiple flight comparison
- [ ] 3D visualization option
- [ ] GPX/KML file support
- [ ] Real-time flight tracking integration
- [ ] Weather overlay
- [ ] Airports and airspace database

---

**Made with ✈️ by Flight Track Viewer Team**
