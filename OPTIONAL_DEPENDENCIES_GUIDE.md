# Optional Dependencies - Visual Guide

## 📦 Package Structure

```
┌─────────────────────────────────────────────────────────┐
│                Flight Track Viewer Package              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  CORE (Always Installed)                         │  │
│  │  • numpy, pandas, matplotlib                     │  │
│  │  • imageio, imageio-ffmpeg                       │  │
│  │  • Basic flight analysis & visualization         │  │
│  └──────────────────────────────────────────────────┘  │
│                         │                               │
│         ┌───────────────┴───────────────┬──────────┐    │
│         ▼                               ▼          ▼    │
│  ┌────────────┐                  ┌─────────┐  ┌──────┐ │
│  │ UI (opt.)  │                  │Dev(opt.)│  │ All  │ │
│  │  • PyQt6   │                  │ • pytest│  │(opt.)│ │
│  │  • GUI app │                  │ • black │  │      │ │
│  └────────────┘                  │ • flake8│  └──────┘ │
│                                  └─────────┘           │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Installation Paths

### Path 1: GUI User (Most Common)
```
User → setup_with_ui → Core + UI → Run GUI App ✓
```

### Path 2: Developer/Scripter
```
Developer → setup_core → Core Only → Use Python API ✓
```

### Path 3: Contributor
```
Contributor → pip install -e ".[all]" → Everything ✓
```

## 📋 What Each Installation Includes

### `pip install -e .` (Core Only)
```
✓ NumPy
✓ Pandas  
✓ Matplotlib
✓ ImageIO
✓ ImageIO-FFmpeg
✗ PyQt6
✗ Dev tools
```

**Can do:**
- ✓ Load and parse CSV files
- ✓ Analyze flight data
- ✓ Generate plots and animations
- ✓ Save figures and videos
- ✗ Run GUI application

### `pip install -e ".[ui]"` (Core + GUI)
```
✓ NumPy
✓ Pandas
✓ Matplotlib
✓ ImageIO
✓ ImageIO-FFmpeg
✓ PyQt6 ← Added
✗ Dev tools
```

**Can do:**
- ✓ Everything from Core
- ✓ Run GUI application ← New!
- ✗ Run tests, linting

### `pip install -e ".[all]"` (Everything)
```
✓ NumPy
✓ Pandas
✓ Matplotlib
✓ ImageIO
✓ ImageIO-FFmpeg
✓ PyQt6
✓ pytest ← Added
✓ black ← Added
✓ flake8 ← Added
```

**Can do:**
- ✓ Everything!

## 🔄 Migration Between Installations

```
Core Only
   │
   ├─ pip install -e ".[ui]" ──→ Core + UI
   │
   └─ pip install -e ".[all]" ──→ Everything

Core + UI
   │
   └─ pip install -e ".[dev]" ──→ Everything
```

## 💡 Real-World Examples

### Example 1: Flight Instructor
**Need:** Easy-to-use app for reviewing student flights

**Solution:** `setup_with_ui.bat`

**Result:** Point-and-click interface, no coding needed

---

### Example 2: Data Scientist
**Need:** Batch process 100 flights in a pipeline

**Solution:** `setup_core.bat`

**Script:**
```python
for csv_file in flight_files:
    result = run(csv_file=csv_file, save_figures=True)
    store_results(result)
```

**Result:** Lightweight installation, no GUI overhead

---

### Example 3: Open Source Contributor
**Need:** Add new features and run tests

**Solution:** `pip install -e ".[all]"`

**Result:** Full development environment

---

## 🎓 Decision Tree

```
Do you want to use the graphical interface?
│
├─ YES → setup_with_ui (or pip install -e ".[ui]")
│         │
│         └─ Simple usage, visual feedback
│
└─ NO  → setup_core (or pip install -e .)
          │
          └─ Programmatic usage, lighter install
```

## 📊 Feature Comparison Table

| Feature | Core | Core + UI | All |
|---------|------|-----------|-----|
| Parse CSV | ✓ | ✓ | ✓ |
| Flight analysis | ✓ | ✓ | ✓ |
| Generate plots | ✓ | ✓ | ✓ |
| Save figures | ✓ | ✓ | ✓ |
| Create animations | ✓ | ✓ | ✓ |
| **GUI application** | ✗ | **✓** | ✓ |
| **Live animation viewer** | ✗ | **✓** | ✓ |
| **Interactive controls** | ✗ | **✓** | ✓ |
| **Unit tests** | ✗ | ✗ | **✓** |
| **Code formatting** | ✗ | ✗ | **✓** |
| **Linting** | ✗ | ✗ | **✓** |
| Install size | ~150MB | ~210MB | ~230MB |

## 🚀 Quick Commands Reference Card

```bash
# Install Options
pip install -e .           # Core only
pip install -e ".[ui]"     # Core + GUI
pip install -e ".[dev]"    # Core + Dev tools
pip install -e ".[all]"    # Everything

# Or use setup scripts
setup_core.bat             # Core (Windows)
setup_with_ui.bat          # Core + GUI (Windows)
./setup_core.sh            # Core (Mac/Linux)
./setup_with_ui.sh         # Core + GUI (Mac/Linux)

# Check installation
pip show flight-track-viewer
python -c "from ftv import run; print('OK')"
python -c "import PyQt6; print('UI OK')"  # Only if UI installed
```

## 📖 Learn More

- **Full installation guide:** See `INSTALLATION_GUIDE.md`
- **API documentation:** See `examples/example_usage.py`
- **GUI guide:** See `README.md`

---

**Remember:** You can always add features later!

Start with what you need, upgrade when you want more.
