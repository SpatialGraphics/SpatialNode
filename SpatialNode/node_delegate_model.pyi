#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from abc import ABC, abstractmethod
from typing import override

from PySide6 import QtCore, QtWidgets

from SpatialNode.definitions import PortType, PortIndex, ConnectionId, ConnectionPolicy
from SpatialNode.node_data import NodeData, NodeDataType
from SpatialNode.node_style import NodeStyle
from SpatialNode.serializable import Serializable

class NodeDelegateModel(QtCore.QObject, Serializable, ABC):
    def __init__(self):
        self._nodeStyle: NodeStyle = None

    def captionVisible(self) -> bool:
        """It is possible to hide caption in GUI"""
        ...

    def caption(self) -> str:
        """
        Caption is used in GUI
        """
        ...

    def portCaptionVisible(
        self, portType: PortType | None, portIndex: PortIndex
    ) -> bool:
        """
        It is possible to hide port caption in GUI
        """
        ...

    def portCaption(self, portType: PortType | None, portIndex: PortIndex) -> str:
        """
        Port caption is used in GUI to label individual ports
        """
        ...

    @staticmethod
    def register(registry, *args, **kwargs): ...
    @override
    def save(self): ...
    @override
    def load(self, p: QtCore.QJsonArray): ...
    @abstractmethod
    def nPorts(self, portType: PortType | None) -> int: ...
    @abstractmethod
    def dataType(
        self, portType: PortType | None, portIndex: PortIndex
    ) -> NodeDataType: ...
    def portConnectionPolicy(
        self, portType: PortType | None, portIndex: PortIndex
    ) -> ConnectionPolicy: ...
    @property
    def nodeStyle(self) -> NodeStyle: ...
    @nodeStyle.setter
    def nodeStyle(self, style: NodeStyle): ...
    @abstractmethod
    def setInData(self, nodeData: NodeData, portIndex: PortIndex) -> None: ...
    @abstractmethod
    def outData(self, port: PortIndex) -> NodeData: ...
    @abstractmethod
    def embeddedWidget(self) -> QtWidgets.QWidget: ...
    def resizable(self) -> bool: ...

    dataUpdated: QtCore.Signal(PortIndex)
    """Triggers the updates in the nodes downstream."""

    dataInvalidated: QtCore.Signal(PortIndex)
    """Triggers the propagation of the empty data downstream."""

    computingStarted: QtCore.Signal()

    computingFinished: QtCore.Signal()

    embeddedWidgetSizeUpdated: QtCore.Signal()

    portsAboutToBeDeleted: QtCore.Signal(PortType, PortIndex, PortIndex)

    portsDeleted: QtCore.Signal()

    portsAboutToBeInserted: QtCore.Signal(PortType, PortIndex, PortIndex)

    portsInserted: QtCore.Signal()

    def inputConnectionCreated(self, connectionId: ConnectionId) -> None: ...
    def inputConnectionDeleted(self, connectionId: ConnectionId) -> None: ...
    def outputConnectionCreated(self, connectionId: ConnectionId) -> None: ...
    def outputConnectionDeleted(self, connectionId: ConnectionId) -> None: ...
