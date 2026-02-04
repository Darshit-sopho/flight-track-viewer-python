import sys
from PyQt6.QtWidgets import QApplication
from .main_window import FlightTrackViewerUI  # Relative import within 'ui' package

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = FlightTrackViewerUI()
    window.show()
    
    sys.exit(app.exec())