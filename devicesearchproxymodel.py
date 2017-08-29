import const
import re
from PyQt5.QtCore import QSortFilterProxyModel, QDate, Qt


class DeviceSearchProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(DeviceSearchProxyModel, self).__init__(parent)

        self.filterVendor = 0
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

    def filterAcceptsRow(self, source_row, source_parent_index):
        source_index = self.sourceModel().index(source_row, self.filterKeyColumn(), source_parent_index)
        if source_index.isValid():
            # recursive test children
            rows = self.sourceModel().rowCount(source_index)
            if rows > 0:
                for i in range(rows):
                    if self.filterAcceptsRow(i, source_index):
                        return True

            # test self
            vendor = self.sourceModel().index(source_row, 0, source_parent_index).data(const.RoleVendor)
            if self.filterVendor == 0 or self.filterVendor == vendor:
                for i in range(self.sourceModel().columnCount()):
                    if self._filterRegex.findall(str(self.sourceModel().index(source_row, i,
                                                                              source_parent_index).data(Qt.DisplayRole))):
                        return True

            # test parents
            parent = source_parent_index
            while parent.isValid():
                if self.filterAcceptsRow(parent.row(), parent.parent()):
                    return True
                parent = parent.parent()

        return False
