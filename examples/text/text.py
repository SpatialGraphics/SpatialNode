#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import sys

from PySide6 import QtWidgets

import SpatialNode as sNode
from examples.text.text_display_data_model import TextDisplayDataModel
from examples.text.text_source_data_model import TextSourceDataModel


def registerDataModels():
    ret = sNode.NodeDelegateModelRegistry()
    TextSourceDataModel.register(ret)
    TextDisplayDataModel.register(ret)
    return ret


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    registry = registerDataModels()
    dataFlowGraphModel = sNode.DataFlowGraphModel(registry)
    scene = sNode.DataFlowGraphicsScene(dataFlowGraphModel)
    view = sNode.GraphicsView(scene)

    view.setWindowTitle("Node-based flow editor")
    view.resize(800, 600)
    view.show()

    sys.exit(app.exec())
