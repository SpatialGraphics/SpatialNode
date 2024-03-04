#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtCore

import SpatialNode as sNode


class SimpleGraphModel(sNode.AbstractGraphModel):
    def __init__(self):
        super().__init__()
        self._nextNodeId = 0
        self._nodeIds: set[sNode.NodeId] = set()
        self._connectivity: set[sNode.ConnectionId] = set()
        self._nodeGeometryData: dict[sNode.NodeId, sNode.NodeGeometryData] = {}

    @override
    def allNodeIds(self):
        return self._nodeIds

    @override
    def allConnectionIds(self, nodeId):
        nodeIds: set[sNode.ConnectionId] = set()
        for p in self._connectivity:
            if p.inNodeId == nodeId or p.outNodeId == nodeId:
                nodeIds.add(p)
        return nodeIds

    @override
    def connections(self, nodeId, portType, port_index):
        result: set[sNode.ConnectionId] = set()
        for cid in self._connectivity:
            if (
                sNode.getNodeId(portType, cid) == nodeId
                and sNode.getPortIndex(portType, cid) == port_index
            ):
                result.add(cid)
        return result

    @override
    def connectionExists(self, connectionId):
        return connectionId in self._connectivity

    @override
    def addNode(self, nodeType=""):
        newId = self.newNodeId()
        self._nodeIds.add(newId)
        self.nodeCreated.emit(newId)

        return newId

    @override
    def connectionPossible(self, connectionId):
        return connectionId not in self._connectivity

    @override
    def addConnection(self, connectionId):
        self._connectivity.add(connectionId)
        self.connectionCreated.emit(connectionId)

    @override
    def nodeExists(self, nodeId):
        return nodeId in self._nodeIds

    @override
    def nodeData(self, nodeId, role):
        match role:
            case sNode.NodeRole.Type:
                return "Default Node Type"
            case sNode.NodeRole.Position:
                return self._nodeGeometryData[nodeId].pos
            case sNode.NodeRole.Size:
                return self._nodeGeometryData[nodeId].size
            case sNode.NodeRole.CaptionVisible:
                return True
            case sNode.NodeRole.Caption:
                return "Node"
            case sNode.NodeRole.Style:
                style = sNode.StyleCollection.nodeStyle()
                return style.toJson()
            case sNode.NodeRole.InternalData:
                return
            case sNode.NodeRole.InPortCount:
                return 1
            case sNode.NodeRole.OutPortCount:
                return 1
            case sNode.NodeRole.Widget:
                return

    @override
    def setNodeData(self, nodeId, role, value):
        self._nodeGeometryData.setdefault(
            nodeId, sNode.NodeGeometryData(QtCore.QSize(0, 0), QtCore.QPointF())
        )

        match role:
            case sNode.NodeRole.Position:
                self._nodeGeometryData[nodeId].pos = value
                self.nodePositionUpdated.emit(nodeId)
                result = True
            case sNode.NodeRole.Size:
                self._nodeGeometryData[nodeId].size = value
                return True

        return False

    @override
    def portData(self, nodeId, portType, index, role):
        match role:
            case sNode.PortRole.ConnectionPolicyRole:
                return sNode.ConnectionPolicy.One
            case sNode.PortRole.CaptionVisible:
                return True
            case sNode.PortRole.Caption:
                if portType == sNode.PortType.In:
                    return "Port In"
                else:
                    return "Port Out"

    @override
    def setPortData(self, nodeId, portType, index, value, role=sNode.PortRole.Data):
        return False

    @override
    def deleteConnection(self, connectionId):
        disconnected = False
        if connectionId in self._connectivity:
            disconnected = True
            self._connectivity.remove(connectionId)

        if disconnected:
            self.connectionDeleted.emit(connectionId)

        return disconnected

    @override
    def deleteNode(self, nodeId):
        #  Delete connections to this node first.
        connectionIds = self.allConnectionIds(nodeId)

        for cId in connectionIds:
            self.deleteConnection(cId)

        self._nodeIds.remove(nodeId)
        self._nodeGeometryData.pop(nodeId)

        self.nodeDeleted.emit(nodeId)

        return True

    @override
    def saveNode(self, nodeId):
        nodeJson = sNode.QJsonObject()

        nodeJson["id"] = nodeId

        pos = self.nodeData(nodeId, sNode.NodeRole.Position)
        posJson = sNode.QJsonObject()
        posJson["x"] = pos.x()
        posJson["y"] = pos.y()
        nodeJson["position"] = posJson
        return nodeJson

    @override
    def loadNode(self, nodeJson):
        restoredNodeId = nodeJson["id"]

        # Next NodeId must be larger that any id existing in the graph
        self._nextNodeId = max(self._nextNodeId, restoredNodeId + 1)

        # Create new node.
        self._nodeIds.add(restoredNodeId)

        self.nodeCreated.emit(restoredNodeId)

        posJson = nodeJson["position"]
        pos = QtCore.QPointF(posJson["x"], posJson["y"])
        self.setNodeData(restoredNodeId, sNode.NodeRole.Position, pos)

    @override
    def newNodeId(self):
        self._nextNodeId += 1
        return self._nextNodeId - 1
