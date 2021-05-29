import sys
import os
import fun_line as f_line
import canvas as canvas
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, QTimer, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMessageBox, 
                             QGridLayout, QWidget, QLayout, QColorDialog, QFontDialog)

FONT_WEIGHTS = {12: "extralight", 25: "light", 50: "normal", 75: "bold", 81: "heavy"}
FIGURES_DIRECTORY = os.path.join(os.getcwd(), "figures")

class Ui_line(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GrapHelper - line Plot")
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        # Grid
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)

        # Default grid settings values
        self.dict_attr = {
          "label_color": "black", 
          "ticks_color": "black",
          "title_color": "black",
          "line_color": "blue",
          "marker_inner_color": "red",
          "marker_outer_color": "black"
        }
        self.iter_dict_attr = iter(self.dict_attr)
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
        self.groupbox_font_properties = QtWidgets.QGroupBox("Label/ticks display")
        self.vbox_font_properties = QtWidgets.QVBoxLayout()
        self.vbox_font_properties.setAlignment(QtCore.Qt.AlignCenter)
        
        iter_dict = iter(self.dict_attr)
        # Horizontal group 1 for label
        self.hlayout_font_1 = QtWidgets.QHBoxLayout()
        self.label_style = QtWidgets.QLabel("Label:")
        # Color
        self.tbutton_label_color = QtWidgets.QPushButton(text="Color")
        self.tbutton_label_color.setProperty("id", next(self.iter_dict_attr))
        self.tbutton_label_color.clicked.connect(self.set_color)
        # Label size
        self.label_size = QtWidgets.QLabel("Font size:")
        # Spinbox label size
        self.sbox_label_size = QtWidgets.QSpinBox()
        self.sbox_label_size.setMinimum(1)
        self.sbox_label_size.setMaximum(50)
        self.sbox_label_size.setValue(14)
        self.sbox_label_size.setSingleStep(1)
        # Add to horizontal layout
        self.hlayout_font_1.addWidget(self.label_style)
        self.hlayout_font_1.addWidget(self.tbutton_label_color, stretch=1)
        self.hlayout_font_1.addWidget(self.label_size)
        self.hlayout_font_1.addWidget(self.sbox_label_size)

        # Horizontal group 2 for ticks
        self.hlayout_font_2 = QtWidgets.QHBoxLayout()
        self.ticks_style = QtWidgets.QLabel("Ticks: ")
        # Color
        self.tbutton_ticks_color = QtWidgets.QPushButton(text="Color")
        self.tbutton_ticks_color.setProperty("id", next(self.iter_dict_attr))
        self.tbutton_ticks_color.clicked.connect(self.set_color)
        # Label size
        self.ticks_size = QtWidgets.QLabel("Font size:")
        # Spinbox label size
        self.sbox_ticks_size = QtWidgets.QSpinBox()
        self.sbox_ticks_size.setMinimum(1)
        self.sbox_ticks_size.setMaximum(50)
        self.sbox_ticks_size.setValue(14)
        self.sbox_ticks_size.setSingleStep(1)
        # Add to horizontal layout
        self.hlayout_font_2.addWidget(self.ticks_style)
        self.hlayout_font_2.addWidget(self.tbutton_ticks_color, stretch=1)
        self.hlayout_font_2.addWidget(self.ticks_size)
        self.hlayout_font_2.addWidget(self.sbox_ticks_size)

        # Add to local vertical layout
        self.vbox_font_properties.addLayout(self.hlayout_font_1)
        self.vbox_font_properties.addLayout(self.hlayout_font_2)

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
        self.lineedit_file_name.setEnabled(self.cbox_savefig.isChecked())
        self.cbox_file_ext.setEnabled(self.cbox_savefig.isChecked())

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

        """PLOT TITLE"""
        # Title horizontal groups
        self.hbox_plot_title_1 = QtWidgets.QHBoxLayout()
        self.hbox_plot_title_2 = QtWidgets.QHBoxLayout()
        self.label_plot_title = QtWidgets.QLabel("Plot title:")
        self.lineedit_plot_title = QtWidgets.QLineEdit("My plot")
        self.qbutton_color_title = QtWidgets.QPushButton("Color")
        self.qbutton_color_title.setProperty("id", next(self.iter_dict_attr))
        self.qbutton_color_title.clicked.connect(self.set_color)
        # Label size title
        self.label_size_title = QtWidgets.QLabel("Font size:")
        # Spinbox title size
        self.sbox_title_size = QtWidgets.QSpinBox()
        self.sbox_title_size.setMinimum(1)
        self.sbox_title_size.setMaximum(50)
        self.sbox_title_size.setValue(14)
        self.sbox_title_size.setSingleStep(1)
        # Add to plot title horizontal 1
        self.hbox_plot_title_1.addWidget(self.label_plot_title)
        self.hbox_plot_title_1.addWidget(self.lineedit_plot_title)
        # Add to plot title horizontal 2
        self.hbox_plot_title_2.addWidget(QtWidgets.QLabel("Title color:"))
        self.hbox_plot_title_2.addWidget(self.qbutton_color_title, stretch=1)
        self.hbox_plot_title_2.addWidget(self.label_size_title)
        self.hbox_plot_title_2.addWidget(self.sbox_title_size)

        """PLOT LEGEND"""
        # Plot legend horizontal group 1
        self.hbox_plot_legend_1 = QtWidgets.QHBoxLayout()
        self.hbox_plot_legend_2 = QtWidgets.QHBoxLayout()
        self.label_plot_legend = QtWidgets.QLabel("Plot legend:")
        self.lineedit_plot_legend = QtWidgets.QLineEdit("My legend")
        # Label legend font size
        self.label_legend_size = QtWidgets.QLabel("Font size:")
        # Checkbox match legend color
        self.cbox_match_legend_color = QtWidgets.QCheckBox("Match legend color")
        # Spinbox title size
        self.sbox_legend_size = QtWidgets.QSpinBox()
        self.sbox_legend_size.setMinimum(1)
        self.sbox_legend_size.setMaximum(50)
        self.sbox_legend_size.setValue(14)
        self.sbox_legend_size.setSingleStep(1)
        # Add to plot legend horizontal group 1
        self.hbox_plot_legend_1.addWidget(self.label_plot_legend)
        self.hbox_plot_legend_1.addWidget(self.lineedit_plot_legend)
        # Add to plot legend horizontal group 2
        self.hbox_plot_legend_2.addWidget(self.cbox_match_legend_color)
        self.hbox_plot_legend_2.addWidget(self.label_legend_size)
        self.hbox_plot_legend_2.addWidget(self.sbox_legend_size, stretch=1)

        """ LEGEND POSITION """
        POSITIONS = ["Best", "Upper right", "Upper left", "Lower left",
                     "Lower right", "Right", "Center left", "Center right",
                     "Lower center", "Upper center", "Center"]
        self.hbox_pos_legend = QtWidgets.QHBoxLayout()
        self.label_pos_legend = QtWidgets.QLabel("Legend position:")
        self.qcbox_pos_legend = QtWidgets.QComboBox()
        for pos in POSITIONS:
            self.qcbox_pos_legend.addItem(pos)
        self.hbox_pos_legend.addWidget(self.label_pos_legend)
        self.hbox_pos_legend.addWidget(self.qcbox_pos_legend, stretch=1)

        """LINE PROPERTIES"""
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
        self.pbutton_line_color.setEnabled(self.cbox_line.isChecked())
        self.pbutton_line_color.clicked.connect(self.set_color)
        # Add to line horizontal group 2
        self.hbox_line_properties_2.addWidget(self.label_line_style)
        self.hbox_line_properties_2.addWidget(self.cbox_line_style)
        self.hbox_line_properties_2.addWidget(self.pbutton_line_color)

        """MARKERS PROPERTIES"""
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
        self.hslider_marker_size.setEnabled(self.cbox_marker.isChecked())
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
        self.cbox_marker_style.setEnabled(self.cbox_marker.isChecked())
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
        self.pbutton_marker_inner_color.setEnabled(self.cbox_marker.isChecked())
        self.pbutton_marker_outer_color.setEnabled(self.cbox_marker.isChecked())
        # Add to marker horizontal group 3
        self.hbox_marker_properties_3.addWidget(self.pbutton_marker_inner_color)
        self.hbox_marker_properties_3.addWidget(self.pbutton_marker_outer_color)
        
        """ALPHA"""
        # Horizontal alpha group
        self.hbox_alpha = QtWidgets.QHBoxLayout()
        # Horizontal slider alpha
        self.hslider_alpha = QtWidgets.QSlider()
        self.hslider_alpha.setObjectName("slider_alpha")
        self.hslider_alpha.setOrientation(QtCore.Qt.Horizontal)
        self.hslider_alpha.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.hslider_alpha.setMinimum(0)
        self.hslider_alpha.setMaximum(10)
        self.hslider_alpha.setTickInterval(1)
        self.hslider_alpha.setSliderPosition(10)
        self.hslider_alpha.valueChanged.connect(self.set_slider_label)
        # Alpha label
        slider_value = self.hslider_alpha.value()
        self.label_alpha = QtWidgets.QLabel(f"Alpha: {slider_value/10}")
        # Add to horizontal alpha group
        self.hbox_alpha.addWidget(self.label_alpha)
        self.hbox_alpha.addWidget(self.hslider_alpha)

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
        self.vbox_plot_settings.addLayout(self.hbox_alpha)

        # Add to vertical layout
        self.group_plot_settings.setLayout(self.vbox_plot_settings)
        return self.group_plot_settings

    def set_open_data_gbox(self):
        GROUP_LABELS = ["Open file", "Add data"]
        GROUP_CMDS = [self.browse_file, self.open_data_frame]
        self.group_import_data = QtWidgets.QGroupBox("Import data")
        self.group_import_data.setFixedHeight(120)
        self.v_import_data = QtWidgets.QHBoxLayout()
        self.v_import_data.setAlignment(QtCore.Qt.AlignCenter)
        for i in range(len(GROUP_LABELS)):
            Pbutton_plot = QtWidgets.QPushButton(f"{GROUP_LABELS[i]}")
            Pbutton_plot.clicked.connect(GROUP_CMDS[i])
            size_policy = Pbutton_plot.sizePolicy()
            size_policy.setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
            size_policy.setVerticalPolicy(QtWidgets.QSizePolicy.Expanding)
            Pbutton_plot.setSizePolicy(size_policy)
            # Add to vertical layout
            self.v_import_data.addWidget(Pbutton_plot)
             
        self.group_import_data.setLayout(self.v_import_data)
        return self.group_import_data

    def set_actions_gbox(self):  
        GROUP_LABELS = ["Plot data", "Test case"]
        GROUP_CMDS = [self.browse_file, self.test_case]
        self.group_actions = QtWidgets.QGroupBox("Actions")
        self.v_actions = QtWidgets.QHBoxLayout()
        self.v_actions.setAlignment(QtCore.Qt.AlignCenter)
        for i in range(len(GROUP_LABELS)):
            Pbutton_plot = QtWidgets.QPushButton(GROUP_LABELS[i])
            Pbutton_plot.clicked.connect(GROUP_CMDS[i])
            size_policy = Pbutton_plot.sizePolicy()
            size_policy.setHorizontalPolicy(QtWidgets.QSizePolicy.Expanding)
            size_policy.setVerticalPolicy(QtWidgets.QSizePolicy.Expanding)
            Pbutton_plot.setSizePolicy(size_policy)
            # Add to vertical layout
            self.v_actions.addWidget(Pbutton_plot)

        self.group_actions.setLayout(self.v_actions)
        return self.group_actions

    """ 
    ### CONNECTED METHODS 
    """
    @pyqtSlot()
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

    @pyqtSlot()
    def set_color(self):
        pbutton = self.sender()
        color = QColorDialog.getColor()
        if color.isValid():
            self.dict_attr[pbutton.property("id")] = color.name()
            pbutton.setStyleSheet(f"background-color: {color.name()};")

    @pyqtSlot()
    def set_font(self):
        pbutton = self.sender()
        font, font_selected = QFontDialog.getFont()
        if font_selected:
            self.dict_attr[pbutton.property("id")] = font

    @pyqtSlot()
    def set_slider_label(self):
        name = self.sender().objectName()
        slider_value = self.sender().value()
        if name == "slider_line_width":
            self.label_line_width.setText(f"Width: {slider_value}")
        elif name == "slider_marker_size":
            self.label_marker_size.setText(f"Size: {slider_value}")
        elif name == "slider_alpha":
            self.label_alpha.setText(f'Alpha: {slider_value/10}')

    @pyqtSlot()
    def open_data_frame(self):
        pass

    """PLOT METHODS"""
    @pyqtSlot()
    def test_case(self):
        """INITIALIZE ALL THE NEEDED VALUES FIRST"""
        # Plot title
        plot_title = self.lineedit_plot_title.text()
        # Plot legend
        plot_legend = self.lineedit_plot_legend.text()
        # Plot legend location
        plot_legend_location = self.qcbox_pos_legend.currentText().lower()
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
        label_color = self.dict_attr["label_color"]
        ticks_color = self.dict_attr["ticks_color"]
        title_color = self.dict_attr["title_color"]
        # Label, ticks, title, legend sizes
        label_size = self.sbox_label_size.value()
        ticks_size = self.sbox_ticks_size.value()
        title_size = self.sbox_title_size.value()
        legend_size = self.sbox_legend_size.value()
        # Check boxes data
        latex = self.box_latex.isChecked()
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
        # Alpha
        alpha = self.hslider_alpha.value()/10
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

        x = sorted([random.randint(0, 200) for _ in range(0, 150)])
        y = sorted([random.randint(0, 200) for _ in range(0, 150)])
        """ FINALLY PLOTS THE DATA """
        f_line.line_plot(
                x, y, 
                x_min, x_max, y_min, y_max,
                xlabel, ylabel,
                label_color, label_size,
                plot_legend, plot_legend_location, legend_size,
                ticks_color, ticks_size,
                plot_title, title_color, title_size,
                line_color, line_style, line_width, alpha,
                marker_style, marker_size,
                marker_inner_color, marker_outer_color,
                grid, save_fig, latex, FILE_PATH
            )

    """STATIC METHODS"""
    @staticmethod
    def browse_file():
        USER = os.environ['USERPROFILE']
        DESK = os.path.join(USER, "Desktop")
        data_file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open File", DESK, '*.txt')
        if data_file:
            return data_file    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Ui_line()
    win.show()
    app.setStyle("Breeze")
    print(QtWidgets.QStyleFactory.keys())
    sys.exit(app.exec_())

