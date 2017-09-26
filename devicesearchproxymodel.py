import const
import re
from PyQt5.QtCore import QSortFilterProxyModel, QDate, Qt


class DeviceSearchProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(DeviceSearchProxyModel, self).__init__(parent)

        self.filterVendor = 0
        self.filterDevtype = 0
        self._filterString = ""
        self._filterRegex = re.compile(self._filterString, flags=re.IGNORECASE)

    @property
    def filterString(self):
        return self._filterString

    @filterString.setter
    def filterString(self, string):
        if type(string) == str:
            self._filterString = string
            self._filterRegex = re.compile(string, flags=re.IGNORECASE)
        else:
            raise TypeError("Filter must be a str.")

    def filterAcceptsSelf(self, row, parent_index):
        vendor = self.sourceModel().index(row, 0, parent_index).data(const.RoleVendor)
        devtype = self.sourceModel().index(row, 0, parent_index).data(const.RoleDevtype)
        if self.filterVendor == 0 or self.filterVendor == vendor:
            if self.filterDevtype == 0 or self.filterDevtype == devtype:
                for i in range(self.sourceModel().columnCount()):
                    string = str(self.sourceModel().index(row, i, parent_index).data(Qt.DisplayRole))
                    if self._filterRegex.findall(string):
                        return True
        return False

    def filterAcceptsAnyParent(self, parent_index):
        parent = parent_index
        while parent.isValid():
            if self.filterAcceptsSelf(parent.row(), parent.parent()):
                return True
            parent = parent.parent()
        return False

    def hasAcceptedChildren(self, row, parent_index):
        source_index = self.sourceModel().index(row, self.filterKeyColumn(), parent_index)
        rows = self.sourceModel().rowCount(source_index)
        for i in range(rows):
            if self.filterAcceptsRow(i, source_index):
                return True
        return False

    def filterAcceptsRow(self, source_row, source_parent_index):
        # check self
        if self.filterAcceptsSelf(source_row, source_parent_index):
            return True

        # check parents
        if self.filterAcceptsAnyParent(source_parent_index):
            return True

        # check children
        if self.hasAcceptedChildren(source_row, source_parent_index):
            return True

        return False
