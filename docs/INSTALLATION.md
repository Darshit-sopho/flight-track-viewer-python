# Installation Guide

Complete guide for installing Flight Track Viewer with different options.

---

## 📦 Installation Options

### Quick Setup (Recommended)

Use the automated setup scripts for one-click installation:

#### GUI Application (Most Users)

**Windows:**
```batch
scripts\setup_with_ui.bat
```

**Mac/Linux:**
```bash
chmod +x scripts/setup_with_ui.sh
./scripts/setup_with_ui.sh
```

**What this does:**
1. Checks Python installation
2. Installs core package + PyQt6
3. Launches the GUI automatically

**After installation, run anytime with:**
```bash
flight-track-viewer          # Command-line launcher
python -m ftv.ui             # Module execution
./scripts/run_ui.sh          # Quick launcher (Mac/Linux)
scripts\run_ui.bat           # Quick launcher (Windows)
```

#### Python API Only (Developers/Scripters)

**Windows:**
```batch
scripts\setup_core.bat
```

**Mac/Linux:**
```bash
chmod +x scripts/setup_core.sh
./scripts/setup_core.sh
```

**What this does:**
1. Checks Python installation
2. Installs core package only (no GUI)
3. Displays usage instructions

**Then use programmatically:**
```python
from ftv import run

result = run(csv_file="flight.csv")
```

---

## 🎯 Which Installation Should You Choose?

```
Do you want the graphical interface?
│
├─ YES → Use setup_with_ui
│        • Point-and-click interface
│        • Visual flight animation
│        • No coding required
│        • Run with: flight-track-viewer
│
└─ NO  → Use setup_core
         • Programmatic usage
         • Integrate into scripts
         • Smaller installation (~60MB less)
         • Use the Python API
```

---

## 🔧 Manual Installation

If you prefer manual control:

### Install Core Only
```bash
pip install -e .
```

Installs:
- numpy, pandas, matplotlib
- imageio, imageio-ffmpeg
- **No PyQt6**

**Use with:**
```python
from ftv import run
result = run(csv_file="flight.csv")
```

### Install with GUI
```bash
pip install -e ".[ui]"
```

Installs:
- Everything from core
- **PyQt6** (GUI framework)

**Run with:**
```bash
flight-track-viewer
# or
python -m ftv.ui
```

### Install Everything (Development)
```bash
pip install -e ".[all]"
```

Installs:
- Core + GUI
- Development tools (pytest, black, flake8)

---

## 📋 System Requirements

### Python Version
- **Required:** Python 3.10 or 3.11
- **Not supported:** Python 3.14+ (scientific libraries not yet compatible)

### Operating Systems
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux (Ubuntu 20.04+, Debian, Fedora)

### Disk Space
- **Core only:** ~150 MB
- **With GUI:** ~210 MB
- **Full (with dev tools):** ~230 MB

---

## 🚀 Verifying Installation

After installation, verify everything works:

### Test Core Package
```bash
python -c "from ftv import run; print('Core package working!')"
```

### Test GUI (if installed)
```bash
python -c "import PyQt6; print('GUI dependencies working!')"
```

### Test Entry Point (if GUI installed)
```bash
flight-track-viewer --help 2>/dev/null || echo "Entry point not yet configured"
```

### Run the Application
```bash
# Method 1: Entry point
flight-track-viewer

# Method 2: Module
python -m ftv.ui

# Method 3: Launcher script
./scripts/run_ui.sh     # Mac/Linux
scripts\run_ui.bat      # Windows

# Method 4: Programmatically
python -c "from ftv import launch_ui; launch_ui()"
```

---

## 🔄 Upgrading Installation

### Add GUI to Core Installation
```bash
pip install -e ".[ui]"
```

After this, you can run:
```bash
flight-track-viewer
python -m ftv.ui
```

### Add Development Tools
```bash
pip install -e ".[dev]"
```

### Upgrade to Full Installation
```bash
pip install -e ".[all]"
```

---

## 🐛 Troubleshooting

### "Python not found"

