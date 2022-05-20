import sys
from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from out_window import Ui_OutputDialog


class Ui_Dialog(QDialog):
    def __init__(self):
        super(Ui_Dialog, self).__init__()
        loadUi("mainwindow.ui", self)

        self.runButton.clicked.connect(self.runSlot)

        self.baru = None
        self.tangkap = None

    def refresh(self):
        self.tangkap = "0"

    @pyqtSlot()
    def runSlot(self):
        self.refresh()
        ui.hide()
        self.windowdbaru()

    def windowdbaru(self):
        self.baru = Ui_OutputDialog()
        self.baru.show()
        self.baru.startVideo(self.tangkap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()
    sys.exit(app.exec_())
