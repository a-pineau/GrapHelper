import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        checkBoxNone = QCheckBox("None Selected")
        checkBoxA    = QCheckBox("Select A")
        checkBoxB    = QCheckBox("Select B")

        checkBoxNone.setChecked(True)
        checkBoxNone.stateChanged.connect(lambda checked: (checkBoxA.setChecked(False), checkBoxB.setChecked(False)))
        checkBoxA.stateChanged.connect(lambda checked: checkBoxNone.setChecked(False))
        checkBoxB.stateChanged.connect(lambda checked: checkBoxNone.setChecked(False))

        grid = QGridLayout()

        grid.addWidget(checkBoxNone, 1, 0)
        grid.addWidget(checkBoxA, 2, 0)
        grid.addWidget(checkBoxB, 3, 0)

        self.setLayout(grid)
        self.setWindowTitle('Test')
        self.show()

if __name__ == '__main__':
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    ex = Test()
    sys.exit(app.exec_())