#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtCore, QtGui, QtWidgets

from SpatialNode.node_graphics_object import NodeGraphicsObject

def locateNodeAt(
    scenePoint: QtCore.QPointF,
    scene: QtWidgets.QGraphicsScene,
    viewTransform: QtGui.QTransform,
) -> NodeGraphicsObject: ...
