from abc import abstractmethod, ABC

from PySide6 import QtCore, QtGui, QtWidgets


class AbstractGraphModel(QtCore.QObject, ABC):
    def __init__(self):
        from SpatialNode.definitions import ConnectionId

        super().__init__()
        self._shiftedByDynamicPortsConnections: list[ConnectionId] = []

    @abstractmethod
    def newNodeId(self):
        ...

    @abstractmethod
    def allNodeIds(self):
        ...

    @abstractmethod
    def allConnectionIds(self, node_id):
        ...

    @abstractmethod
    def connections(self, node_id, port_type, index):
        ...

    @abstractmethod
    def connectionExists(self, connection_id):
        ...

    @abstractmethod
    def addNode(self, node_type=""):
        ...

    @abstractmethod
    def connectionPossible(self, connection_id):
        ...

    def detachPossible(self, connection_id) -> bool:
        return True

    @abstractmethod
    def addConnection(self, connection_id):
        ...

    @abstractmethod
    def nodeExists(self, node_id):
        ...

    @abstractmethod
    def nodeData(self, node_id, role):
        ...

    def nodeFlags(self, node_id):
        from SpatialNode.definitions import NodeFlag
        return NodeFlag.NoFlags

    @abstractmethod
    def setNodeData(self, node_id, role, value) -> bool:
        ...

    @abstractmethod
    def portData(self, node_id, port_type, index, role):
        ...

    @abstractmethod
    def setPortData(self, node_id, port_type, index, value, role) -> bool:
        ...

    @abstractmethod
    def deleteConnection(self, connection_id) -> bool:
        ...

    @abstractmethod
    def deleteNode(self, node_id) -> bool:
        ...

    def saveNode(self, node_id):
        ...

    def loadNode(self, p: QtCore.QJsonArray):
        ...

    def portsAboutToBeDeleted(self, node_id, port_type, first, last):
        from SpatialNode.definitions import NodeRole, PortType
        from SpatialNode.connection_id_utils import makeIncompleteConnectionId, makeCompleteConnectionId

        self._shiftedByDynamicPortsConnections.clear()

        portCountRole = NodeRole.InPortCount if port_type == PortType.In else NodeRole.OutPortCount
        portCount = self.nodeData(node_id, portCountRole)

        if first > portCount - 1:
            return

        if last < first:
            return

        clampedLast = min(last, portCount - 1)

        for portIndex in range(first, clampedLast):
            conns = self.connections(node_id, port_type, portIndex)
            for connectionId in conns:
                self.deleteConnection(connectionId)

        nRemovedPorts = clampedLast - first + 1

        for portIndex in range(clampedLast + 1, portCount):
            conns = self.connections(node_id, port_type, portIndex)
            for connectionId in conns:
                # Erases the information about the port on one side;
                c = makeIncompleteConnectionId(connectionId, port_type)
                c = makeCompleteConnectionId(c, node_id, portIndex - nRemovedPorts)
                self._shiftedByDynamicPortsConnections.append(c)
                self.deleteConnection(connectionId)

    def portsDeleted(self):
        for connectionId in self._shiftedByDynamicPortsConnections:
            self.addConnection(connectionId)
        self._shiftedByDynamicPortsConnections.clear()

    def portsAboutToBeInserted(self, node_id, port_type, first, last):
        from SpatialNode.definitions import NodeRole, PortType
        from SpatialNode.connection_id_utils import makeIncompleteConnectionIdFromComplete, makeCompleteConnectionId

        self._shiftedByDynamicPortsConnections.clear()

        portCountRole = NodeRole.InPortCount if port_type == PortType.In else NodeRole.OutPortCount
        portCount = self.nodeData(node_id, portCountRole)

        if first > portCount - 1:
            return

        if last < first:
            return

        nNewPorts = last - first + 1
        for portIndex in range(first, portCount):
            conns = self.connections(node_id, port_type, portIndex)
            for connectionId in conns:
                # Erases the information about the port on one side;
                c = makeIncompleteConnectionIdFromComplete(connectionId, port_type)

                c = makeCompleteConnectionId(c, node_id, portIndex + nNewPorts)

                self._shiftedByDynamicPortsConnections.append(c)

                self.deleteConnection(connectionId)

    def portsInserted(self):
        for connectionId in self._shiftedByDynamicPortsConnections:
            self.addConnection(connectionId)
        self._shiftedByDynamicPortsConnections.clear()

    from SpatialNode.definitions import ConnectionId, NodeId

    connectionCreated = QtCore.Signal(ConnectionId)

    connectionDeleted = QtCore.Signal(ConnectionId)

    nodeCreated = QtCore.Signal(NodeId)

    nodeDeleted = QtCore.Signal(NodeId)

    nodeUpdated = QtCore.Signal(NodeId)

    nodeFlagsUpdated = QtCore.Signal(NodeId)

    nodePositionUpdated = QtCore.Signal(NodeId)

    modelReset = QtCore.Signal()
