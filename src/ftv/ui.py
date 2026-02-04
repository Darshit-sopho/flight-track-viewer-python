"""
Flight Track Viewer - GUI Application
A modern UI for visualizing flight tracks using Leaflet.js and PyQt6
"""

import sys
import os
import json
import pandas as pd
import numpy as np
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QCheckBox, QFileDialog, QLabel, QGroupBox,
    QProgressBar, QTextEdit, QSplitter, QFrame, QGridLayout,
    QSlider, QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView

# Matplotlib is still needed for the Static Plots (Altitude/Speed)
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Import your flight track viewer functions
try:
    from ftv import run
    FTV_AVAILABLE = True
except ImportError:
    FTV_AVAILABLE = False
    print("Warning: ftv module not found. Please ensure it's installed.")


class FlightProcessingThread(QThread):
    """Background thread for processing flight data"""
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, csv_file, config):
        super().__init__()
        self.csv_file = csv_file
        self.config = config
        
    def run(self):
        try:
            self.progress.emit(10, "Loading CSV file...")
            
            if not FTV_AVAILABLE:
                raise ImportError("ftv module not available")
            
            self.progress.emit(30, "Processing flight data...")
            
            # Run the flight track analysis
            result = run(
                csv_file=self.csv_file,
                animate=self.config.get('animate', False),
                animate_step_seconds=self.config.get('step_seconds', 30),
                save_figures_enabled=self.config.get('save_figures', False),
                save_video_enabled=self.config.get('save_video', False)
            )
            
            self.progress.emit(90, "Finalizing...")
            self.finished.emit(result)
            
        except Exception as e:
            self.error.emit(str(e))


