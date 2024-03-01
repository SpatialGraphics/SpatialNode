from PySide6 import QtCore, QtGui

from SpatialNode.style import Style


class NodeStyle(Style):
    NormalBoundaryColor: QtGui.QColor
    SelectedBoundaryColor: QtGui.QColor
    GradientColor0: QtGui.QColor
    GradientColor1: QtGui.QColor
    GradientColor2: QtGui.QColor
    GradientColor3: QtGui.QColor
    ShadowColor: QtGui.QColor
    FontColor: QtGui.QColor
    FontColorFaded: QtGui.QColor

    ConnectionPointColor: QtGui.QColor
    FilledConnectionPointColor: QtGui.QColor

    WarningColor: QtGui.QColor
    ErrorColor: QtGui.QColor

    PenWidth: float
    HoveredPenWidth: float

    ConnectionPointDiameter: float

    Opacity: float

    def __init__(self):
        super().__init__()

    def loadJson(self, json: QtCore.QJsonArray):
        return NotImplemented

    def toJson(self):
        return NotImplemented
