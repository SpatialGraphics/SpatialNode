#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.
from typing import override

from PySide6 import QtGui

from SpatialNode.definitions import QJsonObject
from SpatialNode.style import Style, json_read_color, json_read_float
from SpatialNode.resources import qInitResources


class NodeStyle(Style):
    NormalBoundaryColor: QtGui.QColor = None
    SelectedBoundaryColor: QtGui.QColor = None
    GradientColor0: QtGui.QColor = None
    GradientColor1: QtGui.QColor = None
    GradientColor2: QtGui.QColor = None
    GradientColor3: QtGui.QColor = None
    ShadowColor: QtGui.QColor = None
    FontColor: QtGui.QColor = None
    FontColorFaded: QtGui.QColor = None

    ConnectionPointColor: QtGui.QColor = None
    FilledConnectionPointColor: QtGui.QColor = None

    WarningColor: QtGui.QColor = None
    ErrorColor: QtGui.QColor = None

    PenWidth: float = 0
    HoveredPenWidth: float = 0

    ConnectionPointDiameter: float = 0

    Opacity: float = 0

    def __init__(self):
        super().__init__()
        qInitResources()
        self.loadJsonFile(":DefaultStyle.json")

    def fromJsonText(self, jsonText: str):
        self.loadJsonText(jsonText)

    def fromJsonObject(self, obj: QJsonObject):
        self.loadJson(obj)

    @staticmethod
    def setNodeStyle(jsonText: str):
        from SpatialNode.style_collection import StyleCollection

        style = NodeStyle()
        style.fromJsonText(jsonText)
        StyleCollection.setNodeStyle(style)

    @override
    def loadJson(self, json):
        obj = json["NodeStyle"]

        self.NormalBoundaryColor = json_read_color(
            obj, "NormalBoundaryColor", self.NormalBoundaryColor
        )
        self.SelectedBoundaryColor = json_read_color(
            obj, "SelectedBoundaryColor", self.SelectedBoundaryColor
        )
        self.GradientColor0 = json_read_color(
            obj, "GradientColor0", self.GradientColor0
        )
        self.GradientColor1 = json_read_color(
            obj, "GradientColor1", self.GradientColor1
        )
        self.GradientColor2 = json_read_color(
            obj, "GradientColor2", self.GradientColor2
        )
        self.GradientColor3 = json_read_color(
            obj, "GradientColor3", self.GradientColor3
        )
        self.ShadowColor = json_read_color(obj, "ShadowColor", self.ShadowColor)
        self.FontColor = json_read_color(obj, "FontColor", self.FontColor)
        self.FontColorFaded = json_read_color(
            obj, "FontColorFaded", self.FontColorFaded
        )
        self.ConnectionPointColor = json_read_color(
            obj, "ConnectionPointColor", self.ConnectionPointColor
        )
        self.FilledConnectionPointColor = json_read_color(
            obj, "FilledConnectionPointColor", self.FilledConnectionPointColor
        )
        self.WarningColor = json_read_color(obj, "WarningColor", self.WarningColor)
        self.ErrorColor = json_read_color(obj, "ErrorColor", self.ErrorColor)

        self.PenWidth = json_read_float(obj, "PenWidth", self.PenWidth)
        self.HoveredPenWidth = json_read_float(
            obj, "HoveredPenWidth", self.HoveredPenWidth
        )
        self.ConnectionPointDiameter = json_read_float(
            obj, "ConnectionPointDiameter", self.ConnectionPointDiameter
        )
        self.Opacity = json_read_float(obj, "Opacity", self.Opacity)

    @override
    def toJson(self):
        obj = QJsonObject()
        obj["NormalBoundaryColor"] = self.NormalBoundaryColor.name()
        obj["SelectedBoundaryColor"] = self.SelectedBoundaryColor.name()
        obj["GradientColor0"] = self.GradientColor0.name()
        obj["GradientColor1"] = self.GradientColor1.name()
        obj["GradientColor2"] = self.GradientColor2.name()
        obj["GradientColor3"] = self.GradientColor3.name()
        obj["ShadowColor"] = self.ShadowColor.name()
        obj["FontColor"] = self.FontColor.name()
        obj["FontColorFaded"] = self.FontColorFaded.name()
        obj["ConnectionPointColor"] = self.ConnectionPointColor.name()
        obj["FilledConnectionPointColor"] = self.FilledConnectionPointColor.name()
        obj["WarningColor"] = self.WarningColor.name()
        obj["ErrorColor"] = self.ErrorColor.name()

        obj["PenWidth"] = self.PenWidth
        obj["HoveredPenWidth"] = self.HoveredPenWidth
        obj["ConnectionPointDiameter"] = self.ConnectionPointDiameter
        obj["Opacity"] = self.Opacity

        root = QJsonObject()
        root["NodeStyle"] = obj

        return root
