import sys
import os
import linear as lin

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QMainWindow, QApplication, QMessageBox, 
                             QGridLayout, QWidget, QLayout)

class Ui_MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("GrapHelper - Linear Plot")
        self.setObjectName("self")
        self.resize(400, 350)
        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)

        self.V_layout = QtWidgets.QVBoxLayout(self.central_widget)
        # # Dialogs
        self.dialog_linear = lin.Ui_Linear()
        # Create menu bar
        self.set_menu_bar()
        # Top label
        self.set_top_label()
        # Main grid
        self.set_main_grid()

        QtCore.QMetaObject.connectSlotsByName(self)

    def set_menu_bar(self):
        """ Create the menu bar
        Parameters:
            None
        Returns:
            None
        """
        # Main 
        self.menubar_main = QtWidgets.QMenuBar(self)
        # Files
        self.menu_files = QtWidgets.QMenu("File", self)
        # Edit
        self.menu_edit = QtWidgets.QMenu("Edit", self)

        # self.action_hard = QtWidgets.QAction('Hard (20x35, 99 bombs)', self)

        self.menubar_main.addMenu(self.menu_files)
        self.menubar_main.addMenu(self.menu_edit)

        # Adding to main
        self.setMenuBar(self.menubar_main)


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
        labels = ["Linear Plot", "Bar Plot", "Scatter Plot"
                  "", "", ""
                  "", "", ""
                  ]
        # Grid
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setSizeConstraint(QLayout.SetFixedSize)
        self.grid_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout.setHorizontalSpacing(0)
        self.grid_layout.setVerticalSpacing(0)
        # 0, 0
        Pbutton_line_plot = QtWidgets.QPushButton()
        Pbutton_line_plot.clicked.connect(self.dialog_linear.show)
        self.grid_layout.addWidget(Pbutton_line_plot, 0, 0)
        # 0, 1
        Pbutton_bar_plot = QtWidgets.QPushButton()
        self.grid_layout.addWidget(Pbutton_bar_plot, 0, 1)
        # 0, 2
        Pbutton_TBD1 = QtWidgets.QPushButton()
        Pbutton_TBD1.setFixedSize(button_size_w, button_size_h)
        self.grid_layout.addWidget(Pbutton_TBD1, 0, 2)
        # 1, 0
        Pbutton_TBD1 = QtWidgets.QPushButton()
        Pbutton_TBD1.setFixedSize(button_size_w, button_size_h)
        self.grid_layout.addWidget(Pbutton_TBD1, 1, 0)
        # 1, 1
        Pbutton_TBD2 = QtWidgets.QPushButton()
        Pbutton_TBD2.setFixedSize(button_size_w, button_size_h)
        self.grid_layout.addWidget(Pbutton_TBD2, 1, 1)
        # 1, 2
        Pbutton_TBD3 = QtWidgets.QPushButton()
        Pbutton_TBD3.setFixedSize(button_size_w, button_size_h)
        self.grid_layout.addWidget(Pbutton_TBD3, 1, 2)

        # Set font, buttons sizes
        for i in range(self.grid_layout.count()):
            button = self.grid_layout.itemAt(i).widget()
            button.setText(labels[i])
            button.setFont(font)
            button.setFixedSize(button_size_w, button_size_h)


        # Add to layout
        self.V_layout.addLayout(self.grid_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Ui_MainWindow()
    win.show()
    sys.exit(app.exec_())