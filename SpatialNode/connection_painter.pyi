#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtGui

from SpatialNode.connection_graphics_object import ConnectionGraphicsObject

def cubicPath(connection: ConnectionGraphicsObject) -> QtGui.QPainterPath: ...
def drawSketchLine(painter: QtGui.QPainter, cgo: ConnectionGraphicsObject) -> None: ...
def drawHoveredOrSelected(
    painter: QtGui.QPainter, cgo: ConnectionGraphicsObject
) -> None: ...
def drawNormalLine(painter: QtGui.QPainter, cgo: ConnectionGraphicsObject) -> None: ...

class ConnectionPainter:
    @staticmethod
    def paint(painter: QtGui.QPainter, cgo: ConnectionGraphicsObject) -> None: ...
    @staticmethod
    def getPainterStroke(
        connection: ConnectionGraphicsObject,
    ) -> QtGui.QPainterPath: ...
