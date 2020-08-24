import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets
from main_window import Ui_MainWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.setFixedSize(710,455)

    MainWindow.show()
    sys.exit(app.exec_())
