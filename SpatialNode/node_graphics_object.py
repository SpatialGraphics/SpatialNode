#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtWidgets, QtCore, QtGui


class NodeGraphicsObject(QtWidgets.QGraphicsObject):
    def __init__(self, scene, node):
        from SpatialNode.node_state import NodeState
        from SpatialNode.node_style import NodeStyle
        from SpatialNode.definitions import NodeRole

        super().__init__()
        self._nodeId = node
        self._graphModel = scene.graphModel
        self._nodeState = NodeState()
        self._proxyWidget = None

        scene.addItem(self)

        self.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemDoesntPropagateOpacityToChildren,
            True,
        )
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsFocusable, True)

        self._setLockedState()

        self.setCacheMode(QtWidgets.QGraphicsItem.CacheMode.DeviceCoordinateCache)

        nodeStyle = NodeStyle()
        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setOffset(4, 4)
        effect.setBlurRadius(20)
        effect.setColor(nodeStyle.ShadowColor)

        self.setGraphicsEffect(effect)
        self.setOpacity(nodeStyle.Opacity)
        self.setAcceptHoverEvents(True)
        self.setZValue(0)

        self._embedQWidget()

        self.nodeScene().nodeGeometry.recomputeSize(self._nodeId)

        pos = self._graphModel.nodeData(self._nodeId, NodeRole.Position)
        self.setPos(pos)
        self._graphModel.nodeFlagsUpdated.connect(
            lambda nodeId: self._setLockedState() if self._nodeId == nodeId else None
        )

    @property
    def graphModel(self):
        return self._graphModel

    def nodeScene(self):
        return self.scene()

    def nodeId(self):
        return self._nodeId

    @property
    def nodeState(self):
        return self._nodeState

    @override
    def boundingRect(self):
        geometry = self.nodeScene().nodeGeometry
        return geometry.boundingRect(self._nodeId)

    def setGeometryChanged(self):
        self.prepareGeometryChange()

    def moveConnections(self):
        connected = self._graphModel.allConnectionIds(self._nodeId)

        for cnId in connected:
            cgo = self.nodeScene().connectionGraphicsObject(cnId)
            if cgo:
                cgo.move()

    def reactToConnection(self, cgo):
        self._nodeState.connectionForReaction = cgo
        self.update()

    @override
    def paint(self, painter, option, widget=...):
        painter.setClipRect(option.exposedRect)
        self.nodeScene().nodePainter.paint(painter, self)

    @override
    def itemChange(self, change, value):
        if (
            change
            == QtWidgets.QGraphicsItem.GraphicsItemChange.ItemScenePositionHasChanged
            and self.scene()
        ):
            self.moveConnections()

        return super().itemChange(change, value)

    @override
    def mousePressEvent(self, event):
        from SpatialNode.definitions import (
            PortType,
            InvalidPortIndex,
            PortRole,
            ConnectionPolicy,
            NodeFlag,
        )
        from SpatialNode.connection_id_utils import makeIncompleteConnectionId
        from SpatialNode.node_connection_interaction import NodeConnectionInteraction

        geometry = self.nodeScene().nodeGeometry

        for portToCheck in [PortType.In, PortType.Out]:
            nodeCoord = self.sceneTransform().inverted()[0].map(event.scenePos())

            portIndex = geometry.checkPortHit(self._nodeId, portToCheck, nodeCoord)

            if portIndex == InvalidPortIndex:
                continue

            connected = self._graphModel.connections(
                self._nodeId, portToCheck, portIndex
            )

            # Start dragging existing connection.
            if len(connected) > 0 and portToCheck == PortType.In:
                cnId = list(connected)[0]
                interaction = NodeConnectionInteraction(
                    self,
                    self.nodeScene().connectionGraphicsObject(cnId),
                    self.nodeScene(),
                )

                if self._graphModel.detachPossible(cnId):
                    interaction.disconnect(portToCheck)
            else:
                if portToCheck == PortType.Out:
                    outPolicy = self._graphModel.portData(
                        self._nodeId,
                        portToCheck,
                        portIndex,
                        PortRole.ConnectionPolicyRole,
                    )

                    if len(connected) > 0 and outPolicy == ConnectionPolicy.One:
                        for cnId in connected:
                            self._graphModel.deleteConnection(cnId)

                incompleteConnectionId = makeIncompleteConnectionId(
                    self._nodeId, portToCheck, portIndex
                )
                self.nodeScene().makeDraftConnection(incompleteConnectionId)

        if self._graphModel.nodeFlags(self._nodeId) & NodeFlag.Resizable:
            pos = event.pos()
            hit = geometry.resizeHandleRect(self._nodeId).contains(
                QtCore.QPoint(pos.x(), pos.y())
            )
            self._nodeState.resizing = hit

        super().mousePressEvent(event)

        if self.isSelected():
            self.nodeScene().nodeSelected.emit(self._nodeId)

    @override
    def mouseMoveEvent(self, event):
        from SpatialNode.definitions import NodeRole
        from SpatialNode.undo_commands import MoveNodeCommand

        if not self.isSelected():
            if not event.modifiers().testFlag(
                QtCore.Qt.KeyboardModifier.ControlModifier
            ):
                self.scene().clearSelection()
            self.setSelected(True)

        if self._nodeState.resizing:
            diff = event.pos() - event.lastPos()
            w = self._graphModel.nodeData(self._nodeId, NodeRole.Widget)

            if w is not None:
                self.prepareGeometryChange()
                oldSize = w.size()
                oldSize += QtCore.QSize(diff.x(), diff.y())
                w.resize(oldSize)

                geometry = self.nodeScene().nodeGeometry
                geometry.recomputeSize(self._nodeId)

                self.update()
                self.moveConnections()
                event.accept()
        else:
            diff = event.pos() - event.lastPos()
            self.nodeScene().undoStack.push(MoveNodeCommand(self.nodeScene(), diff))
            event.accept()

        r = self.nodeScene().sceneRect()
        r = r.united(self.mapToScene(self.boundingRect()).boundingRect())
        self.nodeScene().setSceneRect(r)

    @override
    def mouseReleaseEvent(self, event):
        self._nodeState.resizing = False
        super().mouseReleaseEvent(event)
        # position connections precisely after fast node move
        self.moveConnections()
        self.nodeScene().nodeClicked.emit(self._nodeId)

    @override
    def hoverEnterEvent(self, event):
        # bring all the colliding nodes to background
        overlapItems = self.collidingItems()

        for item in overlapItems:
            if item.zValue() > 0.0:
                item.setZValue(0.0)
        # bring this node forward
        self.setZValue(1.0)
        self._nodeState.hovered = True
        self.update()
        self.nodeScene().nodeHovered.emit(self._nodeId, event.screenPos())

        event.accept()

    @override
    def hoverLeaveEvent(self, event):
        self._nodeState.hovered = False
        self.setZValue(0.0)
        self.update()
        self.nodeScene().nodeHoverLeft.emit(self._nodeId)
        event.accept()

    @override
    def hoverMoveEvent(self, event):
        from SpatialNode.definitions import NodeFlag

        pos = event.pos()

        geometry = self.nodeScene().nodeGeometry

        if (
            self._graphModel.nodeFlags(self._nodeId) | NodeFlag.Resizable
        ) and geometry.resizeHandleRect(self._nodeId).contains(
            QtCore.QPoint(pos.x(), pos.y())
        ):
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.SizeFDiagCursor))
        else:
            self.setCursor(QtGui.QCursor())

        event.accept()

    @override
    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        self.nodeScene().nodeDoubleClicked.emit(self._nodeId)

    @override
    def contextMenuEvent(self, event):
        self.nodeScene().nodeContextMenu.emit(
            self._nodeId, self.mapToScene(event.pos())
        )

    def _embedQWidget(self):
        from SpatialNode.definitions import NodeRole

        geometry = self.nodeScene().nodeGeometry
        geometry.recomputeSize(self._nodeId)

        w = self._graphModel.nodeData(self._nodeId, NodeRole.Widget)
        if w is not None:
            self._proxyWidget = QtWidgets.QGraphicsProxyWidget(self)
            self._proxyWidget.setWidget(w)
            self._proxyWidget.setPreferredWidth(5)
            geometry.recomputeSize(self._nodeId)

            if (
                w.sizePolicy().verticalPolicy().value
                & QtWidgets.QSizePolicy.PolicyFlag.ExpandFlag.value
            ):
                widgetHeight = (
                    geometry.size(self._nodeId).height()
                    - geometry.captionRect(self._nodeId).height()
                )
                self._proxyWidget.setMinimumHeight(widgetHeight)

            self._proxyWidget.setPos(geometry.widgetPosition(self._nodeId))
            self._proxyWidget.setOpacity(1.0)
            self._proxyWidget.setFlag(
                QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresParentOpacity
            )

    def _setLockedState(self):
        from SpatialNode.definitions import NodeFlag

        flags = self._graphModel.nodeFlags(self._nodeId)
        locked = NodeFlag.Locked in flags

        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable, not locked)
        self.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, not locked
        )
        self.setFlag(
            QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemSendsScenePositionChanges,
            not locked,
        )
