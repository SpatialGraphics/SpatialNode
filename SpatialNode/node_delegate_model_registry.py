#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.


class NodeDelegateModelRegistry:
    def __init__(self):
        self._registeredModelsCategory = {}
        self._categories = set()
        self._registeredItemCreators = {}

    def registerModel(self, creator, category="Nodes"):
        name = creator().name()
        if name not in self._registeredItemCreators:
            self._registeredItemCreators[name] = creator
            self._categories.add(category)
            self._registeredModelsCategory[name] = category

    def create(self, modelName):
        creator = self._registeredItemCreators.get(modelName)
        if creator:
            return creator()

    def registeredModelsCategoryAssociation(self):
        return self._registeredModelsCategory

    def categories(self):
        return self._categories
