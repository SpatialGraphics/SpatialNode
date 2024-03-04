#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtWidgets, QtCore

import SpatialNode as sNode
from examples.dynamic_ports.dynamic_ports_model import DynamicPortsModel

class PortAddRemoveWidget(QtWidgets.QWidget):
    def __init__(
        self,
        nInPorts: int,
        nOutPorts: int,
        nodeId: sNode.NodeId,
        model: DynamicPortsModel,
        parent=None,
    ):
        super().__init__(parent)
        self._nodeId: sNode.NodeId = None
        self._model: DynamicPortsModel = None
        self._left: QtWidgets.QVBoxLayout = None
        self._right: QtWidgets.QVBoxLayout = None

    def populateButtons(self, portType: sNode.PortType, nPorts: int): ...
    def addButtonGroupToLayout(
        self, vbl: QtWidgets.QVBoxLayout, portIndex: int
    ) -> QtWidgets.QHBoxLayout: ...
    def removeButtonGroupFromLayout(
        self, vbl: QtWidgets.QVBoxLayout, portIndex: int
    ): ...
    def onPlusClicked(self): ...
    def onMinusClicked(self): ...
    def findWhichPortWasClicked(
        self, sender: QtCore.QObject, buttonIndex: int
    ) -> tuple[sNode.PortType, sNode.PortIndex]: ...
