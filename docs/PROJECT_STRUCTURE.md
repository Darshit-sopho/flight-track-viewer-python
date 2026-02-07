# Flight Track Viewer - Detailed Project Structure

## Complete Directory Layout with Descriptions

```markdown
flight-track-viewer/
│
├── frontend/                         # Frontend Application (Electron Renderer)
│   │
│   ├── index.html                    # Main UI Layout
│   │   ├── Header section:
│   │   │   ├── App title
│   │   │   ├── Browse CSV button
│   │   │   ├── File name display
│   │   │   └── Process button
│   │   ├── Left panel:
│   │   │   ├── Map container (Leaflet)
│   │   │   ├── Animation controls:
│   │   │   │   ├── Play/Pause button
│   │   │   │   ├── Reset button
│   │   │   │   ├── Progress slider
│   │   │   │   ├── Speed selector
│   │   │   │   └── Save map button
│   │   │   └── Flight information panel
│   │   ├── Right panel:
│   │   │   ├── Altitude chart container
│   │   │   ├── Speed chart container
│   │   │   └── Distance chart button
│   │   └── Distance modal (popup)
│   │
│   ├── src/                          # Frontend Source Code
│   │   │
│   │   ├── js/                       # JavaScript Modules
│   │   │   │
│   │   │   ├── app.js                # Main Application Controller
│   │   │   │   ├── Application initialization
│   │   │   │   ├── Backend health check
│   │   │   │   ├── Component coordination:
│   │   │   │   │   ├── MapManager integration
│   │   │   │   │   ├── ChartManager integration
│   │   │   │   │   └── AnimationController integration
│   │   │   │   ├── Event handler setup:
│   │   │   │   │   ├── File selection (browseFile)
│   │   │   │   │   ├── CSV processing (processFile)
│   │   │   │   │   ├── Animation controls
│   │   │   │   │   └── Save operations
│   │   │   │   ├── Backend communication (Axios):
│   │   │   │   │   └── POST /api/analyze-flight
│   │   │   │   ├── Visualization initialization
│   │   │   │   ├── Flight info display
│   │   │   │   └── Image export handlers
│   │   │   │
│   │   │   ├── map-manager.js        # Map Visualization Module
│   │   │   │   ├── Leaflet map initialization
│   │   │   │   ├── Tile layer setup (OpenStreetMap)
│   │   │   │   ├── Flight path rendering:
│   │   │   │   │   ├── createFlightPath()
│   │   │   │   │   └── Full polyline display
│   │   │   │   ├── Aircraft marker management:
│   │   │   │   │   ├── createAircraftMarker()
│   │   │   │   │   ├── updateAircraftPosition()
│   │   │   │   │   └── Rotation based on heading
│   │   │   │   ├── Progress path visualization:
│   │   │   │   │   ├── updateProgressPath()
│   │   │   │   │   ├── Gray path (未traveled)
│   │   │   │   │   └── Blue path (traveled)
│   │   │   │   ├── Map layer control
│   │   │   │   ├── Bounds fitting
│   │   │   │   └── Window resize handling
│   │   │   │
│   │   │   ├── chart-manager.js      # Chart Visualization Module
│   │   │   │   ├── Chart.js configuration
│   │   │   │   ├── Common chart options:
│   │   │   │   │   ├── Dark theme colors
│   │   │   │   │   ├── Grid styling
│   │   │   │   │   ├── Tooltip configuration
│   │   │   │   │   └── Axis setup
│   │   │   │   ├── Chart creation methods:
│   │   │   │   │   ├── createAltitudeChart()
│   │   │   │   │   │   ├── Line chart, blue color
│   │   │   │   │   │   ├── Y-axis: Altitude (ft)
│   │   │   │   │   │   └── X-axis: Time (seconds)
│   │   │   │   │   ├── createSpeedChart()
│   │   │   │   │   │   ├── Line chart, green color
│   │   │   │   │   │   ├── Y-axis: Speed (kts)
│   │   │   │   │   │   └── X-axis: Time (seconds)
│   │   │   │   │   └── createDistanceChart()
│   │   │   │   │       ├── Line chart, red color
│   │   │   │   │       ├── Y-axis: Distance (m)
│   │   │   │   │       └── X-axis: Time (seconds)
│   │   │   │   ├── Chart instance management
│   │   │   │   ├── getChart() accessor
│   │   │   │   └── destroyAll() cleanup
│   │   │   │
│   │   │   └── animation-controller.js # Animation Logic Module
│   │   │       ├── Animation state management:
│   │   │       │   ├── currentIndex tracking
│   │   │       │   ├── isPlaying state
│   │   │       │   ├── speed multiplier
│   │   │       │   └── animationFrameId
│   │   │       ├── Playback controls:
│   │   │       │   ├── play() - Start animation
│   │   │       │   ├── pause() - Pause animation
│   │   │       │   ├── reset() - Reset to start
│   │   │       │   ├── setSpeed() - Change speed (0.25x-10x)
│   │   │       │   └── seek() - Jump to position
│   │   │       ├── Animation loop:
│   │   │       │   ├── animate() - Main loop
│   │   │       │   ├── requestAnimationFrame
│   │   │       │   ├── Frame increment by speed
│   │   │       │   └── Position update trigger
│   │   │       ├── Position updates:
│   │   │       │   ├── updatePosition()
│   │   │       │   ├── MapManager integration
│   │   │       │   └── Progress path update
│   │   │       ├── Callback system:
│   │   │       │   └── onUpdate(state) to app.js
│   │   │       └── State accessor (getState)
│   │   │
│   │   └── css/                      # Stylesheets
│   │       └── styles.css            # Application Styling
│   │           ├── Global styles:
│   │           │   ├── CSS reset
│   │           │   ├── Dark theme (#1a1a1a)
│   │           │   └── Font family
│   │           ├── Header styles:
│   │           │   ├── Gradient background
│   │           │   ├── File controls layout
│   │           │   └── Button positioning
│   │           ├── Layout styles:
│   │           │   ├── Main content flex
│   │           │   ├── Left panel (60%)
│   │           │   └── Right panel (38%)
│   │           ├── Map container:
│   │           │   ├── Relative positioning
│   │           │   ├── Loading overlay
│   │           │   └── Border radius
│   │           ├── Control panels:
│   │           │   ├── Map controls bar
│   │           │   ├── Slider styling
│   │           │   └── Button groups
│   │           ├── Flight info display:
│   │           │   ├── Info grid layout
│   │           │   └── Statistics styling
│   │           ├── Chart containers:
│   │           │   ├── Chart background
│   │           │   ├── Chart headers
│   │           │   └── Canvas max-height
│   │           ├── Button styles:
│   │           │   ├── Primary (blue)
│   │           │   ├── Secondary (gray)
│   │           │   ├── Success (green)
│   │           │   ├── Hover effects
│   │           │   └── Disabled states
│   │           ├── Modal styles:
│   │           │   ├── Overlay background
│   │           │   ├── Modal content box
│   │           │   ├── Animations (fadeIn, slideIn)
│   │           │   └── Close button
│   │           └── Responsive design:
│   │               ├── Media queries
│   │               └── Mobile adaptations
│   │
│   └── public/                       # Static Assets (empty for now)
│       └── (Place icons, images here)
│
├── backend/                          # Python FastAPI Backend
│   │
│   ├── src/                          # Backend Source Code
│   │   │
│   │   ├── main.py                   # FastAPI Application & Routes
│   │   │   ├── FastAPI app initialization:
│   │   │   │   ├── Title & description
│   │   │   │   ├── Version info
│   │   │   │   └── CORS middleware setup
│   │   │   ├── Route endpoints:
│   │   │   │   ├── GET / - API info
│   │   │   │   ├── GET /health - Health check
│   │   │   │   └── POST /api/analyze-flight:
│   │   │   │       ├── Accept CSV file upload
│   │   │   │       ├── Call FlightDataProcessor
│   │   │   │       ├── Return JSON response
│   │   │   │       └── Error handling
│   │   │   └── FlightDataProcessor integration
│   │   │
│   │   ├── data_processor.py         # CSV Processing Pipeline
│   │   │   ├── FlightDataProcessor class:
│   │   │   │   ├── CSV parsing:
│   │   │   │   │   ├── detect_delimiter() - Auto-detect , or \t
│   │   │   │   │   ├── parse_csv() - Load with pandas
│   │   │   │   │   └── validate_csv() - Check columns
│   │   │   │   ├── Position processing:
│   │   │   │   │   ├── process_positions()
│   │   │   │   │   ├── Parse "lat,lon" strings
│   │   │   │   │   ├── Create Latitude/Longitude columns
│   │   │   │   │   └── Remove invalid rows
│   │   │   │   ├── Calculations:
│   │   │   │   │   ├── calculate_headings()
│   │   │   │   │   │   ├── Call flight_utils.calculate_heading()
│   │   │   │   │   │   ├── Bearing between consecutive points
│   │   │   │   │   │   └── Use Direction for first point
│   │   │   │   │   ├── calculate_distances()
│   │   │   │   │   │   ├── Call flight_utils.calculate_distance()
│   │   │   │   │   │   ├── Haversine formula
│   │   │   │   │   │   └── Distance from start point
│   │   │   │   │   └── calculate_time_series()
│   │   │   │   │       ├── Relative timestamps
│   │   │   │   │       └── Time from start
│   │   │   │   ├── Output generation:
│   │   │   │   │   ├── generate_statistics()
│   │   │   │   │   │   ├── Total points, duration
│   │   │   │   │   │   ├── Max altitude, max speed
│   │   │   │   │   │   ├── Total distance
│   │   │   │   │   │   └── Bounds (N/S/E/W)
│   │   │   │   │   ├── generate_plot_data()
│   │   │   │   │   │   ├── Altitude plot (x, y, label)
│   │   │   │   │   │   ├── Speed plot
│   │   │   │   │   │   └── Distance plot
│   │   │   │   │   └── generate_flight_points()
│   │   │   │   │       └── Array of point objects
│   │   │   │   └── process_flight_data() - Main pipeline
│   │   │   └── Required columns validation
│   │   │
│   │   ├── flight_utils.py           # Calculation Utilities
│   │   │   ├── calculate_heading():
│   │   │   │   ├── Input: lat1, lon1, lat2, lon2
│   │   │   │   ├── Forward azimuth formula
│   │   │   │   ├── Convert to radians
│   │   │   │   ├── atan2 calculation
│   │   │   │   ├── Convert to degrees
│   │   │   │   └── Normalize to 0-360°
│   │   │   ├── calculate_distance():
│   │   │   │   ├── Input: lat1, lon1, lat2, lon2
│   │   │   │   ├── Haversine formula
│   │   │   │   ├── Earth radius: 6,371,000m
│   │   │   │   ├── Great-circle distance
│   │   │   │   └── Return meters
│   │   │   └── parse_position():
│   │   │       ├── Parse "lat,lon" string
│   │   │       ├── Handle quoted values
│   │   │       ├── Strip whitespace
│   │   │       └── Return (lat, lon) tuple
│   │   │
│   │   └── __init__.py               # Package Initialization
│   │       ├── Import app from main
│   │       ├── Import FlightDataProcessor
│   │       ├── Import utility functions
│   │       ├── Define __version__
│   │       └── Define __all__ exports
│   │
│   ├── run.py                        # Backend Entry Point
│   │   ├── Import uvicorn
│   │   ├── Import app from src.main
│   │   ├── Run server:
│   │   │   ├── Host: 127.0.0.1
│   │   │   ├── Port: 8000
│   │   │   └── Log level: info
│   │   └── __main__ guard
│   │
│   └── requirements.txt              # Python Dependencies
│       ├── fastapi>=0.100.0
│       ├── uvicorn[standard]>=0.23.0
│       ├── pandas>=2.0.0
│       ├── numpy>=1.24.0
│       └── python-multipart>=0.0.6
│
├── docs/                             # Documentation
│   ├── ARCHITECTURE.md               # Technical Architecture
│   │   ├── Module hierarchies
│   │   ├── API reference
│   │   ├── Data flow diagrams
│   │   ├── Dependencies
│   │   └── Performance notes
│   ├── README.md                     # Comprehensive Guide
│   ├── QUICKSTART.md                 # 5-minute Setup
│   ├── SETUP.md                      # Detailed Setup
│   ├── DEPLOYMENT.md                 # Build & Distribution
│   ├── CHANGELOG.md                  # Version History
│   └── PROJECT_STRUCTURE.md          # This file
│
├── assets/                           # Application Assets
│   └── icon.png                      # App icon (to be added)
│
├── main.js                           # Electron Main Process
│   ├── Window management:
│   │   ├── createWindow()
│   │   │   ├── Size: 1400x900
│   │   │   ├── Min size: 1200x700
│   │   │   ├── webPreferences setup
│   │   │   └── Load frontend/index.html
│   │   └── Window lifecycle
│   ├── Python subprocess management:
│   │   ├── startPythonBackend()
│   │   │   ├── Spawn python3 backend/run.py
│   │   │   ├── Port: 8000
│   │   │   ├── stdout/stderr logging
│   │   │   └── Process cleanup
│   │   └── 2-second startup delay
│   ├── IPC handlers:
│   │   ├── select-csv-file:
│   │   │   ├── Open file dialog
│   │   │   ├── Filter: .csv files
│   │   │   └── Return file path
│   │   ├── save-image:
│   │   │   ├── Save dialog
│   │   │   ├── Convert base64 to buffer
│   │   │   ├── Write to file
│   │   │   └── Return success status
│   │   └── get-backend-url:
│   │       └── Return http://127.0.0.1:8000
│   ├── App lifecycle:
│   │   ├── whenReady() - Start backend & window
│   │   ├── activate() - macOS reopen
│   │   ├── window-all-closed() - Quit app
│   │   └── quit() - Kill python process
│   └── Error handling
│
├── package.json                      # Node.js Configuration
│   ├── Metadata:
│   │   ├── name: "flight-track-viewer"
│   │   ├── version: "1.0.1"
│   │   ├── description
│   │   └── author
│   ├── Scripts:
│   │   ├── start - electron .
│   │   ├── dev - electron . --dev
│   │   └── build - electron-builder
│   ├── Dependencies:
│   │   ├── axios: ^1.6.2
│   │   └── html2canvas: ^1.4.1
│   ├── DevDependencies:
│   │   ├── electron: ^28.0.0
│   │   └── electron-builder: ^24.9.1
│   └── Build configuration:
│       ├── appId
│       ├── productName
│       ├── directories
│       ├── files to include
│       └── Platform-specific settings:
│           ├── win: NSIS installer
│           ├── mac: DMG image
│           └── linux: AppImage
│
├── sample_flight.csv                 # Test Data
│   ├── FlightRadar24 format
│   ├── Comma-separated values
│   ├── 1,214 data points
│   ├── Columns:
│   │   ├── Timestamp (Unix)
│   │   ├── UTC (ISO 8601)
│   │   ├── Callsign (N503SP)
│   │   ├── Position ("lat,lon")
│   │   ├── Altitude (feet)
│   │   ├── Speed (knots)
│   │   └── Direction (degrees)
│   └── Full flight trajectory example
│
├── .gitignore                        # Git Ignore Rules
│   ├── node_modules/
│   ├── __pycache__/
│   ├── dist/, build/
│   ├── venv/, env/
│   ├── .vscode/, .idea/
│   ├── *.log
│   ├── .env files
│   └── OS files (.DS_Store, etc.)
│
└── README.md                         # Main Documentation
    ├── Project overview
    ├── Features list
    ├── Project structure diagram
    ├── Quick start guide
    ├── Module overview
    ├── Development instructions
    ├── Building for production
    ├── Adding new features
    ├── Contributing guidelines
    ├── Troubleshooting
    ├── License information
    └── Links to detailed docs

```

