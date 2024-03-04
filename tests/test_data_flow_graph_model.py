from SpatialNode.data_flow_graph_model import DataFlowGraphModel
from SpatialNode.node_delegate_model_registry import NodeDelegateModelRegistry


def test_create():
    registry = NodeDelegateModelRegistry()
    model = DataFlowGraphModel(registry)
    assert True


def test_data_model_registry():
    registry = NodeDelegateModelRegistry()
    model = DataFlowGraphModel(registry)
    assert True
