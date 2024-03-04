#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtGui, QtCore


def cubicPath(connection):
    from SpatialNode.definitions import PortType

    inSlot = connection.endPoint(PortType.In)
    outSlot = connection.endPoint(PortType.Out)

    c1, c2 = connection.pointsC1C2()

    # cubic spline
    cubic = QtGui.QPainterPath(outSlot)

    cubic.cubicTo(c1, c2, inSlot)

    return cubic


def drawSketchLine(painter, cgo):
    from SpatialNode.style_collection import StyleCollection

    state = cgo.connectionState

    if state.requiresPort():
        connectionStyle = StyleCollection.connectionStyle()

        pen = QtGui.QPen()
        pen.setWidth(connectionStyle.ConstructionLineWidth)
        pen.setColor(connectionStyle.ConstructionColor)
        pen.setStyle(QtCore.Qt.PenStyle.DashLine)

        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)

        cubic = cubicPath(cgo)

        # cubic spline
        painter.drawPath(cubic)


def drawHoveredOrSelected(painter, cgo):
    from SpatialNode.style_collection import StyleCollection

    hovered = cgo.connectionState.hovered
    selected = cgo.isSelected()

    # drawn as a fat background
    if hovered or selected:
        connectionStyle = StyleCollection.connectionStyle()

        lineWidth = connectionStyle.LineWidth

        pen = QtGui.QPen()
        pen.setWidth(2 * lineWidth)
        pen.setColor(
            connectionStyle.SelectedHaloColor
            if selected
            else connectionStyle.HoveredColor
        )

        painter.setPen(pen)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)

        # cubic spline
        cubic = cubicPath(cgo)
        painter.drawPath(cubic)


def drawNormalLine(painter, cgo):
    from SpatialNode.style_collection import StyleCollection
    from SpatialNode.definitions import PortType, PortRole

    state = cgo.connectionState

    if state.requiresPort():
        return

    # colors

    connectionStyle = StyleCollection.connectionStyle()

    normalColorOut = connectionStyle.NormalColor
    normalColorIn = connectionStyle.NormalColor
    selectedColor = connectionStyle.SelectedColor

    useGradientColor = False

    graphModel = cgo.graphModel

    if connectionStyle.UseDataDefinedColors:
        cId = cgo.connectionId

        dataTypeOut = graphModel.portData(
            cId.outNodeId, PortType.Out, cId.outPortIndex, PortRole.DataType
        )
        dataTypeIn = graphModel.portData(
            cId.inNodeId, PortType.In, cId.inPortIndex, PortRole.DataType
        )
        useGradientColor = dataTypeOut.id != dataTypeIn.id

        normalColorOut = connectionStyle.normalColor(dataTypeOut.id)
        normalColorIn = connectionStyle.normalColor(dataTypeIn.id)
        selectedColor = normalColorOut.darker(200)

    # geometry

    lineWidth = connectionStyle.LineWidth

    # draw normal line
    p = QtGui.QPen()

    p.setWidth(lineWidth)

    selected = cgo.isSelected()

    cubic = cubicPath(cgo)
    if useGradientColor:
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)

        cOut = normalColorOut
        if selected:
            cOut = cOut.darker(200)
        p.setColor(cOut)
        painter.setPen(p)

        segments = 60
        for i in range(segments):
            ratioPrev = float(i) / segments
            ratio = float(i + 1) / segments

            if i == segments / 2:
                cIn = normalColorIn
                if selected:
                    cIn = cIn.darker(200)

                p.setColor(cIn)
                painter.setPen(p)
            painter.drawLine(
                cubic.pointAtPercent(ratioPrev), cubic.pointAtPercent(ratio)
            )

            icon = QtGui.QIcon(":convert.png")

            pixmap = icon.pixmap(QtCore.QSize(22, 22))
            painter.drawPixmap(
                cubic.pointAtPercent(0.50)
                - QtCore.QPoint(pixmap.width() / 2, pixmap.height() / 2),
                pixmap,
            )
    else:
        p.setColor(normalColorOut)

        if selected:
            p.setColor(selectedColor)

        painter.setPen(p)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)

        painter.drawPath(cubic)


class ConnectionPainter:
    @staticmethod
    def paint(painter, cgo):
        from SpatialNode.style_collection import StyleCollection

        drawHoveredOrSelected(painter, cgo)
        drawSketchLine(painter, cgo)
        drawNormalLine(painter, cgo)

        connectionStyle = StyleCollection.connectionStyle()
        pointDiameter = connectionStyle.PointDiameter

        painter.setPen(connectionStyle.ConstructionColor)
        painter.setBrush(connectionStyle.ConstructionColor)

        pointRadius = pointDiameter / 2.0
        painter.drawEllipse(cgo.outSlot(), pointRadius, pointRadius)
        painter.drawEllipse(cgo.inSlot(), pointRadius, pointRadius)

    @staticmethod
    def getPainterStroke(connection):
        from SpatialNode.definitions import PortType

        cubic = cubicPath(connection)

        out = connection.endPoint(PortType.Out)

        result = QtGui.QPainterPath(out)

        segments = 20
        for i in range(segments):
            ratio = float(i + 1) / segments
            result.lineTo(cubic.pointAtPercent(ratio))

        stroker = QtGui.QPainterPathStroker()
        stroker.setWidth(10.0)

        return stroker.createStroke(result)
