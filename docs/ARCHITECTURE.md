# Flight Track Viewer - Architecture & Module Documentation

## Table of Contents
- [Overview](#overview)
- [Frontend Architecture](#frontend-architecture)
- [Backend Architecture](#backend-architecture)
- [Module API Reference](#module-api-reference)
- [Data Flow](#data-flow)
- [Dependencies](#dependencies)

## Overview

The Flight Track Viewer follows a modular, separation-of-concerns architecture:

```
┌─────────────────────────────────────────┐
│         Electron Main Process           │
│  ┌──────────────────────────────────┐  │
│  │   Python Backend (FastAPI)       │  │
│  │   - CSV Processing               │  │
│  │   - Flight Calculations          │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
                    │ HTTP/JSON API
                    ▼
┌─────────────────────────────────────────┐
│      Electron Renderer Process          │
│  ┌──────────────────────────────────┐  │
│  │   app.js (Coordinator)           │  │
│  │   ├── MapManager                 │  │
│  │   ├── ChartManager               │  │
│  │   └── AnimationController        │  │
│  └──────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Frontend Architecture

### Module Hierarchy

```
app.js (Main Controller)
  ├── MapManager
  │   ├── Leaflet Map Instance
  │   ├── Flight Path Polyline
  │   └── Aircraft Marker
  │
  ├── ChartManager
  │   ├── Altitude Chart (Chart.js)
  │   ├── Speed Chart (Chart.js)
  │   └── Distance Chart (Chart.js)
  │
  └── AnimationController
      ├── Animation State
      ├── Frame Management
      └── Position Updates
```

### Frontend Modules

#### 1. **app.js** - Main Application Controller

**Responsibilities:**
- Application initialization
- Backend communication
- Event handler setup
- Component coordination
- File I/O operations

**Key Methods:**
```javascript
class FlightTrackApp {
  initialize()              // Setup app and check backend
  browseFile()              // File selection dialog
  processFile()             // Send CSV to backend
  initializeVisualization() // Setup map, charts, animation
  togglePlayPause()         // Control animation
  saveMapImage()            // Export map screenshot
  saveChartImage(type)      // Export chart image
}
```

**Dependencies:**
- MapManager
- ChartManager
- AnimationController
- Electron IPC
- Axios

---

#### 2. **map-manager.js** - Map Visualization

**Responsibilities:**
- Leaflet map initialization
- Flight path rendering
- Aircraft marker management
- Map layer control

**Key Methods:**
```javascript
class MapManager {
  initialize()                              // Create Leaflet map
  createFlightPath(coordinates)             // Draw flight path
  createAircraftMarker(lat, lon, heading)   // Add aircraft
  updateAircraftPosition(lat, lon, heading) // Move aircraft
  updateProgressPath(fullPath, index)       // Show progress
  clear()                                   // Remove all layers
}
```

**Dependencies:**
- Leaflet.js
- Leaflet-rotatedmarker

**Configuration:**
- Tile Server: OpenStreetMap
- Default View: [42.187, -71.176], zoom 13
- Marker Size: 32x32px
- Path Colors: Blue (#3498db) for active, Gray (#34495e) for inactive

---

#### 3. **chart-manager.js** - Data Visualization

**Responsibilities:**
- Chart.js configuration
- Chart creation and updates
- Chart export functionality

**Key Methods:**
```javascript
class ChartManager {
  createAltitudeChart(xData, yData)  // Altitude vs Time
  createSpeedChart(xData, yData)     // Speed vs Time
  createDistanceChart(xData, yData)  // Distance vs Time
  getChart(type)                     // Get chart instance
  destroyAll()                       // Cleanup all charts
}
```

**Dependencies:**
- Chart.js

**Chart Configuration:**
- Type: Line charts
- Tension: 0.4 (smooth curves)
- Point Radius: 0 (for performance)
- Colors: Blue (altitude), Green (speed), Red (distance)

---

#### 4. **animation-controller.js** - Animation Logic

**Responsibilities:**
- Animation state management
- Frame-by-frame updates
- Speed control
- Progress tracking

**Key Methods:**
```javascript
class AnimationController {
  setFlightData(data)       // Load flight data
  play()                    // Start animation
  pause()                   // Pause animation
  reset()                   // Reset to start
  setSpeed(speed)           // Change speed multiplier
  seek(progress)            // Jump to position
  animate()                 // Animation loop
  updatePosition()          // Update map position
}
```

**Dependencies:**
- MapManager (for position updates)
- requestAnimationFrame

**State:**
```javascript
{
  flightData: Object,        // Complete flight data
  currentIndex: number,      // Current frame index
  isPlaying: boolean,        // Animation state
  speed: number,             // Speed multiplier (0.25-10)
  animationFrameId: number   // RAF ID for cancellation
}
```

---

## Backend Architecture

### Module Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI app & routes
│   ├── data_processor.py    # CSV processing pipeline
│   ├── flight_utils.py      # Calculation utilities
│   └── __init__.py          # Package exports
└── run.py                   # Entry point
```

### Backend Modules

#### 1. **main.py** - API Routes

**Endpoints:**
```python
GET  /              # API information
GET  /health        # Health check
POST /api/analyze-flight  # Process CSV file
```

**Dependencies:**
- FastAPI
- FlightDataProcessor

---

#### 2. **data_processor.py** - Data Processing Pipeline

**Class: FlightDataProcessor**

**Processing Pipeline:**
```
CSV Input
  ↓
detect_delimiter() → Detect comma vs tab
  ↓
parse_csv() → Load into pandas DataFrame
  ↓
validate_csv() → Check required columns
  ↓
process_positions() → Parse lat/lon
  ↓
calculate_headings() → Bearing between points
  ↓
calculate_distances() → Haversine distance
  ↓
calculate_time_series() → Relative timestamps
  ↓
generate_output() → JSON response
```

**Key Methods:**
```python
class FlightDataProcessor:
    detect_delimiter(csv_string)        # Auto-detect delimiter
    validate_csv(df)                    # Check required columns
    parse_csv(csv_content)              # Load CSV
    process_positions(df)               # Parse coordinates
    calculate_headings(df)              # Calculate bearings
    calculate_distances(df)             # Haversine formula
    calculate_time_series(df)           # Time calculations
    generate_statistics(df)             # Flight stats
    generate_plot_data(df)              # Chart data
    generate_flight_points(df)          # Point-by-point data
    process_flight_data(csv_content)    # Main pipeline
```

**Dependencies:**
- pandas
- flight_utils

---

#### 3. **flight_utils.py** - Mathematical Utilities

**Functions:**

```python
calculate_heading(lat1, lon1, lat2, lon2) -> float
```
- Uses forward azimuth formula
- Returns heading in degrees (0-360)
- Formula: `θ = atan2(sin(Δλ)·cos(φ₂), cos(φ₁)·sin(φ₂) − sin(φ₁)·cos(φ₂)·cos(Δλ))`

```python
calculate_distance(lat1, lon1, lat2, lon2) -> float
```
- Uses Haversine formula
- Returns distance in meters
- Formula: `a = sin²(Δφ/2) + cos(φ₁)·cos(φ₂)·sin²(Δλ/2); d = R·2·atan2(√a, √(1−a))`

```python
parse_position(position_str) -> tuple
```
- Parses "lat,lon" string
- Handles quoted values
- Returns (latitude, longitude) or (None, None)

**Dependencies:**
- math (standard library)

---

## Module API Reference

### Frontend Module APIs

#### MapManager

```javascript
const mapManager = new MapManager();

// Initialize map
mapManager.initialize();

// Create flight path
mapManager.createFlightPath([
  [42.187, -71.176],
  [42.188, -71.175],
  // ...
]);

// Create aircraft marker
mapManager.createAircraftMarker(42.187, -71.176, 45);

// Update position
mapManager.updateAircraftPosition(42.188, -71.175, 50);

// Update progress
mapManager.updateProgressPath(fullPath, currentIndex);

// Clear all layers
mapManager.clear();
```

#### ChartManager

```javascript
const chartManager = new ChartManager();

// Create charts
chartManager.createAltitudeChart(timeData, altitudeData);
chartManager.createSpeedChart(timeData, speedData);
chartManager.createDistanceChart(timeData, distanceData);

// Get chart instance
const altChart = chartManager.getChart('altitude');

// Export chart
const dataUrl = altChart.toBase64Image();

// Cleanup
chartManager.destroyAll();
```

#### AnimationController

```javascript
const controller = new AnimationController(
  mapManager,
  (state) => console.log(state) // Update callback
);

// Set data
controller.setFlightData(flightData);

// Control playback
controller.play();
controller.pause();
controller.reset();

// Change speed
controller.setSpeed(2); // 2x speed

// Seek to position
controller.seek(50); // 50% progress

// Get state
const state = controller.getState();
// { currentIndex, isPlaying, speed, progress }
```

### Backend API Reference

#### Endpoints

**GET /**
```json
{
  "message": "Flight Track Analyzer API",
  "status": "running",
  "version": "1.0.1",
  "endpoints": {
    "health": "/health",
    "analyze": "/api/analyze-flight"
  }
}
```

**GET /health**
```json
{
  "status": "healthy"
}
```

**POST /api/analyze-flight**

Request:
```
Content-Type: multipart/form-data
file: CSV file
```

Response:
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
      "altitude": { "x": [...], "y": [...], "label": "..." },
      "speed": { "x": [...], "y": [...], "label": "..." },
      "distance": { "x": [...], "y": [...], "label": "..." }
    }
  }
}
```

---

## Data Flow

### CSV Upload to Visualization

```
1. User clicks "Browse"
   ↓
2. File selected via Electron dialog
   ↓
3. User clicks "Process"
   ↓
4. app.js reads file → FormData
   ↓
5. HTTP POST to backend
   ↓
6. Backend processes CSV:
   - Parse & validate
   - Calculate headings
   - Calculate distances
   - Generate statistics
   ↓
7. Backend returns JSON
   ↓
8. app.js receives data
   ↓
9. Initialize visualization:
   - MapManager.createFlightPath()
   - MapManager.createAircraftMarker()
   - ChartManager.createAltitudeChart()
   - ChartManager.createSpeedChart()
   - AnimationController.setFlightData()
   ↓
10. User controls animation
```

### Animation Frame Update

```
1. AnimationController.animate()
   ↓
2. Increment currentIndex by speed
   ↓
3. AnimationController.updatePosition()
   ↓
4. MapManager.updateAircraftPosition()
   ↓
5. MapManager.updateProgressPath()
   ↓
6. Callback to app.js with state
   ↓
7. app.js updates UI (progress bar, etc.)
   ↓
8. requestAnimationFrame() → loop back to step 1
```

---

## Dependencies

### Frontend

| Library | Version | Purpose |
|---------|---------|---------|
| Electron | 28.0.0 | Desktop application framework |
| Leaflet.js | 1.9.4 | Interactive maps |
| Chart.js | 4.4.1 | Data visualization charts |
| html2canvas | 1.4.1 | Map screenshot capture |
| Axios | 1.6.2 | HTTP client |
| leaflet-rotatedmarker | 0.2.0 | Rotated marker support |

### Backend

| Library | Version | Purpose |
|---------|---------|---------|
| FastAPI | 0.100+ | Web framework |
| Uvicorn | 0.23+ | ASGI server |
| Pandas | 2.0+ | Data processing |
| NumPy | 1.24+ | Numerical computations |
| python-multipart | 0.0.6+ | File upload handling |

---

## Performance Considerations

### Frontend Optimization

- **Chart Rendering**: Point radius set to 0 for large datasets
- **Animation**: requestAnimationFrame for 60 FPS
- **Map Tiles**: Canvas-based rendering (Leaflet default)
- **Memory**: Cleanup on component destruction

### Backend Optimization

- **CSV Parsing**: Pandas for efficient processing
- **Calculations**: NumPy vectorization where possible
- **API**: Async/await for non-blocking operations

---

## Testing

### Frontend Module Testing

```javascript
// Test MapManager
const map = new MapManager();
map.initialize();
console.assert(map.getMap() instanceof L.Map);

// Test ChartManager
const charts = new ChartManager();
charts.createAltitudeChart([0,1,2], [0,100,200]);
console.assert(charts.getChart('altitude') instanceof Chart);
```

### Backend Module Testing

```python
# Test flight_utils
from backend.src.flight_utils import calculate_heading

heading = calculate_heading(42.0, -71.0, 42.1, -71.0)
assert 0 <= heading <= 360

# Test data_processor
from backend.src.data_processor import FlightDataProcessor

processor = FlightDataProcessor()
# ... test processing pipeline
```

---

**Version:** 1.0.1
**Last Updated:** 2026-02-06