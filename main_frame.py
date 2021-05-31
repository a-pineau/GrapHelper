import sys
import os
import line as line

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMessageBox, 
                             QGridLayout, QWidget, QLayout)

class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GrapHelper - Data Visualization")
        self.setObjectName("self")
        self.resize(400, 350)
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.V_layout = QtWidgets.QVBoxLayout(self.central_widget)
        # Dialogs
        self.dialog_line = line.Ui_line()
        # Top label
        self.set_top_label()
        # Main grid
        self.set_main_grid()

    def set_top_label(self):
        font = QtGui.QFont()
        font.setFamily("Forte")
        font.setPointSize(20)
        # font.setBold(True)
        font.setWeight(75)
        # Text
        self.label_graphelper = QtWidgets.QLabel()
        self.label_graphelper.setText("GrapHelper - Data Visualization")
        self.label_graphelper.setFont(font)
        self.label_graphelper.setAlignment(QtCore.Qt.AlignCenter)

        self.V_layout.addWidget(self.label_graphelper)
        
    def set_main_grid(self):
        """ Create the main grid
        Parameters:
            None
        Returns:
            None
        """
        button_size_w, button_size_h = 150, 100
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        BUTTONS_DATA = {
            "Line Plot": self.dialog_line.show,
            "Bar Graphs": self.to_add,
            "Scatter Plot": self.to_add,
            "Area Plot": self.to_add,
            "Histograms": self.to_add,
            "Stream Plot": self.to_add,
            "Polar Plot": self.to_add,
            "3D Plot": self.to_add,
            "Images": self.to_add
        }

        # Grid
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.grid_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.setHorizontalSpacing(0)
        self.grid_layout.setVerticalSpacing(0)

        col = [0, 0, 0, 1, 1, 1, 2, 2, 2]
        row = [0, 1, 2] * 3
        iterkey_BUTTONS_DATA = iter(BUTTONS_DATA.keys())
        iterval_BUTTONS_DATA = iter(BUTTONS_DATA.values())
        for r, c in zip(col, row):
            pbutton = QtWidgets.QPushButton()
            pbutton.setText(next(iterkey_BUTTONS_DATA))
            pbutton.setFont(font)
            pbutton.setFixedSize(button_size_w, button_size_h)
            pbutton.clicked.connect(next(iterval_BUTTONS_DATA))
            self.grid_layout.addWidget(pbutton, r, c)

        # Add to layout
        self.V_layout.addLayout(self.grid_layout)

    def to_add(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Ui_MainWindow()
    win.show()
    app.setStyle("Fusion")
    sys.exit(app.exec_())