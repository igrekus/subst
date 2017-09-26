import const
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QLineEdit, QRadioButton
from PyQt5.QtCore import Qt, QModelIndex

from deviceitem import DeviceItem
from dlgsubstlist import DlgSubstList
from domainmodel import DomainModel
from mapmodel import MapModel
from inputdialog import InputDialog


class DeviceEditor(QDialog):
    def __init__(self, parent=None, domainModel=None, data: DeviceItem=None, mapping: list=None):
        super(DeviceEditor, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("deviceeditor.ui", self)

        # instance variables
        self._modelDomain: DomainModel = domainModel
        self.substModel = MapModel(self, {m: self._modelDomain.deviceMapModel.getData(m) for m in mapping})
        self.filteredVendorModel = MapModel(self, {k: v[0] for k, v in self._modelDomain.vendorList.items()})

        self._data = data
        self._substList = set()

        self.initDialog()

        self.ui.btnOk.clicked.connect(self.onBtnOkClicked)
        self.ui.btnAddSubst.clicked.connect(self.onBtnAddSubstClicked)
        self.ui.btnRemoveSubst.clicked.connect(self.onBtnRemoveSubstClicked)
        self.ui.btnAddVendor.clicked.connect(self.onBtnAddVendorClicked)
        self.ui.btnAddDevtype.clicked.connect(self.onBtnAddDevtypeClicked)
        self.ui.radioImport.toggled.connect(self.onRadioStatusChange)
        self.ui.radioHomebrew.toggled.connect(self.onRadioStatusChange)

    def initDialog(self):
        self.ui.comboVendor.setModel(self.filteredVendorModel)
        self.ui.comboDevtype.setModel(self._modelDomain.devtypeMapModel)
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
        self.ui.comboDevtype.setCurrentIndex(0)
        self.ui.editDesc.setText("")
        self.ui.textSpec.setPlainText("")

    def updateWidgets(self):
        self.ui.editName.setText(self._data.item_name)
        self.ui.comboVendor.setCurrentText(self._modelDomain.vendorMapModel.getData(self._data.item_vendor))
        self.ui.comboDevtype.setCurrentText(self._modelDomain.devtypeMapModel.getData(self._data.item_devtype))
        self.ui.editDesc.setText(self._data.item_desc)
        self.ui.textSpec.setPlainText(self._data.item_spec)
        if self._data.item_origin == 1:
            self.ui.radioImport.setChecked(True)
        elif self._data.item_origin == 2:
            self.ui.radioHomebrew.setChecked(True)

    def filterVendorModel(self, imported):
        self.filteredVendorModel.clear()
        self.filteredVendorModel.initModel(
            {k: v[0] for k, v in self._modelDomain.vendorList.items() if v[1] == int(not imported) + 1})

    def onBtnAddSubstClicked(self):
        origin = int(self.ui.radioImport.isChecked()) + 1
        dialog = DlgSubstList(deviceModel=self._modelDomain.buildDeviceMapModel(origin=origin))

        if dialog.exec() != QDialog.Accepted:
            return

        for d in dialog.getData():
            self.substModel.addItem(d[0], d[1])

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

    def onBtnAddVendorClicked(self):
        dialog = InputDialog(parent=self, title="Введите информацию о производителе",
                             widgetList=[QLineEdit, QRadioButton, QRadioButton],
                             widgetTitleList=["Название:", "Импортный", "Отечественный"],
                             widgetDataList=["", True, False])
        if dialog.exec() != QDialog.Accepted:
            return

        data = dialog.getData()
        self._modelDomain.addVendorRecord([data[0], int(data[2]) + 1])
        self.filterVendorModel(data[1])

    def onBtnAddDevtypeClicked(self):
        dialog = InputDialog(parent=self, title="Введите информацию о типе устройства",
                             widgetList=[QLineEdit],
                             widgetTitleList=["Название:"],
                             widgetDataList=[""])
        if dialog.exec() != QDialog.Accepted:
            return

        self._modelDomain.addDictRecord("devtype", dialog.getData()[0])

    def onRadioStatusChange(self, dummy):
        self.filterVendorModel(self.ui.radioImport.isChecked())

    def onBtnOkClicked(self):
        if self.verifyInput():
            self.collectData()
            self.accept()
        else:
            return

    def verifyInput(self):
        print("verifying user input")
        if not self.ui.editName.text():
            QMessageBox.information(self, "Ошибка!", "Введите наименование прибора.")
            return False

        if self.ui.comboVendor.currentIndex() == 0:
            QMessageBox.information(self, "Ошибка!", "Выберите производителя прибора.")
            return False

        if self.ui.comboDevtype.currentIndex() == 0:
            QMessageBox.information(self, "Ошибка!", "Выберите тип прибора.")
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
                                devtype=self.ui.comboDevtype.currntData(const.RoleNodeId),
                                desc=self.ui.editDesc.text(),
                                spec=self.ui.textSpec.toPlainText(),
                                tags="",
                                origin=origin)

        # make subst set for mapping info
        self._substList = {self.substModel.data(self.substModel.index(row, 0), const.RoleNodeId).value()
                           for row in range(self.substModel.rowCount(QModelIndex()))}

        # remove self from subst list
        if self._data.item_id in self._substList:
            self._substList.remove(self._data.item_id)

    def getData(self):
        return self._data, self._substList
