#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from SpatialNode.connection_id_utils import makeIncompleteConnectionIdFromComplete
from SpatialNode.definitions import ConnectionId, PortType, InvalidNodeId, InvalidPortIndex


def test_make_incomplete_connection_id_from_complete():
    connection_id = ConnectionId(1, 2, 3, 4)
    connect = makeIncompleteConnectionIdFromComplete(connection_id, PortType.In)
    assert connect.outNodeId == 1
    assert connect.outPortIndex == 2
    assert connect.inNodeId == InvalidNodeId
    assert connect.inPortIndex == InvalidPortIndex
