#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtWidgets

import SpatialNode as sNode
from examples.text.text_data import TextData


class TextSourceDataModel(sNode.NodeDelegateModel):
    def __init__(self):
        super().__init__()
        self._lineEdit: QtWidgets.QLineEdit | None = None

    @override
    def caption(self):
        return "Text Source"

    @override
    def captionVisible(self):
        return False

    @staticmethod
    @override
    def register(registry: sNode.NodeDelegateModelRegistry, *args, **kwargs):
        registry.registerModel(TextSourceDataModel, TextSourceDataModel.__name__)

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
        return TextData().type()

    @override
    def outData(self, port):
        return TextData(self._lineEdit.text())

    @override
    def setInData(self, nodeData, portIndex): ...

    @override
    def embeddedWidget(self):
        if not self._lineEdit:
            self._lineEdit = QtWidgets.QLineEdit("Default Text")
            self._lineEdit.textEdited.connect(self.onTextEdited)
        return self._lineEdit

    def onTextEdited(self, string: str):
        self.dataUpdated.emit(0)
