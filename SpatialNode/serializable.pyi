#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from SpatialNode.definitions import QJsonObject

class Serializable:
    def save(self) -> QJsonObject: ...
    def load(self, p: QJsonObject) -> None: ...
