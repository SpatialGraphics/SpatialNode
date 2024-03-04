#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from abc import abstractmethod
from typing import override

import SpatialNode as sNode
from examples.calculator.decimal_data import DecimalData


class MathOperationDataModel(sNode.NodeDelegateModel):
    def __init__(self):
        super().__init__()
        self._number1: DecimalData | None = None
        self._number2: DecimalData | None = None
        self._result: DecimalData | None = None

    @override
    def nPorts(self, portType):
        if portType == sNode.PortType.In:
            result = 2
        else:
            result = 1

        return result

    @override
    def dataType(self, portType, portIndex):
        return DecimalData().type()

    @override
    def outData(self, port):
        return self._result

    @override
    def setInData(self, nodeData, portIndex):
        if not nodeData:
            self.dataInvalidated.emit(0)

        if portIndex == 0:
            self._number1 = nodeData
        else:
            self._number2 = nodeData

        self.compute()

    @override
    def embeddedWidget(self):
        return None

    @abstractmethod
    def compute(self): ...
