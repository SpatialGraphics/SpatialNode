#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from SpatialNode.connection_graphics_object import ConnectionGraphicsObject
from SpatialNode.definitions import NodeId, PortType

class ConnectionState:
    """
    Stores currently dragging end.
    Remembers last hovered Node.
    """

    def __init__(self, cgo: ConnectionGraphicsObject):
        self._cgo: ConnectionGraphicsObject = None
        self._hovered: bool = None
        self._lastHoveredNode: NodeId = None

    def requiredPort(self) -> PortType: ...
    def requiresPort(self) -> bool: ...
    @property
    def hovered(self) -> bool: ...
    @hovered.setter
    def hovered(self, value: bool): ...
    @property
    def lastHoveredNode(self) -> NodeId: ...
    @lastHoveredNode.setter
    def lastHoveredNode(self, value: NodeId): ...
    def resetLastHoveredNode(self) -> None: ...
