#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import random
from typing import override

from PySide6 import QtGui

from SpatialNode.definitions import QJsonObject
from SpatialNode.style import Style, json_read_color, json_read_float, json_read_bool
from SpatialNode.resources import qInitResources


class ConnectionStyle(Style):
    ConstructionColor: QtGui.QColor = None
    NormalColor: QtGui.QColor = None
    SelectedColor: QtGui.QColor = None
    SelectedHaloColor: QtGui.QColor = None
    HoveredColor: QtGui.QColor = None

    LineWidth: float = 0
    ConstructionLineWidth: float = 0
    PointDiameter: float = 0

    UseDataDefinedColors: bool = False

    def __init__(self):
        super().__init__()
        qInitResources()
        self.loadJsonFile(":DefaultStyle.json")

    def fromJsonText(self, jsonText: str):
        self.loadJsonText(jsonText)

    @staticmethod
    def setConnectionStyle(jsonText: str):
        from SpatialNode.style_collection import StyleCollection

        style = ConnectionStyle()
        style.fromJsonText(jsonText)

        StyleCollection.setConnectionStyle(style)

    @override
    def loadJson(self, json):
        obj = json["ConnectionStyle"]

        self.ConstructionColor = json_read_color(
            obj, "ConstructionColor", self.ConstructionColor
        )
        self.NormalColor = json_read_color(obj, "NormalColor", self.NormalColor)
        self.SelectedColor = json_read_color(obj, "SelectedColor", self.SelectedColor)
        self.SelectedHaloColor = json_read_color(
            obj, "SelectedHaloColor", self.SelectedHaloColor
        )
        self.HoveredColor = json_read_color(obj, "HoveredColor", self.HoveredColor)

        self.LineWidth = json_read_float(obj, "LineWidth", self.LineWidth)
        self.ConstructionLineWidth = json_read_float(
            obj, "ConstructionLineWidth", self.ConstructionLineWidth
        )
        self.PointDiameter = json_read_float(obj, "PointDiameter", self.PointDiameter)

        self.UseDataDefinedColors = json_read_bool(
            obj, "UseDataDefinedColors", self.UseDataDefinedColors
        )

    @override
    def toJson(self):
        obj = QJsonObject()
        obj["ConstructionColor"] = self.ConstructionColor.name()
        obj["NormalColor"] = self.NormalColor.name()
        obj["SelectedColor"] = self.SelectedColor.name()
        obj["SelectedHaloColor"] = self.SelectedHaloColor.name()
        obj["HoveredColor"] = self.HoveredColor.name()

        obj["LineWidth"] = self.LineWidth
        obj["ConstructionLineWidth"] = self.ConstructionLineWidth
        obj["PointDiameter"] = self.PointDiameter

        obj["UseDataDefinedColors"] = self.UseDataDefinedColors

        root = QJsonObject()
        root["ConnectionStyle"] = obj

        return root

    def normalColor(self, typeId):
        random.seed(hash(typeId))
        hue = random.randint(0, 0xFF)
        sat = 120 + hash(typeId) % 129
        return QtGui.QColor.fromHsl(hue, sat, 160)
