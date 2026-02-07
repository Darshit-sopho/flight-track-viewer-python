# ✈️ Flight Track Viewer

A modular desktop application for visualizing and analyzing flight trajectories from FlightRadar24 CSV data.

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/Darshit-sopho/flight-track-viewer-python)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

![Flight Track Viewer](docs/screenshot.png)

## 🌟 Features

- **Interactive Map Visualization** - Live flight path animation with Leaflet.js
- **Real-time Charts** - Altitude, Speed, and Distance tracking
- **Animation Controls** - Play/pause, speed control (0.25x-10x), progress scrubbing
- **High-Quality Exports** - Save maps and charts as PNG images
- **Modular Architecture** - Clean separation of concerns for easy maintenance
- **Cross-Platform** - Works on Windows, macOS, and Linux

## 📁 Project Structure

```
flight-track-viewer/
├── frontend/                    # Frontend application
│   ├── src/
│   │   ├── js/                  # JavaScript modules
│   │   │   ├── app.js           # Main application coordinator
│   │   │   ├── map-manager.js   # Map and marker management
│   │   │   ├── chart-manager.js # Chart creation and updates
│   │   │   └── animation-controller.js # Animation logic
│   │   └── css/
│   │       └── styles.css       # Application styles
│   ├── public/                  # Static assets
│   └── index.html               # Main HTML file
│
├── backend/                     # Python FastAPI backend
│   ├── src/
│   │   ├── main.py              # FastAPI app and routes
│   │   ├── data_processor.py    # CSV processing pipeline
│   │   ├── flight_utils.py      # Calculation utilities
│   │   └── __init__.py          # Package initialization
│   ├── run.py                   # Backend entry point
│   └── requirements.txt         # Python dependencies
│
├── docs/                        # Documentation
│   ├── README.md                # Detailed documentation
│   ├── QUICKSTART.md            # Quick setup guide
│   ├── PROJECT_STRUCTURE.md     # Technical details
│   ├── DEPLOYMENT.md            # Build and distribution
│   ├── CHANGELOG.md             # Version history
│   └── SETUP.md                 # Setup instructions
│
├── assets/                      # Application assets
│   └── icon.png                 # App icon
│
├── main.js                      # Electron main process
├── package.json                 # Node.js configuration
├── sample_flight.csv            # Sample data for testing
└── README.md                    # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 16+ ([Download](https://nodejs.org/))
- **Python** 3.8+ ([Download](https://www.python.org/))
- **npm** or **yarn**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Darshit-sopho/flight-track-viewer-python.git
   cd flight-track-viewer-python
   ```

2. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Install Frontend Dependencies**
   ```bash
   npm install
   ```

4. **Run the Application**
   ```bash
   npm start
   ```

5. **Test with Sample Data**
   - Click "Browse CSV File"
   - Select `sample_flight.csv`
   - Click "Process Flight Data"
   - Watch the flight animation! ✨

## 📖 Documentation

- **[Quick Start Guide](docs/QUICKSTART.md)** - Get up and running in 5 minutes
- **[Setup Instructions](docs/SETUP.md)** - Detailed installation and configuration
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Technical architecture details
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Building and distributing
- **[Changelog](docs/CHANGELOG.md)** - Version history and updates

## 🎯 Module Overview

### Frontend Modules

#### **app.js** - Main Application Controller
- Coordinates all components
- Handles user interactions
- Manages application state
- Processes backend responses

#### **map-manager.js** - Map Management
- Leaflet map initialization
- Flight path rendering
- Aircraft marker with rotation
- Progress path visualization

#### **chart-manager.js** - Chart Management
- Chart.js configuration
- Altitude/Speed/Distance charts
- Responsive chart updates
- Chart export functionality

#### **animation-controller.js** - Animation Logic
- Frame-by-frame animation
- Speed control (0.25x-10x)
- Progress tracking
- Play/pause/reset controls

### Backend Modules

#### **main.py** - API Routes
- FastAPI application setup
- `/api/analyze-flight` endpoint
- `/health` health check
- CORS configuration

#### **data_processor.py** - Data Processing
- CSV parsing (comma/tab-separated)
- Flight data validation
- Statistics generation
- Plot data preparation

#### **flight_utils.py** - Calculations
- Heading calculation (bearing formula)
- Distance calculation (Haversine)
- Position parsing

## 🔧 Development

### Run in Development Mode
```bash
npm run dev
```

### Backend Development
```bash
cd backend
python run.py
```

### Frontend Testing
```bash
# Open index.html in browser with Live Server
# Or use the Electron app
```

## 📦 Building for Production

```bash
npm run build
```

Creates distributable packages in `dist/`:
- **Windows**: `.exe` installer
- **macOS**: `.dmg` image
- **Linux**: `.AppImage` file

## 🧩 Adding New Features

### Adding a New Frontend Module

1. Create module in `frontend/src/js/your-module.js`
2. Export functionality:
   ```javascript
   class YourModule {
     // Your code
   }
   if (typeof module !== 'undefined' && module.exports) {
     module.exports = { YourModule };
   }
   ```
3. Add script tag to `index.html`:
   ```html
   <script src="src/js/your-module.js"></script>
   ```
4. Use in `app.js`:
   ```javascript
   this.yourModule = new YourModule();
   ```

### Adding a New Backend Module

1. Create module in `backend/src/your_module.py`
2. Import in `main.py`:
   ```python
   from .your_module import YourClass
   ```
3. Use in routes or data processing

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- **JavaScript**: Use consistent naming (camelCase for functions/variables)
- **Python**: Follow PEP 8 style guide
- **Comments**: Write clear, descriptive comments
- **Documentation**: Update docs when adding features

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.8+

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
- Reduce speed multiplier
- Close other applications
- Check system resources

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Leaflet.js](https://leafletjs.com/) - Interactive maps
- [Chart.js](https://www.chartjs.org/) - Beautiful charts
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Electron](https://www.electronjs.org/) - Desktop application framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Darshit-sopho/flight-track-viewer-python/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Darshit-sopho/flight-track-viewer-python/discussions)
- **Documentation**: [docs/](docs/)

## 🗺️ Roadmap

- [ ] Video export of flight animation
- [ ] Multiple flight comparison
- [ ] 3D visualization mode
- [ ] GPX/KML file support
- [ ] Real-time tracking integration
- [ ] Weather overlay
- [ ] Airport database integration
- [ ] Web-based version

---

**Made with ✈️ by the Flight Track Viewer Team**

[⭐ Star this project](https://github.com/Darshit-sopho/flight-track-viewer-python) if you find it useful!