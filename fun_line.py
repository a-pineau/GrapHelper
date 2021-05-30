import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

from matplotlib import rcParams
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

# markers list: https://matplotlib.org/stable/api/markers_api.html
# TODO: add ticks parameters?
def line_plot(x, y,
        xmin, xmax, ymin, ymax,
        x_label, y_label,
        label_color, label_size,
        my_legend, my_loc, legend_size, match_color,
        ticks_color, ticks_size,
        my_title, title_color, title_size,
        my_color, line_style, width, my_alpha,   
        my_marker, marker_size, marker_inner_color, marker_outer_color,
        logx, logy,
        grid, save, latex, file_name
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
    plt.rcParams['toolbar'] = 'None'
    if latex:
        rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
        rc('text', usetex=True)
    fig, ax = plt.subplots(constrained_layout=True)
    ax.plot(x, y,
            color=my_color, linestyle=line_style, linewidth=width, 
            alpha=my_alpha, label=my_legend,
            marker=my_marker, markersize=marker_size, 
            markerfacecolor=marker_inner_color,
            markeredgecolor=marker_outer_color)

    if logx: ax.semilogx()
    if logy: ax.semilogy()
    # Axes limits
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    # Label
    ax.set_xlabel(x_label, fontsize=label_size, color=label_color)
    ax.set_ylabel(y_label, fontsize=label_size, color=label_color)
    # Ticks
    ax.tick_params(axis='x', labelsize=ticks_size, colors=ticks_color)
    ax.tick_params(axis='y', labelsize=ticks_size, colors=ticks_color)

    if not logx and not logy:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
        ax.yaxis.set_minor_locator(AutoMinorLocator())

    # Title
    ax.set_title(my_title, fontsize=title_size, color=title_color)
    # Legend
    if my_legend:
        leg = ax.legend(loc=my_loc, prop={"size": legend_size})
        if match_color:
            for line, text in zip(leg.get_lines(), leg.get_texts()):
                text.set_color(line.get_color())
            for marker, text in zip(leg.get_markers(), leg.get_texts()):
                text.set_color(line.get_color())


    if grid: ax.grid()
    if save: plt.savefig(file_name, bbox_inches='tight', pad_inches=0.05)

    rc("text", usetex=False)
    # display
    fig.show()


