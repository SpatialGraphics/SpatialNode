from PySide6 import QtCore


class Style:
    def __init__(self):
        return

    def loadJson(self, json: QtCore.QJsonArray):
        return NotImplementedError()

    def toJson(self):
        return NotImplementedError()
