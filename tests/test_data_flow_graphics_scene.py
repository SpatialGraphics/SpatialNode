from PySide6 import QtWidgets

from SpatialNode.data_flow_graph_model import DataFlowGraphModel
from SpatialNode.data_flow_graphics_scene import DataFlowGraphicsScene
from SpatialNode.node_delegate_model_registry import NodeDelegateModelRegistry


def test_create():
    QtWidgets.QApplication()

    registry = NodeDelegateModelRegistry()
    model = DataFlowGraphModel(registry)
    scene = DataFlowGraphicsScene(model)
    assert True
