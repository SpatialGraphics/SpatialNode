#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtWidgets, QtGui, QtCore

import SpatialNode as sNode
from examples.resizable_images.pixmap_data import PixmapData


class ImageLoaderModel(sNode.NodeDelegateModel):
    def __init__(self):
        super().__init__()

        self._pixmap = QtGui.QPixmap()
        self._label = QtWidgets.QLabel("Double click to load image")
        self._label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignHCenter
        )

        f = self._label.font()
        f.setBold(True)
        f.setItalic(True)

        self._label.setFont(f)

        self._label.setMinimumSize(200, 200)
        self._label.setMaximumSize(500, 300)

        self._label.installEventFilter(self)

    @override
    def caption(self):
        return "Image Source"

    @staticmethod
    @override
    def name():
        return "ImageLoaderModel"

    @staticmethod
    @override
    def register(registry: sNode.NodeDelegateModelRegistry, *args, **kwargs):
        registry.registerModel(ImageLoaderModel, ImageLoaderModel.name())

    def modelName(self):
        return "Source Image"

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
        return PixmapData(None).type()

    @override
    def outData(self, port):
        return PixmapData(self._pixmap)

    @override
    def setInData(self, nodeData, portIndex): ...

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

            if event.type() == QtCore.QEvent.Type.MouseButtonPress:
                fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
                    None,
                    "Open Image",
                    QtCore.QDir.homePath(),
                    "Image Files (*.png *.jpg *.bmp)",
                )
                self._pixmap = QtGui.QPixmap(fileName)
                self._label.setPixmap(
                    self._pixmap.scaled(w, h, QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                )
                self.dataUpdated.emit(0)

                return True
            elif event.type() == QtCore.QEvent.Type.Resize:
                if self._pixmap:
                    self._label.setPixmap(
                        self._pixmap.scaled(
                            w, h, QtCore.Qt.AspectRatioMode.KeepAspectRatio
                        )
                    )

        return False
