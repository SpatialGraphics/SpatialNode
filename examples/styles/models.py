#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

import SpatialNode as sNode


class MyNodeData(sNode.NodeData):
    @override
    def type(self):
        return sNode.NodeDataType("MyNodeData", "My Node Data")


class MyDataModel(sNode.NodeDelegateModel):
    @override
    def caption(self):
        return "My Data Model"

    @staticmethod
    @override
    def register(registry: sNode.NodeDelegateModelRegistry, *args, **kwargs):
        registry.registerModel(MyDataModel, MyDataModel.__name__)

    @override
    def save(self):
        modelJson = sNode.QJsonObject()
        modelJson["name"] = type(self).__name__
        return modelJson

    @override
    def nPorts(self, portType):
        return 3

    @override
    def dataType(self, portType, portIndex):
        return MyNodeData().type()

    @override
    def outData(self, port):
        return MyNodeData()

    @override
    def setInData(self, nodeData, portIndex): ...

    @override
    def embeddedWidget(self):
        return None
