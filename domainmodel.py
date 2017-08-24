from PyQt5.QtCore import QObject, QModelIndex, pyqtSignal, QDate

from deviceitem import DeviceItem
from mapmodel import MapModel


class DomainModel(QObject):

    dict_list = ["category", "period", "priority", "project", "shipment", "status", "vendor"]

    # billItemsBeginInsert = pyqtSignal(int, int)
    # billItemsEndInsert = pyqtSignal()
    # billItemsBeginRemove = pyqtSignal(int, int)
    # billItemsEndRemove = pyqtSignal()
    #
    # planItemsBeginInsert = pyqtSignal(int, int)
    # planItemsEndInsert = pyqtSignal()
    # planItemsBeginRemove = pyqtSignal(int, int)
    # planItemsEndRemove = pyqtSignal()
    #
    # billItemsInserted = pyqtSignal(int, int)
    # billItemsRemoved = pyqtSignal(int, int)

    def __init__(self, parent=None, persistenceFacade=None):
        super(DomainModel, self).__init__(parent)

        self._persistenceFacade = persistenceFacade

        self.deviceList = dict()
        self.importToHomebrew = dict()
        self.homebrewToImport = dict()

        self.vendorList = dict()

        self.deviceMapModel = None
        self.vendorMapModel = None

    def buildMapModels(self):
        print("building map models")
        self.deviceMapModel = MapModel(self, {k: v.item_name for k, v in self.deviceList.items()})
        self.vendorMapModel = MapModel(self, {k: v[0] for k, v in self.vendorList.items()})

    def initModel(self):
        print("init domain model")
        self.deviceList = self._persistenceFacade.getDeviceList()
        self.importToHomebrew, self.homebrewToImport = self._persistenceFacade.getSubstMap()
        self.vendorList = self._persistenceFacade.getVendorDict()
        self.buildMapModels()

    def getItemById(self, id_):
        return self.deviceList[id_]

    def getVendorById(self, id_):
        """
        :param id_: int 
        :return: list(name: str, origin: int) 
        """
        return self.vendorList[id_]

    def addDeviceItem(self, item: DeviceItem):
        print("domain model add device item call:", item)
        newId = self._persistenceFacade.insertDeviceItem(item)
        item.item_id = newId

        self.deviceList[newId] = item
        print(self.deviceList)
    #     self._billData.append(newItem)
    #     self._rawPlanData[newItem.item_id] = [0, 0, 0]
    #     # self.refreshPlanData()
    #
    #     row = len(self._billData) - 1
    #
    #     self.billItemsInserted.emit(row, row)
    #     return row

    # def updateBillItem(self, index: QModelIndex, updatedItem: BillItem):
    #     row = index.row()
    #     print("domain model update bill item call, row:", row, updatedItem)
    #     self._persistenceFacade.updateBillItem(updatedItem)
    #     self._billData[row] = updatedItem
    #
    # def deleteBillItem(self, index: QModelIndex):
    #     row = index.row()
    #     print("domain model delete bill item call, row", row)
    #     self._persistenceFacade.deleteBillItem(self._billData[row])
    #     del self._billData[row]
    #     self.billItemsRemoved.emit(row, row)
    #
    # def savePlanData(self):
    #     print("domain model persist plan data call")
    #     return self._persistenceFacade.persistPlanData(self._rawPlanData)
    #
    # def addDictRecord(self, dictName, data):
    #     print("domain model add dict record:", dictName, data)
    #     newId = self._persistenceFacade.addDictRecord(dictName, data)
    #
    #     self.dicts[dictName].addItem(100, data)
    #
    # def editDictRecord(self, dictName, data):
    #     print("domain model edit dict record:", dictName, data)
    #     self._persistenceFacade.editDictRecord(dictName, data)
    #
    #     self.dicts[dictName].updateItem(data[0], data[1])
    #
    # def deleteDictRecord(self, dictName, data):
    #     # TODO: check for existing references
    #     print("domain model delete dict record:", dictName, data)
    #     self._persistenceFacade.deleteDictRecord(dictName, data)
    #
    #     self.dicts[dictName].removeItem(data)
