import random
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rcParams
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Canvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots(figsize=(1, 1), dpi=150)
        super().__init__(fig)
        self.setParent(parent)
        
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)
        self.ax.plot(t, s)
        self.ax.set(xlabel="time (s)", ylabel="voltage (mV)",
                    title="My title")
        self.ax.grid()

# tests
if __name__ == '__main__':
    C = Canvas()

 
