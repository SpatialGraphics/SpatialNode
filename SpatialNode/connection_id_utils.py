#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtCore


def getNodeId(portType, connectionId):
    from SpatialNode.definitions import InvalidNodeId, PortType

    index = InvalidNodeId

    if portType == PortType.Out:
        index = connectionId.outNodeId
    elif portType == PortType.In:
        index = connectionId.inNodeId

    return index


def getPortIndex(portType, connectionId):
    from SpatialNode.definitions import InvalidPortIndex, PortType

    index = InvalidPortIndex

    if portType == PortType.Out:
        index = connectionId.outPortIndex
    elif portType == PortType.In:
        index = connectionId.inPortIndex

    return index


def oppositePort(port):
    from SpatialNode.definitions import PortType

    result = None

    match port:
        case PortType.In:
            result = PortType.Out
        case PortType.Out:
            result = PortType.In
        case None:
            result = None

    return result


def isPortIndexValid(index):
    from SpatialNode.definitions import InvalidPortIndex

    return index != InvalidPortIndex


def isPortTypeValid(portType):
    return portType is not None


def makeIncompleteConnectionId(connectedNodeId,
                               connectedPort,
                               connectedPortIndex):
    from SpatialNode.definitions import InvalidPortIndex, InvalidNodeId, ConnectionId, PortType

    return ConnectionId(InvalidNodeId, InvalidPortIndex, connectedNodeId, connectedPortIndex) \
        if connectedPort == PortType.In \
        else ConnectionId(connectedNodeId, connectedPortIndex, InvalidNodeId, InvalidPortIndex)


def makeIncompleteConnectionIdFromComplete(connectionId,
                                           portToDisconnect):
    from SpatialNode.definitions import InvalidPortIndex, InvalidNodeId, PortType

    if portToDisconnect == PortType.Out:
        connectionId.outNodeId = InvalidNodeId
        connectionId.outPortIndex = InvalidPortIndex
    else:
        connectionId.inNodeId = InvalidNodeId
        connectionId.inPortIndex = InvalidPortIndex
    return connectionId


def makeCompleteConnectionId(incompleteConnectionId,
                             nodeId,
                             portIndex):
    from SpatialNode.definitions import InvalidNodeId

    if incompleteConnectionId.outNodeId == InvalidNodeId:
        incompleteConnectionId.outNodeId = nodeId
        incompleteConnectionId.outPortIndex = portIndex
    else:
        incompleteConnectionId.inNodeId = nodeId
        incompleteConnectionId.inPortIndex = portIndex

    return incompleteConnectionId


def toJson(connId):
    connJson = QtCore.QJsonDocument().object()
    return connJson
