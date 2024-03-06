#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtWidgets, QtCore, QtGui

import SpatialNode as sNode
from examples.resizable_images.pixmap_data import PixmapData


class ImageShowModel(sNode.NodeDelegateModel):
    def __init__(self):
        super().__init__()
        self._label = QtWidgets.QLabel("Image will appear here")
        self._label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        f = self._label.font()
        f.setBold(True)
        f.setItalic(True)

        self._label.setFont(f)
        self._label.setMinimumSize(200, 200)
        self._label.installEventFilter(self)

        self._nodeData: sNode.NodeData | None = None

    @override
    def caption(self):
        return "Image Display"

    @staticmethod
    @override
    def name():
        return "ImageShowModel"

    @staticmethod
    @override
    def register(registry: sNode.NodeDelegateModelRegistry, *args, **kwargs):
        registry.registerModel(ImageShowModel, ImageShowModel.name())

    def modelName(self):
        return "Resulting Image"

    @override
    def nPorts(self, portType):
        result = 1
        match portType:
            case sNode.PortType.In:
                result = 1
            case sNode.PortType.Out:
                result = 1
        return result

    @override
    def dataType(self, portType, portIndex):
        return PixmapData(None).type()

    @override
    def outData(self, port):
        return self._nodeData

    @override
    def setInData(self, nodeData, portIndex):
        self._nodeData = nodeData

        if self._nodeData:
            if isinstance(self._nodeData, PixmapData):
                w = self._label.width()
                h = self._label.height()
                self._label.setPixmap(
                    self._nodeData.pixmap().scaled(
                        w, h, QtCore.Qt.AspectRatioMode.KeepAspectRatio
                    )
                )
        else:
            self._label.setPixmap(QtGui.QPixmap())

        self.dataUpdated.emit(0)

    @override
    def embeddedWidget(self):
        return self._label

    @override
    def resizable(self):
        return True

    @override
    def eventFilter(self, object, event):
        if object == self._label:
            w = self._label.width()
            h = self._label.height()

            if event.type() == QtCore.QEvent.Type.Resize:
                d = self._nodeData
                if isinstance(d, PixmapData):
                    self._label.setPixmap(
                        d.pixmap().scaled(
                            w, h, QtCore.Qt.AspectRatioMode.KeepAspectRatio
                        )
                    )
        return False
