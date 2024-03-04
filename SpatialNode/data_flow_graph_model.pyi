#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtCore

from SpatialNode.abstract_graph_model import AbstractGraphModel
from SpatialNode.definitions import (
    NodeId,
    ConnectionId,
    PortIndex,
    PortType,
    NodeRole,
    PortRole,
)
from SpatialNode.node_delegate_model import NodeDelegateModel
from SpatialNode.node_delegate_model_registry import NodeDelegateModelRegistry
from SpatialNode.serializable import Serializable

class NodeGeometryData:
    size: QtCore.QSize
    pos: QtCore.QPointF

    def __init__(self, size: QtCore.QSize, pos: QtCore): ...

class DataFlowGraphModel(AbstractGraphModel, Serializable):
    def __init__(self, registry: NodeDelegateModelRegistry):
        self._registry: NodeDelegateModelRegistry = None
        self._nextNodeId: int = None
        self._models: dict[NodeId, NodeDelegateModel] = None
        self._connectivity: set[ConnectionId] = None
        self._nodeGeometryData: dict[NodeId, NodeGeometryData] = None

    @property
    def dataModelRegistry(self) -> NodeDelegateModelRegistry: ...
    @override
    def allNodeIds(self) -> set[NodeId]: ...
    @override
    def allConnectionIds(self, nodeId: NodeId) -> set[ConnectionId]: ...
    @override
    def connections(
        self, nodeId: NodeId, portType: PortType | None, portIndex: PortIndex
    ) -> set[ConnectionId]: ...
    @override
    def connectionExists(self, connectionId: ConnectionId) -> bool: ...
    @override
    def addNode(self, nodeType="") -> NodeId: ...
    @override
    def connectionPossible(self, connectionId: ConnectionId): ...
    @override
    def addConnection(self, connectionId: ConnectionId): ...
    @override
    def nodeExists(self, nodeId: NodeId): ...
    @override
    def nodeData(self, nodeId: NodeId, role: NodeRole): ...
    @override
    def nodeFlags(self, nodeId: NodeId): ...
    @override
    def setNodeData(self, nodeId: NodeId, role: NodeRole, value): ...
    @override
    def portData(
        self,
        nodeId: NodeId,
        portType: PortType | None,
        portIndex: PortIndex,
        role: PortRole,
    ): ...
    @override
    def setPortData(
        self,
        nodeId: NodeId,
        portType: PortType | None,
        index: PortIndex,
        value,
        role: PortRole = PortRole.Data,
    ): ...
    @override
    def deleteConnection(self, connectionId: ConnectionId): ...
    @override
    def deleteNode(self, nodeId: NodeId): ...
    @override
    def saveNode(self, nodeId: NodeId): ...
    @override
    def save(self): ...
    @override
    def loadNode(self, p: QtCore.QJsonArray): ...
    @override
    def load(self, p: QtCore.QJsonArray): ...
    def delegateModel(self, nodeId: NodeId): ...

    inPortDataWasSet: QtCore.Signal(NodeId, PortType, PortIndex)

    @override
    def newNodeId(self) -> NodeId: ...
    def sendConnectionCreation(self, connectionId: ConnectionId) -> None: ...
    def sendConnectionDeletion(self, connectionId: ConnectionId) -> None: ...
    def onOutPortDataUpdated(self, nodeId: NodeId, portIndex: PortIndex) -> None: ...
    def propagateEmptyDataTo(self, nodeId: NodeId, portIndex: PortIndex) -> None: ...
