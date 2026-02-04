from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QSplitter, QProgressBar, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Modular Imports
from .widgets.control_panel import ControlPanel
from .widgets.leaflet_map import LeafletMapCanvas
from .widgets.plot_canvas import StaticPlotCanvas
from .widgets.animation_controls import AnimationControls
from .widgets.info_panel import InfoPanel
from .threads.processing_thread import ProcessingThread
from .utils.csv_parser import parse_flight_data
from .styles.stylesheet import STYLESHEET

class FlightTrackViewerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flight Track Viewer")
        self.resize(1400, 900)
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # 1. Top Controls
        self.controls = ControlPanel()
        self.controls.process_requested.connect(self.start_processing)
        main_layout.addWidget(self.controls)

        # 2. Main Visualization Splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left: Map & Animation Controls
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.addWidget(QLabel("Flight Track Map", font=QFont("Arial", 12, QFont.Weight.Bold)))
        
        self.map_view = LeafletMapCanvas()
        left_layout.addWidget(self.map_view)
        
        self.anim_controls = AnimationControls()
        self.anim_controls.frame_changed.connect(self.map_view.update_marker)
        left_layout.addWidget(self.anim_controls)
        
        splitter.addWidget(left_container)

        # Right: Plots & Info
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        
        self.alt_plot = StaticPlotCanvas(title="Altitude")
        right_layout.addWidget(self.alt_plot)
        
        self.speed_plot = StaticPlotCanvas(title="Speed")
        right_layout.addWidget(self.speed_plot)
        
        self.info_panel = InfoPanel()
        right_layout.addWidget(self.info_panel)
        
        splitter.addWidget(right_container)
        splitter.setSizes([800, 600])
        main_layout.addWidget(splitter)

        # 3. Status
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        main_layout.addWidget(self.progress)

    def apply_styles(self):
        self.setStyleSheet(STYLESHEET)

    def start_processing(self, csv_file, config):
        self.progress.setVisible(True)
        self.progress.setValue(0)
        
        self.thread = ProcessingThread(csv_file, config)
        self.thread.progress.connect(lambda val, msg: (self.progress.setValue(val), self.statusBar().showMessage(msg)))
        self.thread.finished.connect(lambda res: self.processing_done(csv_file, res))
        self.thread.error.connect(lambda err: self.statusBar().showMessage(f"Error: {err}"))
        self.thread.start()

    def processing_done(self, csv_file, result):
        self.progress.setVisible(False)
        self.controls.reset_state()
        self.statusBar().showMessage("Processing Complete")
        
        # Parse data for UI display
        data, info_text = parse_flight_data(csv_file)
        
        # Update Widgets
        self.map_view.load_flight_data(data['lats'], data['lons'])
        self.anim_controls.setup(data['count'])
        
        if len(data['alt']) > 0: self.alt_plot.plot_data(data['alt'], "Altitude (ft)")
        if len(data['speed']) > 0: self.speed_plot.plot_data(data['speed'], "Speed (kts)")
            
        self.info_panel.update_info(info_text)