#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from SpatialNode.connection_style import ConnectionStyle
from SpatialNode.graphics_view_style import GraphicsViewStyle
from SpatialNode.node_style import NodeStyle

# initialize global runtime
collection = None


class StyleCollection:
    def __init__(self):
        self._nodeStyle = NodeStyle()
        self._connectionStyle = ConnectionStyle()
        self._flowViewStyle = GraphicsViewStyle()

    @staticmethod
    def nodeStyle() -> NodeStyle:
        return StyleCollection._instance()._nodeStyle

    @staticmethod
    def connectionStyle() -> ConnectionStyle:
        return StyleCollection._instance()._connectionStyle

    @staticmethod
    def flowViewStyle() -> GraphicsViewStyle:
        return StyleCollection._instance()._flowViewStyle

    @staticmethod
    def setNodeStyle(style: NodeStyle):
        StyleCollection._instance()._nodeStyle = style

    @staticmethod
    def setConnectionStyle(style: ConnectionStyle):
        StyleCollection._instance()._connectionStyle = style

    @staticmethod
    def setGraphicsViewStyle(style: GraphicsViewStyle):
        StyleCollection._instance()._flowViewStyle = style

    @staticmethod
    def _instance():
        global collection

        if collection is None:
            collection = StyleCollection()
        return collection
