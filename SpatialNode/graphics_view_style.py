#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.
from typing import override

from PySide6 import QtGui

from SpatialNode.definitions import QJsonObject
from SpatialNode.style import Style, json_read_color
from SpatialNode.resources import qInitResources


class GraphicsViewStyle(Style):
    BackgroundColor: QtGui.QColor = None
    FineGridColor: QtGui.QColor = None
    CoarseGridColor: QtGui.QColor = None

    def __init__(self):
        super().__init__()
        qInitResources()
        self.loadJsonFile(":DefaultStyle.json")

    def fromJsonText(self, jsonText: str):
        self.loadJsonText(jsonText)

    @staticmethod
    def setStyle(jsonText: str):
        from SpatialNode.style_collection import StyleCollection

        style = GraphicsViewStyle()
        style.fromJsonText(jsonText)

        StyleCollection.setGraphicsViewStyle(style)

    @override
    def loadJson(self, json):
        obj = json["GraphicsViewStyle"]

        self.BackgroundColor = json_read_color(
            obj, "BackgroundColor", self.BackgroundColor
        )
        self.FineGridColor = json_read_color(obj, "FineGridColor", self.FineGridColor)
        self.CoarseGridColor = json_read_color(
            obj, "CoarseGridColor", self.CoarseGridColor
        )

    @override
    def toJson(self):
        obj = QJsonObject()

        obj["BackgroundColor"] = self.BackgroundColor.name()
        obj["FineGridColor"] = self.FineGridColor.name()
        obj["CoarseGridColor"] = self.CoarseGridColor.name()

        root = QJsonObject()
        root["GraphicsViewStyle"] = obj
        return root
