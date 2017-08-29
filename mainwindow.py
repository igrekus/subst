from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QAction, QMessageBox, QTreeView
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex

import const
from devicesearchproxymodel import DeviceSearchProxyModel
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
        self._persistenceEngine = MysqlEngine(parent=self)

        # facades
        self._persistenceFacade = PersistenceFacade(parent=self, persistenceEngine=self._persistenceEngine)
        # self._uiFacade = UiFacade(parent=self, reportManager=self._reportManager)
        self._uiFacade = UiFacade(parent=self)

        # models
        # domain
        self._modelDomain = DomainModel(parent=self, persistenceFacade=self._persistenceFacade)

        # device tree + search proxy
        self._modelDeviceTree = DeviceListModel(parent=self, domainModel=self._modelDomain)
        # self._modelSearchProxy = QSortFilterProxyModel(parent=self)
        self._modelSearchProxy = DeviceSearchProxyModel(parent=self)
        self._modelSearchProxy.setSourceModel(self._modelDeviceTree)

        # connect ui facade to models
        self._uiFacade.setDomainModel(self._modelDomain)

        # actions
        self.actRefresh = QAction("Обновить", self)
        self.actDeviceAdd = QAction("Добавить устройство", self)
        self.actDeviceEdit = QAction("Изменить устройство", self)
        self.actDeviceDelete = QAction("Удалить устройство", self)

    def initApp(self):
        # init instances
        # engines
        self._persistenceEngine.initEngine()

        # facades
        self._persistenceFacade.initFacade()
        self._uiFacade.initFacade()

        # models
        self._modelDomain.initModel()
        self._modelDeviceTree.treeType = 1

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
        self.ui.treeDeviceList.setColumnHidden(5, True)

    #     # setup filter widgets
        self.ui.comboVendorFilter.setModel(self._modelDomain.vendorMapModel)

        # create actions
        self.initActions()

        # setup ui widget signals
        # buttons
        self.ui.radioImport.toggled.connect(self.onRadioImportToggled)
        self.ui.btnDeviceAdd.clicked.connect(self.onBtnDeviceAddClicked)
        self.ui.btnDeviceEdit.clicked.connect(self.onBtnDeviceEditClicked)
        self.ui.btnDeviceDelete.clicked.connect(self.onBtnDeviceDeleteClicked)

        # tree and selection
        self.ui.treeDeviceList.selectionModel().currentChanged.connect(self.onCurrentTreeItemChanged)
        self.ui.treeDeviceList.doubleClicked.connect(self.onTreeDoubleClicked)

        # search widgets
        self.ui.comboVendorFilter.currentIndexChanged.connect(self.setSearchFilter)
        self.ui.editSearch.textChanged.connect(self.setSearchFilter)

        # self.setSearchFilter()

    def initActions(self):
        self.actRefresh.setShortcut("Ctrl+R")
        self.actRefresh.setStatusTip("Обновить данные")
        self.actRefresh.triggered.connect(self.procActRefresh)

        self.actDeviceAdd.setStatusTip("Добавить устройство")
        self.actDeviceAdd.triggered.connect(self.procActDeviceAdd)

        self.actDeviceEdit.setStatusTip("Изменить устройство")
        self.actDeviceEdit.triggered.connect(self.procActDeviceEdit)

        self.actDeviceDelete.setStatusTip("Удалить устройство")
        self.actDeviceDelete.triggered.connect(self.procActDeviceDelete)

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
        if checked:
            self._modelDeviceTree.treeType = 1
        else:
            self._modelDeviceTree.treeType = 2

    def onBtnDeviceAddClicked(self):
        self.actDeviceAdd.trigger()

    def onBtnDeviceEditClicked(self):
        self.actDeviceEdit.trigger()

    def onBtnDeviceDeleteClicked(self):
        self.actDeviceDelete.trigger()

    def onCurrentTreeItemChanged(self, cur: QModelIndex, prev: QModelIndex):
        sourceIndex = self._modelSearchProxy.mapToSource(cur)
        self.updateItemInfo(sourceIndex)

    def onTreeDoubleClicked(self, index):
        if index.column() != 0:
            self.actDeviceEdit.trigger()

    def setSearchFilter(self, dummy=0):
        self._modelSearchProxy.filterString = self.ui.editSearch.text()
        self._modelSearchProxy.filterVendor = self.ui.comboVendorFilter.currentData(const.RoleNodeId)

        self._modelSearchProxy.invalidate()
        # self.ui.treeDeviceList.setColumnHidden(5, True)

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

    def procActDeviceAdd(self):
        self._uiFacade.requestDeviceAdd()

    def procActDeviceEdit(self):
        if not self.ui.treeDeviceList.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка!", "Выберите запись о приборе для редактирования.")
            return False

        selectedIndex = self.ui.treeDeviceList.selectionModel().selectedIndexes()[0]
        self._uiFacade.requestDeviceEdit(self._modelSearchProxy.mapToSource(selectedIndex))

    def procActDeviceDelete(self):
        if not self.ui.treeDeviceList.selectionModel().hasSelection():
            QMessageBox.information(self, "Ошибка!", "Выберите запись о приборе для удаления.")
            return False

        selectedIndex = self.ui.treeDeviceList.selectionModel().selectedIndexes()[0]
        self._uiFacade.requestDeviceDelete(self._modelSearchProxy.mapToSource(selectedIndex))
