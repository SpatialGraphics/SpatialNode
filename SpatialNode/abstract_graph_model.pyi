#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from abc import abstractmethod, ABC
from typing import Any

from PySide6 import QtCore, QtGui, QtWidgets

from SpatialNode.definitions import (
    NodeId,
    ConnectionId,
    PortIndex,
    PortType,
    NodeRole,
    NodeFlag,
    PortRole,
    QJsonObject,
)

class AbstractGraphModel(QtCore.QObject, ABC):
    """
    The central class in the Model-View approach. It delivers all kinds
    of information from the backing user data structures that represent
    the graph. The class allows to modify the graph structure: create
    and remove nodes and connections.

    We use two types of the unique ids for graph manipulations:
     - NodeId
     - ConnectionId
    """

    def __init__(self):
        self._shiftedByDynamicPortsConnections: list[ConnectionId] = []
        ...

    @abstractmethod
    def newNodeId(self) -> NodeId:
        """
        Generates a new unique NodeId.
        """
        ...

    def allNodeIds(self) -> set[NodeId]:
        """
        Returns the full set of unique Node Ids.
        """
        ...

    def allConnectionIds(self, nodeId: NodeId) -> set[ConnectionId]:
        """
        A collection of all input and output connections for the given `nodeId`.
        """
        ...

    @abstractmethod
    def connections(
        self, nodeId: NodeId, portType: PortType | None, index: PortIndex
    ) -> set[ConnectionId]:
        """
        returns all connected Node Ids for given port.
        """
        ...

    @abstractmethod
    def connectionExists(self, connectionId: ConnectionId) -> bool:
        """
        Checks if two nodes with the given `connectionId` are connected.
        """
        ...

    @abstractmethod
    def addNode(self, nodeType="") -> NodeId:
        """
        Creates a new node instance in the derived class.
        """
        ...

    @abstractmethod
    def connectionPossible(self, connectionId: ConnectionId) -> bool:
        """
        Model decides if a connection with a given connection Id possible.
        """
        ...

    def detachPossible(self, connectionId: ConnectionId) -> bool:
        """
        Defines if detaching the connection is possible.
        """
        ...

    @abstractmethod
    def addConnection(self, connectionId: ConnectionId) -> None:
        """
        Creates a new connection between two nodes.
        """
        ...

    @abstractmethod
    def nodeExists(self, nodeId: NodeId) -> bool:
        """
        returns `true` if there is data in the model associated with the given `nodeId`.
        """
        ...

    @abstractmethod
    def nodeData(self, nodeId: NodeId, role: NodeRole) -> Any:
        """ "
        Returns node-related data for requested NodeRole.
        """
        ...

    def nodeFlags(self, nodeId: NodeId) -> NodeFlag: ...
    @abstractmethod
    def setNodeData(self, nodeId: NodeId, role: NodeRole, value: Any) -> bool:
        """
        Sets node properties.
        """
        ...

    @abstractmethod
    def portData(
        self,
        nodeId: NodeId,
        portType: PortType | None,
        index: PortIndex,
        role: PortRole,
    ) -> Any:
        """
        Returns port-related data for requested NodeRole.
        """
        ...

    @abstractmethod
    def setPortData(
        self,
        nodeId: NodeId,
        portType: PortType | None,
        index: PortIndex,
        value,
        role: PortRole = PortRole.Data,
    ) -> bool: ...
    @abstractmethod
    def deleteConnection(self, connectionId: ConnectionId) -> bool: ...
    @abstractmethod
    def deleteNode(self, nodeId: NodeId) -> bool: ...
    def saveNode(self, nodeId: NodeId) -> QJsonObject:
        """
        Reimplement the function if you want to store/restore the node's
        inner state during undo/redo node deletion operations.
        """
        ...

    def loadNode(self, p: QJsonObject) -> None:
        """
        Reimplement the function if you want to support:

           - graph save/restore operations,
           - undo/redo operations after deleting the node.

        QJsonObject must contain following fields:

        ```
        {
        id : 5,
        position : { x : 100, y : 200 },
        internal-data {
        "your model specific data here"
         }
        }
        ```

        The function must do almost exactly the same thing as the normal addNode().
        The main difference is in a model-specific `inner-data` processing.
        """
        ...

    def portsAboutToBeDeleted(
        self,
        nodeId: NodeId,
        portType: PortType | None,
        first: PortIndex,
        last: PortIndex,
    ) -> None:
        """
        Function clears connections attached to the ports that are scheduled to be
        deleted. It must be called right before the model removes its old port data.

        :param nodeId: Defines the node to be modified
        :param portType: Is either PortType.In or PortType.Out
        :param first: Index of the first port to be removed
        :param last: Index of the last port to be removed
        """
        ...

    def portsDeleted(self):
        """
        Signal emitted when model no longer has the old data associated with the
        given port indices and when the node must be repainted.
        """
        ...

    def portsAboutToBeInserted(
        self,
        nodeId: NodeId,
        portType: PortType | None,
        first: PortIndex,
        last: PortIndex,
    ) -> None:
        """
        Signal emitted when model is about to create new ports on the given node.
        :param nodeId:
        :param portType:
        :param first: Is the first index of the new port after insertion.
        :param last: Is the last index of the new port after insertion.
        :return:
        """
        ...

    def portsInserted(self) -> None:
        """
        Function re-creates the connections that were shifted during the port
        insertion. After that the node is updated.
        """
        ...
    connectionCreated: QtCore.Signal(ConnectionId)

    connectionDeleted: QtCore.Signal(ConnectionId)

    nodeCreated: QtCore.Signal(NodeId)

    nodeDeleted: QtCore.Signal(NodeId)

    nodeUpdated: QtCore.Signal(NodeId)

    nodeFlagsUpdated: QtCore.Signal(NodeId)

    nodePositionUpdated: QtCore.Signal(NodeId)

    modelReset: QtCore.Signal()
