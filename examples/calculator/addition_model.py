#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

import SpatialNode as sNode
from examples.calculator.decimal_data import DecimalData
from examples.calculator.math_operation_data_model import MathOperationDataModel


class AdditionModel(MathOperationDataModel):
    @override
    def caption(self):
        return "Addition"

    @staticmethod
    @override
    def name():
        return "Addition"

    @staticmethod
    @override
    def register(registry: sNode.NodeDelegateModelRegistry, *args, **kwargs):
        registry.registerModel(AdditionModel, AdditionModel.name(), "Operators")

    @override
    def compute(self):
        outPortIndex: sNode.PortIndex = 0

        n1 = self._number1
        n2 = self._number2

        if n1 and n2:
            self._result = DecimalData(n1.number() + n2.number())
        else:
            self._result = None

        self.dataUpdated.emit(outPortIndex)
