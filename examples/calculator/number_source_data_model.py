#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtWidgets, QtGui, QtCore

import SpatialNode as sNode
from examples.calculator.decimal_data import DecimalData


class NumberSourceDataModel(sNode.NodeDelegateModel):
    def __init__(self):
        super().__init__()
        self._number: DecimalData | None = DecimalData(0.0)
        self._lineEdit: QtWidgets.QLineEdit | None = None

    @override
    def caption(self):
        return "Number Source"

    @override
    def captionVisible(self):
        return False

    @override
    def name(self):
        return "NumberSource"

    @override
    def save(self):
        modelJson = super().save()
        modelJson["number"] = QtCore.QJsonValue(self._number.number())

        return modelJson

    @override
    def load(self, p):
        v = p["number"]

        if v:
            strNum = v
            d = float(strNum)
            if d:
                self._number = DecimalData(d)

                if self._lineEdit:
                    self._lineEdit.setText(str(strNum))

    @override
    def nPorts(self, portType):
        result = 1

        match portType:
            case sNode.PortType.In:
                result = 0
            case sNode.PortType.Out:
                result = 1

        return result

    @override
    def dataType(self, portType, portIndex):
        return DecimalData().type()

    @override
    def outData(self, port):
        return self._number

    @override
    def setInData(self, nodeData, portIndex): ...

    @override
    def embeddedWidget(self):
        if not self._lineEdit:
            self._lineEdit = QtWidgets.QLineEdit()

            self._lineEdit.setValidator(QtGui.QDoubleValidator())
            self._lineEdit.setMaximumSize(self._lineEdit.sizeHint())
            self._lineEdit.textChanged.connect(self.onTextEdited)

            self._lineEdit.setText(str(self._number.number()))

        return self._lineEdit

    def setNumber(self, number: float):
        self._number = DecimalData(number)
        self.dataUpdated.emit(0)

        if self._lineEdit:
            self._lineEdit.setText(str(self._number.number()))

    def onTextEdited(self, string: str) -> None:
        try:
            number = float(string)
            self._number = DecimalData(number)
            self.dataUpdated.emit(0)
        except ValueError:
            self.dataInvalidated.emit(0)
