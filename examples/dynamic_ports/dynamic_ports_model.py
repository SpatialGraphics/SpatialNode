#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.
from typing import override

from PySide6 import QtCore

import SpatialNode as sNode


class DynamicPortsModel(sNode.AbstractGraphModel):
    class NodeGeometryData:
        size: QtCore.QSize
        posL: QtCore.QPointF

    class NodePortCount:
        inPort: int = 0
        outPort: int = 0

    def __init__(self):
        super().__init__()
        self._nodeIds = set()
        self._connectivity = set()
        self._nodeGeometryData = {}
        self._nodePortCounts = {}
        self._nodeWidgets = {}
        self._nextNodeId = 0

    def _widget(self, nodeId):
        from examples.dynamic_ports.port_add_remove_widget import PortAddRemoveWidget

        if nodeId not in self._nodeWidgets:
            self._nodeWidgets[nodeId] = PortAddRemoveWidget(0, 0, nodeId, self)

        return self._nodeWidgets[nodeId]

    @override
    def allNodeIds(self):
        return self._nodeIds

    @override
    def allConnectionIds(self, nodeId):
        result = set()
        for cid in self._connectivity:
            if cid.inNodeId == nodeId or cid.outNodeId == nodeId:
                result.add(cid)
        return result

    @override
    def connections(self, nodeId, portType, index):
        result = set()
        for cid in self._connectivity:
            if (
                sNode.getNodeId(portType, cid) == nodeId
                and sNode.getPortIndex(portType, cid) == index
            ):
                result.add(cid)
        return result

    @override
    def connectionExists(self, connectionId):
        return connectionId in self._connectivity

    @override
    def addNode(self, nodeType=""):
        newId = self.newNodeId()

        # Create new node.
        self._nodeIds.add(newId)
        self.nodeCreated.emit(newId)
        return newId

    @override
    def connectionPossible(self, connectionId):
        return not self.connectionExists(connectionId)

    @override
    def addConnection(self, connectionId):
        self._connectivity.add(connectionId)
        self.connectionCreated.emit(connectionId)

    @override
    def nodeExists(self, nodeId):
        return nodeId in self._nodeIds

    @override
    def nodeData(self, nodeId, role):
        self._nodeGeometryData.setdefault(
            nodeId, sNode.NodeGeometryData(QtCore.QSize(0, 0), QtCore.QPointF())
        )
        self._nodePortCounts.setdefault(nodeId, DynamicPortsModel.NodePortCount())
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
            case sNode.NodeRole.InPortCount:
                return self._nodePortCounts[nodeId].inPort
            case sNode.NodeRole.OutPortCount:
                return self._nodePortCounts[nodeId].outPort
            case sNode.NodeRole.Widget:
                return self._widget(nodeId)

    @override
    def setNodeData(self, nodeId, role, value):
        self._nodeGeometryData.setdefault(
            nodeId, sNode.NodeGeometryData(QtCore.QSize(0, 0), QtCore.QPointF())
        )
        self._nodePortCounts.setdefault(nodeId, DynamicPortsModel.NodePortCount())
        match role:
            case sNode.NodeRole.Position:
                self._nodeGeometryData[nodeId].pos = value
                self.nodePositionUpdated.emit(nodeId)
                return True

            case sNode.NodeRole.Size:
                self._nodeGeometryData[nodeId].size = value
                return True

            case sNode.NodeRole.InPortCount:
                self._nodePortCounts[nodeId].inPort = value
                self._widget(nodeId).populateButtons(sNode.PortType.In, value)

            case sNode.NodeRole.OutPortCount:
                self._nodePortCounts[nodeId].outPort = value
                self._widget(nodeId).populateButtons(sNode.PortType.Out, value)
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
        # Delete connections to this node first.
        connectionIds = self.allConnectionIds(nodeId)
        for cId in connectionIds:
            self.deleteConnection(cId)

        self._nodeIds.remove(nodeId)
        self._nodeGeometryData.pop(nodeId)
        self._nodePortCounts.pop(nodeId)
        self._nodeWidgets.pop(nodeId)

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

        nodeJson["inPortCount"] = self._nodePortCounts[nodeId].inPort
        nodeJson["outPortCount"] = self._nodePortCounts[nodeId].outPort

        return nodeJson

    def save(self):
        sceneJson = sNode.QJsonObject()

        nodesJsonArray = QtCore.QJsonArray()
        for nodeId in self.allNodeIds():
            nodesJsonArray.append(self.saveNode(nodeId))
        sceneJson["nodes"] = nodesJsonArray

        connJsonArray = QtCore.QJsonArray()
        for cid in self._connectivity:
            connJsonArray.append(sNode.toJson(cid))

        sceneJson["connections"] = connJsonArray

        return sceneJson

    @override
    def loadNode(self, nodeJson):
        restoredNodeId = nodeJson["id"]

        _nextNodeId = max(self._nextNodeId, restoredNodeId + 1)

        # Create new node.
        self._nodeIds.add(restoredNodeId)

        self.setNodeData(
            restoredNodeId, sNode.NodeRole.InPortCount, nodeJson["inPortCount"]
        )
        self.setNodeData(
            restoredNodeId, sNode.NodeRole.OutPortCount, nodeJson["outPortCount"]
        )

        posJson = nodeJson["position"]
        pos = QtCore.QPointF(posJson["x"], posJson["y"])
        self.setNodeData(restoredNodeId, sNode.NodeRole.Position, pos)

        self.nodeCreated.emit(restoredNodeId)

    def load(self, jsonDocument):
        nodesJsonArray = jsonDocument["nodes"].toArray()

        for nodeJson in nodesJsonArray:
            self.loadNode(nodeJson.toObject())

        connectionJsonArray = jsonDocument["connections"].toArray()

        for connection in connectionJsonArray:
            connJson = connection.toObject()

            connId = sNode.fromJson(connJson)

            # Restore the connection
            self.addConnection(connId)

    def addPort(self, nodeId, portType, portIndex):
        # STAGE 1.
        # Compute new addresses for the existing connections that are shifted and
        # placed after the new ones
        first = portIndex
        last = first
        self.portsAboutToBeInserted(nodeId, portType, first, last)

        # STAGE 2. Change the number of connections in your model
        if portType == sNode.PortType.In:
            self._nodePortCounts[nodeId].inPort += 1
        else:
            self._nodePortCounts[nodeId].outPort += 1

        # STAGE 3. Re-create previously existed and now shifted connections
        self.portsInserted()

        self.nodeUpdated.emit(nodeId)

    def removePort(self, nodeId, portType, first):
        # STAGE 1.
        # Compute new addresses for the existing connections that are shifted upwards
        # instead of the deleted ports.
        last = first
        self.portsAboutToBeDeleted(nodeId, portType, first, last)

        # STAGE 2. Change the number of connections in your model
        if portType == sNode.PortType.In:
            self._nodePortCounts[nodeId].inPort -= 1
        else:
            self._nodePortCounts[nodeId].outPort -= 1

        self.portsDeleted()
        self.nodeUpdated.emit(nodeId)

    @override
    def newNodeId(self):
        self._nextNodeId += 1
        return self._nextNodeId - 1
