#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtCore, QtWidgets

from SpatialNode.basic_graphics_scene import BasicGraphicsScene


class DataFlowGraphicsScene(BasicGraphicsScene):
    def __init__(self, graphModel, parent=None):
        BasicGraphicsScene.__init__(self, graphModel, parent)
        self._graphModel = graphModel
        self._graphModel.inPortDataWasSet.connect(
            lambda nodeId: self.onNodeUpdated(nodeId)
        )

    def selectedNodes(self):
        from SpatialNode.definitions import NodeId

        graphicsItems = self.selectedItems()

        result: list[NodeId] = []
        for item in graphicsItems:
            result.append(item.nodeId())
        return result

    def createSceneMenu(self, scenePos: QtCore.QPointF):
        from SpatialNode.data_flow_graph_model import DataFlowGraphModel

        modelMenu = QtWidgets.QMenu()

        # Add filterbox to the context menu
        txtBox = QtWidgets.QLineEdit(modelMenu)
        txtBox.setPlaceholderText("Filter")
        txtBox.setClearButtonEnabled(True)

        txtBoxAction = QtWidgets.QWidgetAction(modelMenu)
        txtBoxAction.setDefaultWidget(txtBox)

        # 1.
        modelMenu.addAction(txtBoxAction)

        # Add result treeview to the context menu
        treeView = QtWidgets.QTreeWidget(modelMenu)
        treeView.header().close()

        treeViewAction = QtWidgets.QWidgetAction(modelMenu)
        treeViewAction.setDefaultWidget(treeView)

        # 2.
        modelMenu.addAction(treeViewAction)

        if not isinstance(self._graphModel, DataFlowGraphModel):
            raise RuntimeError("_graphModel must be a DataFlowGraphModel")

        registry = self._graphModel.dataModelRegistry

        for cat in registry.categories():
            item = QtWidgets.QTreeWidgetItem(treeView)
            item.setText(0, cat)
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)

        for assoc in registry.registeredModelsCategoryAssociation().items():
            parent = treeView.findItems(assoc[1], QtCore.Qt.MatchFlag.MatchExactly)

            if len(parent) <= 0:
                continue

            item = QtWidgets.QTreeWidgetItem(parent[0])
            item.setText(0, assoc[0])

        def AA(item: QtWidgets.QTreeWidgetItem, count: int):
            from SpatialNode.undo_commands import CreateCommand

            if not (item.flags() & QtCore.Qt.ItemFlag.ItemIsSelectable):
                return

            self.undoStack.push(CreateCommand(self, item.text(0), scenePos))
            modelMenu.close()

        treeView.itemClicked.connect(AA)

        # Setup filtering
        def Filter(text):
            treeView.expandAll()
            categoryIt = QtWidgets.QTreeWidgetItemIterator(
                treeView, QtWidgets.QTreeWidgetItemIterator.IteratorFlag.HasChildren
            )
            while categoryIt.value():
                item = categoryIt.value()
                item.setHidden(False)
                categoryIt += 1
            it = QtWidgets.QTreeWidgetItemIterator(
                treeView, QtWidgets.QTreeWidgetItemIterator.IteratorFlag.NoChildren
            )
            while it.value():
                item = it.value()
                modelName = item.text(0)
                match = text.lower() in modelName.lower()
                item.setHidden(not match)
                if match:
                    parent = item.parent()
                    while parent:
                        parent.setHidden(False)
                        parent = parent.parent()
                it += 1

        txtBox.textChanged.connect(Filter)

        # make sure the text box gets focus so the user doesn't have to click on it
        txtBox.setFocus()

        # QMenu's instance auto-destruction
        modelMenu.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)

        return modelMenu

    sceneLoaded = QtCore.Signal()

    def save(self):
        from SpatialNode.data_flow_graph_model import DataFlowGraphModel

        if not isinstance(self._graphModel, DataFlowGraphModel):
            raise RuntimeError("_graphModel must be a DataFlowGraphModel")

        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, "Open Flow Scene", QtCore.QDir.homePath(), "Flow Scene Files (*.json)"
        )

        if len(fileName) > 0:
            if not fileName.endswith("json"):
                fileName += ".json"

            file = QtCore.QFile(fileName)
            if file.open(QtCore.QIODevice.OpenModeFlag.WriteOnly):
                file.write(QtCore.QJsonDocument(self._graphModel.save()).toJson())

    def load(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open Flow Scene", QtCore.QDir.homePath(), "Flow Scene Files (*.json)"
        )

        if not QtCore.QFileInfo.exists(fileName):
            return

        self.loadUrl(fileName)

    def loadUrl(self, fileName):
        from SpatialNode.data_flow_graph_model import DataFlowGraphModel

        if not isinstance(self._graphModel, DataFlowGraphModel):
            raise RuntimeError("_graphModel must be a DataFlowGraphModel")

        file = QtCore.QFile(fileName)

        if not file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly):
            print(fileName)
            return

        self.clearScene()
        wholeFile = file.readAll()

        self._graphModel.load(QtCore.QJsonDocument.fromJson(wholeFile).object())
        self.sceneLoaded.emit()
