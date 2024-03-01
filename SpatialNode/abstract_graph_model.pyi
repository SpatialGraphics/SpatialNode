from abc import abstractmethod, ABC

from PySide6 import QtCore, QtGui, QtWidgets

from SpatialNode.definitions import NodeId, ConnectionId, PortIndex, PortType, NodeRole, NodeFlag, PortRole


class AbstractGraphModel(QtCore.QObject, ABC):
    def __init__(self):
        ...

    @abstractmethod
    def newNodeId(self) -> NodeId:
        """Generates a new unique NodeId."""
        ...

    def allNodeIds(self) -> set[NodeId]:
        """
        Returns the full set of unique Node Ids.

        Model creator is responsible for generating unique `unsigned int`
        Ids for all the nodes in the graph. From an Id it should be
        possible to trace back to the model's internal representation of
        the node.
        """
        ...

    def allConnectionIds(self, node_id: NodeId) -> set[ConnectionId]:
        """A collection of all input and output connections for the given `nodeId`."""
        ...


    @abstractmethod
    def connections(self, node_id: NodeId, port_type: PortType | None, index: PortIndex) -> set[ConnectionId]:
        """
        returns all connected Node Ids for given port.

        The returned set of nodes and port indices correspond to the type
        opposite to the given `portType`.
        """
        ...

    @abstractmethod
    def connectionExists(self, connection_id: ConnectionId) -> bool:
        """Checks if two nodes with the given `connectionId` are connected."""
        ...

    @abstractmethod
    def addNode(self, node_type="") -> NodeId:
        """Creates a new node instance in the derived class."""
        ...

    @abstractmethod
    def connectionPossible(self, connection_id: ConnectionId) -> bool:
        """
        Model decides if a connection with a given connection Id possible.
        """
        ...

    def detachPossible(self, connection_id: ConnectionId) -> bool:
        """ Defines if detaching the connection is possible. """
        ...

    @abstractmethod
    def addConnection(self, connection_id: ConnectionId):
        """ Creates a new connection between two nodes. """
        ...

    @abstractmethod
    def nodeExists(self, node_id: NodeId) -> bool:
        ...

    @abstractmethod
    def nodeData(self, node_id: NodeId, role: NodeRole):
        """" Returns node-related data for requested NodeRole. """
        ...

    def nodeFlags(self, node_id: NodeId) -> NodeFlag:
        ...

    @abstractmethod
    def setNodeData(self, node_id: NodeId, role: NodeRole, value) -> bool:
        """ Sets node properties. """
        ...

    @abstractmethod
    def portData(self, node_id: NodeId, port_type: PortType | None, index: PortIndex, role: PortRole):
        """ Returns port-related data for requested NodeRole. """
        ...

    @abstractmethod
    def setPortData(self, node_id: NodeId, port_type: PortType | None, index: PortIndex, value,
                    role: PortRole = PortRole.Data) -> bool:
        ...

    @abstractmethod
    def deleteConnection(self, connection_id: ConnectionId) -> bool:
        ...

    @abstractmethod
    def deleteNode(self, node_id: NodeId) -> bool:
        ...

    def saveNode(self, node_id: NodeId):
        ...

    def loadNode(self, p: QtCore.QJsonArray):
        ...

    def portsAboutToBeDeleted(self, node_id: NodeId, port_type: PortType | None, first: PortIndex, last: PortIndex):
        ...

    def portsDeleted(self):
        ...

    def portsAboutToBeInserted(self, node_id: NodeId, port_type: PortType | None, first: PortIndex, last: PortIndex):
        ...

    def portsInserted(self):
        ...
