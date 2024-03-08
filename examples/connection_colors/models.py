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


class SimpleNodeData(sNode.NodeData):
    @override
    def type(self):
        return sNode.NodeDataType("SimpleData", "Simple Data")


class NaiveDataModel(sNode.NodeDelegateModel):
    @override
    def caption(self):
        return "Naive Data Model"

    @staticmethod
    @override
    def register(registry: sNode.NodeDelegateModelRegistry, *args, **kwargs):
        registry.registerModel(NaiveDataModel, NaiveDataModel.__name__)

    @override
    def nPorts(self, portType):
        result = 1
        match portType:
            case sNode.PortType.In:
                result = 2
            case sNode.PortType.Out:
                result = 2
        return result

    @override
    def dataType(self, portType, portIndex):
        match portType:
            case sNode.PortType.In:
                match portIndex:
                    case 0:
                        return MyNodeData().type()
                    case 1:
                        return SimpleNodeData().type()
            case sNode.PortType.Out:
                match portIndex:
                    case 0:
                        return MyNodeData().type()
                    case 1:
                        return SimpleNodeData().type()

    @override
    def outData(self, port): ...

    @override
    def setInData(self, nodeData, portIndex): ...

    @override
    def embeddedWidget(self):
        return None
