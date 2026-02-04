from PyQt6.QtCore import QThread, pyqtSignal

# Try import, fail gracefully if FTV not installed yet
try:
    from ftv import run
    FTV_AVAILABLE = True
except ImportError:
    FTV_AVAILABLE = False

class ProcessingThread(QThread):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, csv_file, config):
        super().__init__()
        self.csv_file = csv_file
        self.config = config

    def run(self):
        try:
            if not FTV_AVAILABLE: raise ImportError("ftv module missing")
            self.progress.emit(20, "Processing data...")
            result = run(
                csv_file=self.csv_file,
                animate=self.config['animate'],
                save_figures_enabled=self.config['save_figures'],
                save_video_enabled=self.config['save_video']
            )
            self.progress.emit(100, "Done")
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))