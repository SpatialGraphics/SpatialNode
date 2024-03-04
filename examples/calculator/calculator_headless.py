#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtCore

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


# This scene JSON was saved by the normal `calculator` example.
# It has one source number node connected to both inputs of an addition node,
# the result is rendered in a displayer node.
#
#                          ____________
#                     /  O[            ]
#    _____________  /     [  addition  ]          ______________
#   [ source node ]O      [    node    ]O- - - -O[ display node ]
#    -------------  \     [            ]          --------------
#                     \  O[____________]
addingNumbersScene = """

    {
        "nodes": [
            {
                "id": 0,
                "internal-data": {
                    "model-name": "NumberSource",
                    "number": "3"
                },
                "position": {
                    "x": -338,
                    "y": -160
                }
            },
            {
                "id": 1,
                "internal-data": {
                    "model-name": "Addition"
                },
                "position": {
                    "x": -31,
                    "y": -264
                }
            },
            {
                "id": 2,
                "internal-data": {
                    "model-name": "Result"
                },
                "position": {
                    "x": 201,
                    "y": -129
                }
            }
        ],
        "connections": [
            {
                "inPortIndex": 0,
                "intNodeId": 2,
                "outNodeId": 1,
                "outPortIndex": 0
            },
            {
                "inPortIndex": 1,
                "intNodeId": 1,
                "outNodeId": 0,
                "outPortIndex": 0
            },
            {
                "inPortIndex": 0,
                "intNodeId": 1,
                "outNodeId": 0,
                "outPortIndex": 0
            }
        ]
    }
"""

if __name__ == "__main__":
    registry = registerDataModels()

    # Here we create a graph model without attaching to any view or scene.
    dataFlowGraphModel = sNode.DataFlowGraphModel(registry)

    # Alternatively you can create the graph by yourself with the functions
    # `DataFlowGraphModel::addNode` and `DataFlowGraphModel::addConnection` and
    # use the obtained `NodeId` to fetch the `NodeDelegateModel`s
    sceneJson = QtCore.QJsonDocument.fromJson(
        QtCore.QByteArray.fromStdString(addingNumbersScene)
    )

    dataFlowGraphModel.load(sceneJson.object())

    print("Data Flow graph was created from a json-serialized graph")

    nodeSource = 0
    nodeResult = 2

    print("========================================")
    print(f"Entering the number {33.3} to the input node")
    dataFlowGraphModel.delegateModel(nodeSource).setNumber(33.3)

    print(
        f"Result of the addiion operation: {dataFlowGraphModel.delegateModel(nodeResult).number()}"
    )

    print(f"========================================")
    print(f"Entering the number {-5.} to the input node")
    dataFlowGraphModel.delegateModel(nodeSource).setNumber(-5)

    print(
        f"Result of the addiion operation: {dataFlowGraphModel.delegateModel(nodeResult).number()}"
    )
