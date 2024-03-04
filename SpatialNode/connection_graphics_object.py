#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import weakref
from typing import override

from PySide6 import QtWidgets, QtCore


class ConnectionGraphicsObject(QtWidgets.QGraphicsObject):
    def __init__(self, scene, connectionId):
        from SpatialNode.connection_state import ConnectionState

        super().__init__()
        self._connectionId = connectionId
        self._graphModel = scene.graphModel
        self._connectionState = ConnectionState(weakref.proxy(self))
        self._out = QtCore.QPointF()
        self._in = QtCore.QPointF()

        scene.addItem(self)

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, True)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setAcceptHoverEvents(True)
        self.setZValue(-1.0)
        self._initializePosition()

    @property
    def graphModel(self):
        return self._graphModel

    @property
    def nodeScene(self):
        return self.scene()

    @property
    def connectionId(self):
        return self._connectionId

    @override
    def boundingRect(self):
        from SpatialNode.style_collection import StyleCollection

        c1, c2 = self.pointsC1C2()
        basicRect = QtCore.QRectF(self._out, self._in).normalized()
        c1c2Rect = QtCore.QRectF(c1, c2).normalized()
        commonRect = basicRect.united(c1c2Rect)
        connectionStyle = StyleCollection.connectionStyle()
        diam = connectionStyle.PointDiameter
        cornerOffset = QtCore.QPointF(diam, diam)

        # Expand rect by port circle diameter
        commonRect.setTopLeft(commonRect.topLeft() - cornerOffset)
        commonRect.setBottomRight(commonRect.bottomRight() + cornerOffset * 2)
        return commonRect

    @override
    def shape(self):
        from SpatialNode.connection_painter import ConnectionPainter

        return ConnectionPainter.getPainterStroke(self)

    def endPoint(self, portType):
        from SpatialNode.definitions import PortType

        return self._out if portType == PortType.Out else self._in

    def outSlot(self):
        return self._out

    def inSlot(self):
        return self._in

    def pointsC1C2(self):
        match self.nodeScene.orientation:
            case QtCore.Qt.Orientation.Horizontal:
                return self._pointsC1C2Horizontal()
            case QtCore.Qt.Orientation.Vertical:
                return self._pointsC1C2Vertical()

    def setEndPoint(self, portType, point):
        from SpatialNode.definitions import PortType

        if portType == PortType.In:
            self._in = point
        else:
            self._out = point

    # Updates the position of both ends
    def move(self):
        from SpatialNode.definitions import ConnectionId, PortType, InvalidNodeId

        def moveEnd(cId: ConnectionId, portType: PortType):
            from SpatialNode.connection_id_utils import getNodeId, getPortIndex

            nodeId = getNodeId(portType, cId)

            if nodeId == InvalidNodeId:
                return

            ngo = self.nodeScene.nodeGraphicsObject(nodeId)

            if ngo is not None:
                geometry = self.nodeScene.nodeGeometry
                scenePos = geometry.portScenePosition(
                    nodeId, portType, getPortIndex(portType, cId), ngo.sceneTransform()
                )
                connectionPos = self.sceneTransform().inverted()[0].map(scenePos)
                self.setEndPoint(portType, connectionPos)

        moveEnd(self._connectionId, PortType.Out)
        moveEnd(self._connectionId, PortType.In)
        self.prepareGeometryChange()
        self.update()

    @property
    def connectionState(self):
        return self._connectionState

    @override
    def paint(self, painter, option, widget=...):
        from SpatialNode.connection_painter import ConnectionPainter

        if not self.scene():
            return

        painter.setClipRect(option.exposedRect)
        ConnectionPainter.paint(painter, self)

    @override
    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    @override
    def mouseMoveEvent(self, event):
        from SpatialNode.locate_node import locateNodeAt

        self.prepareGeometryChange()

        view = QtWidgets.QGraphicsView(event.widget())
        ngo = locateNodeAt(event.scenePos(), self.nodeScene, view.transform())
        if ngo is not None:
            ngo.reactToConnection(self)
            self._connectionState.lastHoveredNode = ngo.nodeId()
        else:
            self._connectionState.resetLastHoveredNode()

        requiredPort = self._connectionState.requiredPort()

        if requiredPort is not None:
            self.setEndPoint(requiredPort, event.pos())

        self.update()
        event.accept()

    @override
    def mouseReleaseEvent(self, event):
        from SpatialNode.locate_node import locateNodeAt
        from SpatialNode.node_connection_interaction import NodeConnectionInteraction

        super().mouseReleaseEvent(event)

        self.ungrabMouse()
        event.accept()

        view = QtWidgets.QGraphicsView(event.widget())
        ngo = locateNodeAt(event.scenePos(), self.nodeScene, view.transform())

        wasConnected = False

        if ngo is not None:
            interaction = NodeConnectionInteraction(ngo, self, self.nodeScene)
            wasConnected = interaction.tryConnect()

        if not wasConnected:
            self.nodeScene.resetDraftConnection()

    @override
    def hoverEnterEvent(self, event):
        self._connectionState.hovered = True
        self.update()
        self.nodeScene.connectionHovered.emit(self.connectionId, event.screenPos())
        event.accept()

    @override
    def hoverLeaveEvent(self, event):
        self._connectionState.hovered = False
        self.update()
        self.nodeScene.connectionHoverLeft.emit(self.connectionId)
        event.accept()

    def _initializePosition(self):
        from SpatialNode.connection_id_utils import (
            oppositePort,
            getPortIndex,
            getNodeId,
        )

        if self._connectionState.requiredPort() is not None:
            attachedPort = oppositePort(self._connectionState.requiredPort())

            portIndex = getPortIndex(attachedPort, self._connectionId)
            nodeId = getNodeId(attachedPort, self._connectionId)

            ngo = self.nodeScene.nodeGraphicsObject(nodeId)

            if ngo is not None:
                nodeSceneTransform = ngo.sceneTransform()
                geometry = self.nodeScene.nodeGeometry
                pos = geometry.portScenePosition(
                    nodeId, attachedPort, portIndex, nodeSceneTransform
                )
                self.setPos(pos)

        self.move()

    def _addGraphicsEffect(self):
        effect = QtWidgets.QGraphicsBlurEffect()
        effect.setBlurRadius(5)
        self.setGraphicsEffect(effect)

    def _pointsC1C2Horizontal(self):
        defaultOffset = 200.0
        xDistance = self._in.x() - self._out.x()
        horizontalOffset = min(defaultOffset, abs(xDistance))
        verticalOffset = 0
        ratioX = 0.5

        if xDistance <= 0:
            yDistance = self._in.y() - self._out.y() + 20
            vector = -1.0 if yDistance < 0 else 1.0
            verticalOffset = min(defaultOffset, abs(yDistance)) * vector
            ratioX = 1.0

        horizontalOffset *= ratioX
        c1 = QtCore.QPointF(
            self._out.x() + horizontalOffset, self._out.y() + verticalOffset
        )
        c2 = QtCore.QPointF(
            self._in.x() - horizontalOffset, self._in.y() - verticalOffset
        )
        return c1, c2

    def _pointsC1C2Vertical(self):
        defaultOffset = 200.0
        yDistance = self._in.y() - self._out.y()
        verticalOffset = min(defaultOffset, abs(yDistance))
        horizontalOffset = 0
        ratioY = 0.5

        if yDistance <= 0:
            xDistance = self._in.x() - self._out.x() + 20
            vector = -1.0 if xDistance < 0 else 1.0
            horizontalOffset = min(defaultOffset, abs(xDistance)) * vector
            ratioY = 1.0

        verticalOffset *= ratioY
        c1 = QtCore.QPointF(
            self._out.x() + horizontalOffset, self._out.y() + verticalOffset
        )
        c2 = QtCore.QPointF(
            self._in.x() - horizontalOffset, self._in.y() - verticalOffset
        )
        return c1, c2
