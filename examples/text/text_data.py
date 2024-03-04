#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

import SpatialNode as sNode


class TextData(sNode.NodeData):
    def __init__(self, text: str = ""):
        super().__init__()
        self._text = text

    @override
    def type(self):
        return sNode.NodeDataType("text", "Text")

    def text(self):
        return self._text
