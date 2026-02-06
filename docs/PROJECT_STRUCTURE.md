# Flight Track Viewer - Project Structure

## Complete Directory Layout

```
flight-track-viewer/
│
├── backend/                          # Python FastAPI Backend
│   ├── main.py                       # Main FastAPI application
│   │   ├── /api/analyze-flight      # CSV processing endpoint
│   │   ├── /health                  # Health check endpoint
│   │   └── Flight calculations:
│   │       ├── Heading calculation (bearing between points)
│   │       ├── Distance calculation (Haversine formula)
│   │       └── Time-series analysis
│   └── requirements.txt              # Python dependencies
│
├── main.js                           # Electron Main Process
│   ├── Window management
│   ├── Python subprocess management
│   ├── IPC handlers:
│   │   ├── select-csv-file          # File dialog
│   │   ├── save-image               # Image export
│   │   └── get-backend-url          # Backend URL
│   └── Lifecycle management
│
├── renderer.js                       # Frontend Logic (Renderer Process)
│   ├── Map initialization (Leaflet)
│   ├── Animation engine:
│   │   ├── Play/Pause controls
│   │   ├── Speed multipliers
│   │   ├── Progress tracking
│   │   └── Aircraft marker rotation
│   ├── Chart creation (Chart.js):
│   │   ├── Altitude chart
│   │   ├── Speed chart
│   │   └── Distance chart
│   ├── Backend communication (Axios)
│   └── Image export functionality
│
├── index.html                        # Main UI Layout
│   ├── Header (file controls)
│   ├── Left panel:
│   │   ├── Map container
│   │   ├── Animation controls
│   │   └── Flight information
│   ├── Right panel:
│   │   ├── Altitude chart
│   │   ├── Speed chart
│   │   └── Distance chart button
│   └── Distance modal
│
├── styles.css                        # Application Styling
│   ├── Dark theme
│   ├── Responsive layout
│   ├── Control panels
│   ├── Chart containers
│   └── Modal styles
│
├── package.json                      # Node.js Configuration
│   ├── Dependencies
│   ├── Build scripts
│   └── Electron-builder config
│
├── sample_flight.csv                 # Test Data
│   └── FlightRadar24 CSV format
│
├── README.md                         # Main Documentation
├── QUICKSTART.md                     # Setup Guide
└── .gitignore                        # Git ignore rules

```

## Component Interactions

### Data Flow

1. **CSV Upload**
   ```
   User → Browse Button → IPC Handler → File Dialog → File Path
   ```

2. **Processing**
   ```
   File → FormData → Axios POST → FastAPI Backend → Pandas Processing
   → Calculations → JSON Response → Frontend State Update
   ```

3. **Visualization**
   ```
   Flight Data → Leaflet Map (Path + Marker)
                → Chart.js (3 Charts)
                → Flight Info Display
   ```

4. **Animation**
   ```
   requestAnimationFrame → Update Point Index → Move Marker
   → Rotate Icon → Update Progress → Repeat
   ```

## Key Technologies

### Frontend Stack
- **Electron** - Desktop app framework
- **Leaflet.js** - Interactive maps
- **Chart.js** - Data visualization
- **Vanilla JavaScript** - No heavy frameworks for simplicity

### Backend Stack
- **FastAPI** - Modern Python web framework
- **Pandas** - CSV parsing and data manipulation
- **NumPy** - Numerical calculations

### Communication
- **IPC** (Inter-Process Communication) - Electron main ↔ renderer
- **HTTP/JSON** - Frontend ↔ Backend API
- **Axios** - HTTP client library

## State Management

### Global State (renderer.js)
```javascript
{
  flightData: null,           // All flight point data
  map: null,                  // Leaflet map instance
  flightPath: null,           // Polyline layer
  aircraftMarker: null,       // Marker with rotation
  currentPointIndex: 0,       // Animation position
  isPlaying: false,           // Animation state
  animationSpeed: 1,          // Speed multiplier
  charts: {                   // Chart.js instances
    altitude: null,
    speed: null,
    distance: null
  }
}
```

## API Specification

### POST /api/analyze-flight

**Request:**
- Content-Type: multipart/form-data
- Body: CSV file

**Response:**
```json
{
  "success": true,
  "data": {
    "flightPoints": [
      {
        "timestamp": 1768060778,
        "utc": "2026-01-10T15:59:38Z",
        "callsign": "N503SP",
        "latitude": 42.187042,
        "longitude": -71.176376,
        "altitude": 0,
        "speed": 0,
        "heading": 61.0,
        "distanceFromStart": 0.0,
        "relativeTime": 0.0
      }
    ],
    "statistics": {
      "totalPoints": 1212,
      "callsign": "N503SP",
      "maxAltitude": 3575,
      "maxSpeed": 128,
      "totalDistance": 45230.5,
      "duration": 3600.0,
      "startTime": "2026-01-10T15:59:38Z",
      "endTime": "2026-01-10T16:59:38Z",
      "bounds": {
        "north": 42.2,
        "south": 42.1,
        "east": -71.1,
        "west": -71.2
      }
    },
    "plots": {
      "altitude": {
        "x": [0, 1, 2, ...],
        "y": [0, 100, 200, ...],
        "label": "Altitude (ft)"
      },
      "speed": { ... },
      "distance": { ... }
    }
  }
}
```

## Calculation Algorithms

### Heading (Bearing) Calculation
```python
def calculate_heading(lat1, lon1, lat2, lon2):
    # Convert to radians
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    lon_diff = radians(lon2 - lon1)
    
    # Calculate bearing
    x = sin(lon_diff) * cos(lat2_rad)
    y = cos(lat1_rad) * sin(lat2_rad) - 
        sin(lat1_rad) * cos(lat2_rad) * cos(lon_diff)
    
    heading = atan2(x, y)
    heading = degrees(heading)
    heading = (heading + 360) % 360  # Normalize to 0-360
    
    return heading
```

### Distance Calculation (Haversine)
```python
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth's radius in meters
    
    # Convert to radians
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    
    # Haversine formula
    a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    distance = R * c  # Distance in meters
    return distance
```

## Performance Considerations

### Map Rendering
- Uses canvas-based tile rendering (Leaflet default)
- Marker rotation via CSS transform (hardware accelerated)
- Progressive path rendering for smooth animation

### Chart Rendering
- Point radius set to 0 for datasets >100 points
- Line tension for smooth curves
- Responsive canvas sizing

### Animation
- RequestAnimationFrame for 60 FPS
- Integer index interpolation for smooth movement
- Cancellable animation frames

### Data Loading
- Async/await for non-blocking operations
- Loading overlay during processing
- Progress feedback to user

## Build Configuration

### Electron Builder Settings
```json
{
  "appId": "com.flighttrack.viewer",
  "productName": "Flight Track Viewer",
  "files": [
    "**/*",
    "!**/{.git,node_modules,dist,backend}/*"
  ],
  "win": { "target": "nsis" },
  "mac": { "target": "dmg" },
  "linux": { "target": "AppImage" }
}
```

## Future Enhancements

### Planned Features
1. Video export (record animation)
2. Multiple flight overlay
3. 3D terrain visualization
4. GPX/KML import/export
5. Real-time tracking integration
6. Weather data overlay
7. Airport database integration
8. Flight plan validation

### Code Optimization Opportunities
1. Web Workers for heavy calculations
2. Virtual scrolling for large datasets
3. Canvas-based chart rendering for >10k points
4. IndexedDB for local flight history
5. Streaming CSV parsing for large files

---

**Version:** 1.0.0
**Last Updated:** 2026-02-05
