import random

from PySide6 import QtCore, QtGui

from SpatialNode.style import Style


class ConnectionStyle(Style):
    ConstructionColor: QtGui.QColor
    NormalColor: QtGui.QColor
    SelectedColor: QtGui.QColor
    SelectedHaloColor: QtGui.QColor
    HoveredColor: QtGui.QColor

    LineWidth: float
    ConstructionLineWidth: float
    PointDiameter: float

    UseDataDefinedColors: bool

    def __init__(self):
        super().__init__()

    def loadJson(self, json: QtCore.QJsonArray):
        return NotImplemented

    def toJson(self):
        return NotImplemented

    @staticmethod
    def setConnectionStyle(jsonText):
        return NotImplemented

    def normalColor(self, typeId):
        hue = random.randint(0, 0xFF)
        sat = 120 + hash(typeId) % 129
        return QtGui.QColor.fromHsl(hue, sat, 160)
