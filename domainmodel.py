import copy
from collections import defaultdict
from deviceitem import DeviceItem
from mapmodel import MapModel
from PyQt5.QtCore import QObject, QModelIndex, pyqtSignal, QDate


class DomainModel(QObject):

    dict_list = ["vendor"]

    deviceAdded = pyqtSignal(int)
    deviceUpdated = pyqtSignal(int)
    deviceRemoved = pyqtSignal(int)

    def __init__(self, parent=None, persistenceFacade=None):
        super(DomainModel, self).__init__(parent)

        self._persistenceFacade = persistenceFacade

        self.deviceList = dict()
        self.substMap = dict()

        self.vendorList = dict()
        self.devtypeList = dict()

        self.deviceMapModel = None
        self.vendorMapModel = None
        self.devtypeMapModel = None

    def buildDeviceMapModel(self):
        self.deviceMapModel = MapModel(self, {k: v.item_name for k, v in self.deviceList.items()})

    def builVendorMapModel(self):
        self.vendorMapModel = MapModel(self, {k: v[0] for k, v in self.vendorList.items()})
        self.vendorMapModel.addItemAtPosition(0, 0, "Все")

    def buildDevtypeMapModel(self):
        self.devtypeMapModel = MapModel(self, self.devtypeList)
        self.devtypeMapModel.addItemAtPosition(0, 0, "Все")

    def buildMapModels(self):
        print("building map models")
        self.buildDeviceMapModel()
        self.builVendorMapModel()
        self.buildDevtypeMapModel()

    def initModel(self):
        print("init domain model")
        self.deviceList = self._persistenceFacade.getDeviceDict()
        self.vendorList = self._persistenceFacade.getVendorDict()
        self.devtypeList = self._persistenceFacade.getDevtypeDict()
        self.substMap = self._persistenceFacade.getSubstMap()
        self.buildMapModels()

    def getItemById(self, id_):
        return self.deviceList[id_]

    def getVendorById(self, id_):
        """
        :param id_: int 
        :return: list(name: str, origin: int) 
        """
        return self.vendorList[id_]

    def getDevtypeById(self, id_):
        return self.devtypeList[id_]

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

    def addVendorRecord(self, data):
        print("domain model add vendor record call", data)
        newId = self._persistenceFacade.addVendorRecord(data)

        self.vendorList[newId] = data[0]
        self.vendorMapModel.addItem(newId, data[0])

        print(self.vendorList)

    def addDictRecord(self, dictName, data):
        print("domain model add dict record:", dictName, data)
        newId = self._persistenceFacade.addDictRecord(dictName, data)

        if dictName == "vendor":
            self.vendorMapModel.addItem(newId, data)
        elif dictName == "devtype":
            self.devtypeMapModel.addItem(newId, data)

    def editDictRecord(self, dictName, data):
        print("domain model edit dict record:", dictName, data)
        self._persistenceFacade.editDictRecord(dictName, data)

        if dictName == "vendor":
            self.vendorMapModel.updateItem(data[0], data[1])
        elif dictName == "devtype":
            self.devtypeMapModel.updateItem(data[0], data[1])

    def deleteDictRecord(self, dictName, data):
        print("domain model delete dict record:", dictName, data)
        if not self._persistenceFacade.checkDictRef(dictName, data):

            self._persistenceFacade.deleteDictRecord(dictName, data)

            if dictName == "vendor":
                self.vendorMapModel.removeItem(data)
            elif dictName == "devtype":
                self.vendorMapModel.removeItem(data)
            return True
        return False
