#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtCore, QtGui, QtWidgets

from SpatialNode.abstract_node_geometry import AbstractNodeGeometry


class DefaultVerticalNodeGeometry(AbstractNodeGeometry):
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

        height = self._portSpacing
        w = self._graphModel.nodeData(nodeId, NodeRole.Widget)
        if w is not None:
            height = max(height, w.height())

        capRect = self.captionRect(nodeId)

        height += capRect.height()
        # space above caption
        height += self._portSpacing
        # space below caption
        height += self._portSpacing

        nInPorts = self._graphModel.nodeData(nodeId, NodeRole.InPortCount)
        nOutPorts = self._graphModel.nodeData(nodeId, NodeRole.OutPortCount)

        # Adding double step (top and bottom) to reserve space for port captions.
        height += self._portCaptionsHeight(nodeId, PortType.In)
        height += self._portCaptionsHeight(nodeId, PortType.Out)

        inPortWidth = self._maxPortsTextAdvance(nodeId, PortType.In)
        outPortWidth = self._maxPortsTextAdvance(nodeId, PortType.Out)

        totalInPortsWidth = (
            inPortWidth * nInPorts + self._portSpacing * (nInPorts - 1)
            if nInPorts > 0
            else 0
        )
        totalOutPortsWidth = (
            outPortWidth * nOutPorts + self._portSpacing * (nOutPorts - 1)
            if nOutPorts > 0
            else 0
        )
        width = max(totalInPortsWidth, totalOutPortsWidth)

        if w is not None:
            width = max(width, w.width())

        width = max(width, capRect.width())
        width += self._portSpacing
        width += self._portSpacing

        size = QtCore.QSize(width, height)
        self._graphModel.setNodeData(nodeId, NodeRole.Size, size)

    @override
    def portPosition(self, nodeId, portType, port_index):
        from SpatialNode.definitions import NodeRole, PortType

        result = QtCore.QPointF()
        size = self._graphModel.nodeData(nodeId, NodeRole.Size)
        match portType:
            case PortType.In:
                inPortWidth = (
                    self._maxPortsTextAdvance(nodeId, PortType.In) + self._portSpacing
                )
                nInPorts = self._graphModel.nodeData(nodeId, NodeRole.InPortCount)
                x = (
                    size.width() - (nInPorts - 1) * inPortWidth
                ) / 2.0 + port_index * inPortWidth
                y = 0.0

                result = QtCore.QPointF(x, y)
            case PortType.Out:
                outPortWidth = (
                    self._maxPortsTextAdvance(nodeId, PortType.Out) + self._portSpacing
                )
                nOutPorts = self._graphModel.nodeData(nodeId, NodeRole.OutPortCount)
                x = (
                    size.width() - (nOutPorts - 1) * outPortWidth
                ) / 2.0 + port_index * outPortWidth
                y = size.height()

                result = QtCore.QPointF(x, y)
        return result

    @override
    def portTextPosition(self, nodeId, portType, port_index):
        from SpatialNode.definitions import NodeRole, PortType

        p = self.portPosition(nodeId, portType, port_index)
        rect = self._portTextRect(nodeId, portType, port_index)
        p.setX(p.x() - rect.width() / 2.0)
        size = self._graphModel.nodeData(nodeId, NodeRole.Size)

        match portType:
            case PortType.In:
                p.setY(5.0 + rect.height())
            case PortType.Out:
                p.setY(size.height() - 5.0)
        return p

    @override
    def captionPosition(self, nodeId):
        from SpatialNode.definitions import NodeRole, PortType

        size = self._graphModel.nodeData(nodeId, NodeRole.Size)
        step = self._portCaptionsHeight(nodeId, PortType.In)
        step += self._portSpacing
        rect = self.captionRect(nodeId)
        return QtCore.QPointF(0.5 * (size.width() - rect.width()), step + rect.height())

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
                    self._portSpacing + self._maxPortsTextAdvance(nodeId, PortType.In),
                    captionHeight,
                )
            else:
                return QtCore.QPointF(
                    self._portSpacing + self._maxPortsTextAdvance(nodeId, PortType.In),
                    (captionHeight + size.height() - w.height()) / 2.0,
                )
        return QtCore.QPointF()

    @override
    def resizeHandleRect(self, nodeId):
        from SpatialNode.definitions import NodeRole

        size = self._graphModel.nodeData(nodeId, NodeRole.Size)
        rectSize = 7
        return QtCore.QRect(
            size.width() - rectSize, size.height() - rectSize, rectSize, rectSize
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

    def _maxPortsTextAdvance(self, node_id, port_type):
        from SpatialNode.definitions import NodeRole, PortType, PortRole

        width = 0

        n = self._graphModel.nodeData(
            node_id,
            (
                NodeRole.OutPortCount
                if port_type == PortType.Out
                else NodeRole.InPortCount
            ),
        )

        for portIndex in range(n):
            if self._graphModel.portData(
                node_id, port_type, portIndex, PortRole.CaptionVisible
            ):
                name = self._graphModel.portData(
                    node_id, port_type, portIndex, PortRole.Caption
                )
            else:
                portData = self._graphModel.portData(
                    node_id, port_type, portIndex, PortRole.DataType
                )
                name = portData.name

            width = max(self._fontMetrics.horizontalAdvance(name), width)

        return width

    def _portCaptionsHeight(self, node_id, port_type):
        from SpatialNode.definitions import NodeRole, PortType, PortRole

        h = 0
        match port_type:
            case PortType.In:
                nInPorts = self._graphModel.nodeData(node_id, NodeRole.InPortCount)
                for i in range(nInPorts):
                    if self._graphModel.portData(
                        node_id, PortType.In, i, PortRole.CaptionVisible
                    ):
                        h += self._portSpacing

            case PortType.Out:
                nOutPorts = self._graphModel.nodeData(node_id, NodeRole.OutPortCount)
                for i in range(nOutPorts):
                    if self._graphModel.portData(
                        node_id, PortType.Out, i, PortRole.CaptionVisible
                    ):
                        h += self._portSpacing

        return h