## Module Communication Flow

```
User Action (Frontend)
    ↓
app.js (Main Controller)
    ↓
├─→ MapManager (Map operations)
│   └─→ Leaflet.js
│
├─→ ChartManager (Chart operations)
│   └─→ Chart.js
│
├─→ AnimationController (Animation)
│   └─→ requestAnimationFrame
│
└─→ Backend API (Data processing)
    ↓
    main.py (Routes)
    ↓
    data_processor.py (Pipeline)
    ↓
    flight_utils.py (Calculations)
    ↓
    JSON Response
    ↓
    app.js (Update UI)
```

## Data Flow

```
CSV File
    ↓
[Frontend] app.js
    ↓ HTTP POST
[Backend] main.py
    ↓
[Backend] data_processor.py
    ├─→ Parse CSV
    ├─→ Validate
    ├─→ Calculate headings (flight_utils)
    ├─→ Calculate distances (flight_utils)
    ├─→ Generate statistics
    └─→ Generate plots
    ↓
JSON Response
    ↓
[Frontend] app.js
    ├─→ MapManager.createFlightPath()
    ├─→ MapManager.createAircraftMarker()
    ├─→ ChartManager.createAltitudeChart()
    ├─→ ChartManager.createSpeedChart()
    └─→ AnimationController.setFlightData()
    ↓
Visualization Ready
```

