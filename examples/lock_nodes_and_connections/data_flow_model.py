#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from typing import override

import SpatialNode as sNode


class DataFlowModel(sNode.DataFlowGraphModel):
    def __init__(self, registry: sNode.NodeDelegateModelRegistry):
        super().__init__(registry)
        self._detachPossible = True
        self._nodesLocked = False

    @override
    def detachPossible(self, connectionId):
        return self._detachPossible

    def setDetachPossible(self, d: bool = True):
        self._detachPossible = d

    @override
    def nodeFlags(self, nodeId):
        basicFlags = super().nodeFlags(nodeId)
        if self._nodesLocked:
            basicFlags |= sNode.NodeFlag.Locked

        return basicFlags

    def setNodesLocked(self, b: bool = True):
        self._nodesLocked = b

        for nodeId in self.allNodeIds():
            self.nodeFlagsUpdated.emit(nodeId)
