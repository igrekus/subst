import const
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt, QModelIndex


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

        # output data
        self.selectedIdList = list()

        self.initDialog()

        self.ui.btnOk.clicked.connect(self.onBtnOkClicked)

    def initDialog(self):
        self.ui.listView.setModel(self.deviceModel)

    def collectData(self):
        if self.ui.listView.selectionModel().hasSelection():
            for i in self.ui.listView.selectionModel().selectedIndexes():
                self.selectedIdList.append([i.data(const.RoleNodeId), i.data(Qt.DisplayRole)])

    def getData(self):
        return self.selectedIdList

    def onBtnOkClicked(self):
        self.collectData()
        self.accept()

    # def onListViewDoubleClicked(self, index):
    #     pass