## Key Design Patterns

### 1. **Separation of Concerns**
- Each module has a single responsibility
- Clear boundaries between components
- Independent testing possible

### 2. **Module Pattern**
- Each JS file exports a class
- Clean public API
- Private state encapsulation

### 3. **Observer Pattern**
- AnimationController uses callbacks
- app.js coordinates updates
- Loose coupling between modules

### 4. **Pipeline Pattern**
- data_processor.py chains operations
- Each step transforms data
- Clear data flow

### 5. **Factory Pattern**
- ChartManager creates chart instances
- Common configuration
- Easy to add new chart types

## File Size Reference

```
Frontend:
├── app.js                    ~8 KB   (Main controller)
├── map-manager.js            ~5 KB   (Map logic)
├── chart-manager.js          ~4 KB   (Chart logic)
├── animation-controller.js   ~4 KB   (Animation logic)
├── styles.css                ~7 KB   (All styles)
└── index.html                ~6 KB   (UI structure)

Backend:
├── main.py                   ~2 KB   (Routes only)
├── data_processor.py         ~8 KB   (Processing pipeline)
└── flight_utils.py           ~3 KB   (Pure functions)

Documentation:
├── README.md                 ~8 KB
├── ARCHITECTURE.md           ~15 KB
└── Other docs                ~20 KB total

Total Project: ~100 KB (excluding dependencies)
```

## Dependencies Tree

```
Electron App
├── Main Process (main.js)
│   ├── electron
│   ├── child_process (Python backend)
│   └── fs (file operations)
│
└── Renderer Process (frontend)
    ├── app.js
    │   ├── axios (HTTP)
    │   ├── html2canvas (screenshots)
    │   ├── MapManager
    │   ├── ChartManager
    │   └── AnimationController
    │
    ├── MapManager
    │   └── Leaflet.js
    │       └── leaflet-rotatedmarker
    │
    └── ChartManager
        └── Chart.js

Python Backend
├── FastAPI (web framework)
├── Uvicorn (ASGI server)
├── Pandas (data processing)
├── NumPy (calculations)
└── python-multipart (file uploads)
```

---

**Version:** 2.0.0 
**Last Updated:** 2026-02-06  
**Maintained by:** Flight Track Viewer Team