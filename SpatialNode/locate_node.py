#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtCore


def locateNodeAt(scenePoint, scene, viewTransform):
    from SpatialNode.node_graphics_object import NodeGraphicsObject

    # items under cursor
    items = scene.items(
        scenePoint,
        QtCore.Qt.ItemSelectionMode.IntersectsItemShape,
        QtCore.Qt.SortOrder.DescendingOrder,
        viewTransform,
    )

    filteredItems = []
    for item in items:
        if isinstance(item, NodeGraphicsObject):
            filteredItems.append(item)

    if len(filteredItems) > 0:
        return filteredItems[0]
