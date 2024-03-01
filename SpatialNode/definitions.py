import sys
from enum import *


class NodeRole(IntEnum):
    """Constants used for fetching QVariant data from GraphModel."""

    Type = 0
    """Type of the current node, usually a string."""
    Position = 1
    """`QPointF` position of the node on the scene."""
    Size = 2
    """`QSize` for resizable nodes."""
    CaptionVisible = 3
    """`bool` for caption visibility."""
    Caption = 4
    """`QString` for node caption."""
    Style = 5
    """Custom NodeStyle as QJsonDocument"""
    InternalData = 6
    """Node-specific user data as QJsonObject"""
    InPortCount = 7
    """unsigned int"""
    OutPortCount = 9
    """unsigned int"""
    Widget = 10
    """Optional `QWidget * ` or `nullptr`"""


class NodeFlag(IntEnum):
    """Specific flags regulating node features and appearance."""

    NoFlags = 0x0
    """Default NodeFlag"""
    Resizable = 0x1
    """Lets the node be resizable"""
    Locked = 0x2


class PortRole(IntEnum):
    """Constants for fetching port-related information from the GraphModel."""

    Data = 0
    """std::shared_ptr<NodeData>"""
    DataType = 1
    """`QString` describing the port data type."""
    ConnectionPolicyRole = 2
    """`enum` ConnectionPolicyRole"""
    CaptionVisible = 3
    """`bool` for caption visibility."""
    Caption = 4
    """`QString` for port caption."""


class ConnectionPolicy(Enum):
    """
    Defines how many connections are possible to attach to ports.
    The values are fetched using PortRole::ConnectionPolicy.
    """

    One = auto()
    """Just one connection for each port."""
    Many = auto()
    """Any number of connections possible for the port."""


class PortType(IntEnum):
    """Used for distinguishing input and output node ports."""

    In = 0
    """Input node port (from the left)."""
    Out = 1
    """Output node port (from the right)."""


PortCount = int
PortIndex = int
NodeId = int

InvalidPortIndex = sys.maxsize
InvalidNodeId = sys.maxsize


class ConnectionId:
    """
     A unique connection identificator that stores
    out `NodeId`, out `PortIndex`, in `NodeId`, in `PortIndex`
    """
    outNodeId: NodeId
    outPortIndex: PortIndex
    inNodeId: NodeId
    inPortIndex: PortIndex

    def __init__(self, outNodeId: NodeId, outPortIndex: PortIndex, inNodeId: NodeId, inPortIndex: PortIndex):
        self.outNodeId = outNodeId
        self.outPortIndex = outPortIndex
        self.inNodeId = inNodeId
        self.inPortIndex = inPortIndex


def invertConnection(id: ConnectionId):
    """Inverts the Connection"""
    (id.outNodeId, id.inNodeId) = (id.inNodeId, id.outNodeId)
    (id.outPortIndex, id.inPortIndex) = (id.inPortIndex, id.outPortIndex)
