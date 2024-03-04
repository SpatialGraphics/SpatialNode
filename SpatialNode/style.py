#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from abc import abstractmethod

from PySide6 import QtCore, QtGui


class Style:
    def __init__(self):
        return

    @abstractmethod
    def loadJson(self, json): ...

    @abstractmethod
    def toJson(self): ...

    def loadJsonFromByteArray(self, byteArray):
        json = QtCore.QJsonDocument.fromJson(byteArray).object()
        self.loadJson(json)

    def loadJsonText(self, jsonText: str):
        self.loadJsonFromByteArray(QtCore.QByteArray.fromStdString(jsonText))

    def loadJsonFile(self, fileName: str):
        file = QtCore.QFile(fileName)

        if not file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly):
            QtCore.qWarning("Couldn't open file")
            return
        self.loadJsonFromByteArray(file.readAll())


def json_read_color(obj, key, default):
    valueRef = obj.get(key, default)
    if isinstance(valueRef, str):
        return QtGui.QColor(valueRef)
    elif isinstance(valueRef, list):
        return QtGui.QColor(valueRef[0], valueRef[1], valueRef[2])
    else:
        return valueRef


def json_read_float(obj, key, default):
    return obj.get(key, default)


def json_read_bool(obj, key, default):
    return obj.get(key, default)
