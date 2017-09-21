import const
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt


class DictEditor(QDialog):

    def __init__(self, parent=None, domainModel=None):
        super(DictEditor, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("dicteditor.ui", self)

        # instance variables
        self._modelDomain = domainModel
        self.dictList = {0: ["vendor", self._modelDomain.vendorMapModel]}

        self.initDialog()

        self.ui.btnAdd.clicked.connect(self.onBtnAddClicked)
        self.ui.btnEdit.clicked.connect(self.onBtnEditClicked)
        self.ui.btnDelete.clicked.connect(self.onBtnDeleteClicked)
        self.ui.comboDict.currentIndexChanged.connect(self.onComboDictIndexChanged)
        self.ui.listView.doubleClicked.connect(self.onListViewDoubleClicked)

    def initDialog(self):
        self.ui.comboDict.addItems(["Производитель"])
        self.ui.comboDict.setCurrentIndex(0)
        self.ui.listView.setModel(self.dictList[0][1])
        self.ui.listView.setRowHidden(0, True)

    def onBtnAddClicked(self):
        self.addRecord()

    def onBtnEditClicked(self):
        if not self.ui.listView.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка", "Изменить: пожалуйста, выберите запись.")
            return

        self.editRecord(self.ui.listView.selectionModel().selectedIndexes()[0])

    def onBtnDeleteClicked(self):
        if not self.ui.listView.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка", "Удалить: пожалуйста, выберите запись.")
            return

        self.delRecord(self.ui.listView.selectionModel().selectedIndexes()[0])

    def onComboDictIndexChanged(self, index):
        self.ui.listView.setModel(self.dictList[index][1])
        self.ui.listView.setRowHidden(0, True)

    def addRecord(self):
        data, ok = QInputDialog.getText(self, "Добавить запись", "Введите название:", QLineEdit.Normal, "")

        if not ok:
            return

        data = data[0].upper() + data[1:]
        self._modelDomain.addDictRecord(self.dictList[self.ui.comboDict.currentIndex()][0], data)

    def editRecord(self, index):
        data, ok = QInputDialog.getText(self, "Изменить запись", "Введите название:", QLineEdit.Normal,
                                        index.data(Qt.DisplayRole))

        if not ok:
            return

        data = data[0].upper() + data[1:]
        self._modelDomain.editDictRecord(self.dictList[self.ui.comboDict.currentIndex()][0],
                                         (index.data(const.RoleNodeId), data))

    def delRecord(self, index):
        result = QMessageBox.question(self.parent(), "Вопрос",
                                      "Вы действительно хотите удалить выбранную запись?")
        if result != QMessageBox.Yes:
            return

        if not self._modelDomain.deleteDictRecord(self.dictList[self.ui.comboDict.currentIndex()][0],
                                                  index.data(const.RoleNodeId)):
            QMessageBox.information(self, "Ошибка", "Выбранный производитель используется в базе.")
            return

    def onListViewDoubleClicked(self, index):
        self.editRecord(index)
