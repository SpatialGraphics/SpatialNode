#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import sys

from PySide6 import QtWidgets, QtCore

import SpatialNode as sNode
from examples.lock_nodes_and_connections.data_flow_model import DataFlowModel
from examples.lock_nodes_and_connections.delegate_node_model import (
    SimpleDataModel,
    SimpleNodeData,
)


def registerDataModels():
    ret = sNode.NodeDelegateModelRegistry()
    ret.registerModel(SimpleDataModel)
    return ret


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    graphModel = DataFlowModel(registerDataModels())

    # Initialize and connect two nodes.
    id1 = graphModel.addNode(SimpleNodeData().type().id)
    graphModel.setNodeData(id1, sNode.NodeRole.Position, QtCore.QPointF(0, 0))

    id2 = graphModel.addNode(SimpleNodeData().type().id)
    graphModel.setNodeData(id2, sNode.NodeRole.Position, QtCore.QPointF(300, 300))

    graphModel.addConnection(sNode.ConnectionId(id1, 0, id2, 0))

    scene = sNode.DataFlowGraphicsScene(graphModel)

    window = QtWidgets.QWidget()
    l = QtWidgets.QHBoxLayout(window)

    view = sNode.GraphicsView(scene)

    l.addWidget(view)

    groupBox = QtWidgets.QGroupBox("Options")

    cb1 = QtWidgets.QCheckBox("Nodes are locked")
    cb2 = QtWidgets.QCheckBox("Connections detachable")
    cb2.setChecked(True)

    vbl = QtWidgets.QVBoxLayout()
    vbl.addWidget(cb1)
    vbl.addWidget(cb2)
    vbl.addStretch()
    groupBox.setLayout(vbl)

    cb1.stateChanged.connect(
        lambda state: graphModel.setNodesLocked(
            state == QtCore.Qt.CheckState.Checked.value
        )
    )
    cb2.stateChanged.connect(
        lambda state: graphModel.setDetachPossible(
            state == QtCore.Qt.CheckState.Checked.value
        )
    )

    l.addWidget(groupBox)

    window.setWindowTitle("Locked Nodes and Connections")
    window.resize(800, 600)

    # Center window.
    window.move(
        QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        - view.rect().center()
    )
    window.showNormal()

    sys.exit(app.exec())
