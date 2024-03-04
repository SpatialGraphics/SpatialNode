#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override
from PySide6 import QtCore, QtGui, QtWidgets
from SpatialNode.abstract_node_geometry import AbstractNodeGeometry


class DefaultHorizontalNodeGeometry(AbstractNodeGeometry):
    def __init__(self, graphModel):
        super().__init__(graphModel)
        self._portSize = 20
        self._portSpacing = 10
        self._fontMetrics = QtGui.QFontMetrics(QtGui.QFont())

        f = QtGui.QFont()
        f.setBold(True)
        self._boldFontMetrics = QtGui.QFontMetrics(f)
        self._portSize = self._fontMetrics.height()

    @override
    def size(self, nodeId):
        from SpatialNode.definitions import NodeRole

        return self._graphModel.nodeData(nodeId, NodeRole.Size)

    @override
    def recomputeSize(self, nodeId):
        from SpatialNode.definitions import NodeRole, PortType

        height = self._maxVerticalPortsExtent(nodeId)
        w = self._graphModel.nodeData(nodeId, NodeRole.Widget)
        if w is not None:
            height = max(height, w.height())

        capRect = self.captionRect(nodeId)

        height += capRect.height()
        # space above caption
        height += self._portSpacing
        # space below caption
        height += self._portSpacing

        inPortWidth = self._maxPortsTextAdvance(nodeId, PortType.In)
        outPortWidth = self._maxPortsTextAdvance(nodeId, PortType.Out)
        width = inPortWidth + outPortWidth + 4 * self._portSpacing
        if w is not None:
            width += w.width()
        width = max(width, int(capRect.width()) + 2 * self._portSpacing)

        size = QtCore.QSize(width, height)
        self._graphModel.setNodeData(nodeId, NodeRole.Size, size)

    @override
    def portPosition(self, nodeId, portType, port_index):
        from SpatialNode.definitions import NodeRole, PortType

        step = self._portSize + self._portSpacing
        totalHeight = 0.0
        totalHeight += self.captionRect(nodeId).height()
        totalHeight += self._portSpacing

        totalHeight += step * port_index
        totalHeight += step / 2.0

        size = self._graphModel.nodeData(nodeId, NodeRole.Size)

        result = QtCore.QPointF()
        match portType:
            case PortType.In:
                x = 0.0
                result = QtCore.QPointF(x, totalHeight)
            case PortType.Out:
                x = size.width()
                result = QtCore.QPointF(x, totalHeight)
        return result

    @override
    def portTextPosition(self, nodeId, portType, port_index):
        from SpatialNode.definitions import NodeRole, PortType

        p = self.portPosition(nodeId, portType, port_index)
        rect = self._portTextRect(nodeId, portType, port_index)
        p.setY(p.y() + rect.height() / 4.0)
        size = self._graphModel.nodeData(nodeId, NodeRole.Size)

        match portType:
            case PortType.In:
                p.setX(self._portSpacing)
            case PortType.Out:
                p.setX(size.width() - self._portSpacing - rect.width())
        return p

    @override
    def captionPosition(self, nodeId):
        from SpatialNode.definitions import NodeRole

        size = self._graphModel.nodeData(nodeId, NodeRole.Size)
        return QtCore.QPointF(
            0.5 * (size.width() - self.captionRect(nodeId).width()),
            0.5 * self._portSpacing + self.captionRect(nodeId).height(),
        )

    @override
    def captionRect(self, nodeId):
        from SpatialNode.definitions import NodeRole

        if not self._graphModel.nodeData(nodeId, NodeRole.CaptionVisible):
            return QtCore.QRectF()

        name = self._graphModel.nodeData(nodeId, NodeRole.Caption)
        return self._boldFontMetrics.boundingRect(name)

    @override
    def widgetPosition(self, nodeId):
        from SpatialNode.definitions import NodeRole, PortType

        size = self._graphModel.nodeData(nodeId, NodeRole.Size)

        captionHeight = self.captionRect(nodeId).height()

        w = self._graphModel.nodeData(nodeId, NodeRole.Widget)
        if w is not None:
            # If the widget wants to use as much vertical space as possible,
            # place it immediately after the caption.
            if (
                w.sizePolicy().verticalPolicy().value
                & QtWidgets.QSizePolicy.PolicyFlag.ExpandFlag.value
            ):
                return QtCore.QPointF(
                    2.0 * self._portSpacing
                    + self._maxPortsTextAdvance(nodeId, PortType.In),
                    captionHeight,
                )
            else:
                return QtCore.QPointF(
                    2.0 * self._portSpacing
                    + self._maxPortsTextAdvance(nodeId, PortType.In),
                    (captionHeight + size.height() - w.height()) / 2.0,
                )
        return QtCore.QPointF()

    @override
    def resizeHandleRect(self, nodeId):
        from SpatialNode.definitions import NodeRole

        size = self._graphModel.nodeData(nodeId, NodeRole.Size)
        rectSize = 7
        return QtCore.QRect(
            size.width() - self._portSpacing,
            size.height() - self._portSpacing,
            rectSize,
            rectSize,
        )

    def _portTextRect(self, node_id, portType, portIndex):
        from SpatialNode.definitions import PortRole

        if self._graphModel.portData(
            node_id, portType, portIndex, PortRole.CaptionVisible
        ):
            s = self._graphModel.portData(
                node_id, portType, portIndex, PortRole.Caption
            )
        else:
            portData = self._graphModel.portData(
                node_id, portType, portIndex, PortRole.DataType
            )
            s = portData.name

        return self._fontMetrics.boundingRect(s)

    def _maxVerticalPortsExtent(self, node_id):
        from SpatialNode.definitions import NodeRole

        nInPorts = self._graphModel.nodeData(node_id, NodeRole.InPortCount)
        nOutPorts = self._graphModel.nodeData(node_id, NodeRole.OutPortCount)
        maxNumOfEntries = max(nInPorts, nOutPorts)
        step = self._portSize + self._portSpacing

        return step * maxNumOfEntries

    def _maxPortsTextAdvance(self, nodeId, portType):
        from SpatialNode.definitions import NodeRole, PortType, PortRole

        width = 0

        n = self._graphModel.nodeData(
            nodeId,
            NodeRole.OutPortCount if portType == PortType.Out else NodeRole.InPortCount,
        )

        for portIndex in range(n):
            if self._graphModel.portData(
                nodeId, portType, portIndex, PortRole.CaptionVisible
            ):
                name = self._graphModel.portData(
                    nodeId, portType, portIndex, PortRole.Caption
                )
            else:
                portData = self._graphModel.portData(
                    nodeId, portType, portIndex, PortRole.DataType
                )
                name = portData.name

            width = max(self._fontMetrics.horizontalAdvance(name), width)

        return width
