#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import sys

from PySide6 import QtWidgets
import SpatialNode as sNode

from examples.styles.models import MyDataModel


def registerDataModels():
    ret = sNode.NodeDelegateModelRegistry()
    MyDataModel.register(ret)
    return ret


def setStyle():
    sNode.GraphicsViewStyle.setStyle(
        """
  {
    "GraphicsViewStyle": {
      "BackgroundColor": [255, 255, 240],
      "FineGridColor": [245, 245, 230],
      "CoarseGridColor": [235, 235, 220]
    }
  }
      """
    )

    sNode.NodeStyle.setNodeStyle(
        """
  {
    "NodeStyle": {
      "NormalBoundaryColor": "darkgray",
      "SelectedBoundaryColor": "deepskyblue",
      "GradientColor0": "mintcream",
      "GradientColor1": "mintcream",
      "GradientColor2": "mintcream",
      "GradientColor3": "mintcream",
      "ShadowColor": [200, 200, 200],
      "FontColor": [10, 10, 10],
      "FontColorFaded": [100, 100, 100],
      "ConnectionPointColor": "white",
      "PenWidth": 2.0,
      "HoveredPenWidth": 2.5,
      "ConnectionPointDiameter": 10.0,
      "Opacity": 1.0
    }
  }
        """
    )

    sNode.ConnectionStyle.setConnectionStyle(
        """
  {
    "ConnectionStyle": {
      "ConstructionColor": "gray",
      "NormalColor": "black",
      "SelectedColor": "gray",
      "SelectedHaloColor": "deepskyblue",
      "HoveredColor": "deepskyblue",

      "LineWidth": 3.0,
      "ConstructionLineWidth": 2.0,
      "PointDiameter": 10.0,

      "UseDataDefinedColors": false
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

    view.setWindowTitle("Style example")
    view.resize(800, 600)
    view.show()

    sys.exit(app.exec())
