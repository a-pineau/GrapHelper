import random
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rcParams
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# markers list: https://matplotlib.org/stable/api/markers_api.html
# TODO: add ticks parameters?
def line_plot(x, y,
                xmin, xmax, ymin, ymax,
                x_label, y_label, font_label, 
                my_legend, my_loc,
                xticks_size, yticks_size,
                xticks_color, yticks_color,
                my_title, font_title,
                my_color, line_style, width, my_alpha,   
                my_marker, marker_size, marker_inner_color, marker_outer_color,
                grid, save, file_name
                ):
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

    ax.plot(x, y,
            color=my_color, linestyle=line_style, linewidth=width, 
            alpha=my_alpha,
            marker=my_marker, markersize=marker_size, 
            markerfacecolor=marker_inner_color,
            markeredgecolor=marker_outer_color)
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel(x_label, fontdict=font_label)
    ax.set_ylabel(y_label, fontdict=font_label)
    ax.set_title(my_title, fontdict=font_title)
    ax.legend([my_legend], loc=my_loc)

    ax.tick_params(axis='x', labelsize=xticks_size, colors=xticks_color)
    ax.tick_params(axis='y', labelsize=yticks_size, colors=yticks_color)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())

    if grid: ax.grid()
    if save: plt.savefig(file_name, bbox_inches='tight', pad_inches=0.05)

    # display
    plt.show()

# tests
if __name__ == '__main__':
    x = sorted([random.randint(0, x) for x in range(0, 100)])
    y = sorted([random.randint(0, x) for x in range(0, 100)])
    font = {'family': 'serif',
    'color':  'darkred',
    'weight': 'heavy',
    'size': 16,
    }
    line_plot(x, y, 
                None, None, None, None,
                x_label='x [m]', y_label='y [s]', font_label=font, 
                my_legend="My legend", my_loc="best",
                xticks_size=font["size"], yticks_size=font["size"], 
                xticks_color="red", yticks_color="blue",
                my_title='$x = f(y)$', font_title=font,
                my_color='green', line_style="dotted", width=4, my_alpha=0.5,
                my_marker="*", marker_size=20, marker_inner_color="blue",
                marker_outer_color="black",
                grid=False, save=True, file_name='test.pdf')

