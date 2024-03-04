#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtGui

from SpatialNode.abstract_node_painter import AbstractNodePainter
from SpatialNode.node_graphics_object import NodeGraphicsObject

class DefaultNodePainter(AbstractNodePainter):
    @override
    def paint(self, painter: QtGui.QPainter, ngo: NodeGraphicsObject) -> None: ...
    def drawNodeRect(
        self, painter: QtGui.QPainter, ngo: NodeGraphicsObject
    ) -> None: ...
    def drawConnectionPoints(
        self, painter: QtGui.QPainter, ngo: NodeGraphicsObject
    ) -> None: ...
    def drawFilledConnectionPoints(
        self, painter: QtGui.QPainter, ngo: NodeGraphicsObject
    ) -> None: ...
    def drawNodeCaption(
        self, painter: QtGui.QPainter, ngo: NodeGraphicsObject
    ) -> None: ...
    def drawEntryLabels(
        self, painter: QtGui.QPainter, ngo: NodeGraphicsObject
    ) -> None: ...
    def drawResizeRect(
        self, painter: QtGui.QPainter, ngo: NodeGraphicsObject
    ) -> None: ...
