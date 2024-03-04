#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import sys

from PySide6 import QtWidgets, QtCore, QtGui
import SpatialNode as sNode
from examples.vertical_layout.simple_graph_model import SimpleGraphModel

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

    scene.orientation = QtCore.Qt.Orientation.Vertical

    window = QtWidgets.QWidget()

    l = QtWidgets.QHBoxLayout(window)
    view = sNode.GraphicsView(scene)
    l.addWidget(view)

    groupBox = QtWidgets.QGroupBox("Orientation")
    radio1 = QtWidgets.QRadioButton("Vertical")
    radio2 = QtWidgets.QRadioButton("Horizontal")
    vbl = QtWidgets.QVBoxLayout()
    vbl.addWidget(radio1)
    vbl.addWidget(radio2)
    vbl.addStretch()
    groupBox.setLayout(vbl)

    def vertical():
        scene.orientation = QtCore.Qt.Orientation.Vertical

    radio1.clicked.connect(vertical)

    def horizontal():
        scene.orientation = QtCore.Qt.Orientation.Horizontal

    radio2.clicked.connect(horizontal)
    radio1.setChecked(True)
    l.addWidget(groupBox)

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

    window.setWindowTitle("Graph Orientation Demo")
    window.resize(800, 600)

    # Center window.
    window.move(
        QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        - view.rect().center()
    )
    window.showNormal()

    sys.exit(app.exec())
