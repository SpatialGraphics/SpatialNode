#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import SpatialNode as sNode


class DecimalData(sNode.NodeData):
    """
    The class can potentially incapsulate any user data which
    need to be transferred within the Node Editor graph
    """

    def __init__(self, number: float = 0.0):
        super().__init__()
        self._number = number

    def type(self):
        return sNode.NodeDataType("decimal", "Decimal")

    def number(self) -> float:
        return self._number

    def numberAsText(self) -> str:
        return str(self._number)
