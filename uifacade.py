import const
from PyQt5.QtCore import QObject, QModelIndex, Qt
from PyQt5.QtWidgets import QDialog, QMessageBox

from deviceeditor import DeviceEditor
from deviceitem import DeviceItem
from dicteditor import DictEditor


class UiFacade(QObject):

    def __init__(self, parent=None, domainModel=None, reportManager=None):
        super(UiFacade, self).__init__(parent)
        self._domainModel = domainModel
        self._reportManager = reportManager

    def setDomainModel(self, domainModel=None):
        self._domainModel = domainModel

    def initFacade(self):
        print("init ui facade")

    # process ui requests
    def requestRefresh(self):
        self._domainModel.refreshData()
        print("ui facade refresh request")

    def requestItemInfo(self, index: QModelIndex):
        item: DeviceItem = self._domainModel.getItemById(index.data(const.RoleNodeId))
        return "Наименование:\n" + item.item_name + \
               "\n\nПроизводитель:\n" + self._domainModel.getVendorById(item.item_vendor)[0] + \
               "\n\nТип устройства:\n" + self._domainModel.getDevtypeById(item.item_devtype) + \
               "\n\nОписание:\n" + item.item_desc + \
               "\n\nПараметры:\n" + item.item_spec

    def requestDeviceAdd(self):
        print("ui facade add device request")
        dialog = DeviceEditor(domainModel=self._domainModel, data=DeviceItem(), mapping=list())  # empty dialog for new item

        if dialog.exec() != QDialog.Accepted:
            return

        newItem, mapping = dialog.getData()
        self._domainModel.addDeviceItem(newItem, mapping)

    def requestDeviceEdit(self, index: QModelIndex):
        item = self._domainModel.getItemById(index.data(const.RoleNodeId))
        print("ui facade edit device request", item)

        dialog = DeviceEditor(domainModel=self._domainModel, data=item,
                              mapping=self._domainModel.substMap[item.item_id])

        if dialog.exec() != QDialog.Accepted:
            return

        item, mapping = dialog.getData()
        self._domainModel.updateDeviceItem(item, mapping)

    def requestDeviceDelete(self, index: QModelIndex):
        item = self._domainModel.getItemById(index.data(const.RoleNodeId))
        print("ui facade delete device request", item)
        result = QMessageBox.question(self.parent(), "Внимание!",
                                      "Вы хотите удалить выбранную запись?")

        if result != QMessageBox.Yes:
            return

        self._domainModel.deleteDeviceItem(item)

    def requestDictEditorOpen(self):
        print("ui facade dict editor open request")
        dialog = DictEditor(domainModel=self._domainModel)

        dialog.exec()

    # def requestExit(self, index):
    #     # TODO make settings class if needed, only current week is saved for now
    #     print("ui facade exit request...")
    #     print("saving preferences...", index)
    #     # TODO extract saving process into settings class, only send a message from UI
    #     with open("settings.ini", mode='tw') as f:
    #         f.write("week="+str(index + 1))
    #
    #     if self._domainModel.savePlanData():
    #         print("...exit request ok")
    #     else:
    #         raise RuntimeError("DB connection error")
