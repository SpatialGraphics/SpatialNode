#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtWidgets

import SpatialNode as sNode
from examples.calculator.decimal_data import DecimalData


class NumberDisplayDataModel(sNode.NodeDelegateModel):
    def __init__(self):
        super().__init__()
        self._numberData: DecimalData | None = None
        self._label: QtWidgets.QLabel | None = None

    @override
    def caption(self):
        return "Result"

    @override
    def captionVisible(self):
        return False

    @staticmethod
    @override
    def register(registry: sNode.NodeDelegateModelRegistry, *args, **kwargs):
        registry.registerModel(
            NumberDisplayDataModel, NumberDisplayDataModel.__name__, "Displays"
        )

    @override
    def nPorts(self, portType):
        result = 1

        match portType:
            case sNode.PortType.In:
                result = 1
            case sNode.PortType.Out:
                result = 0

        return result

    @override
    def dataType(self, portType, portIndex):
        return DecimalData().type()

    @override
    def outData(self, port):
        return None

    @override
    def setInData(self, nodeData, portIndex):
        self._numberData = nodeData

        if not self._label:
            return

        if self._numberData:
            if isinstance(self._numberData, DecimalData):
                self._label.setText(self._numberData.numberAsText())
        else:
            self._label.clear()

        self._label.adjustSize()

    @override
    def embeddedWidget(self):
        if not self._label:
            self._label = QtWidgets.QLabel()
            self._label.setMargin(3)

        return self._label

    def number(self) -> float:
        if self._numberData:
            return self._numberData.number()

        return 0.0
