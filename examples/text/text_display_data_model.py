#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtWidgets

import SpatialNode as sNode
from examples.text.text_data import TextData


class TextDisplayDataModel(sNode.NodeDelegateModel):
    def __init__(self):
        super().__init__()
        self._inputText = ""
        self._label = QtWidgets.QLabel("Resulting Text")
        self._label.setMargin(3)

    @override
    def caption(self):
        return "Text Display"

    @override
    def captionVisible(self):
        return False

    @override
    def name(self):
        return "TextDisplayDataModel"

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
        return TextData().type()

    @override
    def outData(self, port):
        return None

    @override
    def setInData(self, nodeData, portIndex):
        if isinstance(nodeData, TextData):
            self._inputText = nodeData.text()
        else:
            self._inputText = ""

        self._label.setText(self._inputText)
        self._label.adjustSize()

    @override
    def embeddedWidget(self):
        return self._label
