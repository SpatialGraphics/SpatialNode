#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import sys

from PySide6 import QtWidgets, QtCore, QtGui

import SpatialNode as sNode
from examples.dynamic_ports.dynamic_ports_model import DynamicPortsModel


def initializeModel(graphModel: DynamicPortsModel):
    id1 = graphModel.addNode()
    graphModel.setNodeData(id1, sNode.NodeRole.Position, QtCore.QPointF(0, 0))
    graphModel.setNodeData(id1, sNode.NodeRole.InPortCount, 1)
    graphModel.setNodeData(id1, sNode.NodeRole.OutPortCount, 1)

    id2 = graphModel.addNode()
    graphModel.setNodeData(id2, sNode.NodeRole.Position, QtCore.QPointF(300, 300))

    graphModel.setNodeData(id2, sNode.NodeRole.InPortCount, 1)
    graphModel.setNodeData(id2, sNode.NodeRole.OutPortCount, 1)

    graphModel.addConnection(sNode.ConnectionId(id1, 0, id2, 0))


def createSaveRestoreMenu(
    graphModel: DynamicPortsModel,
    scene: sNode.BasicGraphicsScene,
    view: sNode.GraphicsView,
) -> QtWidgets.QMenuBar:
    menuBar = QtWidgets.QMenuBar()
    menu = menuBar.addMenu("File")
    saveAction = menu.addAction("Save Scene")
    loadAction = menu.addAction("Load Scene")

    def save():
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, "Open Flow Scene", QtCore.QDir.homePath(), "Flow Scene Files (*.flow)"
        )

        if len(fileName) > 0:
            if not fileName.endswith("flow"):
                fileName += ".flow"

                file = QtCore.QFile(fileName)
                if file.open(QtCore.QIODevice.OpenModeFlag.WriteOnly):
                    file.write(QtCore.QJsonDocument(graphModel.save()).toJson())

    saveAction.triggered.connect(save)

    def load():
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open Flow Scene", QtCore.QDir.homePath(), "Flow Scene Files (*.flow)"
        )
        if not QtCore.QFileInfo.exists(fileName):
            return

        file = QtCore.QFile(fileName)
        if not file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly):
            return

        scene.clearScene()
        wholeFile = file.readAll()
        graphModel.load(QtCore.QJsonDocument.fromJson(wholeFile).object())
        view.centerScene()

    loadAction.triggered.connect(load)
    return menuBar


def createNodeAction(
    graphModel: DynamicPortsModel, view: sNode.GraphicsView
) -> QtGui.QAction:
    action = QtGui.QAction("Create Node", view)

    def create():
        # Mouse position in scene coordinates.
        posView = view.mapToScene(view.mapFromGlobal(QtGui.QCursor.pos()))

        newId = graphModel.addNode()
        graphModel.setNodeData(newId, sNode.NodeRole.Position, posView)

    action.triggered.connect(create)
    return action


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    graphModel = DynamicPortsModel()

    # Initialize and connect two nodes.
    initializeModel(graphModel)

    # Main app window holding menu and a scene view.
    window = QtWidgets.QWidget()
    window.setWindowTitle("Dynamic Nodes Example")
    window.resize(800, 600)

    scene = sNode.BasicGraphicsScene(graphModel)

    view = sNode.GraphicsView(scene)
    # Setup context menu for creating new nodes.
    view.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)
    view.insertAction(view.actions()[0], createNodeAction(graphModel, view))

    # Pack all elements into layout.
    l = QtWidgets.QVBoxLayout(window)
    l.setContentsMargins(0, 0, 0, 0)
    l.setSpacing(0)
    l.addWidget(createSaveRestoreMenu(graphModel, scene, view))
    l.addWidget(view)

    # Center window
    window.move(
        QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        - view.rect().center()
    )
    window.showNormal()

    sys.exit(app.exec())
