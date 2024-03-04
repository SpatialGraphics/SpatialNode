#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

import SpatialNode as sNode
from examples.calculator.decimal_data import DecimalData
from examples.calculator.math_operation_data_model import MathOperationDataModel


class DivisionModel(MathOperationDataModel):
    def __init__(self):
        super().__init__()

    @override
    def caption(self):
        return "Division"

    @override
    def portCaptionVisible(self, portType, portIndex):
        return True

    @override
    def portCaption(self, portType, portIndex):
        match portType:
            case sNode.PortType.In:
                if portIndex == 0:
                    return "Dividend"
                elif portIndex == 1:
                    return "Divisor"
            case sNode.PortType.Out:
                "Result"

    @override
    def name(self):
        return "Division"

    @override
    def compute(self):
        outPortIndex = 0

        n1 = self._number1
        n2 = self._number2

        if n2 and n2.number() == 0.0:
            self._result = None
        elif n1 and n2:
            self._result = DecimalData(n1.number() / n2.number())
        else:
            self._result = None

        self.dataUpdated.emit(outPortIndex)
