#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

from PySide6 import QtCore, QtGui

from SpatialNode.abstract_graph_model import AbstractGraphModel
from SpatialNode.basic_graphics_scene import BasicGraphicsScene
from SpatialNode.definitions import NodeId, ConnectionId, QJsonObject

def serializeSelectedItems(scene: BasicGraphicsScene) -> QJsonObject: ...
def insertSerializedItems(json: QJsonObject, scene: BasicGraphicsScene) -> None: ...
def deleteSerializedItems(
    sceneJson: QJsonObject, graphModel: AbstractGraphModel
) -> None: ...
def computeAverageNodePosition(sceneJson: QJsonObject) -> QtCore.QPointF: ...
def offsetNodeGroup(sceneJson: QJsonObject, diff: QtCore.QPointF) -> None: ...

class CreateCommand(QtGui.QUndoCommand):
    def __init__(
        self, scene: BasicGraphicsScene, name: str, mouseScenePos: QtCore.QPointF
    ):
        self._scene: BasicGraphicsScene = None
        self._nodeId: NodeId = None
        self._sceneJson: QJsonObject = None

    @override
    def undo(self): ...
    @override
    def redo(self): ...

class DeleteCommand(QtGui.QUndoCommand):
    def __init__(self, scene: BasicGraphicsScene):
        self._scene: BasicGraphicsScene = None
        self._sceneJson: QJsonObject = None

    @override
    def undo(self): ...
    @override
    def redo(self): ...

class CopyCommand(QtGui.QUndoCommand):
    def __init__(self, scene: BasicGraphicsScene):
        self._scene: BasicGraphicsScene = None

    @override
    def undo(self): ...
    @override
    def redo(self): ...

class PasteCommand(QtGui.QUndoCommand):
    def __init__(self, scene: BasicGraphicsScene, mouseScenePos: QtCore.QPointF):
        self._scene: BasicGraphicsScene = None
        self._mouseScenePos: QtCore.QPointF = None
        self._newSceneJson: QJsonObject = None

    @override
    def undo(self): ...
    @override
    def redo(self): ...
    def _takeSceneJsonFromClipboard(self) -> QJsonObject: ...
    def _makeNewNodeIdsInScene(self, sceneJson: QJsonObject) -> QJsonObject: ...

class DisconnectCommand(QtGui.QUndoCommand):
    def __init__(self, scene: BasicGraphicsScene, connection_id: ConnectionId):
        self._scene: BasicGraphicsScene = None
        self._connection_id: ConnectionId = None

    @override
    def undo(self): ...
    @override
    def redo(self): ...

class ConnectCommand(QtGui.QUndoCommand):
    def __init__(self, scene: BasicGraphicsScene, connection_id: ConnectionId):
        self._scene: BasicGraphicsScene = None
        self._connection_id: ConnectionId = None

    @override
    def undo(self): ...
    @override
    def redo(self): ...

class MoveNodeCommand(QtGui.QUndoCommand):
    def __init__(self, scene: BasicGraphicsScene, diff: QtCore.QPointF):
        self._scene: BasicGraphicsScene = None
        self._diff: QtCore.QPointF = None
        self._selectedNodes: set[NodeId] = None

    @override
    def undo(self): ...
    @override
    def redo(self): ...
    @override
    def id(self): ...
    @override
    def mergeWith(self, other): ...
