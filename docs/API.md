# API Documentation

Python API reference for programmatic use of Flight Track Viewer.

---

## Quick Start

```python
from ftv import run

# Simplest usage - file picker dialog
result = run()

# Or specify a file
result = run(csv_file="flight.csv")

# With all options
result = run(
    csv_file="flight.csv",
    callsign="N503SP",
    animate=True,
    animate_step_seconds=30,
    save_figures=True,
    save_video=True
)

# Launch the GUI programmatically
from ftv import launch_ui
launch_ui()
```

---

## Main Functions

### `run()` - Process Flight Data

The primary entry point for flight track analysis.

#### Signature

```python
def run(
    csv_file: str | None = None,
    callsign: str | None = None,
    animate: bool = False,
    animate_step_seconds: float = 30,
    save_figures: bool = False,
    save_video: bool = False
) -> dict
```

#### Parameters

**`csv_file` (str | None)**
- **Default:** `None` (opens file picker)
- **Description:** Path to CSV file containing flight data
- **Example:** `"path/to/flight.csv"`

**`callsign` (str | None)**  
- **Default:** `None` (uses all data)
- **Description:** Filter data by specific aircraft callsign
- **Example:** `"N503SP"`

**`animate` (bool)**
- **Default:** `False`
- **Description:** Create animated flight playback
- **Note:** Requires matplotlib display backend

**`animate_step_seconds` (float)**
- **Default:** `30`
- **Description:** Time interval between animation frames (in seconds)
- **Example:** `60` for 1-minute intervals

**`save_figures` (bool)**
- **Default:** `False`
- **Description:** Save static plots as PNG files
- **Output:** Creates PNG files in same directory as CSV

**`save_video` (bool)**
- **Default:** `False`
- **Description:** Save animation as MP4 video
- **Output:** Creates MP4 file in same directory as CSV
- **Requires:** `animate=True`

#### Return Value

Returns a dictionary with the following structure:

```python
{
    'config': {...},      # Configuration used
    'data': {...},        # Processed flight data
    'figures': {...},     # Matplotlib figure objects
    'outputs': {...}      # Paths to saved files
}
```

---

### `launch_ui()` - Launch GUI Application

Launch the graphical user interface programmatically.

#### Signature

```python
def launch_ui() -> None
```

#### Usage

```python
from ftv import launch_ui

# Launch the GUI
launch_ui()
```

#### Requirements

- PyQt6 must be installed
- Install with: `pip install -e ".[ui]"`

#### Error Handling

If UI dependencies are not installed, shows helpful error message:
```
UI dependencies not installed!

To use the GUI, install with UI support:
  pip install -e '.[ui]'

Or run the setup script:
  Windows: scripts\setup_with_ui.bat
  Mac/Linux: ./scripts/setup_with_ui.sh
```

---

## Return Dictionary Structure

### `result['config']`

Configuration parameters used:

```python
{
    'csv_file': str,
    'callsign': str | None,
    'animate': bool,
    'animate_step_seconds': float,
    'save_figures': bool,
    'save_video': bool
}
```

### `result['data']`

Processed flight data:

```python
{
    # DataFrame with flight track data
    'df': pandas.DataFrame,
    
    # Coordinate arrays
    'lat': numpy.ndarray,
    'lon': numpy.ndarray,
    'alt_ft': numpy.ndarray,
    'speed_kts': numpy.ndarray,
    'timestamps': numpy.ndarray,
    
    # Computed metrics
    'max_altitude_ft': float,
    'min_altitude_ft': float,
    'max_speed_kts': float,
    'avg_speed_kts': float,
    'max_radius_nm': float,
    
    # Flight events (if detected)
    'i_liftoff': int | None,
    'i_touchdown': int | None,
    
    # Geographic bounds
    'lat_min': float,
    'lat_max': float,
    'lon_min': float,
    'lon_max': float
}
```

### `result['figures']`

Matplotlib figure objects (if created):

```python
{
    'map': matplotlib.figure.Figure,
    'altitude': matplotlib.figure.Figure,
    'speed': matplotlib.figure.Figure
}
```

