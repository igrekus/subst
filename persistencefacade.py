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
        importToHomebrew = defaultdict(list)
        homebrewToImport = defaultdict(list)

        for r in self._engine.fetchSubstMap():
            importToHomebrew[r[0]].append(r[1])
            homebrewToImport[r[1]].append(r[0])

        return importToHomebrew, homebrewToImport

    def getVendorDict(self):
        return {v[0]: [v[1], v[2]] for v in self._engine.fetchVendorList()}

    def insertDeviceItem(self, item: DeviceItem):
        print("persistence facade insert device item call:", item)
        return self._engine.insertDeviceRecord(item.toTuple())

    # def updateBillItem(self, item: BillItem):
    #     print("persistence facade update call:", item)
    #     self._engine.updateBillRecord(item.toTuple())
    #
    # def deleteBillItem(self, item):
    #     print("persistence facade delete call:", item)
    #     self._engine.deleteBillRecord(item)
    #
    # def persistPlanData(self, data):
    #     print("persistence facade persist plan data call")
    #     return self._engine.updatePlanData([tuple([v[0], v[1], v[2], k]) for k, v in data.items()])
    #
    # def addDictRecord(self, dictName, data):
    #     print("persistence facade add dict record:", dictName, data)
    #     return self._engine.insertDictRecord(dictName, (data, ))
    #
    # def editDictRecord(self, dictName, data):
    #     print("persistence facade add dict record:", dictName, data)
    #     return self._engine.updateDictRecord(dictName, (data[1], data[0]))
    #
    # def deleteDictRecord(self, dictName, data):
    #     print("persistence facade add dict record:", dictName, data)
    #     return self._engine.deleteDictRecord(dictName, (data, ))
