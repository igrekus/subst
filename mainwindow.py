import const
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QAction, QMessageBox, QTreeView
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex

from domainmodel import DomainModel
from devicelistmodel import DeviceListModel
from mysqlengine import MysqlEngine
from persistencefacade import PersistenceFacade
from uifacade import UiFacade


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # ui
        self.ui = uic.loadUi("mainwindow.ui", self)

        # report manager
        # self._reportManager = ReportManager(parent=self)

        # report engines
        # self._xlsxEngine = XlsxEngine(parent=self)
        # self._reportManager.setEngine(self._xlsxEngine)
        # self._printEngine = PrintEngine(parent=self)
        # self._reportManager.setEngine(self._printEngine)

        # persistence engine
        # self._persistenceEngine = CsvEngine(parent=self)
        self._persistenceEngine = MysqlEngine(parent=self)

        # facades
        self._persistenceFacade = PersistenceFacade(parent=self, persistenceEngine=self._persistenceEngine)
        # self._uiFacade = UiFacade(parent=self, reportManager=self._reportManager)
        self._uiFacade = UiFacade(parent=self)
        #
        # models
        # domain
        self._modelDomain = DomainModel(parent=self, persistenceFacade=self._persistenceFacade)

        # bill list + search proxy
        self._modelDeviceList = DeviceListModel(parent=self, domainModel=self._modelDomain)
        self._modelSearchProxy = QSortFilterProxyModel(parent=self)
        self._modelSearchProxy.setSourceModel(self._modelDeviceList)
        #
        # # bill plan + search proxy
        # self._modelBillPlan = BillPlanModel(parent=self, domainModel=self._modelDomain)
        # self._modelPlanSearchProxy = QSortFilterProxyModel(parent=self)
        # self._modelPlanSearchProxy.setSourceModel(self._modelBillPlan)
        #
        # connect ui facade to models
        self._uiFacade.setDomainModel(self._modelDomain)

        # actions
        self.actRefresh = QAction("Обновить", self)
        self.actOpenDeviceEditor = QAction("Редактор устройств", self)
        # self.actAddBillRecord = QAction("Добавить счёт...", self)
        # self.actEditBillRecord = QAction("Изменить счёт...", self)
        # self.actDeleteBillRecord = QAction("Удалить счёт...", self)
        # self.actPrint = QAction("Распечатать...", self)
        # self.actOpenDictEditor = QAction("Словари", self)

    def initApp(self):
        # init instances
        # engines
        self._persistenceEngine.initEngine()

        # facades
        self._persistenceFacade.initFacade()
        # self._uiFacade.initFacade()

        # models
        self._modelDomain.initModel()
        self._modelDeviceList.initModel(self._modelDeviceList.buildImportToHomebrewTree)

        # init UI
        # main table
        self.ui.treeDeviceList: QTreeView
        self.ui.treeDeviceList.setModel(self._modelSearchProxy)
        self.ui.treeDeviceList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.treeDeviceList.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.ui.treeDeviceList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # formatting
        self.ui.treeDeviceList.setUniformRowHeights(True)
        self.ui.treeDeviceList.header().setHighlightSections(False)
        self.ui.treeDeviceList.header().setStretchLastSection(True)

    #     # setup filter widgets
    #     self.ui.comboProjectFilter.setModel(self._modelDomain.dicts["project"])
    #     self.ui.comboStatusFilter.setModel(self._modelDomain.dicts["status"])
    #     self.ui.comboPriorityFilter.setModel(self._modelDomain.dicts["priority"])
    #     self.ui.comboShipmentFilter.setModel(self._modelDomain.dicts["shipment"])
    #     self.ui.dateFromFilter.setDate(QDate.fromString(self._modelDomain.getEarliestBillDate(), "dd.MM.yyyy"))
    #     self.ui.dateUntilFilter.setDate(QDate.currentDate())
    #
        # create actions
        self.initActions()

        # setup ui widget signals
        # buttons
        self.ui.radioImport.toggled.connect(self.onRadioImportToggled)
        self.ui.btnDeviceEditor.clicked.connect(self.onBtnDeviceEditorClicked)

        # tree and selection
        self.ui.treeDeviceList.selectionModel().currentChanged.connect(self.onCurrentTreeItemChanged)

        # search widgets
    #     self.ui.comboWeek.currentIndexChanged.connect(self.onComboWeekCurrentIndexChanged)
    #     self.ui.editSearch.textChanged.connect(self.setSearchFilter)
    #     self.ui.comboProjectFilter.currentIndexChanged.connect(self.setSearchFilter)
    #     self.ui.comboStatusFilter.currentIndexChanged.connect(self.setSearchFilter)
    #     self.ui.comboPriorityFilter.currentIndexChanged.connect(self.setSearchFilter)
    #     self.ui.comboShipmentFilter.currentIndexChanged.connect(self.setSearchFilter)
    #     self.ui.dateFromFilter.dateChanged.connect(self.setSearchFilter)
    #     self.ui.dateUntilFilter.dateChanged.connect(self.setSearchFilter)
    #
    #     self.setSearchFilter()
    #
    #     self.ui.btnRefresh.setVisible(False)

    def initActions(self):
        self.actRefresh.setShortcut("Ctrl+R")
        self.actRefresh.setStatusTip("Обновить данные")
        self.actRefresh.triggered.connect(self.procActRefresh)

        self.actOpenDeviceEditor.setStatusTip("Открыть редактор устройств")
        self.actOpenDeviceEditor.triggered.connect(self.procActOpenDeviceEditor)

    def refreshView(self):
        windowRect = self.geometry()
        tdwidth = windowRect.width() - 50

        self.ui.treeDeviceList.setColumnWidth(0, tdwidth * 0.15)
        self.ui.treeDeviceList.setColumnWidth(1, tdwidth * 0.05)
        self.ui.treeDeviceList.setColumnWidth(2, tdwidth * 0.10)
        self.ui.treeDeviceList.setColumnWidth(3, tdwidth * 0.25)
        self.ui.treeDeviceList.setColumnWidth(4, tdwidth * 0.30)
        self.ui.treeDeviceList.setColumnWidth(5, tdwidth * 0.15)

    def updateItemInfo(self, index):
        self.ui.textDeviceInfo.setPlainText(self._uiFacade.requestItemInfo(index))

    # ui events
    def onRadioImportToggled(self, checked):
        self._modelDeviceList.clear()
        if checked:
            self._modelDeviceList.initModel(self._modelDeviceList.buildImportToHomebrewTree)
        else:
            self._modelDeviceList.initModel(self._modelDeviceList.buildHomebrewToImportTree)

    def onBtnDeviceEditorClicked(self):
        self.actOpenDeviceEditor.trigger()

    # def onBtnAddBillClicked(self):
    #     self.actAddBillRecord.trigger()
    #
    # def onBtnEditBillClicked(self):
    #     self.actEditBillRecord.trigger()
    #
    # def onBtnDeleteBillClicked(self):
    #     self.actDeleteBillRecord.trigger()
    #
    # def onBtnDictEditorClicked(self):
    #     self.actOpenDictEditor.trigger()
    #
    # def onBtnPrintClicked(self):
    #     self.actPrint.trigger()
    #
    # def onTableBillDoubleClicked(self):
    #     self.actEditBillRecord.trigger()
    #
    # def onTabBarCurrentChanged(self, index):
    #     if index == 1:
    #         self._modelDomain.buildPlanData()
    #
    def onCurrentTreeItemChanged(self, cur: QModelIndex, prev: QModelIndex):
        # currentSourceIndex = self._modelSearchProxy.mapToSource(self.ui.treeDeviceList.selectionModel().selectedIndexes()[0])
        sourceIndex = self._modelSearchProxy.mapToSource(cur)
        self.updateItemInfo(sourceIndex)

    # misc events
    def resizeEvent(self, event):
        self.actRefresh.trigger()

    # def closeEvent(self, *args, **kwargs):
    #     self._uiFacade.requestExit()
    #     super(MainWindow, self).closeEvent(*args, **kwargs)

    # action processing
    # send user commands to the ui facade: (command, parameters (like indexes, etc.))
    def procActRefresh(self):
        # print("act refresh triggered")
        # self._uiFacade.requestRefresh()
        self.refreshView()

    def procActOpenDeviceEditor(self):
        self._uiFacade.requestOpenDeviceEditor()
