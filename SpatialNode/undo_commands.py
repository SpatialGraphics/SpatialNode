#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtGui, QtCore, QtWidgets

from SpatialNode.connection_id_utils import toJson, fromJson
from SpatialNode.definitions import QJsonObject, NodeId, ConnectionId, NodeRole


def serializeSelectedItems(scene):
    from SpatialNode.connection_graphics_object import ConnectionGraphicsObject
    from SpatialNode.node_graphics_object import NodeGraphicsObject

    serializedScene = QJsonObject()

    graphModel = scene.graphModel

    selectedNodes: set[NodeId] = set()

    nodesJsonArray = QtCore.QJsonArray()

    for item in scene.selectedItems():
        if isinstance(item, NodeGraphicsObject):
            nodesJsonArray.append(graphModel.saveNode(item.nodeId()))
            selectedNodes.add(item.nodeId())

    connJsonArray = QtCore.QJsonArray()

    for item in scene.selectedItems():
        if isinstance(item, ConnectionGraphicsObject):
            cid = item.connectionId
            if cid.outNodeId in selectedNodes and cid.inNodeId in selectedNodes:
                connJsonArray.append(toJson(cid))

    serializedScene["nodes"] = nodesJsonArray
    serializedScene["connections"] = connJsonArray

    return serializedScene


def insertSerializedItems(json, scene):
    graphModel = scene.graphModel
    nodesJsonArray = json["nodes"].toArray().toVariantList()

    for node in nodesJsonArray:
        graphModel.loadNode(node)

        id = node["id"]
        scene.nodeGraphicsObject(id).setZValue(1.0)
        scene.nodeGraphicsObject(id).setSelected(True)

    connJsonArray = json["connections"].toVariantList()

    for connection in connJsonArray:
        connId = fromJson(connection)

        # Restore the connection
        graphModel.addConnection(connId)

        scene.connectionGraphicsObject(connId).setSelected(True)


def deleteSerializedItems(sceneJson, graphModel):
    connectionJsonArray = sceneJson["connections"].toArray().toVariantList()

    for connection in connectionJsonArray:
        connId = fromJson(connection)
        graphModel.deleteConnection(connId)

    nodesJsonArray = sceneJson["nodes"].toArray().toVariantList()

    for node in nodesJsonArray:
        graphModel.deleteNode(node["id"])


def computeAverageNodePosition(sceneJson):
    averagePos = QtCore.QPointF(0, 0)
    nodesJsonArray = sceneJson["nodes"].toVariantList()

    for node in nodesJsonArray:
        averagePos += QtCore.QPointF(node["position"]["x"], node["position"]["y"])

    averagePos /= len(nodesJsonArray)

    return averagePos


def offsetNodeGroup(sceneJson, diff):
    nodesJsonArray = sceneJson["nodes"].toVariantList()

    newNodesJsonArray = QtCore.QJsonArray()
    for node in nodesJsonArray:
        oldPos = QtCore.QPointF(node["position"]["x"], node["position"]["y"])

        oldPos += diff

        posJson = QJsonObject()
        posJson["x"] = oldPos.x()
        posJson["y"] = oldPos.y()
        node["position"] = posJson

        newNodesJsonArray.append(node)

    sceneJson["nodes"] = QtCore.QJsonValue(newNodesJsonArray)


class CreateCommand(QtGui.QUndoCommand):
    def __init__(self, scene, name, mouseScenePos):
        from SpatialNode.definitions import InvalidNodeId, NodeRole, QJsonObject

        super().__init__()
        self._scene = scene
        self._sceneJson = QJsonObject()
        self._nodeId = self._scene.graphModel.addNode(name)
        if self._nodeId is not InvalidNodeId:
            self._scene.graphModel.setNodeData(
                self._nodeId, NodeRole.Position, mouseScenePos
            )
        else:
            self.setObsolete(True)

    @override
    def undo(self):
        nodesJsonArray = QtCore.QJsonArray()
        nodesJsonArray.append(self._scene.graphModel.saveNode(self._nodeId))
        self._sceneJson["nodes"] = QtCore.QJsonValue(nodesJsonArray)

        self._scene.graphModel.deleteNode(self._nodeId)

    @override
    def redo(self):
        if len(self._sceneJson) == 0 or len(self._sceneJson["nodes"].toArray()) == 0:
            return
        insertSerializedItems(self._sceneJson, self._scene)


class DeleteCommand(QtGui.QUndoCommand):
    def __init__(self, scene):
        from SpatialNode.node_graphics_object import NodeGraphicsObject
        from SpatialNode.connection_graphics_object import ConnectionGraphicsObject

        super().__init__()
        self._scene = scene
        self._sceneJson = QJsonObject()

        graphModel = self._scene.graphModel

        connJsonArray = QtCore.QJsonArray()
        # Delete the selected connections first, ensuring that they won't be
        # automatically deleted when selected nodes are deleted (deleting a
        # node deletes some connections as well)
        for item in self._scene.selectedItems():
            if isinstance(item, ConnectionGraphicsObject):
                # saving connections attached to the selected nodes
                cid = item.connectionId
                connJsonArray.append(toJson(cid))

        nodesJsonArray = QtCore.QJsonArray()
        # Delete the nodes; this will delete many of the connections.
        # Selected connections were already deleted prior to this loop,
        for item in self._scene.selectedItems():
            if isinstance(item, NodeGraphicsObject):
                # saving connections attached to the selected nodes
                for cid in graphModel.allConnectionIds(item.nodeId()):
                    connJsonArray.append(toJson(cid))

                nodesJsonArray.append(graphModel.saveNode(item.nodeId()))

        # If nothing is deleted, cancel this operation
        if connJsonArray.isEmpty() and nodesJsonArray.isEmpty():
            self.setObsolete(True)

        self._sceneJson["nodes"] = QtCore.QJsonValue(nodesJsonArray)
        self._sceneJson["connections"] = QtCore.QJsonValue(connJsonArray)

    @override
    def undo(self):
        insertSerializedItems(self._sceneJson, self._scene)

    @override
    def redo(self):
        deleteSerializedItems(self._sceneJson, self._scene.graphModel)


