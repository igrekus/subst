import const
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt


class DlgSubstList(QDialog):

    def __init__(self, parent=None, deviceModel=None):
        super(DlgSubstList, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("dlgsubstlist.ui", self)

        # instance variables
        self.deviceModel = deviceModel

        # self.initDialog()

        self.ui.btnOk.clicked.connect(self.onBtnOkClicked)

    def initDialog(self):
        pass

    def onBtnOkClicked(self):
        print("ok")

    def onListViewDoubleClicked(self, index):
        pass
