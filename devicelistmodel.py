import const
from deviceitem import DeviceItem
from PyQt5.QtCore import Qt, QModelIndex, QVariant, QDate, pyqtSlot, pyqtSignal, QAbstractItemModel
from PyQt5.QtGui import QBrush, QColor


class TreeNode(object):

    def __init__(self, data=None, parent=None):
        self.data = data
        self.parentNode = parent
        self.childNodes = list()

    def appendChild(self, item):
        self.childNodes.append(item)

    def child(self, row):
        return self.childNodes[row]

    def childCount(self):
        return len(self.childNodes)

    def parent(self):
        return self.parentNode

    def row(self):
        if self.parentNode:
            return self.parentNode.childItems.index(self)
        return 0

    @classmethod
    def makeNode(cls, data, parent):
        return cls(data, parent)

class DeviceListModel(QAbstractItemModel):

    ColumnId = 0
    ColumnName = ColumnId + 1
    ColumnVendor = ColumnName + 1
    ColumnDescription = ColumnVendor + 1
    ColumnSpec = ColumnDescription + 1
    ColumnTags = ColumnSpec + 1
    ColumnCount = ColumnTags + 1

    _headers = ["Каталог", "Наименование", "Производитель", "Описание", "Характеристики", "Теги"]

    def __init__(self, parent=None, domainModel=None):
        super(DeviceListModel, self).__init__(parent)
        self._modelDomain = domainModel

        self.rootNode = TreeNode(None, None)

    def clear(self):
        pass

    def buildNode(self, root, data):
        for d in data:
            node = TreeNode(d, root)
            self.buildNode(node, self._modelDomain.getHomebrewItemListByParentId(d.item_id))
            root.appendChild(node)

    def initModel(self):
        print("init tree model")
        self.buildNode(self.rootNode, self._modelDomain.importDeviceList)

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole and section < len(self._headers):
            return QVariant(self._headers[section])
        return QVariant()

    def rowCount(self, parent=QModelIndex(), *args, **kwargs):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentNode = self.rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent=QModelIndex(), *args, **kwargs):
        return self.ColumnCount

    def index(self, row, col, parent, *args, **kwargs):

        if not self.hasIndex(row, col, parent):
            return QModelIndex()

        if not parent.isValid():
            parentNode = self.rootNode
        else:
            parentNode = parent.internalPointer()

        childNode = parentNode.child(row)
        if childNode:
            return self.createIndex(row, col, childNode)
        else:
            return QModelIndex()

    def parent(self, index):

        if not index.isValid():
            return QModelIndex()

        childNode = index.internalPointer()
        if not childNode:
            return QModelIndex()

        parentNode = childNode.parent()

        if parentNode == self.rootNode:
            return QModelIndex()

        return self.createIndex(parentNode.row(), index.column(), parentNode)

    # def setData(self, index, value, role):
    #     return True

    def data(self, index: QModelIndex, role=None):

        if not index.isValid():
            return QVariant()

        col = index.column()
        row = index.row()

        item = index.internalPointer()

        if role == Qt.DisplayRole or role == Qt.ToolTipRole:
            if col == self.ColumnId:
                return QVariant(item.data.item_id)
            elif col == self.ColumnName:
                return QVariant(item.data.item_name)
            elif col == self.ColumnVendor:
                return QVariant(item.data.item_vendor)
            elif col == self.ColumnDescription:
                return QVariant(item.data.item_desc)
            elif col == self.ColumnSpec:
                return QVariant(item.data.item_spec)
            elif col == self.ColumnTags:
                return QVariant(item.data.item_tags)

        # elif role == Qt.BackgroundRole:
        #     # FIXME hardcoded ids for coloring - add color codes to SQL table?
        #     retcolor = Qt.white;
        #
        #     if item.item_status == 1:
        #         retcolor = const.COLOR_PAYMENT_FINISHED
        #
        #     if col == self.ColumnStatus:
        #         if item.item_status == 2:
        #             retcolor = const.COLOR_PAYMENT_PENDING
        #     if col == self.ColumnPriority:
        #         if item.item_status != 1:
        #             if item.item_priority == 2:  # 3 4
        #                 retcolor = const.COLOR_PRIORITY_LOW
        #             elif item.item_priority == 3:
        #                 retcolor = const.COLOR_PRIORITY_MEDIUM
        #             elif item.item_priority == 4:
        #                 retcolor = const.COLOR_PRIORITY_HIGH
        #     if col == self.ColumnShipmentStatus:
        #         if item.item_shipment_status == 2:
        #             retcolor = const.COLOR_ARRIVAL_PENDING
        #         if item.item_shipment_status == 3:
        #             retcolor = const.COLOR_ARRIVAL_PARTIAL
        #         if item.item_shipment_status == 4:
        #             retcolor = const.COLOR_ARRIVAL_RECLAIM
        #     return QVariant(QBrush(QColor(retcolor)))

        elif role == const.RoleNodeId:
            return QVariant(item.data.item_id)

        return QVariant()

    # def flags(self, index):
    #     f = super(DeviceListModel, self).flags(index)
    #     return f

    @pyqtSlot(int, int)
    def itemsInserted(self, first: int, last: int):
        self.beginInsertRows(QModelIndex(), first, last)
        # print("table model slot:", first, last)
        self.endInsertRows()

    @pyqtSlot(int, int)
    def itemsRemoved(self, first: int, last: int):
        self.beginRemoveRows(QModelIndex(), first, last)
        # print("table model slot:", first, last)
        self.endRemoveRows()
