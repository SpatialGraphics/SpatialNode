#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtGui, QtCore

from SpatialNode.abstract_graph_model import AbstractGraphModel
from SpatialNode.abstract_node_geometry import AbstractNodeGeometry
from SpatialNode.definitions import NodeId, PortType, PortIndex

class DefaultVerticalNodeGeometry(AbstractNodeGeometry):
    def __init__(self, graphModel: AbstractGraphModel):
        self._portSize: int = None
        self._portSpacing: int = None
        self._fontMetrics: QtGui.QFontMetrics = None
        self._boldFontMetrics: QtGui.QFontMetrics = None
        ...

    @override
    def size(self, nodeId: NodeId) -> QtCore.QSize: ...
    @override
    def recomputeSize(self, nodeId: NodeId): ...
    @override
    def portPosition(
        self, nodeId: NodeId, portType: PortType | None, portIndex: PortIndex
    ) -> QtCore.QPointF: ...
    @override
    def portTextPosition(
        self, nodeId: NodeId, portType: PortType | None, portIndex: PortIndex
    ) -> QtCore.QPointF: ...
    @override
    def captionPosition(self, nodeId: NodeId) -> QtCore.QPointF: ...
    @override
    def captionRect(self, nodeId: NodeId) -> QtCore.QRectF: ...
    @override
    def widgetPosition(self, nodeId: NodeId) -> QtCore.QPointF: ...
    @override
    def resizeHandleRect(self, nodeId: NodeId) -> QtCore.QRect: ...
    def _portTextRect(
        self, nodeId: NodeId, portType: PortType | None, portIndex: PortIndex
    ): ...
    def _maxVerticalPortsExtent(self, nodeId: NodeId): ...
    def _maxPortsTextAdvance(self, nodeId: NodeId, portType: PortType | None): ...
    def _portCaptionsHeight(self, nodeId: NodeId, portType: PortType | None): ...
