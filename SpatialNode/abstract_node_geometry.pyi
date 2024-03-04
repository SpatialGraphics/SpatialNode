#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from abc import ABC, abstractmethod

from PySide6 import QtCore, QtGui

from SpatialNode.abstract_graph_model import AbstractGraphModel
from SpatialNode.definitions import NodeId, PortType, PortIndex

class AbstractNodeGeometry(ABC):
    def __init__(self, graphModel: AbstractGraphModel):
        self._graphModel = graphModel

    def boundingRect(self, nodeId: NodeId) -> QtCore.QRectF: ...
    @abstractmethod
    def size(self, nodeId: NodeId) -> QtCore.QSize:
        """
        A direct rectangle defining the borders of the node's rectangle.
        """
        ...

    @abstractmethod
    def recomputeSize(self, nodeId: NodeId): ...
    @abstractmethod
    def portPosition(
        self, nodeId: NodeId, portType: PortType | None, index: PortIndex
    ) -> QtCore.QPointF:
        """
        Port position in node's coordinate system.
        """
        ...

    def portScenePosition(
        self,
        nodeId: NodeId,
        portType: PortType | None,
        index: PortIndex,
        t: QtGui.QTransform,
    ) -> QtCore.QPointF:
        """
        A convenience function using the `portPosition` and a given transformation.
        """
        ...

    @abstractmethod
    def portTextPosition(
        self, nodeId: NodeId, portType: PortType | None, nodePoint: PortIndex
    ) -> QtCore.QPointF:
        """
        Defines where to draw port label. The point corresponds to a font baseline.
        """
        ...

    @abstractmethod
    def captionPosition(self, nodeId: NodeId) -> QtCore.QPointF:
        """
        Defines where to start drawing the caption. The point corresponds to a font baseline.
        """
        ...

    @abstractmethod
    def captionRect(self, nodeId: NodeId) -> QtCore.QRectF:
        """
        Caption rect is needed for estimating the total node size.
        """
        ...

    @abstractmethod
    def widgetPosition(self, nodeId: NodeId) -> QtCore.QPointF:
        """
        Position for an embedded widget. Return any value if you don't embed.
        """
        ...

    def checkPortHit(
        self, nodeId: NodeId, portType: PortType | None, nodePoint: QtCore.QPointF
    ) -> PortIndex: ...
    @abstractmethod
    def resizeHandleRect(self, nodeId: NodeId) -> QtCore.QRect: ...
