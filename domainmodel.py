from PyQt5.QtCore import QObject, QModelIndex, pyqtSignal, QDate

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

        self.importDeviceList = dict()
        self.homebrewDeviceList = dict()
        self.importToHomebrew = dict()
        self.homebrewToImport = dict()

        self.vendorList = dict()

    def initModel(self):
        print("init domain model")

        self.deviceList = self._persistenceFacade.getDeviceList()
        self.importToHomebrew, self.homebrewToImport = self._persistenceFacade.getSubstMap()
        self.vendorList = self._persistenceFacade.getVendorDict()

        self.deviceMapModel = MapModel(self, {k: v.item_name for k, v in self.deviceList.items()})

        self.vendorMapModel = MapModel(self, {k: v[0] for k, v in self.vendorList.items()})

    def getItemById(self, id_):
        return self.deviceList[id_]

    def getVendorById(self, id_):
        """
        :param id_: int 
        :return: list(name: str, origin: int) 
        """
        return self.vendorList[id_]

    # def refreshPlanData(self):
    #     if self._rawPlanData:
    #         self._rawPlanData.clear()
    #     self._rawPlanData = self._persistenceFacade.fetchRawPlanData()

    # def getBillItemAtRow(self, row: int):
    #     return self._billData[row]
    #
    # def getBillItemAtIndex(self, index: QModelIndex):
    #     return self._billData[index.row()]
    #
    # def getPlanItemAtRow(self, row: int):
    #     return self._planData[row]
    #
    # def getDicts(self):
    #     return self.dicts
    #
    # def getTotalForWeek(self, week):
    #     return sum(p[4] for p in self._planData if p[5] == week)
    #
    # def getPayedTotalForWeek(self, week):
    #     return sum(p[4] for p in self._planData if p[5] == week and self.getBillItemById(p[2]).item_status == 1)
    #
    # def getRemainingTotalForWeek(self, week):
    #     return sum(p[4] for p in self._planData if p[5] == week and self.getBillItemById(p[2]).item_status != 1)
    #
    # def getTotal(self, weeks):
    #     return sum([self.getTotalForWeek(w) for w in weeks])
    #
    # def getPayedTotal(self, weeks):
    #     return sum([self.getPayedTotalForWeek(w) for w in weeks])
    #
    # def getRemainingTotal(self, weeks):
    #     return sum([self.getRemainingTotalForWeek(w) for w in weeks])
    #
    # def getBillTotals(self):
    #     payed = sum(d.item_cost for d in self._billData if d.item_status == 1)
    #     remaining = sum(d.item_cost for d in self._billData if d.item_status == 2)
    #     return payed, remaining, payed + remaining
    #
    # def setWeekForBill(self, bill_id, week):
    #     for i, d in enumerate(self._billData):
    #         if d.item_id == bill_id:
    #             break
    #     self._billData[i].item_payment_week = week
    #
    # def getBillItemById(self, bill_id):
    #     for d in self._billData:
    #         if d.item_id == bill_id:
    #             return d
    #
    # def getEarliestBillDate(self):
    #     return min([d.item_date for d in self._billData],
    #                key=lambda d: QDate.fromString(d, "dd.MM.yyyy"),
    #                default=QDate.currentDate())
    #
    # def refreshData(self):
    #     print("domain model refresh call")
    #
    # def addBillItem(self, newItem):
    #     print("domain model add bill item call:", newItem)
    #     newId = self._persistenceFacade.insertBillItem(newItem)
    #     newItem.item_id = newId
    #
    #     self._billData.append(newItem)
    #     self._rawPlanData[newItem.item_id] = [0, 0, 0]
    #     # self.refreshPlanData()
    #
    #     row = len(self._billData) - 1
    #
    #     self.billItemsInserted.emit(row, row)
    #     return row
    #
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
