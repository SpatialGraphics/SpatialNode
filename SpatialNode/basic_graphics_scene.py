#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtWidgets, QtCore, QtGui


class BasicGraphicsScene(QtWidgets.QGraphicsScene):
    def __init__(self, graph_model, parent=None):
        from SpatialNode.default_node_painter import DefaultNodePainter
        from SpatialNode.default_horizontal_node_geometry import (
            DefaultHorizontalNodeGeometry,
        )

        super().__init__(parent)
        self._graphModel = graph_model
        self._nodeGeometry = DefaultHorizontalNodeGeometry(self._graphModel)
        self._nodePainter = DefaultNodePainter()
        self._nodeDrag = False
        self._undoStack = QtGui.QUndoStack(self)
        self._orientation = QtCore.Qt.Orientation.Horizontal
        self._draftConnection = None
        self._nodeGraphicsObjects = {}
        self._connectionGraphicsObjects = {}

        self.setItemIndexMethod(QtWidgets.QGraphicsScene.ItemIndexMethod.NoIndex)

        self._graphModel.connectionCreated.connect(self.onConnectionCreated)
        self._graphModel.connectionDeleted.connect(self.onConnectionDeleted)
        self._graphModel.nodeCreated.connect(self.onNodeCreated)
        self._graphModel.nodeDeleted.connect(self.onNodeDeleted)
        self._graphModel.nodePositionUpdated.connect(self.onNodePositionUpdated)
        self._graphModel.nodeUpdated.connect(self.onNodeUpdated)
        self.nodeClicked.connect(self.onNodeClicked)
        self._graphModel.modelReset.connect(self.onModelReset)
        self._traverseGraphAndPopulateGraphicsObjects()

    @property
    def graphModel(self):
        return self._graphModel

    @property
    def nodeGeometry(self):
        return self._nodeGeometry

    @property
    def nodePainter(self):
        return self._nodePainter

    @nodePainter.setter
    def nodePainter(self, value):
        self._nodePainter = value

    @property
    def undoStack(self):
        return self._undoStack

    def makeDraftConnection(self, incompleteConnectionId):
        from SpatialNode.connection_graphics_object import ConnectionGraphicsObject

        self._draftConnection = ConnectionGraphicsObject(self, incompleteConnectionId)
        self._draftConnection.grabMouse()
        return self._draftConnection

    def resetDraftConnection(self):
        self.removeItem(self._draftConnection)
        self._draftConnection = None

    def clearScene(self):
        allNodeIds = self.graphModel.allNodeIds()

        for nodeId in allNodeIds:
            self.graphModel.deleteNode(nodeId)

    def nodeGraphicsObject(self, nodeId):
        return self._nodeGraphicsObjects.get(nodeId)

    def connectionGraphicsObject(self, connectionId):
        return self._connectionGraphicsObjects.get(connectionId)

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        from SpatialNode.default_horizontal_node_geometry import (
            DefaultHorizontalNodeGeometry,
        )
        from SpatialNode.default_vertical_node_geometry import (
            DefaultVerticalNodeGeometry,
        )

        if self._orientation != orientation:
            self._orientation = orientation

            match orientation:
                case QtCore.Qt.Orientation.Horizontal:
                    self._nodeGeometry = DefaultHorizontalNodeGeometry(self._graphModel)
                case QtCore.Qt.Orientation.Vertical:
                    self._nodeGeometry = DefaultVerticalNodeGeometry(self._graphModel)
            self.onModelReset()

    def createSceneMenu(self, scenePos):
        return None

    def _traverseGraphAndPopulateGraphicsObjects(self):
        from SpatialNode.connection_graphics_object import ConnectionGraphicsObject
        from SpatialNode.node_graphics_object import NodeGraphicsObject
        from SpatialNode.definitions import NodeRole, PortType

        allNodeIds = self._graphModel.allNodeIds()

        for nodeId in allNodeIds:
            self._nodeGraphicsObjects[nodeId] = NodeGraphicsObject(self, nodeId)

        for nodeId in allNodeIds:
            nOutPorts = self._graphModel.nodeData(nodeId, NodeRole.OutPortCount)

            for index in range(nOutPorts):
                outConnectionIds = self._graphModel.connections(
                    nodeId, PortType.Out, index
                )

                for cid in outConnectionIds:
                    self._connectionGraphicsObjects[cid] = ConnectionGraphicsObject(
                        self, cid
                    )

    def _updateAttachedNodes(self, connectionId, portType):
        from SpatialNode.connection_id_utils import getNodeId

        node = self.nodeGraphicsObject(getNodeId(portType, connectionId))
        if node is not None:
            node.update()

    from SpatialNode.definitions import NodeId, ConnectionId

    nodeMoved = QtCore.Signal(NodeId, QtCore.QPointF)

    nodeClicked = QtCore.Signal(NodeId)

    nodeSelected = QtCore.Signal(NodeId)

    nodeDoubleClicked = QtCore.Signal(NodeId)

    nodeHovered = QtCore.Signal(NodeId, QtCore.QPoint)

    nodeHoverLeft = QtCore.Signal(NodeId)

    connectionHovered = QtCore.Signal(ConnectionId, QtCore.QPoint)

    connectionHoverLeft = QtCore.Signal(ConnectionId)

    # Signal allows showing custom context menu upon clicking a node.
    nodeContextMenu = QtCore.Signal(NodeId, QtCore.QPointF)

    def onConnectionDeleted(self, connectionId):
        from SpatialNode.definitions import PortType

        obj = self._connectionGraphicsObjects.pop(connectionId)
        self.removeItem(obj)

        if (
            self._draftConnection is not None
            and self._draftConnection.connectionId() == connectionId
        ):
            self.removeItem(self._draftConnection)
            self._draftConnection = None

        self._updateAttachedNodes(connectionId, PortType.Out)
        self._updateAttachedNodes(connectionId, PortType.In)

    def onConnectionCreated(self, connectionId):
        from SpatialNode.definitions import PortType
        from SpatialNode.connection_graphics_object import ConnectionGraphicsObject

        self._connectionGraphicsObjects[connectionId] = ConnectionGraphicsObject(
            self, connectionId
        )

        self._updateAttachedNodes(connectionId, PortType.Out)
        self._updateAttachedNodes(connectionId, PortType.In)

    def onNodeDeleted(self, nodeId):
        obj = self._nodeGraphicsObjects.pop(nodeId)
        self.removeItem(obj)

    def onNodeCreated(self, nodeId):
        from SpatialNode.node_graphics_object import NodeGraphicsObject

        self._nodeGraphicsObjects[nodeId] = NodeGraphicsObject(self, nodeId)

    def onNodePositionUpdated(self, nodeId):
        from SpatialNode.definitions import NodeRole

        node = self.nodeGraphicsObject(nodeId)
        if node is not None:
            node.setPos(self._graphModel.nodeData(nodeId, NodeRole.Position))
            node.update()
            self._nodeDrag = True

    def onNodeUpdated(self, nodeId):
        node = self.nodeGraphicsObject(nodeId)

        if node is not None:
            node.setGeometryChanged()
            self._nodeGeometry.recomputeSize(nodeId)

            node.update()
            node.moveConnections()

    def onNodeClicked(self, nodeId):
        from SpatialNode.definitions import NodeRole

        if self._nodeDrag:
            self.nodeMoved.emit(
                nodeId, self._graphModel.nodeData(nodeId, NodeRole.Position)
            )
            self._nodeDrag = False

    def onModelReset(self):
        for obj in self._connectionGraphicsObjects.values():
            self.removeItem(obj)
        self._connectionGraphicsObjects.clear()
        for obj in self._nodeGraphicsObjects.values():
            self.removeItem(obj)
        self._nodeGraphicsObjects.clear()

        self.clear()
        self._traverseGraphAndPopulateGraphicsObjects()