**Solution:** Install Python 3.10 or 3.11 from [python.org](https://www.python.org/downloads/)

Make sure to check "Add Python to PATH" during installation.

### "pip is not recognized"

**Solution:**
```bash
# Windows
python -m pip install -e .

# Mac/Linux
python3 -m pip install -e .
```

### "No module named 'ftv'"

**Solution:** Make sure you're in the project directory and run:
```bash
pip install -e .
```

### "No module named 'PyQt6'" when running GUI

**Solution:** Install UI dependencies:
```bash
pip install -e ".[ui]"
```

Or re-run:
```bash
scripts/setup_with_ui.bat  # Windows
./scripts/setup_with_ui.sh # Mac/Linux
```

### "command not found: flight-track-viewer"

**Possible causes:**
1. You installed core only (no GUI) - Install with: `pip install -e ".[ui]"`
2. Entry point not configured - Run with: `python -m ftv.ui` instead
3. Scripts directory not in PATH - Use full path or launcher scripts

**Solution:**
```bash
# Reinstall with UI
pip install -e ".[ui]"

# Or use alternative methods
python -m ftv.ui
./scripts/run_ui.sh
```

### "UI dependencies not installed" error

**Solution:** This means you installed core only. Add UI support:
```bash
pip install -e ".[ui]"
```

### Qt errors on Linux

**Ubuntu/Debian:**
```bash
sudo apt-get install libxcb-xinerama0 libxcb-cursor0
```

**Fedora:**
```bash
sudo dnf install xcb-util-cursor
```

### Permission errors on Mac/Linux

**Solution:** Make scripts executable:
```bash
chmod +x scripts/*.sh
```

Or run with explicit permissions:
```bash
bash scripts/setup_with_ui.sh
```

---

## 🔍 Advanced Installation

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate

# Install
pip install -e ".[ui]"

# Run
flight-track-viewer
```

### Development Installation

For contributors:

```bash
# Clone repository
git clone https://github.com/Darshit-sopho/flight-track-viewer-python.git
cd flight-track-viewer-python

# Install in development mode with all tools
pip install -e ".[all]"

# Run tests
pytest

# Format code
black .

# Check code quality
flake8

# Run GUI
flight-track-viewer
```

---

## 📊 Dependency Details

### Core Dependencies (Always Installed)
```
numpy>=1.24        # Numerical computing
pandas>=2.0        # Data manipulation
matplotlib>=3.7    # Plotting
imageio>=2.34      # Animation creation
imageio-ffmpeg>=0.5 # Video encoding
```

### Optional: GUI
```
PyQt6>=6.6.0       # GUI framework
```

**Enables:**
- `flight-track-viewer` command
- `python -m ftv.ui`
- `from ftv import launch_ui`

### Optional: Development
```
pytest>=7.0        # Testing
black>=23.0        # Code formatting
flake8>=6.0        # Linting
```

---

## 📍 Entry Points Explained

After installing with `pip install -e ".[ui]"`, the package creates these entry points:

### flight-track-viewer
Main command-line launcher:
```bash
flight-track-viewer
```

Equivalent to:
```bash
python -c "from ftv import launch_ui; launch_ui()"
```

### ftv-gui
Alternative launcher (same as above):
```bash
ftv-gui
```

### Module execution
You can also run as a module:
```bash
python -m ftv.ui
```

All three methods launch the same GUI application.

---

## 🔄 Uninstallation

To remove the package:

```bash
pip uninstall flight-track-viewer
```

To remove virtual environment:
```bash
# Deactivate first
deactivate

# Then delete the folder
# Windows:
rmdir /s .venv

# Mac/Linux:
rm -rf .venv
```

---

## ✅ Installation Checklist

- [ ] Python 3.10 or 3.11 installed
- [ ] pip working (`pip --version`)
- [ ] Cloned/downloaded repository
- [ ] Navigated to project directory (`cd flight-track-viewer-python`)
- [ ] Chose installation type (GUI vs Core)
- [ ] Ran appropriate setup script
- [ ] Verified installation with test commands
- [ ] Successfully ran the application

---

## 💡 Quick Reference

### For GUI Users:
```bash
# Install
scripts/setup_with_ui.sh    # or .bat on Windows

# Run (pick one)
flight-track-viewer
python -m ftv.ui
./scripts/run_ui.sh
```

### For API Users:
```bash
# Install
scripts/setup_core.sh       # or .bat on Windows

# Use in code
python -c "from ftv import run; run()"
```

---

## 💬 Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Search [GitHub Issues](https://github.com/Darshit-sopho/flight-track-viewer-python/issues)
3. Open a new issue with:
   - Your OS and Python version
   - Installation method used
   - Complete error message
   - Steps to reproduce

---

**Next Steps:**
- ✅ Installation complete? See [User Guide](USER_GUIDE.md)
- 💻 Using Python API? See [API Documentation](API.md)
- 📁 Need sample data? Check [examples folder](../examples/)
