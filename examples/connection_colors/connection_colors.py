#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import SpatialNode as sNode
from examples.connection_colors.models import NaiveDataModel
import sys

from PySide6 import QtWidgets


def registerDataModels():
    ret = sNode.NodeDelegateModelRegistry()
    ret.registerModel(NaiveDataModel)
    return ret


def setStyle():
    sNode.ConnectionStyle.setConnectionStyle(
        """
          {
            "ConnectionStyle": {
              "UseDataDefinedColors": true
            }
          }
        """
    )


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    setStyle()

    registry = registerDataModels()
    dataFlowGraphModel = sNode.DataFlowGraphModel(registry)
    scene = sNode.DataFlowGraphicsScene(dataFlowGraphModel)
    view = sNode.GraphicsView(scene)

    view.setWindowTitle("Node-based flow editor")
    view.show()
    sys.exit(app.exec())
