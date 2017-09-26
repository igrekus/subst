import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow
from reportlab.lib.testutils import setOutDir
setOutDir(__name__)


def main():
    app = QApplication(sys.argv)
    # app.setStyle("macintosh")
    w = MainWindow()
    w.initApp()
    # w.showMaximized()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# import csv
#
# with open("ref/1.csv") as f:
#     d = csv.reader(f, delimiter=";")
#     for a in d:
#         print(a)
