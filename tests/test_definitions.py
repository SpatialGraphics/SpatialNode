#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from SpatialNode.definitions import ConnectionId


def test_connection_id():
    connection_id = ConnectionId(1, 2, 3, 4)
    assert connection_id.outNodeId == 1