### `result['outputs']`

Paths to saved files (if any):

```python
{
    'map_png': str,
    'altitude_png': str,
    'speed_png': str,
    'animation_mp4': str
}
```

---

## Examples

### Example 1: Basic Analysis

```python
from ftv import run

# Analyze a flight
result = run(csv_file="my_flight.csv")

# Print statistics
data = result['data']
print(f"Max Altitude: {data['max_altitude_ft']:.0f} ft")
print(f"Max Speed: {data['max_speed_kts']:.0f} knots")
print(f"Distance: {data['max_radius_nm']:.2f} nm")
```

### Example 2: Generate Report

```python
from ftv import run

# Process with all outputs
result = run(
    csv_file="flight.csv",
    save_figures=True,
    save_video=True,
    animate=True
)

# Access saved file paths
outputs = result['outputs']
print(f"Map saved to: {outputs['map_png']}")
print(f"Video saved to: {outputs['animation_mp4']}")
```

### Example 3: Batch Processing

```python
from ftv import run
import os

# Process multiple flights
flight_dir = "flights/"
results = []

for filename in os.listdir(flight_dir):
    if filename.endswith('.csv'):
        csv_path = os.path.join(flight_dir, filename)
        
        result = run(
            csv_file=csv_path,
            save_figures=True
        )
        
        results.append({
            'file': filename,
            'max_alt': result['data']['max_altitude_ft'],
            'max_speed': result['data']['max_speed_kts'],
            'distance': result['data']['max_radius_nm']
        })

# Print summary
for r in results:
    print(f"{r['file']}: {r['max_alt']:.0f}ft, {r['max_speed']:.0f}kts")
```

### Example 4: Launch GUI After Analysis

```python
from ftv import run, launch_ui

# First, analyze programmatically
result = run(csv_file="flight.csv", save_figures=True)

# Check if flight meets criteria
if result['data']['max_altitude_ft'] > 10000:
    print("High altitude flight detected!")
    
    # Launch GUI for detailed review
    launch_ui()
```

### Example 5: Conditional GUI Launch

```python
from ftv import run, launch_ui
import sys

def analyze_and_review(csv_file):
    """Analyze flight and optionally launch GUI"""
    result = run(csv_file=csv_file)
    
    # Auto-detect unusual patterns
    unusual = False
    
    if result['data']['max_altitude_ft'] > 15000:
        print("⚠️ Unusually high altitude detected")
        unusual = True
    
    if result['data']['max_speed_kts'] > 200:
        print("⚠️ Unusually high speed detected")
        unusual = True
    
    if unusual:
        print("\nLaunching GUI for manual review...")
        launch_ui()
    
    return result

# Use it
if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_and_review(sys.argv[1])
    else:
        print("Usage: python script.py <csv_file>")
```

### Example 6: Custom Analysis

```python
from ftv import run
import pandas as pd

# Get raw data
result = run(csv_file="flight.csv")
df = result['data']['df']

# Custom analysis
climb_rate = df['Altitude'].diff() / df['Timestamp'].diff().dt.total_seconds()
max_climb_rate = climb_rate.max()

print(f"Max climb rate: {max_climb_rate:.0f} ft/min")

# Access specific flight segments
if result['data']['i_liftoff'] is not None:
    liftoff_idx = result['data']['i_liftoff']
    liftoff_time = df.iloc[liftoff_idx]['Timestamp']
    print(f"Liftoff at: {liftoff_time}")
```

### Example 7: Filter by Callsign

```python
from ftv import run

# CSV with multiple aircraft
result = run(
    csv_file="airport_traffic.csv",
    callsign="N503SP"
)

# Only data for N503SP
print(f"Processed {len(result['data']['df'])} points for N503SP")
```

### Example 8: Access Figures

