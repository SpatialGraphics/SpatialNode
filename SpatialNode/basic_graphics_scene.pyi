#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtWidgets, QtGui, QtCore

from SpatialNode.abstract_graph_model import AbstractGraphModel
from SpatialNode.abstract_node_geometry import AbstractNodeGeometry
from SpatialNode.abstract_node_painter import AbstractNodePainter
from SpatialNode.connection_graphics_object import ConnectionGraphicsObject
from SpatialNode.definitions import ConnectionId, NodeId, PortType
from SpatialNode.node_graphics_object import NodeGraphicsObject

class BasicGraphicsScene(QtWidgets.QGraphicsScene):
    """
    An instance of QGraphicsScene, holds connections and nodes.
    """

    def __init__(self, graphModel: AbstractGraphModel, parent=None):
        self._graphModel: AbstractGraphModel = None
        self._nodeGeometry: AbstractNodeGeometry = None
        self._nodePainter: AbstractNodePainter = None
        self._nodeDrag: bool = None
        self._undoStack: QtGui.QUndoStack = None
        self._orientation: QtCore.Qt.Orientation = None
        self._draftConnection = None
        self._nodeGraphicsObjects: dict[NodeId, NodeGraphicsObject] = None
        self._connectionGraphicsObjects: dict[
            ConnectionId, ConnectionGraphicsObject
        ] = None

    @property
    def graphModel(self) -> AbstractGraphModel: ...
    @property
    def nodeGeometry(self) -> AbstractNodeGeometry: ...
    @property
    def nodePainter(self) -> AbstractNodePainter: ...
    @nodePainter.setter
    def nodePainter(self, value: AbstractNodePainter): ...
    @property
    def undoStack(self) -> QtGui.QUndoStack: ...
    def makeDraftConnection(self, incompleteConnectionId: ConnectionId):
        """
        Creates a "draft" instance of ConnectionGraphicsObject.
        """
        ...

    def resetDraftConnection(self) -> None:
        """
        Deletes "draft" connection.
        """
        ...

    def clearScene(self) -> None:
        """
        Deletes all the nodes. Connections are removed automatically.
        """
        ...

    def nodeGraphicsObject(self, nodeId: NodeId) -> NodeGraphicsObject:
        """
        NodeGraphicsObject associated with the given nodeId.
        """
        ...

    def connectionGraphicsObject(
        self, connectionId: ConnectionId
    ) -> ConnectionGraphicsObject:
        """
        ConnectionGraphicsObject corresponding to `connectionId`.
        """
        ...

    @property
    def orientation(self) -> QtCore.Qt.Orientation: ...
    @orientation.setter
    def orientation(self, orientation: QtCore.Qt.Orientation): ...
    def createSceneMenu(self, scenePos: QtCore.QPointF) -> QtWidgets.QMenu:
        """
        return an instance of the scene context menu in subclass.
        """
        ...

    def _traverseGraphAndPopulateGraphicsObjects(self) -> NodeGraphicsObject:
        """
        Creates Node and Connection graphics objects.
        """
        ...

    def _updateAttachedNodes(
        self, connectionId: ConnectionId, portType: PortType | None
    ) -> None:
        """
        Redraws adjacent nodes for given `connectionId`
        """
        ...
    from SpatialNode.definitions import NodeId, ConnectionId

    nodeMoved: QtCore.Signal(NodeId, QtCore.QPointF)

    nodeClicked: QtCore.Signal(NodeId)

    nodeSelected: QtCore.Signal(NodeId)

    nodeDoubleClicked: QtCore.Signal(NodeId)

    nodeHovered: QtCore.Signal(NodeId, QtCore.QPoint)

    nodeHoverLeft: QtCore.Signal(NodeId)

    connectionHovered: QtCore.Signal(ConnectionId, QtCore.QPoint)

    connectionHoverLeft: QtCore.Signal(ConnectionId)

    # Signal allows showing custom context menu upon clicking a node.
    nodeContextMenu: QtCore.Signal(NodeId, QtCore.QPointF)

    def onConnectionDeleted(self, connectionId: ConnectionId) -> None:
        """Slot called when the `connectionId` is erased form the AbstractGraphModel."""
        ...

    def onConnectionCreated(self, connectionId: ConnectionId) -> None:
        """Slot called when the `connectionId` is created in the AbstractGraphModel."""
        ...

    def onNodeDeleted(self, nodeId: NodeId) -> None: ...
    def onNodeCreated(self, nodeId: NodeId) -> None: ...
    def onNodePositionUpdated(self, nodeId: NodeId) -> None: ...
    def onNodeUpdated(self, nodeId: NodeId) -> None: ...
    def onNodeClicked(self, nodeId: NodeId) -> None: ...
    def onModelReset(self) -> None: ...
