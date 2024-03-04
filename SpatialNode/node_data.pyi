#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from abc import ABC, abstractmethod

class NodeDataType:
    id: str
    """ represents an internal unique data type for the given port. """
    name: str
    """ a normal text description. """

    def __init__(self, id: str, name: str): ...

class NodeData(ABC):
    """
    Class represents data transferred between nodes.
    """

    def sameType(self, nodeData: NodeData): ...
    @abstractmethod
    def type(self) -> NodeDataType: ...
