#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import sys

from PySide6 import QtWidgets, QtCore, QtGui

import SpatialNode as sNode
from examples.simple_graph_model.simple_graph_model import SimpleGraphModel

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    graphModel = SimpleGraphModel()

    # Initialize and connect two nodes.

    id1 = graphModel.addNode()
    graphModel.setNodeData(id1, sNode.NodeRole.Position, QtCore.QPointF(0, 0))
    id2 = graphModel.addNode()
    graphModel.setNodeData(id2, sNode.NodeRole.Position, QtCore.QPointF(300, 300))
    graphModel.addConnection(sNode.ConnectionId(id1, 0, id2, 0))

    scene = sNode.BasicGraphicsScene(graphModel)
    view = sNode.GraphicsView(scene)

    # Setup context menu for creating new nodes.
    view.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.ActionsContextMenu)
    createNodeAction = QtGui.QAction("Create Node", view)

    def triggered():
        # Mouse position in scene coordinates.
        posView = view.mapToScene(view.mapFromGlobal(QtGui.QCursor.pos()))
        newId = graphModel.addNode()
        graphModel.setNodeData(newId, sNode.NodeRole.Position, posView)

    createNodeAction.triggered.connect(triggered)

    view.insertAction(view.actions()[0], createNodeAction)
    view.setWindowTitle("Simple Node Graph")
    view.resize(800, 600)
    view.move(
        QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        - view.rect().center()
    )
    view.showNormal()

    sys.exit(app.exec())
