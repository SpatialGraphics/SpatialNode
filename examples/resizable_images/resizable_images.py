#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import sys

from PySide6 import QtWidgets

import SpatialNode as sNode
from examples.resizable_images.image_loader_model import ImageLoaderModel
from examples.resizable_images.image_show_model import ImageShowModel


def registerDataModels():
    ret = sNode.NodeDelegateModelRegistry()
    ImageShowModel.register(ret)
    ImageLoaderModel.register(ret)
    return ret


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    registry = registerDataModels()

    dataFlowGraphModel = sNode.DataFlowGraphModel(registry)

    scene = sNode.DataFlowGraphicsScene(dataFlowGraphModel)

    view = sNode.GraphicsView(scene)

    view.setWindowTitle("Data Flow: Resizable Images")
    view.resize(800, 600)
    view.move(
        QtWidgets.QApplication.primaryScreen().availableGeometry().center()
        - view.rect().center()
    )
    view.show()

    sys.exit(app.exec())
