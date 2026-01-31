# Installation Guide - Flight Track Viewer

This guide explains the different installation options for the Flight Track Viewer package.

---

## 🎯 Quick Decision Guide

**Choose your installation based on how you want to use the package:**

| Use Case | Installation | What You Get |
|----------|-------------|--------------|
| **GUI Application** | `setup_with_ui` | Core + PyQt6 GUI |
| **Python API Only** | `setup_core` | Core only (no GUI) |
| **Everything** | `pip install -e ".[all]"` | Core + GUI + Dev tools |

---

## 📦 Installation Options

### Option 1: GUI Application (Recommended for Most Users)

Install the full application with graphical interface:

**Windows:**
```batch
setup_with_ui.bat
```

**Mac/Linux:**
```bash
chmod +x setup_with_ui.sh
./setup_with_ui.sh
```

**What gets installed:**
- ✓ Core libraries (numpy, pandas, matplotlib, imageio)
- ✓ PyQt6 (GUI framework)
- ✓ Launches the UI automatically

---

### Option 2: Core Package Only (For Developers/Scripters)

Install just the core functionality without GUI dependencies:

**Windows:**
```batch
setup_core.bat
```

**Mac/Linux:**
```bash
chmod +x setup_core.sh
./setup_core.sh
```

**What gets installed:**
- ✓ Core libraries (numpy, pandas, matplotlib, imageio)
- ✗ No PyQt6 (saves ~60MB)

**Use case:** You want to use `ftv` programmatically in your own scripts:

```python
from ftv import run

# Use the API
result = run(csv_file="flight.csv", animate=True, save_figures=True)
```

---

### Option 3: Manual Installation (Advanced Users)

#### Install Core Only:
```bash
pip install -e .
```

#### Install with UI:
```bash
pip install -e ".[ui]"
```

#### Install Everything (including dev tools):
```bash
pip install -e ".[all]"
```

#### Install Multiple Optional Groups:
```bash
pip install -e ".[ui,dev]"
```

---

## 🔧 Understanding Optional Dependencies

Your `pyproject.toml` defines these dependency groups:

### Core Dependencies (Always Installed)
```toml
dependencies = [
    "numpy>=1.24",
    "pandas>=2.0",
    "matplotlib>=3.7",
    "imageio>=2.34",
    "imageio-ffmpeg>=0.5",
]
```

### Optional: UI
```toml
[project.optional-dependencies]
ui = [
    "PyQt6>=6.6.0",
]
```

**Install with:** `pip install -e ".[ui]"`

### Optional: Dev
```toml
dev = [
    "pytest>=7.0",
    "black>=23.0",
    "flake8>=6.0",
]
```

**Install with:** `pip install -e ".[dev]"`

### Optional: All
```toml
all = [
    # Everything above
]
```

**Install with:** `pip install -e ".[all]"`

---

## 🚀 After Installation

### If You Installed with UI:

**Run the application:**

Windows: `run.bat` or `python flight_track_viewerUI.py`

Mac/Linux: `./run.sh` or `python3 flight_track_viewerUI.py`

### If You Installed Core Only:

**Use programmatically:**

```python
from ftv import run

# Basic usage with file picker
result = run()

# Or specify file and options
result = run(
    csv_file="myFlight.csv",
    animate=True,
    save_figures=True
)

# Access results
print(result['data']['max_altitude_ft'])
```

---

## 🔄 Switching Between Installations

### Add UI to Core Installation:
```bash
pip install -e ".[ui]"
```

### Add Dev Tools:
```bash
pip install -e ".[dev]"
```

### Upgrade to Full Installation:
```bash
pip install -e ".[all]"
```

### Reinstall Core Only:
```bash
pip uninstall flight-track-viewer
pip install -e .
```

---

## 📊 Size Comparison

| Installation | Approximate Size | Download Time (10 Mbps) |
|--------------|------------------|-------------------------|
| Core only | ~150 MB | ~2 minutes |
| With UI | ~210 MB | ~3 minutes |
| With all | ~230 MB | ~3-4 minutes |

---

## 🎓 Use Cases

### For Flight Instructors/Pilots:
→ **Install with UI** (`setup_with_ui`)
- You want the graphical application
- Easy point-and-click interface
- Visual feedback and animation

### For Developers/Data Scientists:
→ **Install core only** (`setup_core`)
- You're integrating into your own scripts
- You don't need the GUI
- Smaller installation footprint

### For Contributors:
→ **Install everything** (`pip install -e ".[all]"`)
- You're developing/testing the package
- You need testing and code quality tools
- You want all features

---

## 🐛 Troubleshooting

### "No module named 'PyQt6'" when running UI
You installed core only. Add UI support:
```bash
pip install -e ".[ui]"
```

### Import works but UI won't run
Check if PyQt6 is installed:
```bash
python -c "import PyQt6; print('PyQt6 installed')"
```

If not, install UI dependencies:
```bash
pip install -e ".[ui]"
```

### Want to reduce installation size
Uninstall and reinstall core only:
```bash
pip uninstall flight-track-viewer
pip install -e .
```

---

## 📝 Summary

### Quick Reference:

```bash
# Full GUI application (recommended)
setup_with_ui.bat / ./setup_with_ui.sh

# Core package only (for scripting)
setup_core.bat / ./setup_core.sh

# Manual installation with UI
pip install -e ".[ui]"

# Manual installation core only
pip install -e .

# Everything (UI + dev tools)
pip install -e ".[all]"
```

---

## ✅ Verification

Check what's installed:

```bash
pip show flight-track-viewer
pip list | grep -E "(numpy|pandas|matplotlib|imageio|PyQt6)"
```

Test core functionality:
```python
python -c "from ftv import run; print('Core package working!')"
```

Test UI (if installed):
```python
python -c "import PyQt6; print('UI dependencies working!')"
```

---

**Questions?** Check the main README or open an issue on GitHub.
