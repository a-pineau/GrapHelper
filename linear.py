import sys
import os
import fun_linear as f_lin
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMessageBox, 
                             QGridLayout, QWidget, QLayout, QColorDialog, QFontDialog)

FONT_WEIGHTS = {12: "extralight", 25: "light", 50: "normal", 75: "bold", 81: "heavy"}
FIGURES_DIRECTORY = os.path.join(os.getcwd(), "figures")

def browse_file():
    USER = os.environ['USERPROFILE']
    DESK = os.path.join(USER, "Desktop")
    data_file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open File", DESK, '*.txt')
    if data_file:
        return data_file

class Ui_Linear(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GrapHelper - Linear Plot")
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)

        # Default grid settings values
        default_font = QtGui.QFont()
        default_font.setFamily("Times")
        default_font.setPointSize(16)
        self.dict_attr = {
          "label_color": "black", 
          "label_font": default_font,
          "ticks_color": "black",
          "ticks_font": default_font,
          "title_color": "black",
          "title_font": default_font,
          "legend_color": "black",
          "legend_font": default_font,
          "line_color": "blue",
          "marker_inner_color": "red",
          "marker_outer_color": "black"
        }

        # Grid settings and miscs.
        self.grid_layout.addWidget(self.set_grid_settings_gbox(), 0, 0)
        # Plot settings
        self.grid_layout.addWidget(self.set_plot_settings_gbox(), 0, 1)
        # Import data
        self.grid_layout.addWidget(self.set_open_data_gbox(),     1, 0)
        # Actions
        self.grid_layout.addWidget(self.set_actions_gbox(),       1, 1)
         
    """ 
    ### SETUP METHODS 
    """
    def set_grid_settings_gbox(self):
        self.group_box = QtWidgets.QGroupBox("Grid settings and miscellaneous")
        self.v_box = QtWidgets.QVBoxLayout()
        # Show grid
        self.box_grid = QtWidgets.QCheckBox("Show grid")
        # LaTeX text rendering
        self.box_latex = QtWidgets.QCheckBox("LaTeX text rendering (requires a LaTeX installation)")
        # Log scale horizontal group
        self.h_group_logscale = QtWidgets.QHBoxLayout()
        self.box_xlogscale = QtWidgets.QCheckBox("Logarithmic scale x-axis")
        self.box_ylogscale = QtWidgets.QCheckBox("Logarithmic scale y-axis")
        self.h_group_logscale.addWidget(self.box_xlogscale)
        self.h_group_logscale.addWidget(self.box_ylogscale)
        # x axis label horizontal group
        self.hgroup_xaxis_label = QtWidgets.QHBoxLayout()
        # x-axis label
        self.label_xaxis = QtWidgets.QLabel("x-axis label:")
        self.hgroup_xaxis_label.addWidget(self.label_xaxis)
        # x-axis label line edit
        self.lineedit_xaxis_label = QtWidgets.QLineEdit("My x label")
        self.hgroup_xaxis_label.addWidget(self.lineedit_xaxis_label)
        # y axis label horizontal group
        self.hgroup_yaxis_label = QtWidgets.QHBoxLayout()
        # y-axis label
        self.label_yaxis = QtWidgets.QLabel("y-axis label:")
        self.hgroup_yaxis_label.addWidget(self.label_yaxis)
        # y-axis label line edit
        self.lineedit_yaxis_label = QtWidgets.QLineEdit("My y label")
        self.hgroup_yaxis_label.addWidget(self.lineedit_yaxis_label)
        # x limits horizontal group
        self.hgroup_x_limits = QtWidgets.QHBoxLayout()
        # x limits (min/max) label
        self.label_x_limits = QtWidgets.QLabel("x limits (min/max)")
        # x limits (min) values lineedit
        self.lineedit_x_min = QtWidgets.QLineEdit()
        # x limits (max) values lineedit
        self.lineedit_x_max = QtWidgets.QLineEdit()
        # Add to x limits horizontal group
        self.hgroup_x_limits.addWidget(self.label_x_limits)
        self.hgroup_x_limits.addWidget(self.lineedit_x_min)
        self.hgroup_x_limits.addWidget(self.lineedit_x_max)
        # y limits horizontal group
        self.hgroup_y_limits = QtWidgets.QHBoxLayout()
        # y limits (min/max) label
        self.label_y_limits = QtWidgets.QLabel("y limits (min/max)")
        # y limits (min) values lineedit
        self.lineedit_y_min = QtWidgets.QLineEdit()
        # y limits (max) values lineedit
        self.lineedit_y_max = QtWidgets.QLineEdit()
        # Add to y limits horizontal group
        self.hgroup_y_limits.addWidget(self.label_y_limits)
        self.hgroup_y_limits.addWidget(self.lineedit_y_min)
        self.hgroup_y_limits.addWidget(self.lineedit_y_max)
        # Add to vertical layout
        self.v_box.addWidget(self.box_grid)
        self.v_box.addWidget(self.box_latex)
        self.v_box.addLayout(self.h_group_logscale)
        self.v_box.addLayout(self.hgroup_xaxis_label)
        self.v_box.addLayout(self.hgroup_yaxis_label)
        self.v_box.addLayout(self.hgroup_x_limits)
        self.v_box.addLayout(self.hgroup_y_limits)
        # Font labels/ticks properties
        FONT_LABELS = ["Label", "Ticks"]
        TBUTTON_WIDTH = 120

        self.tbuttons_color, self.tbuttons_font = [], []
        self.groupbox_font_properties = QtWidgets.QGroupBox("Label/ticks display")
        self.vbox_font_properties = QtWidgets.QVBoxLayout()
        self.iter_dict_attr = iter(self.dict_attr.keys())
        
        for elem in FONT_LABELS:
            hlayout_font = QtWidgets.QHBoxLayout()
            label_font = QtWidgets.QLabel(f"{elem} style:")
            # Color
            tbutton_color = QtWidgets.QPushButton(text="Color")
            tbutton_color.setFixedWidth(TBUTTON_WIDTH)
            tbutton_color.setProperty("id", next(self.iter_dict_attr))
            tbutton_color.clicked.connect(self.set_color)
            # Font
            tbutton_font = QtWidgets.QPushButton(text="Font")
            tbutton_font.setFixedWidth(TBUTTON_WIDTH)
            tbutton_font.setProperty("id", next(self.iter_dict_attr))
            tbutton_font.clicked.connect(self.set_font)
            # Add to horizontal layout
            hlayout_font.addWidget(label_font)
            hlayout_font.addWidget(tbutton_color)
            hlayout_font.addWidget(tbutton_font)
            self.tbuttons_font.append(tbutton_font)
            # Add to local vertical layout
            self.vbox_font_properties.addLayout(hlayout_font)

        # Save figure
        self.cbox_savefig = QtWidgets.QCheckBox("Save figure to current directory")
        self.cbox_savefig.clicked.connect(self.change_state)
        # File name
        self.hbox_file_name_ext = QtWidgets.QHBoxLayout()
        self.label_file_name = QtWidgets.QLabel("File name:")
        self.lineedit_file_name = QtWidgets.QLineEdit()
        self.hbox_file_name_ext.addWidget(self.label_file_name)
        self.hbox_file_name_ext.addWidget(self.lineedit_file_name)
        # File extension
        EXTENSIONS = ["PDF", "JPG", "PNG", "BMP"]
        self.label_file_ext = QtWidgets.QLabel("Extension:")
        self.cbox_file_ext = QtWidgets.QComboBox()
        for ext in EXTENSIONS:
            self.cbox_file_ext.addItem(ext)
        self.hbox_file_name_ext.addWidget(self.label_file_ext)
        self.hbox_file_name_ext.addWidget(self.cbox_file_ext)
        if not self.cbox_savefig.isChecked():
            self.lineedit_file_name.setEnabled(False)
            self.cbox_file_ext.setEnabled(False)

        # Add to group and to main vertical layout
        self.groupbox_font_properties.setLayout(self.vbox_font_properties)
        self.v_box.addWidget(self.groupbox_font_properties)
        self.v_box.addWidget(self.cbox_savefig)
        self.v_box.addLayout(self.hbox_file_name_ext)
        self.group_box.setLayout(self.v_box)
        return self.group_box

    def set_plot_settings_gbox(self):
        self.group_plot_settings = QtWidgets.QGroupBox("Plot settings")
        self.vbox_plot_settings = QtWidgets.QVBoxLayout()
        self.grid_line_marker = QtWidgets.QGridLayout()
        """ PLOT'S TITLE """
        # Title horizontal groups
        self.hbox_plot_title_1 = QtWidgets.QHBoxLayout()
        self.hbox_plot_title_2 = QtWidgets.QHBoxLayout()
        self.label_plot_title = QtWidgets.QLabel("Plot title:")
        self.lineedit_plot_title = QtWidgets.QLineEdit("My plot")
        self.qbutton_color_title = QtWidgets.QPushButton("Color")
        self.qbutton_color_title.setProperty("id", next(self.iter_dict_attr))
        self.qbutton_color_title.clicked.connect(self.set_color)
        self.qbutton_font_title = QtWidgets.QPushButton("Font")
        self.qbutton_font_title.setProperty("id", next(self.iter_dict_attr))
        self.qbutton_font_title.clicked.connect(self.set_font)
        # Add to plot title horizontal 1
        self.hbox_plot_title_1.addWidget(self.label_plot_title)
        self.hbox_plot_title_1.addWidget(self.lineedit_plot_title)
        # Add to plot title horizontal 2
        self.hbox_plot_title_2.addWidget(QtWidgets.QLabel("Title display:"))
        self.hbox_plot_title_2.addWidget(self.qbutton_color_title)
        self.hbox_plot_title_2.addWidget(self.qbutton_font_title)
        """ PLOT LEGEND """
        # Plot legend horizontal group 1
        self.hbox_plot_legend_1 = QtWidgets.QHBoxLayout()
        self.hbox_plot_legend_2 = QtWidgets.QHBoxLayout()
        self.label_plot_legend = QtWidgets.QLabel("Plot legend:")
        self.lineedit_plot_legend = QtWidgets.QLineEdit("My legend")
        self.qbutton_color_legend = QtWidgets.QPushButton("Color")
        self.qbutton_color_legend.setProperty("id", next(self.iter_dict_attr))
        self.qbutton_color_legend.clicked.connect(self.set_color)
        self.qbutton_font_legend = QtWidgets.QPushButton("Font")
        self.qbutton_font_legend.setProperty("id", next(self.iter_dict_attr))
        self.qbutton_font_legend.clicked.connect(self.set_font)
        # Add to plot legend horizontal group 1
        self.hbox_plot_legend_1.addWidget(self.label_plot_legend)
        self.hbox_plot_legend_1.addWidget(self.lineedit_plot_legend)
        # Add to plot legend horizontal group 2
        self.hbox_plot_legend_2.addWidget(QtWidgets.QLabel("Legend display:"))
        self.hbox_plot_legend_2.addWidget(self.qbutton_color_legend)
        self.hbox_plot_legend_2.addWidget(self.qbutton_font_legend)

        """ LEGEND POSITION """
        POSITIONS = ["Best", "Upper right", "Upper left", "Lower left",
                     "Lower right", "Right", "Center left", "Center right",
                     "Lower center", "Upper center", "Center"]
        self.hbox_pos_legend = QtWidgets.QHBoxLayout()
        self.label_pos_legend = QtWidgets.QLabel("Legend position:")
        self.qcbox_pos_legend = QtWidgets.QComboBox()
        self.qcbox_pos_legend.setFixedWidth(202)
        for pos in POSITIONS:
            self.qcbox_pos_legend.addItem(pos)
        self.hbox_pos_legend.addWidget(self.label_pos_legend)
        self.hbox_pos_legend.addWidget(self.qcbox_pos_legend)

        """ LINE PROPERTIES """
        # Line horizontal groups
        self.hbox_line_properties_1 = QtWidgets.QHBoxLayout()
        self.hbox_line_properties_2 = QtWidgets.QHBoxLayout()
        # Line
        self.cbox_line = QtWidgets.QCheckBox("Line")
        self.cbox_line.setObjectName("Line")
        self.cbox_line.clicked.connect(self.change_state)
        self.cbox_line.setCheckState(QtCore.Qt.Checked)
        # Line width horizontal slider
        self.hslider_line_width = QtWidgets.QSlider()
        self.hslider_line_width.setObjectName("slider_line_width")
        self.hslider_line_width.setOrientation(QtCore.Qt.Horizontal)
        self.hslider_line_width.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.hslider_line_width.setMinimum(1)
        self.hslider_line_width.setMaximum(10)
        self.hslider_line_width.setSliderPosition(3)
        self.hslider_line_width.setTickInterval(1)
        self.hslider_line_width.valueChanged.connect(self.set_slider_label)
        # Line width label
        slider_value = self.hslider_line_width.value()
        self.label_line_width = QtWidgets.QLabel(f"Width: {slider_value}")
        # Add to line horizontal group 1
        self.hbox_line_properties_1.addWidget(self.cbox_line)
        self.hbox_line_properties_1.addWidget(self.label_line_width)
        self.hbox_line_properties_1.addWidget(self.hslider_line_width)
        # Line style label
        self.label_line_style = QtWidgets.QLabel("Line style:")
        # Line width combo box
        LINE_STYLES = ["Solid", "Dotted", "Dashed", "Dashdot"]
        self.cbox_line_style = QtWidgets.QComboBox()
        for line_style in LINE_STYLES:
            self.cbox_line_style.addItem(line_style)
        self.cbox_line_style.setFixedWidth(130)
        # Line colors
        self.pbutton_line_color = QtWidgets.QPushButton("Line color")
        self.pbutton_line_color.setFixedWidth(110)
        color = self.dict_attr["line_color"]
        self.pbutton_line_color.setStyleSheet(f"background-color: {color};")
        self.pbutton_line_color.setProperty("id", next(self.iter_dict_attr))
        if self.cbox_line.isChecked() == False:
            self.pbutton_line_color.setEnabled(False)
        self.pbutton_line_color.clicked.connect(self.set_color)
        # Add to line horizontal group 2
        self.hbox_line_properties_2.addWidget(self.label_line_style)
        self.hbox_line_properties_2.addWidget(self.cbox_line_style)
        self.hbox_line_properties_2.addWidget(self.pbutton_line_color)

        """ MARKERS PROPERTIES """
        # Marker horizontal groups
        self.hbox_marker_properties_1 = QtWidgets.QHBoxLayout()
        self.hbox_marker_properties_2 = QtWidgets.QHBoxLayout()
        self.hbox_marker_properties_3 = QtWidgets.QHBoxLayout()
        # Markers
        self.cbox_marker = QtWidgets.QCheckBox("Markers")
        self.cbox_marker.clicked.connect(self.change_state)
        self.cbox_marker.setCheckState(QtCore.Qt.Unchecked)
        # Marker size horizontal slider
        self.hslider_marker_size = QtWidgets.QSlider()
        self.hslider_marker_size.setObjectName("slider_marker_size")
        self.hslider_marker_size.setOrientation(QtCore.Qt.Horizontal)
        self.hslider_marker_size.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.hslider_marker_size.setMinimum(1)
        self.hslider_marker_size.setMaximum(20)
        self.hslider_marker_size.setTickInterval(1)
        self.hslider_marker_size.valueChanged.connect(self.set_slider_label)
        # Marker size label
        value = self.hslider_marker_size.value()
        self.label_marker_size = QtWidgets.QLabel(f"Size: {value}")
        # Add to line horizontal group 1
        self.hbox_marker_properties_1.addWidget(self.cbox_marker)
        self.hbox_marker_properties_1.addWidget(self.label_marker_size)
        self.hbox_marker_properties_1.addWidget(self.hslider_marker_size)
        # Marker style label
        self.label_marker_style = QtWidgets.QLabel("Style:")
        # Marker style
        self.cbox_marker_style = QtWidgets.QComboBox()
        self.cbox_marker_style.setFixedWidth(270)
        if self.cbox_marker.isChecked() == False:
            self.cbox_marker_style.setEnabled(False)
        self.MARKER_STYLES = {"Point": ".", 
            "Pixel": ",", 
            "Circle": "o", 
            "Triangle down": "v",
            "Triangle up": "^", 
            "Triangle left": "<", 
            "Triangle right": ">", 
            "Octagon": "8", 
            "Square": "s",
            "Pentagon": "p", 
            "Plus (filled)": "P", 
            "Star": "*", 
            "Hexagon 1": "h", 
            "Hexagon 2": "H",
            "Plus": "+",
            "x": "x",
            "x (filled)": "X",
            "Diamond": "D",
            "Thin diamond": "d",
            "Caret left": 4,
            "Caret right": 5,
            "Caret up": 6,
            "Caret down": 7
        }
        for marker_style in self.MARKER_STYLES.keys():
            self.cbox_marker_style.addItem(marker_style)
        # Add to marker horizontal group 2
        self.hbox_marker_properties_2.addWidget(self.label_marker_style)
        self.hbox_marker_properties_2.addWidget(self.cbox_marker_style)
        # Marker innter color
        self.pbutton_marker_inner_color = QtWidgets.QPushButton("Marker inner color")
        self.pbutton_marker_inner_color.setProperty("id", next(self.iter_dict_attr))
        self.pbutton_marker_inner_color.clicked.connect(self.set_color)
        self.pbutton_marker_outer_color = QtWidgets.QPushButton("Marker outer color")
        self.pbutton_marker_outer_color.setProperty("id", next(self.iter_dict_attr))
        self.pbutton_marker_outer_color.clicked.connect(self.set_color)
        if self.cbox_marker.isChecked() == False:
            self.pbutton_marker_inner_color.setEnabled(False)
            self.pbutton_marker_outer_color.setEnabled(False)
        # Add to marker horizontal group 3
        self.hbox_marker_properties_3.addWidget(self.pbutton_marker_inner_color)
        self.hbox_marker_properties_3.addWidget(self.pbutton_marker_outer_color)
        
        # Add to vertical box
        self.vbox_plot_settings.addLayout(self.hbox_plot_title_1)
        self.vbox_plot_settings.addLayout(self.hbox_plot_title_2)
        self.vbox_plot_settings.addLayout(self.hbox_plot_legend_1)
        self.vbox_plot_settings.addLayout(self.hbox_plot_legend_2)
        self.vbox_plot_settings.addLayout(self.hbox_pos_legend)
        self.vbox_plot_settings.addLayout(self.hbox_line_properties_1)
        self.vbox_plot_settings.addLayout(self.hbox_line_properties_2)
        self.vbox_plot_settings.addLayout(self.hbox_marker_properties_1)
        self.vbox_plot_settings.addLayout(self.hbox_marker_properties_2)
        self.vbox_plot_settings.addLayout(self.hbox_marker_properties_3)

        # Add to vertical layout
        self.group_plot_settings.setLayout(self.vbox_plot_settings)
        return self.group_plot_settings

    def set_open_data_gbox(self):
        GROUP_LABELS = ["Open file", "Add data"]
        GROUP_CMDS = [browse_file, browse_file]
        BUTTON_W, BUTTON_H = 170, 80
        self.group_import_data = QtWidgets.QGroupBox("Import data")
        self.group_import_data.setFixedHeight(120)
        self.v_import_data = QtWidgets.QHBoxLayout()
        self.v_import_data.setAlignment(QtCore.Qt.AlignCenter)
        for i in range(len(GROUP_LABELS)):
            Pbutton_plot = QtWidgets.QPushButton(f"{GROUP_LABELS[i]}")
            Pbutton_plot.setFixedSize(BUTTON_W, BUTTON_H)
            Pbutton_plot.clicked.connect(GROUP_CMDS[i])
            # Add to vertical layout
            self.v_import_data.addWidget(Pbutton_plot)
             
        self.group_import_data.setLayout(self.v_import_data)
        return self.group_import_data

    def set_actions_gbox(self):  
        GROUP_LABELS = ["Plot data", "Test case"]
        GROUP_CMDS = [browse_file, self.test_case]
        BUTTON_W, BUTTON_H = 150, 80
        self.group_actions = QtWidgets.QGroupBox("Actions")
        self.group_actions.setFixedHeight(120)
        self.v_actions = QtWidgets.QHBoxLayout()
        self.v_actions.setAlignment(QtCore.Qt.AlignCenter)
        for i in range(len(GROUP_LABELS)):
            Pbutton_plot = QtWidgets.QPushButton(GROUP_LABELS[i])
            Pbutton_plot.setFixedSize(BUTTON_W, BUTTON_H)
            Pbutton_plot.clicked.connect(GROUP_CMDS[i])
            # Add to vertical layout
            self.v_actions.addWidget(Pbutton_plot)

        self.group_actions.setLayout(self.v_actions)
        return self.group_actions

    """ 
    ### CONNECTED METHODS 
    """
    def change_state(self):
        sender = self.sender()
        state = sender.isChecked()
        name = sender.text()
        if name == "Line":
            self.hslider_line_width.setEnabled(state)
            self.cbox_line_style.setEnabled(state)
            self.pbutton_line_color.setEnabled(state)
        elif name == "Markers":
            self.hslider_marker_size.setEnabled(state)
            self.cbox_marker_style.setEnabled(state)
            self.pbutton_marker_inner_color.setEnabled(state)
            self.pbutton_marker_outer_color.setEnabled(state)
        elif name == "Save figure to current directory":
            self.cbox_file_ext.setEnabled(state)
            self.lineedit_file_name.setEnabled(state)

    def set_color(self):
        pbutton = self.sender()
        color = QColorDialog.getColor()
        if color.isValid():
            self.dict_attr[pbutton.property("id")] = color.name()
            pbutton.setStyleSheet(f"background-color: {color.name()};")

    def set_font(self):
        pbutton = self.sender()
        font, font_selected = QFontDialog.getFont()
        if font_selected:
            self.dict_attr[pbutton.property("id")] = font

    def set_slider_label(self):
        name = self.sender().objectName()
        value = self.sender().value()
        if name == "slider_line_width":
            self.label_line_width.setText(f"Width: {value}")
        else:
            self.label_marker_size.setText(f"Size: {value}")

    """ PLOT METHODS """
    def test_case(self):
        """ INITIALIZE ALL THE NEEDED VALUES FIRST """
        # Plit title
        plot_title = self.lineedit_plot_title.text()
        # Plot legend
        plot_legend = self.lineedit_plot_legend.text()
        # x and y labels
        xlabel = self.lineedit_xaxis_label.text()
        ylabel = self.lineedit_yaxis_label.text()
        # Axes limits
        x_min = self.lineedit_x_min.text()
        x_max = self.lineedit_x_max.text()
        y_min = self.lineedit_y_min.text()
        y_max = self.lineedit_y_max.text()
        if all(item.isdigit() for item in [x_min, x_max, y_min, y_max]):
            x_min, x_max = int(x_min), int(x_max)
            y_min, y_max = int(y_min), int(y_max)
        else:
            x_min = x_max = y_min = y_max = None
        # Dict data
        label_font = self.dict_attr["label_font"]
        label_color = self.dict_attr["label_color"]
        ticks_font = self.dict_attr["ticks_font"]
        ticks_color = self.dict_attr["ticks_color"]
        title_font = self.dict_attr["title_font"]
        title_color = self.dict_attr["title_color"]
        legend_font = self.dict_attr["legend_font"]
        legend_color = self.dict_attr["legend_color"]
        # Defining dict for matplotlib compatibility
        dict_label_font = {'family': label_font.family(),
           'color':  label_color,
           'weight': FONT_WEIGHTS[label_font.weight()],
           'size':   label_font.pointSize()
           }
        dict_title_font = {'family': title_font.family(),
           'color':  title_color,
           'weight': FONT_WEIGHTS[title_font.weight()],
           'size':   title_font.pointSize()
           }
        # Unused?
        dict_legend_font = {'family': legend_font.family(),
           'color':  legend_color,
           'weight': FONT_WEIGHTS[legend_font.weight()],
           'size':   legend_font.pointSize()
           }
        # ticks font cannot be set using a dictionnary in matplotlib
        xticks_size = yticks_size = ticks_font.pointSize()
        xticks_color = yticks_color = ticks_color
        # Check boxes data
        grid = self.box_grid.isChecked()
        save_fig = self.cbox_savefig.isChecked()
        # Line style
        if self.cbox_line.isChecked():
            line_style = self.cbox_line_style.currentText().lower()
            line_width = self.hslider_line_width.value()
            line_color = self.dict_attr["line_color"]
        else:
            line_style = line_width = line_color = None
        # Markers style
        if self.cbox_marker.isChecked():
            current_marker_style = self.cbox_marker_style.currentText()
            marker_style = self.MARKER_STYLES[current_marker_style]
            marker_size = self.hslider_marker_size.value()
            marker_inner_color = self.dict_attr["marker_inner_color"]
            marker_outer_color = self.dict_attr["marker_outer_color"]
        else:
            marker_style = marker_size = None
            marker_inner_color = marker_outer_color = None
        # File name
        if save_fig:
            file_name = self.lineedit_file_name.text()
            file_ext = self.cbox_file_ext.currentText()
            full_file_name = f"{file_name}.{file_ext}"
            FILE_PATH = os.path.join(FIGURES_DIRECTORY, full_file_name)
            if not os.path.exists(FIGURES_DIRECTORY):
                os.mkdir(FIGURES_DIRECTORY)
        else:
            FILE_PATH = None


        x = sorted([random.randint(0, x) for x in range(0, 100)])
        y = sorted([random.randint(0, x) for x in range(0, 100)])
        """ FINALLY PLOTS THE DATA """
        f_lin.single_plot(x, y, 
                          x_min, x_max, y_min, y_max,
                          xlabel, ylabel, dict_label_font,
                          xticks_size, yticks_size,
                          xticks_color, yticks_color,
                          plot_title, dict_title_font, 
                          line_color, line_style, line_width, 1, 
                          marker_style, marker_size,
                          marker_inner_color, marker_outer_color,
                          grid, save_fig, FILE_PATH
                          )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Ui_Linear()
    win.show()
    sys.exit(app.exec_())

