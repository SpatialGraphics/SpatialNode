#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.


class ConnectionState:
    def __init__(self, cgo):
        from SpatialNode.definitions import InvalidNodeId

        self._cgo = cgo
        self._hovered = False
        self._lastHoveredNode = InvalidNodeId

    def requiredPort(self):
        from SpatialNode.definitions import InvalidNodeId, PortType

        t = None

        if self._cgo.connectionId.outNodeId == InvalidNodeId:
            t = PortType.Out
        elif self._cgo.connectionId.inNodeId == InvalidNodeId:
            t = PortType.In

        return t

    def requiresPort(self):
        from SpatialNode.definitions import InvalidNodeId

        id = self._cgo.connectionId
        return id.outNodeId == InvalidNodeId or id.inNodeId == InvalidNodeId

    @property
    def hovered(self):
        return self._hovered

    @hovered.setter
    def hovered(self, value):
        self._hovered = value

    @property
    def lastHoveredNode(self):
        return self._lastHoveredNode

    @lastHoveredNode.setter
    def lastHoveredNode(self, value):
        self._lastHoveredNode = value

    def resetLastHoveredNode(self):
        from SpatialNode.definitions import InvalidNodeId

        if self._lastHoveredNode != InvalidNodeId:
            ngo = self._cgo.nodeScene.nodeGraphicsObject(self._lastHoveredNode)
            ngo.update()
        self._lastHoveredNode = InvalidNodeId
