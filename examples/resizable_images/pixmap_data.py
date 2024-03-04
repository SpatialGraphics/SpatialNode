#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtGui

import SpatialNode as sNode


class PixmapData(sNode.NodeData):
    def __init__(self, pixmap: QtGui.QPixmap | None):
        super().__init__()
        self._pixmap = pixmap

    def type(self):
        return sNode.NodeDataType("pixmap", "P")

    def pixmap(self):
        return self._pixmap
