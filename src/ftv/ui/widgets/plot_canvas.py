import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class StaticPlotCanvas(FigureCanvas):
    def __init__(self, parent=None, title="Plot"):
        # Standard White Background
        self.fig = Figure(figsize=(6, 3), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        super().__init__(self.fig)
        self.setParent(parent)
        
        self.ax.set_title(title)
        self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        
    def plot_data(self, y_data, ylabel="Value"):
        self.ax.clear()
        
        # Standard Blue Line
        self.ax.plot(range(len(y_data)), y_data, 'b-', linewidth=2)
        
        self.ax.set_xlabel("Time Index")
        self.ax.set_ylabel(ylabel)
        self.ax.grid(True, alpha=0.3)
        
        # Restore title if it got cleared
        # (We assume the parent keeps track, or we re-set it here)
        # For simplicity in this lightweight version:
        self.draw()