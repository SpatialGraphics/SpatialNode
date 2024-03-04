#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from SpatialNode.connection_graphics_object import ConnectionGraphicsObject

class NodeState:
    """
    Stores bool for hovering connections and resizing flag.
    """

    def __init__(self):
        self._hovered: bool = None
        self._resizing: bool = None
        self._connectionForReaction: ConnectionGraphicsObject = None

    @property
    def hovered(self) -> bool: ...
    @hovered.setter
    def hovered(self, value: bool):

    @property
    def resizing(self) -> bool: ...
    @resizing.setter
    def resizing(self, resizing: bool):

    @property
    def connectionForReaction(self) -> ConnectionGraphicsObject: ...
    @connectionForReaction.setter
    def connectionForReaction(self, cgo: ConnectionGraphicsObject): ...
    def resetConnectionForReaction(self): ...
