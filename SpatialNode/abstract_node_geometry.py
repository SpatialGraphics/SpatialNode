#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

import math
from abc import ABC, abstractmethod

from PySide6 import QtCore


class AbstractNodeGeometry(ABC):
    def __init__(self, graphModel):
        self._graphModel = graphModel

    def boundingRect(self, node_id):
        s = self.size(node_id)
        ratio = 0.20

        widthMargin = int(s.width() * ratio)
        heightMargin = int(s.height() * ratio)

        margins = QtCore.QMargins(widthMargin, heightMargin, widthMargin, heightMargin)
        r = QtCore.QRectF(QtCore.QPointF(0, 0), s)

        return r.marginsAdded(margins)

    @abstractmethod
    def size(self, node_id): ...

    @abstractmethod
    def recomputeSize(self, node_id): ...

    @abstractmethod
    def portPosition(self, node_id, port_type, index): ...

    def portScenePosition(self, node_id, port_type, index, t):
        result = self.portPosition(node_id, port_type, index)
        return t.map(result)

    @abstractmethod
    def portTextPosition(self, node_id, port_type, node_point): ...

    @abstractmethod
    def captionPosition(self, node_id): ...

    @abstractmethod
    def captionRect(self, node_id): ...

    @abstractmethod
    def widgetPosition(self, node_id): ...

    def checkPortHit(self, node_id, port_type, node_point):
        from SpatialNode.style_collection import StyleCollection
        from SpatialNode.definitions import InvalidPortIndex, NodeRole, PortType

        nodeStyle = StyleCollection.nodeStyle()

        result = InvalidPortIndex

        if port_type is None:
            return result

        tolerance = 2.0 * nodeStyle.ConnectionPointDiameter
        n = self._graphModel.nodeData(
            node_id,
            (
                NodeRole.OutPortCount
                if port_type == PortType.Out
                else NodeRole.InPortCount
            ),
        )
        for portIndex in range(n):
            pp = self.portPosition(node_id, port_type, portIndex)

            p = pp - node_point
            distance = math.sqrt(QtCore.QPointF.dotProduct(p, p))

            if distance < tolerance:
                result = portIndex
                break
        return result

    @abstractmethod
    def resizeHandleRect(self, node_id): ...
