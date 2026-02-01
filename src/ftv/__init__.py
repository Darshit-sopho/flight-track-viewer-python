"""Flight Track Viewer Package"""

from .run import run

__version__ = "0.1.0"
__all__ = ['run']

def launch_ui():
    """Launch the graphical interface"""
    try:
        from .ui import main
        main()
    except ImportError as e:
        print("=" * 60)
        print("UI dependencies not installed!")
        print("=" * 60)
        print("\nTo use the GUI, install with UI support:")
        print("  pip install -e '.[ui]'")
        print("\nOr run the setup script:")
        print("  Windows: scripts\\setup_with_ui.bat")
        print("  Mac/Linux: ./scripts/setup_with_ui.sh")
        print("=" * 60)
        raise SystemExit(1)