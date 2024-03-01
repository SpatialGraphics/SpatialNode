import sys

from PySide6 import QtWidgets

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    widget = QtWidgets.QWidget()
    widget.setWindowTitle('hello qt')
    widget.show()
    sys.exit(app.exec())
