#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.


class NodeConnectionInteraction:
    def __init__(self, ngo, cgo, scene):
        self._ngo = ngo
        self._cgo = cgo
        self._scene = scene

    def canConnect(self, portIndex):
        from SpatialNode.connection_id_utils import (
            getNodeId,
            oppositePort,
            makeCompleteConnectionId,
        )
        from SpatialNode.definitions import InvalidPortIndex

        requiredPort = self._cgo.connectionState.requiredPort()

        if requiredPort is None:
            return False, portIndex

        connectedNodeId = getNodeId(oppositePort(requiredPort), self._cgo.connectionId)

        if self._ngo.nodeId() == connectedNodeId:
            return False, portIndex

        connectionPoint = self._cgo.sceneTransform().map(
            self._cgo.endPoint(requiredPort)
        )

        portIndex = self._nodePortIndexUnderScenePoint(requiredPort, connectionPoint)

        if portIndex == InvalidPortIndex:
            return False, portIndex

        model = self._ngo.nodeScene().graphModel

        connectionId = makeCompleteConnectionId(
            self._cgo.connectionId, self._ngo.nodeId(), portIndex
        )
        return model.connectionPossible(connectionId), portIndex

    def tryConnect(self):
        from SpatialNode.definitions import InvalidPortIndex
        from SpatialNode.connection_id_utils import makeCompleteConnectionId
        from SpatialNode.undo_commands import ConnectCommand

        canConnect, targetPortIndex = self.canConnect(InvalidPortIndex)
        if not canConnect:
            return False

        incompleteConnectionId = self._cgo.connectionId
        newConnectionId = makeCompleteConnectionId(
            incompleteConnectionId, self._ngo.nodeId(), targetPortIndex
        )

        self._ngo.nodeScene().resetDraftConnection()
        self._ngo.nodeScene().undoStack.push(
            ConnectCommand(self._ngo.nodeScene(), newConnectionId)
        )

        return True

    def disconnect(self, portToDisconnect):
        from SpatialNode.undo_commands import DisconnectCommand
        from SpatialNode.connection_id_utils import (
            getPortIndex,
            makeIncompleteConnectionIdFromComplete,
            oppositePort,
            getNodeId,
        )

        connectionId = self._cgo.connectionId
        self._scene.undoStack.push(DisconnectCommand(self._scene, connectionId))

        geometry = self._scene.nodeGeometry
        scenePos = geometry.portScenePosition(
            self._ngo.nodeId(),
            portToDisconnect,
            getPortIndex(portToDisconnect, connectionId),
            self._ngo.sceneTransform(),
        )

        incompleteConnectionId = makeIncompleteConnectionIdFromComplete(
            connectionId, portToDisconnect
        )
        draftConnection = self._scene.makeDraftConnection(incompleteConnectionId)
        looseEndPos = draftConnection.mapFromScene(scenePos)
        draftConnection.setEndPoint(portToDisconnect, looseEndPos)

        connectedNodeId = getNodeId(oppositePort(portToDisconnect), connectionId)
        self._scene.nodeGraphicsObject(connectedNodeId).update()

        disconnectedNodeId = getNodeId(portToDisconnect, connectionId)
        self._scene.nodeGraphicsObject(disconnectedNodeId).update()

        return True

    def _connectionRequiredPort(self):
        state = self._cgo.connectionState
        return state.requiredPort()

    def _nodePortScenePosition(self, portType, portIndex):
        geometry = self._scene.nodeGeometry
        p = geometry.portScenePosition(
            self._ngo.nodeId(), portType, portIndex, self._ngo.sceneTransform()
        )
        return p

    def _nodePortIndexUnderScenePoint(self, portType, scenePoint):
        geometry = self._scene.nodeGeometry
        sceneTransform = self._ngo.sceneTransform()
        nodePoint = sceneTransform.inverted()[0].map(scenePoint)
        return geometry.checkPortHit(self._ngo.nodeId(), portType, nodePoint)
