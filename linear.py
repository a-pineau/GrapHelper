import sys
import os
import fun_linear as fun_linear
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMessageBox, 
                             QGridLayout, QWidget, QLayout, QColorDialog)


def browse_file():
    USER = os.environ['USERPROFILE']
    DESK = os.path.join(USER, "Desktop")
    data_file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open File", DESK, '*.txt')
    if data_file:
        return data_file

class Ui_Linear(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GrapHelper - Linear Plot")
        self.setObjectName("self")
        self.resize(400, 350)
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.addWidget(self.set_group_settings_gbox(), 0, 0)
        self.grid_layout.addWidget(self.set_group_settings_gbox(), 0, 1)
        self.grid_layout.addWidget(self.set_open_data_gbox(),      1, 0)
        self.grid_layout.addWidget(self.set_actions_gbox(),        1, 1)

    def test(self):
        # x = sorted([random.randint(0, x) for x in range(0, 100)])
        # y = sorted([random.randint(0, x) for x in range(0, 100)])
        savefig = self.box_savefig.isChecked()
        grid = self.box_grid.isChecked()
        # fun_linear.single_plot(x, y, x_label='x [m]', y_label='y [s]', my_title='$x = f(y)$', t_fontsize=20, grid=grid,
        #         x_fontsize=20, y_fontsize=20, my_color='green', width=4, my_alpha=0.5, my_marker='o',
        #         save=savefig, file_name='test.pdf')
         
    def set_group_settings_gbox(self):
        self.group_box = QtWidgets.QGroupBox("Grid settings and miscs.")
        self.v_box = QtWidgets.QVBoxLayout()
        self.box_savefig = QtWidgets.QCheckBox("Save figure to desktop")
        self.box_grid = QtWidgets.QCheckBox("Show grid")
        # Add to vertical layout
        self.v_box.addWidget(self.box_savefig)
        self.v_box.addWidget(self.box_grid)
        self.group_box.setLayout(self.v_box)
        return self.group_box

    def set_open_data_gbox(self):
        self.group_open_data = QtWidgets.QGroupBox("Import data")
        self.v_button = QtWidgets.QVBoxLayout()
        self.v_button.setAlignment(QtCore.Qt.AlignCenter)
        # Open file
        self.Pbutton_openf = QtWidgets.QPushButton()
        self.Pbutton_openf.setFixedSize(150, 50)
        self.Pbutton_openf.clicked.connect(browse_file)
        self.Pbutton_openf.setText("Open file")
        # Data manually
        self.Pbutton_datam = QtWidgets.QPushButton()
        self.Pbutton_datam.setFixedSize(150, 50)
        self.Pbutton_datam.clicked.connect(browse_file)
        self.Pbutton_datam.setText("Add data")
        # Add to vertical layout
        self.v_button.addWidget(self.Pbutton_openf)
        self.v_button.addWidget(self.Pbutton_datam)
        # Add to box
        self.group_open_data.setLayout(self.v_button)
        return self.group_open_data

    def set_actions_gbox(self):  
        self.group_actions = QtWidgets.QGroupBox("Actions")
        self.v_actions = QtWidgets.QVBoxLayout()
        self.v_actions.setAlignment(QtCore.Qt.AlignCenter)
        # Plot
        self.Pbutton_plot = QtWidgets.QPushButton()
        self.Pbutton_plot.setFixedSize(150, 50)
        self.Pbutton_plot.clicked.connect(browse_file)
        self.Pbutton_plot.setText("Plot data")
        # Reset
        self.Pbutton_reset = QtWidgets.QPushButton()
        self.Pbutton_reset.setFixedSize(150, 50)
        self.Pbutton_reset.clicked.connect(self.reset_settings)
        self.Pbutton_reset.setText("Reset to default settings")
        # Add to vertical layout
        self.v_actions.addWidget(self.Pbutton_plot)
        self.v_actions.addWidget(self.Pbutton_reset)
        # Add to box
        self.group_actions.setLayout(self.v_actions)
        return self.group_actions

    def reset_settings(self):
        self.box_savefig.setCheckable(False)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Ui_Linear()
    win.show()
    sys.exit(app.exec_())