#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import sys

from PySide6 import QtWidgets

import SpatialNode as sNode
from examples.calculator.addition_model import AdditionModel
from examples.calculator.division_model import DivisionModel
from examples.calculator.multiplication_model import MultiplicationModel
from examples.calculator.number_display_data_model import NumberDisplayDataModel
from examples.calculator.number_source_data_model import NumberSourceDataModel
from examples.calculator.subtraction_model import SubtractionModel


def registerDataModels():
    registry = sNode.NodeDelegateModelRegistry()
    registry.registerModel(NumberSourceDataModel, "Sources")
    registry.registerModel(NumberDisplayDataModel, "Displays")
    registry.registerModel(AdditionModel, "Operators")
    registry.registerModel(SubtractionModel, "Operators")
    registry.registerModel(MultiplicationModel, "Operators")
    registry.registerModel(DivisionModel, "Operators")

    return registry


def setStyle():
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
        
              "UseDataDefinedColors": true
            }
          }
        """
    )


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    setStyle()

    registry = registerDataModels()
    mainWidget = QtWidgets.QWidget()

    menuBar = QtWidgets.QMenuBar()
    menu = menuBar.addMenu("File")
    saveAction = menu.addAction("Save Scene")
    loadAction = menu.addAction("Load Scene")
    l = QtWidgets.QVBoxLayout(mainWidget)

    dataFlowGraphModel = sNode.DataFlowGraphModel(registry)

    l.addWidget(menuBar)
    scene = sNode.DataFlowGraphicsScene(dataFlowGraphModel, mainWidget)

    view = sNode.GraphicsView(scene)
    l.addWidget(view)
    l.setContentsMargins(0, 0, 0, 0)
    l.setSpacing(0)

    saveAction.triggered.connect(scene.save)
    loadAction.triggered.connect(scene.load)
    scene.sceneLoaded.connect(view.centerScene)

    mainWidget.setWindowTitle("calculator")
    mainWidget.showNormal()
    sys.exit(app.exec())
