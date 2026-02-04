import os
from PyQt6.QtWidgets import (
    QGroupBox, QGridLayout, QLabel, QPushButton, QCheckBox, QFileDialog, QFrame
)
from PyQt6.QtCore import pyqtSignal

class ControlPanel(QGroupBox):
    # Signal emits (csv_path, config_dict)
    process_requested = pyqtSignal(str, dict)

    def __init__(self):
        super().__init__("Controls")
        self.csv_file = None
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout()
        
        # File Selection
        self.file_label = QLabel("No file selected")
        self.file_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.browse_btn = QPushButton("📁 Browse")
        self.browse_btn.clicked.connect(self.browse_file)
        
        layout.addWidget(QLabel("CSV File:"), 0, 0)
        layout.addWidget(self.file_label, 0, 1)
        layout.addWidget(self.browse_btn, 0, 2)
        
        # Options
        self.save_fig_cb = QCheckBox("Save Figures")
        self.save_vid_cb = QCheckBox("Save Video")
        self.animate_cb = QCheckBox("Live Animation")
        self.animate_cb.setChecked(True)
        
        layout.addWidget(self.save_fig_cb, 1, 0)
        layout.addWidget(self.save_vid_cb, 1, 1)
        layout.addWidget(self.animate_cb, 1, 2)
        
        # Process Button
        self.process_btn = QPushButton("🚀 Process Flight Data")
        self.process_btn.setEnabled(False)
        self.process_btn.clicked.connect(self.emit_process)
        # Style is handled in stylesheet.py, but we set object name for targeting
        self.process_btn.setObjectName("processButton") 
        
        layout.addWidget(self.process_btn, 2, 0, 1, 3)
        self.setLayout(layout)

    def browse_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if f:
            self.csv_file = f
            self.file_label.setText(os.path.basename(f))
            self.process_btn.setEnabled(True)

    def emit_process(self):
        config = {
            'animate': self.animate_cb.isChecked(),
            'save_figures': self.save_fig_cb.isChecked(),
            'save_video': self.save_vid_cb.isChecked()
        }
        self.process_requested.emit(self.csv_file, config)
        self.process_btn.setEnabled(False) # Prevent double click

    def reset_state(self):
        self.process_btn.setEnabled(True)