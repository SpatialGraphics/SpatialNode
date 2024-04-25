#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from abc import ABC, abstractmethod
from typing import override

from PySide6 import QtCore

from SpatialNode.definitions import QJsonObject
from SpatialNode.serializable import Serializable


class NodeDelegateModel(QtCore.QObject, Serializable):
    def __init__(self):
        from SpatialNode.node_style import NodeStyle

        super().__init__()
        self._nodeStyle = NodeStyle()

    def captionVisible(self):
        return True

    def caption(self):
        return "NodeDelegateModel"

    def portCaptionVisible(self, port_type, port_index):
        return False

    def portCaption(self, port_type, port_index):
        return ""

    @staticmethod
    def register(registry, *args, **kwargs): ...

    @override
    def save(self):
        modelJson = QJsonObject()
        modelJson["model-name"] = type(self).__name__
        return modelJson

    @override
    def load(self, p): ...

    @abstractmethod
    def nPorts(self, portType): ...

    @abstractmethod
    def dataType(self, portType, portIndex): ...

    def portConnectionPolicy(self, port_type, port_index):
        from SpatialNode.definitions import ConnectionPolicy, PortType

        result = ConnectionPolicy.One
        match port_type:
            case PortType.In:
                result = ConnectionPolicy.One
            case PortType.Out:
                result = ConnectionPolicy.Many

        return result

    @property
    def nodeStyle(self):
        return self._nodeStyle

    @nodeStyle.setter
    def nodeStyle(self, style):
        self._nodeStyle = style

    @abstractmethod
    def setInData(self, nodeData, portIndex): ...

    @abstractmethod
    def outData(self, port): ...

    @abstractmethod
    def embeddedWidget(self): ...

    def resizable(self):
        return False

    from SpatialNode.definitions import PortIndex, PortType

    dataUpdated = QtCore.Signal(PortIndex)
    """Triggers the updates in the nodes downstream."""

    dataInvalidated = QtCore.Signal(PortIndex)
    """Triggers the propagation of the empty data downstream."""

    computingStarted = QtCore.Signal()

    computingFinished = QtCore.Signal()

    embeddedWidgetSizeUpdated = QtCore.Signal()

    portsAboutToBeDeleted = QtCore.Signal(PortType, PortIndex, PortIndex)

    portsDeleted = QtCore.Signal()

    portsAboutToBeInserted = QtCore.Signal(PortType, PortIndex, PortIndex)

    portsInserted = QtCore.Signal()

    def inputConnectionCreated(self, connection_id): ...

    def inputConnectionDeleted(self, connection_id): ...

    def outputConnectionCreated(self, connection_id): ...

    def outputConnectionDeleted(self, connection_id): ...
