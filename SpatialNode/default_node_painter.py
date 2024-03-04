#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import math
from typing import override

from PySide6 import QtGui, QtCore

from SpatialNode.abstract_node_painter import AbstractNodePainter


class DefaultNodePainter(AbstractNodePainter):
    @override
    def paint(self, painter, ngo):
        self.drawNodeRect(painter, ngo)
        self.drawConnectionPoints(painter, ngo)
        self.drawFilledConnectionPoints(painter, ngo)
        self.drawNodeCaption(painter, ngo)
        self.drawEntryLabels(painter, ngo)
        self.drawResizeRect(painter, ngo)

    def drawNodeRect(self, painter, ngo):
        from SpatialNode.definitions import NodeRole
        from SpatialNode.node_style import NodeStyle

        model = ngo.graphModel
        nodeId = ngo.nodeId()
        geometry = ngo.nodeScene().nodeGeometry
        size = geometry.size(nodeId)

        json = QtCore.QJsonDocument.fromVariant(model.nodeData(nodeId, NodeRole.Style))
        nodeStyle = NodeStyle()
        nodeStyle.fromJsonObject(json.object())

        color = (
            nodeStyle.SelectedBoundaryColor
            if ngo.isSelected()
            else nodeStyle.NormalBoundaryColor
        )

        if ngo.nodeState.hovered:
            p = QtGui.QPen(color, nodeStyle.HoveredPenWidth)
            painter.setPen(p)
        else:
            p = QtGui.QPen(color, nodeStyle.PenWidth)
            painter.setPen(p)

        gradient = QtGui.QLinearGradient(
            QtCore.QPointF(0.0, 0.0), QtCore.QPointF(2.0, size.height())
        )
        gradient.setColorAt(0.0, nodeStyle.GradientColor0)
        gradient.setColorAt(0.10, nodeStyle.GradientColor1)
        gradient.setColorAt(0.90, nodeStyle.GradientColor2)
        gradient.setColorAt(1.0, nodeStyle.GradientColor3)
        painter.setBrush(gradient)

        boundary = QtCore.QRectF(0, 0, size.width(), size.height())
        radius = 3.0
        painter.drawRoundedRect(boundary, radius, radius)

    def drawConnectionPoints(self, painter, ngo):
        from SpatialNode.node_style import NodeStyle
        from SpatialNode.definitions import PortType, NodeRole, PortRole
        from SpatialNode.style_collection import StyleCollection
        from SpatialNode.connection_id_utils import makeCompleteConnectionId

        model = ngo.graphModel
        nodeId = ngo.nodeId()
        geometry = ngo.nodeScene().nodeGeometry

        json = QtCore.QJsonDocument.fromVariant(model.nodeData(nodeId, NodeRole.Style))
        nodeStyle = NodeStyle()
        nodeStyle.fromJsonObject(json.object())

        connectionStyle = StyleCollection.connectionStyle()

        diameter = nodeStyle.ConnectionPointDiameter
        reducedDiameter = diameter * 0.6

        for portType in [PortType.Out, PortType.In]:
            n = model.nodeData(
                nodeId,
                (
                    NodeRole.OutPortCount
                    if (portType == PortType.Out)
                    else NodeRole.InPortCount
                ),
            )

            for portIndex in range(n):
                p = geometry.portPosition(nodeId, portType, portIndex)
                dataType = model.portData(
                    nodeId, portType, portIndex, PortRole.DataType
                )

                r = 1.0

                state = ngo.nodeState
                cgo = state.connectionForReaction
                if cgo is not None:
                    requiredPort = cgo.connectionState.requiredPort()

                    if requiredPort == portType:
                        possibleConnectionId = makeCompleteConnectionId(
                            cgo.connectionId, nodeId, portIndex
                        )
                        possible = model.connectionPossible(possibleConnectionId)

                        cp = cgo.sceneTransform().map(cgo.endPoint(requiredPort))
                        cp = ngo.sceneTransform().inverted()[0].map(cp)

                        diff = cp - p
                        dist = math.sqrt(QtCore.QPointF.dotProduct(diff, diff))

                        if possible:
                            thres = 40.0
                            r = 2.0 - dist / thres if dist < thres else 1.0
                        else:
                            thres = 80.0
                            r = dist / thres if dist < thres else 1.0

                if connectionStyle.UseDataDefinedColors:
                    painter.setBrush(connectionStyle.normalColor(dataType.id))
                else:
                    painter.setBrush(nodeStyle.ConnectionPointColor)

                painter.drawEllipse(p, reducedDiameter * r, reducedDiameter * r)

        if ngo.nodeState.connectionForReaction:
            ngo.nodeState.resetConnectionForReaction()

    def drawFilledConnectionPoints(self, painter, ngo):
        from SpatialNode.node_style import NodeStyle
        from SpatialNode.definitions import PortType, NodeRole, PortRole
        from SpatialNode.style_collection import StyleCollection

        model = ngo.graphModel
        nodeId = ngo.nodeId()
        geometry = ngo.nodeScene().nodeGeometry

        json = QtCore.QJsonDocument.fromVariant(model.nodeData(nodeId, NodeRole.Style))
        nodeStyle = NodeStyle()
        nodeStyle.fromJsonObject(json.object())

        diameter = nodeStyle.ConnectionPointDiameter

        for portType in [PortType.Out, PortType.In]:
            n = model.nodeData(
                nodeId,
                (
                    NodeRole.OutPortCount
                    if portType == PortType.Out
                    else NodeRole.InPortCount
                ),
            )

            for portIndex in range(n):
                p = geometry.portPosition(nodeId, portType, portIndex)
                connected = model.connections(nodeId, portType, portIndex)

                if len(connected) > 0:
                    dataType = model.portData(
                        nodeId, portType, portIndex, PortRole.DataType
                    )
                    connectionStyle = StyleCollection.connectionStyle()

                    if connectionStyle.UseDataDefinedColors:
                        c = connectionStyle.normalColor(dataType.id)
                        painter.setPen(c)
                        painter.setBrush(c)
                    else:
                        painter.setPen(nodeStyle.FilledConnectionPointColor)
                        painter.setBrush(nodeStyle.FilledConnectionPointColor)

                    painter.drawEllipse(p, diameter * 0.4, diameter * 0.4)

    def drawNodeCaption(self, painter, ngo):
        from SpatialNode.node_style import NodeStyle
        from SpatialNode.definitions import NodeRole

        model = ngo.graphModel
        nodeId = ngo.nodeId()
        geometry = ngo.nodeScene().nodeGeometry

        if not model.nodeData(nodeId, NodeRole.CaptionVisible):
            return

        name = model.nodeData(nodeId, NodeRole.Caption)

        f = painter.font()
        f.setBold(True)

        position = geometry.captionPosition(nodeId)

        json = QtCore.QJsonDocument.fromVariant(model.nodeData(nodeId, NodeRole.Style))
        nodeStyle = NodeStyle()
        nodeStyle.fromJsonObject(json.object())

        painter.setFont(f)
        painter.setPen(nodeStyle.FontColor)
        painter.drawText(position, name)

        f.setBold(False)
        painter.setFont(f)

    def drawEntryLabels(self, painter, ngo):
        from SpatialNode.node_style import NodeStyle
        from SpatialNode.definitions import PortType, NodeRole, PortRole

        model = ngo.graphModel
        nodeId = ngo.nodeId()
        geometry = ngo.nodeScene().nodeGeometry

        json = QtCore.QJsonDocument.fromVariant(model.nodeData(nodeId, NodeRole.Style))
        nodeStyle = NodeStyle()
        nodeStyle.fromJsonObject(json.object())

        for portType in [PortType.Out, PortType.In]:
            n = model.nodeData(
                nodeId,
                (
                    NodeRole.OutPortCount
                    if portType == PortType.Out
                    else NodeRole.InPortCount
                ),
            )

            for portIndex in range(n):
                connected = model.connections(nodeId, portType, portIndex)

                p = geometry.portTextPosition(nodeId, portType, portIndex)

                if len(connected) == 0:
                    painter.setPen(nodeStyle.FontColorFaded)
                else:
                    painter.setPen(nodeStyle.FontColor)

                s = ""
                if model.portData(nodeId, portType, portIndex, PortRole.CaptionVisible):
                    s = model.portData(nodeId, portType, portIndex, PortRole.Caption)
                else:
                    portData = model.portData(
                        nodeId, portType, portIndex, PortRole.DataType
                    )
                    s = portData.name

                painter.drawText(p, s)

    def drawResizeRect(self, painter, ngo):
        from SpatialNode.definitions import NodeFlag

        model = ngo.graphModel
        nodeId = ngo.nodeId()
        geometry = ngo.nodeScene().nodeGeometry

        if model.nodeFlags(nodeId) & NodeFlag.Resizable:
            painter.setBrush(QtCore.Qt.GlobalColor.gray)
            painter.drawEllipse(geometry.resizeHandleRect(nodeId))
