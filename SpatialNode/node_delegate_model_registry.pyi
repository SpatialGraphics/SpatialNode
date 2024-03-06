#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from SpatialNode.node_delegate_model import NodeDelegateModel

class NodeDelegateModelRegistry:
    """
    Class uses map for storing models (name, model)
    """

    def __init__(self):
        self._registeredModelsCategory: dict[str, str] = None
        self._categories: set[str] = None
        self._registeredItemCreators: dict[str, lambda: NodeDelegateModel] = None

    def registerModel(
        self, creator: lambda: NodeDelegateModel, name: str, category="Nodes"
    ): ...
    def create(self, modelName: str) -> NodeDelegateModel | None: ...
    def registeredModelsCategoryAssociation(self) -> dict[str, str]: ...
    def categories(self) -> set[str]: ...
