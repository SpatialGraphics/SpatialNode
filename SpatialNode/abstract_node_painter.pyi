#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from abc import ABC, abstractmethod

from PySide6 import QtGui

class AbstractNodePainter(ABC):
    """
    Class enables custom painting.
    """

    @abstractmethod
    def paint(self, painter: QtGui.QPainter, ngo) -> None:
        """
        Reimplement this function in order to have a custom painting.
        """
        ...
