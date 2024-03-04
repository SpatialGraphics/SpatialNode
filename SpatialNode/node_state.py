#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.


class NodeState:
    def __init__(self):
        self._hovered = False
        self._resizing = False
        self._connectionForReaction = None

    @property
    def hovered(self):
        return self._hovered

    @hovered.setter
    def hovered(self, value):
        self._hovered = value

    @property
    def resizing(self):
        return self._resizing

    @resizing.setter
    def resizing(self, resizing: bool):
        self._resizing = resizing

    @property
    def connectionForReaction(self):
        return self._connectionForReaction

    @connectionForReaction.setter
    def connectionForReaction(self, cgo):
        self._connectionForReaction = cgo

    def resetConnectionForReaction(self):
        self._connectionForReaction = None