class LeafletMapCanvas(QWebEngineView):
    """
    A modern map canvas using Leaflet.js inside QWebEngineView.
    Offers 60FPS smooth zooming, panning, and vector graphics.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.flight_data = None
        self.current_frame = 0
        
        # HTML Template for Leaflet Map
        self.html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
            <style>
                body, html, #map { margin: 0; padding: 0; height: 100%; width: 100%; }
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                // Initialize Map
                var map = L.map('map').setView([0, 0], 2);
                
                // Add OpenStreetMap Tiles
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: '© OpenStreetMap'
                }).addTo(map);

                // Flight Path Polyline
                var flightPath = L.polyline([], {color: 'blue', weight: 3}).addTo(map);
                
                // Plane Marker (Red Circle)
                var planeMarker = L.circleMarker([0, 0], {
                    color: 'red',
                    fillColor: '#f03',
                    fillOpacity: 0.9,
                    radius: 3
                }).addTo(map);

                // --- Functions called by Python ---

                function loadPath(latlngs) {
                    // latlngs is an array of [lat, lon]
                    flightPath.setLatLngs(latlngs);
                    if (latlngs.length > 0) {
                        map.fitBounds(flightPath.getBounds());
                    }
                }

                function updatePosition(lat, lon) {
                    // Move the red marker
                    var newLatLng = [lat, lon];
                    planeMarker.setLatLng(newLatLng);
                }
            </script>
        </body>
        </html>
        """
        self.setHtml(self.html_template)
        
    def load_flight_data(self, data):
        """Send the full flight path to the JavaScript map"""
        self.flight_data = data
        self.current_frame = 0
        
        if 'lat' in data and 'lon' in data:
            # Convert numpy arrays to a standard Python list of [lat, lon]
            lats = data['lat']
            lons = data['lon']
            
            # Create list of [lat, lon] points
            # We take every Nth point to avoid passing 100k points to JS (which might lag)
            step = max(1, len(lats) // 5000) 
            path_points = [[float(lats[i]), float(lons[i])] for i in range(0, len(lats), step)]
            
            # Send to JavaScript
            js_code = f"loadPath({json.dumps(path_points)});"
            self.page().runJavaScript(js_code)

    def update_frame(self, frame_idx):
        """Update the marker position on the map"""
        if self.flight_data is None:
            return
            
        lats = self.flight_data['lat']
        lons = self.flight_data['lon']
        
        if frame_idx >= len(lats):
            frame_idx = len(lats) - 1
            
        lat = float(lats[frame_idx])
        lon = float(lons[frame_idx])
        
        # Call the JavaScript function 'updatePosition'
        self.page().runJavaScript(f"updatePosition({lat}, {lon});")
        self.current_frame = frame_idx


class StaticPlotCanvas(FigureCanvas):
    """Canvas for displaying static plots (altitude, speed)"""
    
    def __init__(self, parent=None, title="Plot"):
        self.fig = Figure(figsize=(6, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        
        self.ax.set_title(title)
        self.ax.grid(True, alpha=0.3)
        
    def plot_data(self, x_data, y_data, xlabel="Time", ylabel="Value", title=None):
        """Plot data on the canvas"""
        self.ax.clear()
        self.ax.plot(x_data, y_data, 'b-', linewidth=2)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        if title:
            self.ax.set_title(title)
        self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.draw()


class FlightTrackViewerUI(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.csv_file = None
        self.flight_result = None
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.is_animating = False
        self.base_interval = 100  # Standard speed (ms)
        self.frame_step = 1
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Flight Track Viewer")
        icon = QIcon("icon.ico")
        self.setWindowIcon(icon)
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Create top control panel
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
        
        # Create splitter for visualization area
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - Animation canvas (Leaflet Map)
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        animation_label = QLabel("Flight Track Animation")
        animation_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        left_layout.addWidget(animation_label)
        
        # --- CHANGED: Use LeafletMapCanvas instead of AnimationCanvas ---
        self.animation_canvas = LeafletMapCanvas(self)
        # left_layout.addWidget(self.animation_canvas)
        left_layout.addWidget(self.animation_canvas, 1)  # Add stretch factor of 1 to make it expand
        # ----------------------------------------------------------------
        
        # --- ANIMATION CONTROLS ---
        
        # 1. Slider Row
        slider_layout = QHBoxLayout()
        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.timeline_slider.setRange(0, 100)
        self.timeline_slider.setEnabled(False)
        self.timeline_slider.valueChanged.connect(self.slider_moved)
        slider_layout.addWidget(self.timeline_slider)
        
        left_layout.addLayout(slider_layout)

        # 2. Buttons and Speed Row
        anim_controls = QHBoxLayout()
        
        self.play_pause_btn = QPushButton("▶ Play")
        self.play_pause_btn.clicked.connect(self.toggle_animation)
        self.play_pause_btn.setEnabled(False)
        
        self.reset_btn = QPushButton("⟲ Reset")
        self.reset_btn.clicked.connect(self.reset_animation)
        self.reset_btn.setEnabled(False)
        
        # Speed Control
        speed_label = QLabel("Speed:")
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["1x", "2x", "5x", "10x", "20x"])
        self.speed_combo.currentTextChanged.connect(self.change_speed)
        self.speed_combo.setEnabled(False)
        
        anim_controls.addWidget(self.play_pause_btn)
        anim_controls.addWidget(self.reset_btn)
        anim_controls.addWidget(speed_label)
        anim_controls.addWidget(self.speed_combo)
        anim_controls.addStretch()
        
        left_layout.addLayout(anim_controls)
        
        splitter.addWidget(left_widget)
        
        # Right side - Static plots and info
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Altitude plot
        altitude_label = QLabel("Altitude vs Time")
        altitude_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        right_layout.addWidget(altitude_label)
        
        self.altitude_canvas = StaticPlotCanvas(self, "Altitude vs Time")
        right_layout.addWidget(self.altitude_canvas)
        
        # Speed plot
        speed_label = QLabel("Speed vs Time")
        speed_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        right_layout.addWidget(speed_label)
        
        self.speed_canvas = StaticPlotCanvas(self, "Speed vs Time")
        right_layout.addWidget(self.speed_canvas)
        
        # Info panel
        info_group = QGroupBox("Flight Information")
        info_layout = QVBoxLayout()
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMaximumHeight(150)
        self.info_text.setText("No flight data loaded. Please select a CSV file.")
        info_layout.addWidget(self.info_text)
        info_group.setLayout(info_layout)
        right_layout.addWidget(info_group)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([700, 700])
        
        main_layout.addWidget(splitter)
        
        # Progress bar at bottom
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
    def create_control_panel(self):
        """Create the top control panel with file selection and options"""
        panel = QGroupBox("Controls")
        layout = QGridLayout()
        
        # File selection row
        file_label = QLabel("CSV File:")
        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.browse_btn = QPushButton("📁 Browse")
        self.browse_btn.clicked.connect(self.browse_file)
        
        layout.addWidget(file_label, 0, 0)
        layout.addWidget(self.file_path_label, 0, 1, 1, 3)
        layout.addWidget(self.browse_btn, 0, 4)
        
        # Options row
        options_label = QLabel("Options:")
        self.save_figures_enabled_cb = QCheckBox("Save Figures (PNG)")
        self.save_video_enabled_cb = QCheckBox("Save Animation (MP4)")
        self.animate_cb = QCheckBox("Live Animation")
        self.animate_cb.setChecked(True)
        
        layout.addWidget(options_label, 1, 0)
        layout.addWidget(self.save_figures_enabled_cb, 1, 1)
        layout.addWidget(self.save_video_enabled_cb, 1, 2)
        layout.addWidget(self.animate_cb, 1, 3)
        
        # Process button
        self.process_btn = QPushButton("🚀 Process Flight Data")
        self.process_btn.clicked.connect(self.process_flight)
        self.process_btn.setEnabled(False)
        self.process_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        layout.addWidget(self.process_btn, 2, 0, 1, 5)
        
        panel.setLayout(layout)
        return panel
    
    def browse_file(self):
        """Open file dialog to select CSV file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Flight CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.csv_file = file_path
            self.file_path_label.setText(os.path.basename(file_path))
            self.process_btn.setEnabled(True)
            self.statusBar().showMessage(f"Selected: {file_path}")
    
    def process_flight(self):
        """Process the selected flight CSV file"""
        if not self.csv_file:
            self.statusBar().showMessage("Please select a CSV file first")
            return
        
        # Disable controls during processing
        self.process_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Prepare configuration
        config = {
            'animate': self.animate_cb.isChecked(),
            'save_figures': self.save_figures_enabled_cb.isChecked(),
            'save_video': self.save_video_enabled_cb.isChecked(),
            'step_seconds': 30
        }
        
        # Create and start processing thread
        self.processing_thread = FlightProcessingThread(self.csv_file, config)
        self.processing_thread.progress.connect(self.update_progress)
        self.processing_thread.finished.connect(self.processing_finished)
        self.processing_thread.error.connect(self.processing_error)
        self.processing_thread.start()
    
    def update_progress(self, value, message):
        """Update progress bar and status"""
        self.progress_bar.setValue(value)
        self.statusBar().showMessage(message)
    
    def processing_finished(self, result):
        """Handle completion of flight processing"""
        self.flight_result = result
        
        # Re-enable controls
        self.process_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Display results
        self.display_results(result)
        
        self.statusBar().showMessage("Processing complete!")
    
    def processing_error(self, error_msg):
        """Handle processing errors"""
        self.process_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        self.statusBar().showMessage(f"Error: {error_msg}")
        self.info_text.setText(f"Error processing flight data:\n{error_msg}")
    
    def display_results(self, result):
        """Display the processed flight results"""
        try:
            # Extract data from result
            data = result.get('data', {})
            
            # Parse CSV to get actual data for plotting
            df = pd.read_csv(self.csv_file)
            
            # Parse position data
            if 'Position' in df.columns:
                positions = df['Position'].str.replace('"', '').str.split(',', expand=True)
                lats = positions[0].astype(float).values
                lons = positions[1].astype(float).values
            else:
                lats = df['Latitude'].values if 'Latitude' in df.columns else []
                lons = df['Longitude'].values if 'Longitude' in df.columns else []
            
            # Get timestamps
            time_col = 'Timestamp UTC' if 'Timestamp UTC' in df.columns else 'UTC'
            timestamps = df[time_col].values if time_col in df.columns else range(len(lats))
            
            # Load animation data
            flight_data = {
                'lat': lats,
                'lon': lons,
                'timestamps': timestamps
            }
            self.animation_canvas.load_flight_data(flight_data)
            
            # --- UPDATE CONTROLS STATE ---
            # Set slider range based on data length
            total_frames = len(lats)
            self.timeline_slider.setRange(0, total_frames - 1)
            self.timeline_slider.setValue(0)
            self.timeline_slider.setEnabled(True)
            self.speed_combo.setEnabled(True)
            
            self.play_pause_btn.setEnabled(True)
            self.reset_btn.setEnabled(True)
            
            # Plot altitude if available
            if 'Altitude' in df.columns:
                altitudes = df['Altitude'].values
                self.altitude_canvas.plot_data(
                    range(len(altitudes)),
                    altitudes,
                    xlabel="Time Index",
                    ylabel="Altitude (ft)",
                    title="Altitude vs Time"
                )
            
            # Plot speed if available
            if 'Speed' in df.columns:
                speeds = df['Speed'].values
                self.speed_canvas.plot_data(
                    range(len(speeds)),
                    speeds,
                    xlabel="Time Index",
                    ylabel="Speed (knots)",
                    title="Speed vs Time"
                )
            
            # Display flight info
            info_text = "Flight Data Summary\n" + "="*50 + "\n\n"
            
            if 'Callsign' in df.columns:
                callsign = df['Callsign'].iloc[0]
                info_text += f"Callsign: {callsign}\n"
            
            info_text += f"Total Data Points: {len(df)}\n"
            
            if 'Altitude' in df.columns:
                info_text += f"Max Altitude: {df['Altitude'].max():.0f} ft\n"
                info_text += f"Min Altitude: {df['Altitude'].min():.0f} ft\n"
            
            if 'Speed' in df.columns:
                info_text += f"Max Speed: {df['Speed'].max():.0f} knots\n"
                info_text += f"Avg Speed: {df['Speed'].mean():.0f} knots\n"
            
            # Add info from result if available
            if 'max_radius_nm' in data:
                info_text += f"\nMax Distance from Origin: {data['max_radius_nm']:.2f} nm\n"
            
            if 'i_liftoff' in data and data['i_liftoff'] is not None:
                info_text += f"Liftoff Index: {data['i_liftoff']}\n"
            
            if 'i_touchdown' in data and data['i_touchdown'] is not None:
                info_text += f"Touchdown Index: {data['i_touchdown']}\n"
            
            # Check for saved outputs
            outputs = result.get('outputs', {})
            if outputs:
                info_text += "\n" + "="*50 + "\n"
                info_text += "Saved Files:\n"
                for key, value in outputs.items():
                    info_text += f"  • {key}: {value}\n"
            
            self.info_text.setText(info_text)
            
        except Exception as e:
            self.info_text.setText(f"Error displaying results:\n{str(e)}")
            import traceback
            traceback.print_exc()

    def slider_moved(self, value):
        """Handle slider movement (scrubbing)"""
        # Update the canvas to the specific frame
        self.animation_canvas.update_frame(value)
    
    def change_speed(self, text):
        """Update animation speed based on selection"""
        if not text:
            return
            
        # Extract multiplier (e.g., "2x" -> 2)
        try:
            multiplier = int(text.replace('x', ''))
        except ValueError:
            multiplier = 1

        # Instead of shrinking interval too much, increase frame step
        self.frame_step = multiplier
        self.current_interval = self.base_interval  # keep timer stable, like 100ms

        # If currently running, restart timer with new interval
        if self.is_animating:
            self.animation_timer.stop()
            self.animation_timer.start(self.current_interval)


    def toggle_animation(self):
        """Start/stop the animation"""
        if self.is_animating:
            self.animation_timer.stop()
            self.play_pause_btn.setText("▶ Play")
            self.is_animating = False
        else:
            # Determine interval based on current speed selection
            current_speed_text = self.speed_combo.currentText()
            try:
                multiplier = int(current_speed_text.replace('x', ''))
            except ValueError:
                multiplier = 1
            
            interval = max(1, int(self.base_interval / multiplier))
            
            self.animation_timer.start(interval)
            self.play_pause_btn.setText("⏸ Pause")
            self.is_animating = True
    
    def update_animation(self):
        if self.animation_canvas.flight_data is None:
            return

        max_frames = len(self.animation_canvas.flight_data['lat'])
        current = self.animation_canvas.current_frame

        current = current + getattr(self, "frame_step", 1)
        if current >= max_frames:
            current = 0

        self.timeline_slider.blockSignals(True)
        self.timeline_slider.setValue(current)
        self.timeline_slider.blockSignals(False)

        self.animation_canvas.update_frame(current)

    
    def reset_animation(self):
        """Reset animation to start"""
        if self.is_animating:
            self.toggle_animation()
        
        self.timeline_slider.setValue(0)
        self.animation_canvas.update_frame(0)


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = FlightTrackViewerUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()