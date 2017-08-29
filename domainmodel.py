import copy
from collections import defaultdict
from deviceitem import DeviceItem
from mapmodel import MapModel
from PyQt5.QtCore import QObject, QModelIndex, pyqtSignal, QDate


class DomainModel(QObject):

    dict_list = ["category", "period", "priority", "project", "shipment", "status", "vendor"]

    deviceAdded = pyqtSignal(int)
    deviceUpdated = pyqtSignal(int)
    deviceRemoved = pyqtSignal(int)

    def __init__(self, parent=None, persistenceFacade=None):
        super(DomainModel, self).__init__(parent)

        self._persistenceFacade = persistenceFacade

        self.deviceList = dict()
        self.substMap = dict()

        self.vendorList = dict()

        self.deviceMapModel = None
        self.vendorMapModel = None

    def buildDeviceMapModel(self):
        self.deviceMapModel = MapModel(self, {k: v.item_name for k, v in self.deviceList.items()})

    def builVendorMapModel(self):
        self.vendorMapModel = MapModel(self, {k: v[0] for k, v in self.vendorList.items()})
        self.vendorMapModel.addItemAtPosition(0, 0, "Все")

    def buildMapModels(self):
        print("building map models")
        self.buildDeviceMapModel()
        self.builVendorMapModel()

    def initModel(self):
        print("init domain model")
        self.deviceList = self._persistenceFacade.getDeviceList()
        self.substMap = self._persistenceFacade.getSubstMap()
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

    def addDeviceItem(self, item: DeviceItem, mapping: set):
        print("domain model add device item call:", item)
        newId = self._persistenceFacade.insertDeviceItem(item, mapping)
        item.item_id = newId

        self.deviceList[newId] = item

        self.substMap[newId] = mapping
        for m in mapping:
            self.substMap[m].add(newId)

        self.deviceMapModel.addItem(newId, item.item_name)

        self.deviceAdded.emit(newId)

    def updateDeviceItem(self, item: DeviceItem, mapping: set):
        print("domain model update device item call:", item)

        self.deviceList[item.item_id] = item

        self.substMap[item.item_id] = mapping
        affected_maps = dict()
        affected_maps[item.item_id] = self.substMap[item.item_id]
        for k, v in self.substMap.items():
            if item.item_id in v and item.item_id not in mapping:
                v.remove(item.item_id)
                affected_maps[k] = v
        for m in mapping:
            self.substMap[m].add(item.item_id)
            affected_maps[m] = self.substMap[m]

        self._persistenceFacade.updateDeviceItem(item, affected_maps)

        self.deviceMapModel.updateItem(item.item_id, item.item_name)

        self.deviceUpdated.emit(item.item_id)

    def deleteDeviceItem(self, item: DeviceItem):
        print("domain model delete device item call:", item)

        self.deviceList.pop(item.item_id, 0)
        self.substMap.pop(item.item_id, 0)

        affected_maps = dict()
        for k, v in self.substMap.items():
            if item.item_id in v:
                v.remove(item.item_id)
                affected_maps[k] = v

        self._persistenceFacade.deleteDeviceItem(item, affected_maps)

        self.deviceMapModel.removeItem(item.item_id)

        self.deviceRemoved.emit(item.item_id)

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
