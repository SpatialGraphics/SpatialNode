#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtCore

from SpatialNode.abstract_graph_model import AbstractGraphModel
from SpatialNode.connection_id_utils import fromJson
from SpatialNode.definitions import (
    PortRole,
    NodeId,
    PortType,
    PortIndex,
    QJsonObject,
    NodeRole,
)
from SpatialNode.serializable import Serializable


class NodeGeometryData:
    size: QtCore.QSize
    pos: QtCore.QPointF

    def __init__(self, size: QtCore.QSize, pos: QtCore):
        self.size = size
        self.pos = pos


class DataFlowGraphModel(AbstractGraphModel, Serializable):
    def __init__(self, registry):
        super().__init__()
        self._registry = registry
        self._nextNodeId = 0
        self._models = {}
        self._connectivity = set()
        self._nodeGeometryData = {}

    @property
    def dataModelRegistry(self):
        return self._registry

    @override
    def allNodeIds(self):
        from SpatialNode.definitions import NodeId

        nodeIds: set[NodeId] = set()
        for p in self._models:
            nodeIds.add(p)
        return nodeIds

    @override
    def allConnectionIds(self, nodeId):
        from SpatialNode.definitions import ConnectionId

        nodeIds: set[ConnectionId] = set()
        for p in self._connectivity:
            if p.inNodeId == nodeId or p.outNodeId == nodeId:
                nodeIds.add(p)
        return nodeIds

    @override
    def connections(self, nodeId, portType, port_index):
        from SpatialNode.definitions import ConnectionId
        from SpatialNode.connection_id_utils import getNodeId, getPortIndex

        result: set[ConnectionId] = set()
        for cid in self._connectivity:
            if (
                getNodeId(portType, cid) == nodeId
                and getPortIndex(portType, cid) == port_index
            ):
                result.add(cid)
        return result

    @override
    def connectionExists(self, connectionId):
        return connectionId in self._connectivity

    @override
    def addNode(self, nodeType=""):
        from SpatialNode.definitions import InvalidNodeId

        model = self._registry.create(nodeType)

        if model is not None:
            newId = self.newNodeId()
            model.dataUpdated.connect(
                lambda portIndex: self.onOutPortDataUpdated(newId, portIndex)
            )
            model.portsAboutToBeDeleted.connect(
                lambda portType, first, last: self.portsAboutToBeDeleted(
                    newId, portType, first, last
                )
            )
            model.portsDeleted.connect(self.portsDeleted)
            model.portsAboutToBeInserted.connect(
                lambda portType, first, last: self.portsAboutToBeInserted(
                    newId, portType, first, last
                )
            )
            model.portsInserted.connect(self.portsInserted)
            self._models[newId] = model
            self.nodeCreated.emit(newId)

            return newId
        return InvalidNodeId

    @override
    def connectionPossible(self, connectionId):
        from SpatialNode.definitions import PortType, PortRole, ConnectionPolicy
        from SpatialNode.connection_id_utils import getNodeId, getPortIndex

        def getDataType(portType: PortType):
            return self.portData(
                getNodeId(portType, connectionId),
                portType,
                getPortIndex(portType, connectionId),
                PortRole.DataType,
            )

        def portVacant(portType: PortType):
            nodeId = getNodeId(portType, connectionId)
            portIndex = getPortIndex(portType, connectionId)
            connected = self.connections(nodeId, portType, portIndex)

            policy = self.portData(
                nodeId, portType, portIndex, PortRole.ConnectionPolicyRole
            )
            return len(connected) == 0 or policy == ConnectionPolicy.Many

        return (
            getDataType(PortType.Out).id == getDataType(PortType.In).id
            and portVacant(PortType.Out)
            and portVacant(PortType.In)
        )

    @override
    def addConnection(self, connectionId):
        from SpatialNode.definitions import PortType, PortRole

        self._connectivity.add(connectionId)
        self.sendConnectionCreation(connectionId)
        portDataToPropagate = self.portData(
            connectionId.outNodeId,
            PortType.Out,
            connectionId.outPortIndex,
            PortRole.Data,
        )
        self.setPortData(
            connectionId.inNodeId,
            PortType.In,
            connectionId.inPortIndex,
            portDataToPropagate,
            PortRole.Data,
        )

    @override
    def nodeExists(self, nodeId):
        return nodeId in self._models

    @override
    def nodeData(self, nodeId, role):
        from SpatialNode.definitions import NodeRole, PortType
        from SpatialNode.style_collection import StyleCollection

        result = self._models.get(nodeId)
        if result is None:
            return result

        match role:
            case NodeRole.Type:
                return result.name()

            case NodeRole.Position:
                return self._nodeGeometryData[nodeId].pos

            case NodeRole.Size:
                return self._nodeGeometryData[nodeId].size

            case NodeRole.CaptionVisible:
                return result.captionVisible()

            case NodeRole.Caption:
                return result.caption()

            case NodeRole.Style:
                style = StyleCollection.nodeStyle()
                return style.toJson()

            case NodeRole.InternalData:
                nodeJson = QJsonObject()
                nodeJson["internal-data"] = self._models[nodeId].save()
                return nodeJson

            case NodeRole.InPortCount:
                return result.nPorts(PortType.In)

            case NodeRole.OutPortCount:
                return result.nPorts(PortType.Out)

            case NodeRole.Widget:
                return result.embeddedWidget()

    @override
    def nodeFlags(self, nodeId):
        from SpatialNode.definitions import NodeFlag

        it = self._models[nodeId]
        if it is not None and it.resizable():
            return NodeFlag.Resizable
        return NodeFlag.NoFlags

    @override
    def setNodeData(self, nodeId, role, value):
        from SpatialNode.definitions import NodeRole

        self._nodeGeometryData.setdefault(
            nodeId, NodeGeometryData(QtCore.QSize(0, 0), QtCore.QPointF())
        )

        result = False
        match role:
            case NodeRole.Position:
                self._nodeGeometryData[nodeId].pos = value
                self.nodePositionUpdated.emit(nodeId)
                result = True
            case NodeRole.Size:
                self._nodeGeometryData[nodeId].size = value
                result = True
        return result

    @override
    def portData(self, nodeId, portType, port_index, role):
        from SpatialNode.definitions import PortRole, PortType

        model = self._models[nodeId]
        if model is None:
            return model

        match role:
            case PortRole.Data:
                if portType == PortType.Out:
                    return model.outData(port_index)

            case PortRole.DataType:
                return model.dataType(portType, port_index)

            case PortRole.ConnectionPolicyRole:
                return model.portConnectionPolicy(portType, port_index)

            case PortRole.CaptionVisible:
                return model.portCaptionVisible(portType, port_index)

            case PortRole.Caption:
                return model.portCaption(portType, port_index)

    @override
    def setPortData(self, nodeId, portType, index, value, role=PortRole.Data):
        from SpatialNode.definitions import PortType

        model = self._models[nodeId]
        if model is None:
            return False

        match role:
            case PortRole.Data:
                if portType == PortType.In:
                    model.setInData(value, index)
                    self.inPortDataWasSet.emit(nodeId, portType, index)

        return False

    @override
    def deleteConnection(self, connectionId):
        from SpatialNode.definitions import PortType
        from SpatialNode.connection_id_utils import getNodeId, getPortIndex

        disconnected = False
        if connectionId in self._connectivity:
            disconnected = True
            self._connectivity.remove(connectionId)

        if disconnected:
            self.sendConnectionDeletion(connectionId)
            self.propagateEmptyDataTo(
                getNodeId(PortType.In, connectionId),
                getPortIndex(PortType.In, connectionId),
            )

        return disconnected

    @override
    def deleteNode(self, nodeId):
        connectionIds = self.allConnectionIds(nodeId)
        for cId in connectionIds:
            self.deleteConnection(cId)

        self._nodeGeometryData.pop(nodeId)
        self._models.pop(nodeId)

        self.nodeDeleted.emit(nodeId)

        return True

    @override
    def saveNode(self, nodeId):
        from SpatialNode.definitions import NodeRole

        nodeJson = QJsonObject()
        nodeJson["id"] = nodeId
        nodeJson["internal-data"] = self._models[nodeId].save()

        pos = self.nodeData(nodeId, NodeRole.Position)

        posJson = QJsonObject()
        posJson["x"] = pos.x()
        posJson["y"] = pos.y()
        nodeJson["position"] = posJson

        return nodeJson

    @override
    def save(self):
        from SpatialNode.connection_id_utils import toJson

        sceneJson = QJsonObject()

        nodesJsonArray = QtCore.QJsonArray()
        for nodeId in self.allNodeIds():
            nodesJsonArray.append(self.saveNode(nodeId))
        sceneJson["nodes"] = nodesJsonArray

        connJsonArray = QtCore.QJsonArray()
        for cid in self._connectivity:
            connJsonArray.append(toJson(cid))
        sceneJson["connections"] = connJsonArray

        return sceneJson

    @override
    def loadNode(self, nodeJson):
        restoredNodeId = nodeJson["id"]
        self._nextNodeId = max(self._nextNodeId, restoredNodeId + 1)

        internalDataJson = nodeJson["internal-data"]
        delegateModelName = internalDataJson["model-name"]

        model = self._registry.create(delegateModelName)
        if model:
            model.dataUpdated.connect(
                lambda portIndex: self.onOutPortDataUpdated(restoredNodeId, portIndex)
            )
            self._models[restoredNodeId] = model
            self.nodeCreated.emit(restoredNodeId)

            posJson = nodeJson["position"]
            pos = QtCore.QPointF(posJson["x"], posJson["y"])
            self.setNodeData(restoredNodeId, NodeRole.Position, pos)
            self._models[restoredNodeId].load(internalDataJson)

        else:
            raise Exception("No registered model with name {delegateModelName}")

    @override
    def load(self, jsonDocument):
        nodesJsonArray = jsonDocument["nodes"]

        for nodeJson in nodesJsonArray:
            self.loadNode(nodeJson)

        connectionJsonArray = jsonDocument["connections"]

        for connection in connectionJsonArray:
            connId = fromJson(connection)

            # Restore the connection
            self.addConnection(connId)

    def delegateModel(self, nodeId):
        return self._models[nodeId]

    inPortDataWasSet = QtCore.Signal(NodeId, PortType, PortIndex)

    @override
    def newNodeId(self):
        result = self._nextNodeId
        self._nextNodeId += 1
        return result

    def sendConnectionCreation(self, connectionId):
        self.connectionCreated.emit(connectionId)

        modeli = self._models[connectionId.inNodeId]
        modelo = self._models[connectionId.outNodeId]
        if modeli is not None and modelo is not None:
            modeli.inputConnectionCreated(connectionId)
            modelo.outputConnectionCreated(connectionId)

    def sendConnectionDeletion(self, connectionId):
        self.connectionDeleted.emit(connectionId)

        modeli = self._models[connectionId.inNodeId]
        modelo = self._models[connectionId.outNodeId]
        if modeli is not None and modelo is not None:
            modeli.inputConnectionDeleted(connectionId)
            modelo.outputConnectionDeleted(connectionId)

    def onOutPortDataUpdated(self, nodeId, portIndex):
        connected = self.connections(nodeId, PortType.Out, portIndex)
        portDataToPropagate = self.portData(
            nodeId, PortType.Out, portIndex, PortRole.Data
        )

        for cn in connected:
            self.setPortData(
                cn.inNodeId,
                PortType.In,
                cn.inPortIndex,
                portDataToPropagate,
                PortRole.Data,
            )

    def propagateEmptyDataTo(self, nodeId, portIndex):
        self.setPortData(nodeId, PortType.In, portIndex, None, PortRole.Data)