```python
from ftv import run
import matplotlib.pyplot as plt

# Generate analysis
result = run(csv_file="flight.csv")

# Get matplotlib figures
map_fig = result['figures']['map']
alt_fig = result['figures']['altitude']

# Customize and save manually
map_fig.suptitle("My Custom Title")
map_fig.savefig("custom_map.png", dpi=300)

# Or display interactively
plt.show()
```

---

## CSV Data Format

### Required Columns

| Column | Format | Example |
|--------|--------|---------|
| Position | "lat,lon" | "42.1900,-71.1720" |
| UTC or Timestamp UTC | ISO 8601 | "2026-01-15T14:30:00Z" |

### Optional Columns

| Column | Format | Unit | Example |
|--------|--------|------|---------|
| Altitude | Float | Feet | 1500 |
| Speed | Float | Knots | 120 |
| Direction | Float | Degrees | 270 |
| Callsign | String | - | "N503SP" |

### Example CSV

```csv
Timestamp UTC,Callsign,Position,Altitude,Speed,Direction
2026-01-15T14:30:00Z,N503SP,"42.1900,-71.1720",0,0,0
2026-01-15T14:31:00Z,N503SP,"42.1950,-71.1680",500,80,45
2026-01-15T14:32:00Z,N503SP,"42.2000,-71.1640",1000,95,45
```

---

## Error Handling

The `run()` function may raise exceptions:

```python
from ftv import run

try:
    result = run(csv_file="flight.csv")
except FileNotFoundError:
    print("CSV file not found")
except ValueError as e:
    print(f"Invalid data: {e}")
except Exception as e:
    print(f"Error: {e}")
```

The `launch_ui()` function handles missing dependencies gracefully:

```python
from ftv import launch_ui

try:
    launch_ui()
except SystemExit:
    print("UI dependencies not installed")
    print("Install with: pip install -e '.[ui]'")
```

### Common Exceptions

- `FileNotFoundError` - CSV file doesn't exist
- `ValueError` - Invalid CSV format or data
- `KeyError` - Required columns missing
- `ImportError` - Missing dependencies (core)
- `SystemExit` - UI dependencies missing (from launch_ui)

---

## Advanced Usage

### Working with DataFrames

```python
from ftv import run
import pandas as pd

result = run(csv_file="flight.csv")
df = result['data']['df']

# DataFrame operations
df['Time_Minutes'] = (df['Timestamp'] - df['Timestamp'].iloc[0]).dt.total_seconds() / 60

# Calculate ground speed
df['Ground_Speed'] = df['Speed']  # Already in knots

# Export to other formats
df.to_csv("processed_flight.csv", index=False)
df.to_excel("processed_flight.xlsx", index=False)
```

### Geographic Calculations

```python
from ftv.analysis.haversine_nm import haversine_nm

# Calculate distance between two points
lat1, lon1 = 42.19, -71.17
lat2, lon2 = 42.20, -71.16

distance = haversine_nm(lat1, lon1, lat2, lon2)
print(f"Distance: {distance:.2f} nautical miles")
```

### Custom Visualization

```python
from ftv import run
import matplotlib.pyplot as plt

result = run(csv_file="flight.csv")
data = result['data']

# Create custom plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data['lon'], data['lat'], c=data['alt_ft'], cmap='viridis')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.colorbar(ax.collections[0], label='Altitude (ft)')
plt.title('Flight Path Colored by Altitude')
plt.savefig('custom_viz.png')
```

---

## Module Structure

```python
ftv/
├── __init__.py               # Exports: run, launch_ui
├── __main__.py               # Module entry point (python -m ftv.ui)
├── run.py                    # Main API function
├── ui.py                     # GUI application
├── config.py                 # Configuration
├── data/
│   ├── read_flight_csv.py    # CSV parsing
│   ├── parse_position.py     # Position extraction
│   └── ...
├── analysis/
│   ├── haversine_nm.py       # Distance calculations
│   ├── detect_takeoff_landing.py
│   └── ...
├── plotting/
│   ├── plot_map.py           # Map visualization
│   ├── plot_time_series.py   # Time series plots
│   └── animate_playback.py   # Animation
└── io/
    ├── save_figures.py       # Figure export
    └── save_playback_video.py # Video export
```

