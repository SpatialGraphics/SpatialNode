#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtCore, QtWidgets

from SpatialNode.basic_graphics_scene import BasicGraphicsScene
from SpatialNode.data_flow_graph_model import DataFlowGraphModel
from SpatialNode.definitions import NodeId

class DataFlowGraphicsScene(BasicGraphicsScene):
    def __init__(self, graphModel: DataFlowGraphModel, parent=None): ...
    def selectedNodes(self) -> list[NodeId]: ...
    def createSceneMenu(self, scenePos: QtCore.QPointF) -> QtWidgets.QMenu: ...

    sceneLoaded: QtCore.Signal = None

    def save(self) -> None: ...
    def load(self) -> None: ...
    def loadUrl(self, fileName: str) -> None: ...
