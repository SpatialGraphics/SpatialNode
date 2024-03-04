#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from abc import abstractmethod

from PySide6 import QtCore


class AbstractGraphModel(QtCore.QObject):
    def __init__(self):
        from SpatialNode.definitions import ConnectionId

        super().__init__()
        self._shiftedByDynamicPortsConnections: list[ConnectionId] = []

    @abstractmethod
    def newNodeId(self): ...

    @abstractmethod
    def allNodeIds(self): ...

    @abstractmethod
    def allConnectionIds(self, nodeId): ...

    @abstractmethod
    def connections(self, nodeId, portType, index): ...

    @abstractmethod
    def connectionExists(self, connectionId): ...

    @abstractmethod
    def addNode(self, nodeType=""): ...

    @abstractmethod
    def connectionPossible(self, connectionId): ...

    def detachPossible(self, connectionId) -> bool:
        return True

    @abstractmethod
    def addConnection(self, connectionId): ...

    @abstractmethod
    def nodeExists(self, nodeId): ...

    @abstractmethod
    def nodeData(self, nodeId, role): ...

    def nodeFlags(self, node_id):
        from SpatialNode.definitions import NodeFlag

        return NodeFlag.NoFlags

    @abstractmethod
    def setNodeData(self, node_id, role, value) -> bool: ...

    @abstractmethod
    def portData(self, node_id, port_type, index, role): ...

    @abstractmethod
    def setPortData(self, node_id, port_type, index, value, role) -> bool: ...

    @abstractmethod
    def deleteConnection(self, connection_id) -> bool: ...

    @abstractmethod
    def deleteNode(self, node_id) -> bool: ...

    def saveNode(self, node_id):
        return {}

    def loadNode(self, p: QtCore.QJsonArray):
        pass

    def portsAboutToBeDeleted(self, node_id, port_type, first, last):
        from SpatialNode.definitions import NodeRole, PortType
        from SpatialNode.connection_id_utils import (
            makeIncompleteConnectionIdFromComplete,
            makeCompleteConnectionId,
        )

        self._shiftedByDynamicPortsConnections.clear()

        portCountRole = (
            NodeRole.InPortCount if port_type == PortType.In else NodeRole.OutPortCount
        )
        portCount = self.nodeData(node_id, portCountRole)

        if first > portCount - 1:
            return

        if last < first:
            return

        clampedLast = min(last, portCount - 1)

        for portIndex in range(first, clampedLast + 1):
            conns = self.connections(node_id, port_type, portIndex)
            for connectionId in conns:
                self.deleteConnection(connectionId)

        nRemovedPorts = clampedLast - first + 1

        for portIndex in range(clampedLast + 1, portCount):
            conns = self.connections(node_id, port_type, portIndex)
            for connectionId in conns:
                # Erases the information about the port on one side;
                c = makeIncompleteConnectionIdFromComplete(connectionId, port_type)
                c = makeCompleteConnectionId(c, node_id, portIndex - nRemovedPorts)
                self._shiftedByDynamicPortsConnections.append(c)
                self.deleteConnection(connectionId)

    def portsDeleted(self):
        for connectionId in self._shiftedByDynamicPortsConnections:
            self.addConnection(connectionId)
        self._shiftedByDynamicPortsConnections.clear()

    def portsAboutToBeInserted(self, node_id, port_type, first, last):
        from SpatialNode.definitions import NodeRole, PortType
        from SpatialNode.connection_id_utils import (
            makeIncompleteConnectionIdFromComplete,
            makeCompleteConnectionId,
        )

        self._shiftedByDynamicPortsConnections.clear()

        portCountRole = (
            NodeRole.InPortCount if port_type == PortType.In else NodeRole.OutPortCount
        )
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
