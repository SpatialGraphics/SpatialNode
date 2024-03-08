#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

import SpatialNode as sNode


class SimpleNodeData(sNode.NodeData):
    @override
    def type(self):
        return sNode.NodeDataType("SimpleDataModel", "Simple Data")


class SimpleDataModel(sNode.NodeDelegateModel):
    @override
    def caption(self):
        return "Simple Data Model"

    @staticmethod
    @override
    def register(registry: sNode.NodeDelegateModelRegistry, *args, **kwargs):
        registry.registerModel(SimpleDataModel, SimpleDataModel.__name__)

    @override
    def nPorts(self, portType):
        return 2

    @override
    def dataType(self, portType, portIndex):
        return SimpleNodeData().type()

    @override
    def outData(self, port):
        return SimpleNodeData()

    @override
    def setInData(self, nodeData, portIndex): ...

    @override
    def embeddedWidget(self):
        return None
