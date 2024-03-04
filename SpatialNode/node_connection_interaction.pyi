#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtCore

from SpatialNode.basic_graphics_scene import BasicGraphicsScene
from SpatialNode.connection_graphics_object import ConnectionGraphicsObject
from SpatialNode.definitions import PortIndex, PortType
from SpatialNode.node_graphics_object import NodeGraphicsObject

class NodeConnectionInteraction:
    def __init__(
        self,
        ngo: NodeGraphicsObject,
        cgo: ConnectionGraphicsObject,
        scene: BasicGraphicsScene,
    ):
        self._ngo: NodeGraphicsObject = None
        self._cgo: ConnectionGraphicsObject = None
        self._scene: BasicGraphicsScene = None

    def canConnect(self, portIndex: PortIndex) -> bool:
        """
        Can connect when following conditions are met:
        * 1. Connection 'requires' a port.
        * 2. Connection loose end is above the node port.
        * 3. Source and target `nodeId`s are different.
        * 4. GraphModel permits connection.
        :param portIndex:
        :return:
        """
        ...

    def tryConnect(self) -> bool:
        """
        Creates a new connection if possible.
        * 1. Check conditions from 'canConnect'.
        * 2. Creates new connection with `GraphModel::addConnection`.
        * 3. Adjust connection geometry.
        :return:
        """
        ...

    def disconnect(self, portToDisconnect: PortType | None) -> bool:
        """
        * 1. Delete connection with `GraphModel::deleteConnection`.
        * 2. Create a "draft" connection with incomplete `ConnectionId`.
        * 3. Repaint both previously connected nodes.
        :param portToDisconnect:
        :return:
        """
        ...

    def _connectionRequiredPort(self) -> PortType: ...
    def _nodePortScenePosition(
        self, portType: PortType | None, portIndex: PortIndex
    ) -> QtCore.QPointF: ...
    def _nodePortIndexUnderScenePoint(
        self, portType: PortType | None, scenePoint: QtCore.QPointF
    ) -> PortIndex: ...
