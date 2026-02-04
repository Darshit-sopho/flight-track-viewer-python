# import matplotlib
# matplotlib.use('QtAgg')
# from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure

# class StaticPlotCanvas(FigureCanvas):
#     def __init__(self, parent=None, title="Plot"):
#         # CHANGED: Set facecolor to match UI dark grey
#         self.fig = Figure(figsize=(6, 3), dpi=100, facecolor='#3c3f41')
#         self.ax = self.fig.add_subplot(111)
        
#         # CHANGED: Set internal plot background to darker grey
#         self.ax.set_facecolor('#2b2b2b')
        
#         super().__init__(self.fig)
#         self.setParent(parent)
#         self.set_plot_style(title)
        
#     def set_plot_style(self, title):
#         # CHANGED: White text for dark mode
#         self.ax.set_title(title, color='white')
#         self.ax.tick_params(axis='x', colors='white')
#         self.ax.tick_params(axis='y', colors='white')
#         self.ax.xaxis.label.set_color('white')
#         self.ax.yaxis.label.set_color('white')
        
#         # Grid lines subtle
#         self.ax.grid(True, color='#555555', linestyle='--', linewidth=0.5)
        
#         # Border color
#         for spine in self.ax.spines.values():
#             spine.set_edgecolor('#777777')
        
#         self.fig.tight_layout()
        
#     def plot_data(self, y_data, ylabel="Value"):
#         self.ax.clear()
        
#         # CHANGED: Cyan line to match map
#         self.ax.plot(range(len(y_data)), y_data, color='#00ffff', linewidth=1.5)
        
#         self.ax.set_xlabel("Time Index")
#         self.ax.set_ylabel(ylabel)
        
#         # Re-apply style after clearing
#         self.ax.set_facecolor('#2b2b2b')
#         self.set_plot_style(self.ax.get_title())
#         self.draw()

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