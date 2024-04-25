#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

import SpatialNode as sNode
from examples.calculator.decimal_data import DecimalData
from examples.calculator.math_operation_data_model import MathOperationDataModel


class SubtractionModel(MathOperationDataModel):
    @override
    def caption(self):
        return "Subtraction"

    @override
    def portCaptionVisible(self, portType, portIndex):
        return True

    @override
    def portCaption(self, portType, portIndex):
        match portType:
            case sNode.PortType.In:
                if portIndex == 0:
                    return "Minuend"
                elif portIndex == 1:
                    return "Subtrahend"
            case sNode.PortType.Out:
                return "Result"

    @staticmethod
    @override
    def register(registry: sNode.NodeDelegateModelRegistry, *args, **kwargs):
        registry.registerModel(SubtractionModel, SubtractionModel.__name__, "Operators")

    @override
    def compute(self):
        outPortIndex = 0
        n1 = self._number1
        n2 = self._number2

        if n1 and n2:
            self._result = DecimalData(n1.number() - n2.number())
        else:
            self._result = None

        self.dataUpdated.emit(outPortIndex)
