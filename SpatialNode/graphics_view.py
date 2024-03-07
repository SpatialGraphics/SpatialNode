#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import math

from PySide6 import QtWidgets, QtGui, QtCore


class ScaleRange:
    minimum: float = 0
    maximum: float = 0


class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, scene, parent=None):
        from SpatialNode.style_collection import StyleCollection

        super().__init__(parent)
        self.setScene(scene)
        self.setAcceptDrops(True)

        self._clearSelectionAction = None
        self._deleteSelectionAction = None
        self._duplicateSelectionAction = None
        self._copySelectionAction = None
        self._pasteAction = None
        self._clickPos = QtCore.QPointF()
        self._scaleRange = ScaleRange()

        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        flowViewStyle = StyleCollection.flowViewStyle()

        self.setBackgroundBrush(flowViewStyle.BackgroundColor)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTransformationAnchor(
            QtWidgets.QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        self.setCacheMode(QtWidgets.QGraphicsView.CacheModeFlag.CacheBackground)
        self.setViewportUpdateMode(
            QtWidgets.QGraphicsView.ViewportUpdateMode.BoundingRectViewportUpdate
        )
        self.setScaleRange(0.3, 2)

        # Sets the scene rect to its maximum possible ranges to avoid autu scene range
        # re-calculation when expanding the all QGraphicsItems common rect.
        maxSize = 32767
        self.setSceneRect(-maxSize, -maxSize, (maxSize * 2), (maxSize * 2))

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        from SpatialNode.data_flow_graphics_scene import DataFlowGraphicsScene

        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            scene = self.scene()
            if isinstance(scene, DataFlowGraphicsScene):
                scene.loadUrl(urls[0].toLocalFile())

    def clearSelectionAction(self):
        return self._clearSelectionAction

    def deleteSelectionAction(self):
        return self._deleteSelectionAction

    def setScene(self, scene):
        super().setScene(scene)

        def setToolTip(action):
            action.setToolTip(f"{action.toolTip()} ({action.shortcut().toString()})")

        self._clearSelectionAction = QtGui.QAction("Clear Selection", self)
        self._clearSelectionAction.setShortcut(QtCore.Qt.Key.Key_Escape)
        self._clearSelectionAction.triggered.connect(scene.clearSelection)
        setToolTip(self._clearSelectionAction)
        self.addAction(self._clearSelectionAction)

        self._deleteSelectionAction = QtGui.QAction("Delete Selection", self)
        self._deleteSelectionAction.setShortcutContext(
            QtCore.Qt.ShortcutContext.WidgetShortcut
        )
        self._deleteSelectionAction.setShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Delete)
        )
        self._deleteSelectionAction.triggered.connect(self.onDeleteSelectedObjects)
        setToolTip(self._deleteSelectionAction)
        self.addAction(self._deleteSelectionAction)

        self._duplicateSelectionAction = QtGui.QAction("Duplicate Selection", self)
        self._duplicateSelectionAction.setShortcutContext(
            QtCore.Qt.ShortcutContext.WidgetShortcut
        )
        self._duplicateSelectionAction.setShortcut(
            QtGui.QKeySequence(QtCore.Qt.Modifier.CTRL | QtCore.Qt.Key.Key_D)
        )
        self._duplicateSelectionAction.triggered.connect(
            self.onDuplicateSelectedObjects
        )
        setToolTip(self._duplicateSelectionAction)
        self.addAction(self._duplicateSelectionAction)

        self._copySelectionAction = QtGui.QAction("Copy Selection", self)
        self._copySelectionAction.setShortcutContext(
            QtCore.Qt.ShortcutContext.WidgetShortcut
        )
        self._copySelectionAction.setShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Copy)
        )
        self._copySelectionAction.triggered.connect(self.onCopySelectedObjects)
        setToolTip(self._copySelectionAction)
        self.addAction(self._copySelectionAction)

        self._pasteAction = QtGui.QAction("Paste Selection", self)
        self._pasteAction.setShortcutContext(QtCore.Qt.ShortcutContext.WidgetShortcut)
        self._pasteAction.setShortcut(
            QtGui.QKeySequence(QtGui.QKeySequence.StandardKey.Paste)
        )
        self._pasteAction.triggered.connect(self.onPasteObjects)
        setToolTip(self._pasteAction)
        self.addAction(self._pasteAction)

        undoAction = scene.undoStack.createUndoAction(self, "&Undo")
        undoAction.setShortcuts(QtGui.QKeySequence.StandardKey.Undo)
        self.addAction(undoAction)

        redoAction = scene.undoStack.createRedoAction(self, "&Redo")
        redoAction.setShortcuts(QtGui.QKeySequence.StandardKey.Redo)
        self.addAction(redoAction)

    def centerScene(self):
        if self.scene() is not None:
            self.scene().setSceneRect(QtCore.QRectF())
            sceneRect = self.scene().sceneRect()

            if (
                sceneRect.width() > self.rect().width()
                or sceneRect.height() > self.rect().height()
            ):
                self.fitInView(sceneRect, QtCore.Qt.AspectRatioMode.KeepAspectRatio)

            self.centerOn(sceneRect.center())

    def setScaleRange(self, minimum: float = 0, maximum: float = 0):
        """max=0/min=0 indicates infinite zoom in/out"""
        if maximum < minimum:
            (minimum, maximum) = (maximum, minimum)
        minimum = max(0.0, minimum)
        maximum = max(0.0, maximum)

        self._scaleRange.minimum = minimum
        self._scaleRange.maximum = maximum

        self.setupScale(self.transform().m11())

    def getScale(self):
        return self.transform().m11()

    scaleChanged = QtCore.Signal(float)

    def scaleUp(self):
        step = 1.2
        factor = pow(step, 1.0)

        if self._scaleRange.maximum > 0:
            t = self.transform()
            t.scale(factor, factor)
            if t.m11() >= self._scaleRange.maximum:
                self.setupScale(t.m11())
                return

        self.scale(factor, factor)
        self.scaleChanged.emit(self.transform().m11())

    def scaleDown(self):
        step = 1.2
        factor = pow(step, -1.0)

        if self._scaleRange.minimum > 0:
            t = self.transform()
            t.scale(factor, factor)
            if t.m11() <= self._scaleRange.minimum:
                self.setupScale(t.m11())
                return

        self.scale(factor, factor)
        self.scaleChanged.emit(self.transform().m11())

    def setupScale(self, scale: float):
        scale = max(self._scaleRange.minimum, min(self._scaleRange.maximum, scale))

        if scale <= 0:
            return

        if scale == self.transform().m11():
            return

        matrix = QtGui.QTransform()
        matrix.scale(scale, scale)
        self.setTransform(matrix, False)

        self.scaleChanged.emit(scale)

    def onDeleteSelectedObjects(self):
        from SpatialNode.undo_commands import DeleteCommand

        self.nodeScene().undoStack.push(DeleteCommand(self.nodeScene()))

    def onDuplicateSelectedObjects(self):
        from SpatialNode.undo_commands import CopyCommand, PasteCommand

        pastePosition = self.scenePastePosition()

        self.nodeScene().undoStack.push(CopyCommand(self.nodeScene()))
        self.nodeScene().undoStack.push(PasteCommand(self.nodeScene(), pastePosition))

    def onCopySelectedObjects(self):
        from SpatialNode.undo_commands import CopyCommand

        self.nodeScene().undoStack.push(CopyCommand(self.nodeScene()))

    def onPasteObjects(self):
        from SpatialNode.undo_commands import PasteCommand

        pastePosition = self.scenePastePosition()
        self.nodeScene().undoStack.push(PasteCommand(self.nodeScene(), pastePosition))

    def contextMenuEvent(self, event):
        if self.itemAt(event.pos()):
            super().contextMenuEvent(event)
            return

        scenePos = self.mapToScene(event.pos())
        menu = self.nodeScene().createSceneMenu(scenePos)

        if menu is not None:
            menu.exec(event.globalPos())

    def wheelEvent(self, event):
        delta = event.angleDelta()

        if delta.y() == 0:
            event.ignore()
            return

        d = delta.y() / abs(delta.y())

        if d > 0.0:
            self.scaleUp()
        else:
            self.scaleDown()

    def keyPressEvent(self, event):
        match event.key():
            case QtCore.Qt.Key.Key_Shift:
                self.setDragMode(QtWidgets.QGraphicsView.DragMode.RubberBandDrag)

        super().keyPressEvent(event)

    def keyReleaseEvent(self, event):
        match event.key():
            case QtCore.Qt.Key.Key_Shift:
                self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        super().keyReleaseEvent(event)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._clickPos = self.mapToScene(event.pos())

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if (
            self.scene().mouseGrabberItem() is None
            and event.buttons() == QtCore.Qt.MouseButton.LeftButton
        ):
            # Make sure shift is not being pressed
            if (event.modifiers() & QtCore.Qt.KeyboardModifier.ShiftModifier) == 0:
                difference = self._clickPos - self.mapToScene(event.pos())
                self.setSceneRect(
                    self.sceneRect().translated(difference.x(), difference.y())
                )

    def drawBackground(self, painter, rect):
        from SpatialNode.style_collection import StyleCollection

        super().drawBackground(painter, rect)

        def drawGrid(gridStep):
            windowRect = self.rect()
            tl = self.mapToScene(windowRect.topLeft())
            br = self.mapToScene(windowRect.bottomRight())

            left = math.floor(tl.x() / gridStep - 0.5)
            right = math.floor(br.x() / gridStep + 1.0)
            bottom = math.floor(tl.y() / gridStep - 0.5)
            top = math.floor(br.y() / gridStep + 1.0)

            # vertical lines
            for xi in range(left, right + 1):
                line = QtCore.QLineF(
                    xi * gridStep, bottom * gridStep, xi * gridStep, top * gridStep
                )
                painter.drawLine(line)

            # horizontal lines
            for yi in range(bottom, top + 1):
                line = QtCore.QLineF(
                    left * gridStep, yi * gridStep, right * gridStep, yi * gridStep
                )
                painter.drawLine(line)

        flowViewStyle = StyleCollection.flowViewStyle()

        pfine = QtGui.QPen(flowViewStyle.FineGridColor, 1.0)
        painter.setPen(pfine)
        drawGrid(15)

        p = QtGui.QPen(flowViewStyle.CoarseGridColor, 1.0)
        painter.setPen(p)
        drawGrid(150)

    def showEvent(self, event):
        super().showEvent(event)
        self.centerScene()

    def nodeScene(self):
        return self.scene()

    # Computes scene position for pasting the copied/duplicated node groups.
    def scenePastePosition(self):
        origin = self.mapFromGlobal(QtGui.QCursor.pos())

        viewRect = self.rect()
        if not viewRect.contains(origin):
            origin = viewRect.center()

        return self.mapToScene(origin)
