from PyQt5.QtWidgets import QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QFormLayout, QRadioButton
from PyQt5.QtCore import Qt


class InputDialog(QDialog):

    def __init__(self, parent=None, title=None, widgetList=None, widgetTitleList=None, widgetDataList=None):
        super(InputDialog, self).__init__(parent)

        self.setAttribute(Qt.WA_QuitOnClose)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # create instance variables
        # self.widgetList = widgetList
        # self.widgetTitleList = widgetTitleList
        self.widgetDataList = widgetDataList

        self.widgetInstanceList = list()

        # create ui
        # create data widgets from the list

        # fill form layout with provided widgets
        self.formLayout = QFormLayout()
        self.formLayout.setFormAlignment(Qt.AlignRight | Qt.AlignTop)
        self.formLayout.setSpacing(1)
        self.formLayout.setContentsMargins(9, 1, 9, 1)
        for w, t in zip(widgetList, widgetTitleList):
            if "QRadioButton" in str(w):
                wi = w(text=t, parent=self)
                self.widgetInstanceList.append([wi, wi.isChecked, wi.setChecked])
                self.formLayout.addRow('', self.widgetInstanceList[-1][0])
            elif "QLineEdit" in str(w):
                wi = w(parent=self)
                self.widgetInstanceList.append([wi, wi.text, wi.setText])
                self.formLayout.addRow(t, self.widgetInstanceList[-1][0])
            else:
                pass

        # create button row
        self.btnOk = QPushButton("Принять", self)
        self.btnOk.setDefault(True)
        self.btnCancel = QPushButton("Отменить", self)
        self.buttonBlockLayout = QHBoxLayout()
        self.buttonBlockLayout.addStretch(1)
        self.buttonBlockLayout.addWidget(self.btnOk)
        self.buttonBlockLayout.addWidget(self.btnCancel)

        # create dialog layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.formLayout, 1)
        self.mainLayout.addLayout(self.buttonBlockLayout, 1)

        self.setLayout(self.mainLayout)

        if title is not None:
            self.setWindowTitle(title)

        # setup signals
        self.btnOk.clicked.connect(self.onBtnOkClicked)
        self.btnCancel.clicked.connect(self.onBtnCancelClicked)

        self.updateWidgets()

    def updateWidgets(self):
        for w, d in zip(self.widgetInstanceList, self.widgetDataList):
            w[2](d)

    def collectData(self):
        self.widgetDataList = list()
        for w in self.widgetInstanceList:
            self.widgetDataList.append(w[1]())

    def getData(self):
        return self.widgetDataList

    def onBtnOkClicked(self):
        # TODO: make generic data verification
        self.collectData()
        self.accept()

    def onBtnCancelClicked(self):
        self.reject()
