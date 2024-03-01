from SpatialNode.definitions import PortType, ConnectionId, PortIndex, NodeId, InvalidNodeId, InvalidPortIndex


def getNodeId(portType: PortType | None, connectionId: ConnectionId) -> int:
    ...


def getPortIndex(portType: PortType | None, connectionId: ConnectionId) -> int:
    ...


def oppositePort(port: PortType | None) -> PortType | None:
    ...


def isPortIndexValid(index: PortIndex) -> PortIndex:
    ...


def isPortTypeValid(portType: PortType | None) -> bool:
    ...


def makeIncompleteConnectionId(connectedNodeId: NodeId,
                               connectedPort: PortType | None,
                               connectedPortIndex: PortIndex) -> ConnectionId:
    """Creates a connection Id instance filled just on one side."""
    ...


def makeIncompleteConnectionIdFromComplete(connectionId: ConnectionId,
                                           portToDisconnect: PortType | None) -> ConnectionId:
    """
    Turns a full connection Id into an incomplete one by removing the data on the given side
    """
    ...


def makeCompleteConnectionId(incompleteConnectionId: ConnectionId,
                             nodeId: NodeId,
                             portIndex: PortIndex) -> ConnectionId:
    ...


def toJson(connId: ConnectionId):
    ...
