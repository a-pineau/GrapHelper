import random
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rc
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# markers list: https://matplotlib.org/stable/api/markers_api.html
# TODO: add ticks parameters?

def single_plot(X, Y, my_marker='None', my_color='blue', width=2, my_alpha=1,  
                x_label=None, y_label=None, my_title=None, x_fontsize=12, y_fontsize=12, 
                t_fontsize=12,  grid=False, save=False, file_name='my_fig.pdf'):
    """
    A helper function to make a simple plot
    Parameters:
    -----------
    X: list (X-axis data) [required]           
    Y: list (Y-axis data) [required]         
    my_marker: string (marker's type) [optional, default='None']
    my_color: string (color of line/markers) [optional, default='blue']           
    width: float (linewidth) [optional, default=2]
    my_alpha: float (line/marker's alpha) [optional, default=1]
    x_label: string (label of x-axis) [optional, default=None]
    y_label: string (label of y-axis) [optional, default=None]
    my_title: string (plot's title) [optional, default=None]
    x_fontsize: float (fontsize of xlabel) [optional, default=12]
    y_fontsize: float (fontsize of ylabel) [optional, default=12]
    t_fontsize: float (fontsize of title) [optional, default=12]
    grid: boolean (enable/disable grid) [optional, default=False]
    save: boolean (enable/disable save_fig) [optional, default=False]
    file_name: string (figure's file name, only used if save is True) [optional, default='my_fig.pdf']

    Returns: None
    -------
    """
    fig, ax = plt.subplots(constrained_layout=True)

    ax.plot(X, Y, marker=my_marker, color=my_color, linewidth=width, alpha=my_alpha)
    ax.set_xlabel(x_label, fontsize=x_fontsize)
    ax.set_ylabel(y_label, fontsize=y_fontsize)
    ax.set_title(my_title, fontsize=t_fontsize)

    if grid: ax.grid()
    if save: plt.savefig(file_name, bbox_inches='tight', pad_inches=0.025)

    # display
    plt.show()

# tests
if __name__ == '__main__':
    x = sorted([random.randint(0, x) for x in range(0, 100)])
    y = sorted([random.randint(0, x) for x in range(0, 100)])
    single_plot(x, y, x_label='x [m]', y_label='y [s]', my_title='$x = f(y)$', t_fontsize=20, grid=False,
                x_fontsize=20, y_fontsize=20, my_color='green', width=4, my_alpha=0.5, my_marker='o',
                save=True, file_name='test.pdf')

