# Quick Start Guide

## First Time Setup

### 1. Install Dependencies

**Backend (Python):**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend (Node.js):**
```bash
npm install
```

### 2. Run the Application

```bash
npm start
```

The application will:
1. Automatically start the Python FastAPI backend on port 8000
2. Launch the Electron desktop window
3. Wait for backend to be ready (usually 2-3 seconds)

## Development Mode

Run with DevTools open:
```bash
npm run dev
```

## Testing with Sample Data

A sample CSV file is included: `sample_flight.csv`

1. Click "Browse CSV File"
2. Select `sample_flight.csv`
3. Click "Process Flight Data"
4. Watch the flight animation!

## Common Issues

### Port 8000 Already in Use
Kill the process using port 8000:
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Python Not Found
Make sure Python 3.8+ is in your PATH:
```bash
python --version
# or
python3 --version
```

### Module Import Errors
Reinstall Python dependencies:
```bash
cd backend
pip install -r requirements.txt --upgrade
```

## File Structure

```
flight-track-viewer/
├── backend/
│   ├── main.py              # FastAPI server
│   └── requirements.txt      # Python dependencies
├── main.js                   # Electron main process
├── renderer.js               # Frontend logic
├── index.html                # Main UI
├── styles.css                # Styling
├── package.json              # Node.js config
├── sample_flight.csv         # Test data
└── README.md                 # Documentation
```

## Next Steps

1. **Customize the airplane icon**: Replace `AIRPLANE_ICON` in `renderer.js`
2. **Add your own flights**: Load any FlightRadar24 CSV file
3. **Modify the UI**: Edit `styles.css` for custom colors
4. **Extend functionality**: Add new features to `main.py` or `renderer.js`

## Building Distribution

Create installer for your platform:
```bash
npm run build
```

Outputs to `dist/` folder:
- Windows: `Flight-Track-Viewer-Setup.exe`
- macOS: `Flight-Track-Viewer.dmg`
- Linux: `Flight-Track-Viewer.AppImage`

---

Happy flight tracking! ✈️
