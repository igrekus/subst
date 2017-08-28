import const
from copy import copy
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt, QModelIndex, QVariant

from deviceitem import DeviceItem
from mapmodel import MapModel


class DeviceEditor(QDialog):
    def __init__(self, parent=None, domainModel=None, data: DeviceItem=None, mapping: list=None):
        super(DeviceEditor, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("deviceeditor.ui", self)

        # instance variables
        self._modelDomain = domainModel
        self.substModel = MapModel(self, {m: self._modelDomain.deviceMapModel.getData(m) for m in mapping})

        self._data = data
        self._substList = list()

        self.initDialog()

        self.ui.btnOk.clicked.connect(self.onBtnOkClicked)
        self.ui.btnAddSubst.clicked.connect(self.onBtnAddSubstClicked)
        self.ui.btnRemoveSubst.clicked.connect(self.onBtnRemoveSubstClicked)

    def initDialog(self):
        self.ui.comboVendor.setModel(self._modelDomain.vendorMapModel)
        self.ui.listSubst.setModel(self.substModel)

        if self._data.item_id is None:
            self.setWindowTitle("Добавить устройство")
            self.resetWidgets()
        else:
            self.setWindowTitle("Редактировать устройство")
            self.updateWidgets()

    def resetWidgets(self):
        self.ui.editName.setText("")
        self.ui.comboVendor.setCurrentIndex(0)
        self.ui.editDesc.setText("")
        self.ui.textSpec.setPlainText("")

    def updateWidgets(self):
        self.ui.editName.setText(self._data.item_name)
        self.ui.comboVendor.setCurrentText(self._modelDomain.vendorMapModel.getData(self._data.item_vendor))
        self.ui.editDesc.setText(self._data.item_desc)
        self.ui.textSpec.setPlainText(self._data.item_spec)
        if self._data.item_origin == 1:
            self.ui.radioImport.setChecked(True)
        elif self._data.item_origin == 2:
            self.ui.radioHomebrew.setChecked(True)

    def onBtnAddSubstClicked(self):
        print("add subst")
        txt, ok = QInputDialog.getItem(self, "Добавить аналог", "Приборы:",
                                       self._modelDomain.deviceMapModel.strList, 0, False)

        if not ok:
            return

        self.substModel.addItem(self._modelDomain.deviceMapModel.getId(txt), txt)

    def onBtnRemoveSubstClicked(self):
        if not self.ui.listSubst.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка!", "Выберите аналог для удаления из списка.")
            return False

        print("remove subst:", self.ui.listSubst.selectionModel().currentIndex().data(const.RoleNodeId))
        result = QMessageBox.question(self, "Внимание!",
                                      "Вы хотите удалить аналог?")

        if result != QMessageBox.Yes:
            return

        self.substModel.removeItem(self.ui.listSubst.selectionModel().currentIndex().data(const.RoleNodeId))

    def verifyInput(self):
        print("verifying user input")
        if not self.ui.editName.text():
            QMessageBox.information(self, "Ошибка!", "Введите наименование прибора.")
            return False

        # if not self.ui.editDesc.text():
        #     QMessageBox.information(self, "Ошибка!", "Введите описание прибора.")
        #     return False
        #
        # if not self.ui.textSpec.toPlainText():
        #     QMessageBox.information(self, "Ошибка!", "Введите параметры прибора.")
        #     return False

        if not self.ui.radioImport.isChecked() and not self.ui.radioHomebrew.isChecked():
            QMessageBox.information(self, "Ошибка!", "Выберите происхождение прибора.")
            return False

        return True

    def collectData(self):
        print("collecting dlg data")

        origin = 1
        if self.ui.radioHomebrew.isChecked():
            origin = 2

        self._data = DeviceItem(id_=self._data.item_id,
                                name=self.ui.editName.text(),
                                vendor=self.ui.comboVendor.currentData(const.RoleNodeId),
                                desc=self.ui.editDesc.text(),
                                spec=self.ui.textSpec.toPlainText(),
                                tags="",
                                origin=origin)

        self._substList = {self.substModel.data(self.substModel.index(row, 0), const.RoleNodeId).value()
                           for row in range(self.substModel.rowCount(QModelIndex()))}

        if self._data.item_id in self._substList:
            self._substList.remove(self._data.item_id)

    def getData(self):
        return self._data, self._substList

    def onBtnOkClicked(self):
        if self.verifyInput():
            self.collectData()
            self.accept()
        else:
            return