class CopyCommand(QtGui.QUndoCommand):
    def __init__(self, scene):
        super().__init__()
        self._scene = scene

        sceneJson = serializeSelectedItems(scene)

        if len(sceneJson) == 0 or sceneJson["nodes"].empty():
            self.setObsolete(True)
            return

        clipboard = QtWidgets.QApplication.clipboard()
        data = QtCore.QJsonDocument(sceneJson).toJson()
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/qt-nodes-graph", data)
        mimeData.setText(data.toStdString())

        clipboard.setMimeData(mimeData)

        # Copy command does not have any effective redo/undo operations.
        # It copies the data to the clipboard and could be immediately removed
        # from the stack.
        self.setObsolete(True)


class PasteCommand(QtGui.QUndoCommand):
    def __init__(self, scene, mouseScenePos):
        super().__init__()
        self._scene = scene
        self._mouseScenePos = mouseScenePos

        self._newSceneJson = self._takeSceneJsonFromClipboard()

        if len(self._newSceneJson) == 0 or len(self._newSceneJson["nodes"]) == 0:
            self.setObsolete(True)
            return

        self._newSceneJson = self._makeNewNodeIdsInScene(self._newSceneJson)
        averagePos = computeAverageNodePosition(self._newSceneJson)
        offsetNodeGroup(self._newSceneJson, self._mouseScenePos - averagePos)

    @override
    def undo(self):
        deleteSerializedItems(self._newSceneJson, self._scene.graphModel)

    @override
    def redo(self):
        self._scene.clearSelection()
        insertSerializedItems(self._newSceneJson, self._scene)

    def _takeSceneJsonFromClipboard(self):
        clipboard = QtWidgets.QApplication.clipboard()
        mimeData = clipboard.mimeData()

        json = QtCore.QJsonDocument()
        if mimeData.hasFormat("application/qt-nodes-graph"):
            json = QtCore.QJsonDocument.fromJson(
                mimeData.data("application/qt-nodes-graph")
            )
        elif mimeData.hasText():
            json = QtCore.QJsonDocument.fromJson(mimeData.text().toUtf8())

        return json.object()

    def _makeNewNodeIdsInScene(self, sceneJson):
        graphModel = self._scene.graphModel
        mapNodeIds: dict[NodeId, NodeId] = {}

        nodesJsonArray = sceneJson["nodes"]

        newNodesJsonArray = QtCore.QJsonArray()
        for node in nodesJsonArray:
            oldNodeId = node["id"]
            newNodeId = graphModel.newNodeId()
            mapNodeIds[oldNodeId] = newNodeId

            # Replace NodeId in json
            node["id"] = newNodeId

            newNodesJsonArray.append(node)

        connectionJsonArray = sceneJson["connections"]

        newConnJsonArray = QtCore.QJsonArray()
        for connection in connectionJsonArray:
            connId = fromJson(connection)

            newConnId = ConnectionId(
                mapNodeIds[connId.outNodeId],
                connId.outPortIndex,
                mapNodeIds[connId.inNodeId],
                connId.inPortIndex,
            )

            newConnJsonArray.append(toJson(newConnId))

        newSceneJson = QJsonObject()

        newSceneJson["nodes"] = newNodesJsonArray
        newSceneJson["connections"] = newConnJsonArray

        return newSceneJson


class DisconnectCommand(QtGui.QUndoCommand):
    def __init__(self, scene, connection_id):
        super().__init__()
        self._scene = scene
        self._connection_id = connection_id

    @override
    def undo(self):
        self._scene.graphModel.addConnection(self._connection_id)

    @override
    def redo(self):
        self._scene.graphModel.deleteConnection(self._connection_id)


class ConnectCommand(QtGui.QUndoCommand):
    def __init__(self, scene, connection_id):
        super().__init__()
        self._scene = scene
        self._connection_id = connection_id

    @override
    def undo(self):
        self._scene.graphModel.deleteConnection(self._connection_id)

    @override
    def redo(self):
        self._scene.graphModel.addConnection(self._connection_id)


class MoveNodeCommand(QtGui.QUndoCommand):
    def __init__(self, scene, diff):
        from SpatialNode.node_graphics_object import NodeGraphicsObject

        super().__init__()
        self._scene = scene
        self._diff = diff
        self._selectedNodes = set()

        for item in self._scene.selectedItems():
            if isinstance(item, NodeGraphicsObject):
                self._selectedNodes.add(item.nodeId())

    @override
    def undo(self):
        for nodeId in self._selectedNodes:
            oldPos = self._scene.graphModel.nodeData(nodeId, NodeRole.Position)
            oldPos -= self._diff
            self._scene.graphModel.setNodeData(nodeId, NodeRole.Position, oldPos)

    @override
    def redo(self):
        for nodeId in self._selectedNodes:
            oldPos = self._scene.graphModel.nodeData(nodeId, NodeRole.Position)
            oldPos += self._diff
            self._scene.graphModel.setNodeData(nodeId, NodeRole.Position, oldPos)

    @override
    def id(self):
        return hash(self)

    @override
    def mergeWith(self, other):
        if isinstance(other, MoveNodeCommand):
            if self._selectedNodes == other._selectedNodes:
                self._diff += other._diff
                return True
            return False
