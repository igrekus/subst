from collections import defaultdict

from deviceitem import DeviceItem
from mapmodel import MapModel
from PyQt5.QtCore import QObject


class PersistenceFacade(QObject):

    def __init__(self, parent=None, persistenceEngine=None):
        super(PersistenceFacade, self).__init__(parent)

        self._engine = persistenceEngine
        self.engineType = self._engine.engineType

    def initFacade(self):
        print("init persistence facade:", self._engine.engineType)

    def getDeviceList(self):
        return {r[0]: DeviceItem.fromSqlTuple(r) for r in self._engine.fetchDeviceList()}

    def getSubstMap(self):
        substmap = defaultdict(set)
        for r in self._engine.fetchSubstMap():
            for s in r[1].split(","):
                if s:
                    substmap[r[0]].add(int(s))
        return substmap

    def getVendorDict(self):
        return {v[0]: [v[1], v[2]] for v in self._engine.fetchVendorList()}

    def insertDeviceItem(self, item: DeviceItem, mapping: set):
        print("persistence facade insert device item call:", item, mapping)
        string = str()
        for m in mapping:
            string += str(m) + ","

        newId = self._engine.insertDeviceRecord(item.toTuple(), string.strip(","))

        update_list = list()
        for m in mapping:
            update_list.append((m, "," + str(newId), ))

        self._engine.appendDeviceMapping(update_list)
        return newId

    def updateDeviceItem(self, item: DeviceItem, affected_maps: dict):
        print("persistence facade update device item call:", item)
        self._engine.updateDeviceRecord(item.toTuple())
        self.updateAffectedMaps(affected_maps)

    def updateAffectedMaps(self, maps: dict):
        print("persistence facade update affected maps call:", maps)
        tmplist = list()
        for k, v in maps.items():
            string = str()
            for i in v:
                string += str(i) + ","
            tmplist.append((k, string.strip(","), ))

        self._engine.updateDeviceMappings(tmplist)

    def deleteDeviceItem(self, item: DeviceItem, affected_maps: dict):
        print("persistence facade delete item call:", item)
        self._engine.deleteDeviceRecord(item.toTuple())
        self.updateAffectedMaps(affected_maps)

    def addDictRecord(self, dictName, data):
        print("persistence facade add dict record:", dictName, data)
        return self._engine.insertDictRecord(dictName, (data, ))

    def editDictRecord(self, dictName, data):
        print("persistence facade add dict record:", dictName, data)
        self._engine.updateDictRecord(dictName, (data[1], data[0]))

    def deleteDictRecord(self, dictName, data):
        print("persistence facade add dict record:", dictName, data)
        self._engine.deleteDictRecord(dictName, (data, ))

    def checkDictRef(self, dictName, data):
        print("persistence facade check dict ref:", dictName, data)
        return self._engine.checkDictRef(dictName, data)
