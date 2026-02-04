from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QComboBox, QLabel
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

class AnimationControls(QWidget):
    # Signal emits the current frame index
    frame_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.total_frames = 0
        self.current_frame = 0
        self.frame_step = 1
        self.base_interval = 100
        
        self.timer = QTimer()
        self.timer.timeout.connect(self._on_tick)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Slider
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setEnabled(False)
        self.slider.valueChanged.connect(self._on_slider_moved)
        layout.addWidget(self.slider)
        
        # Buttons Row
        row = QHBoxLayout()
        self.play_btn = QPushButton("▶ Play")
        self.play_btn.setEnabled(False)
        self.play_btn.clicked.connect(self.toggle_play)
        
        self.reset_btn = QPushButton("⟲ Reset")
        self.reset_btn.setEnabled(False)
        self.reset_btn.clicked.connect(self.reset)
        
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["1x", "2x", "5x", "10x", "20x"])
        self.speed_combo.setEnabled(False)
        self.speed_combo.currentTextChanged.connect(self._set_speed)
        
        row.addWidget(self.play_btn)
        row.addWidget(self.reset_btn)
        row.addWidget(QLabel("Speed:"))
        row.addWidget(self.speed_combo)
        layout.addLayout(row)
        self.setLayout(layout)

    def setup(self, total_frames):
        self.total_frames = total_frames
        self.slider.setRange(0, total_frames - 1)
        self.slider.setValue(0)
        self.slider.setEnabled(True)
        self.play_btn.setEnabled(True)
        self.reset_btn.setEnabled(True)
        self.speed_combo.setEnabled(True)

    def toggle_play(self):
        if self.timer.isActive():
            self.timer.stop()
            self.play_btn.setText("▶ Play")
        else:
            self.timer.start(int(self.base_interval))
            self.play_btn.setText("⏸ Pause")

    def reset(self):
        self.timer.stop()
        self.play_btn.setText("▶ Play")
        self.slider.setValue(0)

    def _on_tick(self):
        next_frame = self.slider.value() + self.frame_step
        if next_frame >= self.total_frames:
            next_frame = 0
        self.slider.setValue(next_frame)

    def _on_slider_moved(self, val):
        self.frame_changed.emit(val)

    def _set_speed(self, text):
        if not text: return
        self.frame_step = int(text.replace('x', ''))