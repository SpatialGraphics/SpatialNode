#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from abc import ABC, abstractmethod


class NodeDataType:
    id: str
    name: str

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name


class NodeData(ABC):
    def sameType(self, nodeData):
        if isinstance(nodeData, NodeData):
            return self.type().id == nodeData.type().id
        return False

    @abstractmethod
    def type(self) -> NodeDataType: ...