---

## Type Hints

For type checking:

```python
from typing import Dict, Optional
from ftv import run, launch_ui

def analyze_flight(csv_path: str) -> Dict:
    """Analyze a flight and return results"""
    result: Dict = run(csv_file=csv_path)
    return result

def batch_analyze(
    files: list[str],
    save: bool = True
) -> list[Dict]:
    """Analyze multiple flights"""
    return [run(csv_file=f, save_figures=save) for f in files]

def review_flight(csv_path: str) -> None:
    """Analyze and launch GUI for review"""
    result = analyze_flight(csv_path)
    
    if result['data']['max_altitude_ft'] > 10000:
        launch_ui()
```

---

## Performance Tips

### Large Files

For CSV files with >10,000 points:

```python
# Disable animation for speed
result = run(
    csv_file="large_flight.csv",
    animate=False,  # Much faster
    save_figures=True
)
```

### Memory Optimization

```python
# Process and release immediately
def process_flight(csv_file):
    result = run(csv_file=csv_file, save_figures=True)
    stats = {
        'max_alt': result['data']['max_altitude_ft'],
        'max_speed': result['data']['max_speed_kts']
    }
    del result  # Free memory
    return stats
```

---

## Integration Examples

### Web API

```python
from flask import Flask, jsonify, request
from ftv import run

app = Flask(__name__)

@app.route('/analyze/<filename>')
def analyze(filename):
    result = run(csv_file=f"uploads/{filename}")
    return jsonify({
        'max_altitude': result['data']['max_altitude_ft'],
        'max_speed': result['data']['max_speed_kts'],
        'distance': result['data']['max_radius_nm']
    })

@app.route('/launch-ui')
def launch():
    from ftv import launch_ui
    launch_ui()
    return "GUI launched"
```

### Command Line Tool

```python
import sys
from ftv import run, launch_ui

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze.py <csv_file> [--gui]")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    # Always analyze
    result = run(
        csv_file=csv_file,
        save_figures=True,
        save_video=True
    )
    
    print(f"Analysis complete!")
    print(f"Max altitude: {result['data']['max_altitude_ft']:.0f} ft")
    
    # Launch GUI if requested
    if "--gui" in sys.argv:
        launch_ui()
```

---

## Testing

```python
import unittest
from ftv import run, launch_ui

class TestFlightAnalysis(unittest.TestCase):
    def test_basic_run(self):
        result = run(csv_file="examples/sample_flight.csv")
        self.assertIn('data', result)
        self.assertIn('figures', result)
    
    def test_max_altitude(self):
        result = run(csv_file="examples/sample_flight.csv")
        self.assertGreater(result['data']['max_altitude_ft'], 0)
    
    def test_launch_ui_import(self):
        # Just test that import works
        from ftv import launch_ui
        self.assertTrue(callable(launch_ui))

if __name__ == '__main__':
    unittest.main()
```

---

## FAQ

**Q: Can I use this in a Jupyter notebook?**

A: Yes! The API works great in notebooks:
```python
from ftv import run
%matplotlib inline

result = run(csv_file="flight.csv")
# Figures display automatically
```

**Q: How do I launch the GUI from a script?**

A: Use `launch_ui()`:
```python
from ftv import launch_ui
launch_ui()
```

**Q: Can I use both API and GUI together?**

A: Absolutely! Analyze with `run()`, then launch GUI with `launch_ui()`:
```python
from ftv import run, launch_ui

result = run(csv_file="flight.csv")
if result['data']['max_altitude_ft'] > 10000:
    launch_ui()  # Manual review
```

**Q: How do I access individual data points?**

A: Use the DataFrame:
```python
result = run(csv_file="flight.csv")
df = result['data']['df']
first_point = df.iloc[0]
```

**Q: Can I disable the file picker?**

A: Yes, always provide `csv_file` parameter:
```python
result = run(csv_file="flight.csv")  # No picker
```

---

**For more examples, see the [examples folder](../examples/).**
