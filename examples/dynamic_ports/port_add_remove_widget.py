#  Copyright (c) 2024 Feng Yang
#
#  I am making my contributions/submissions to this project solely in my
#  personal capacity and am not conveying any rights to any intellectual
#  property of any third parties.

from PySide6 import QtWidgets

import SpatialNode as sNode


class PortAddRemoveWidget(QtWidgets.QWidget):
    """
    #                PortAddRemoveWidget
    # ```
    #       _left                         _right
    #       layout                        layout
    #     ----------------------------------------
    #     |         |                  |         |
    #     | [+] [-] |                  | [+] [-] |
    #     |         |                  |         |
    #     | [+] [-] |                  | [+] [-] |
    #     |         |                  |         |
    #     | [+] [-] |                  | [+] [-] |
    #     |         |                  |         |
    #     | [+] [-] |                  |         |
    #     |         |                  |         |
    #     |_________|__________________|_________|
    # ```
    *
    # The widget has two main vertical layouts containing groups of buttons for
    # adding and removing ports. Each such a `[+] [-]` group is contained in a
    # dedicated QHVBoxLayout.
    """

    def __init__(self, nInPorts, nOutPorts, nodeId, model, parent=None):
        super().__init__(parent)
        self._nodeId = nodeId
        self._model = model

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum
        )

        hl = QtWidgets.QHBoxLayout(self)
        hl.setContentsMargins(0, 0, 0, 0)
        hl.setSpacing(0)

        self._left = QtWidgets.QVBoxLayout()
        self._left.setSpacing(0)
        self._left.setContentsMargins(0, 0, 0, 0)
        self._left.addStretch()

        self._right = QtWidgets.QVBoxLayout()
        self._right.setSpacing(0)
        self._right.setContentsMargins(0, 0, 0, 0)
        self._right.addStretch()

        hl.addLayout(self._left)
        hl.addSpacing(50)
        hl.addLayout(self._right)

    def populateButtons(self, portType, nPorts):
        vl = self._left if portType == sNode.PortType.In else self._right

        # we use [-1} in the expression `vl->count() - 1` because
        # one element - a spacer - is alvays present in this layout.

        if vl.count() - 1 < nPorts:
            while vl.count() - 1 < nPorts:
                self.addButtonGroupToLayout(vl, 0)

        if vl.count() - 1 > nPorts:
            while vl.count() - 1 > nPorts:
                self.removeButtonGroupFromLayout(vl, 0)

    def addButtonGroupToLayout(self, vbl, portIndex):
        l = QtWidgets.QHBoxLayout()
        l.setContentsMargins(0, 0, 0, 0)

        button = QtWidgets.QPushButton("+")
        button.setFixedHeight(25)
        l.addWidget(button)
        button.clicked.connect(self.onPlusClicked)

        button = QtWidgets.QPushButton("-")
        button.setFixedHeight(25)
        l.addWidget(button)
        button.clicked.connect(self.onMinusClicked)

        vbl.insertLayout(portIndex, l)

        return l

    def removeButtonGroupFromLayout(self, vbl, portIndex):
        # Last item in the layout is always a spacer
        if vbl.count() > 1:
            item = vbl.itemAt(portIndex)

            # Delete [+] and [-] QPushButton widgets
            item.layout().itemAt(0).widget().deleteLater()
            item.layout().itemAt(1).widget().deleteLater()

            vbl.removeItem(item)

    def onPlusClicked(self):
        # index of the plus button in the QHBoxLayout
        plusButtonIndex = 0

        # All existing "plus" buttons trigger the same slot. We need to find out which
        # button has been actually clicked.
        (portType, portIndex) = self.findWhichPortWasClicked(
            self.sender(), plusButtonIndex
        )

        # We add new "plus-minus" button group to the chosen layout.
        self.addButtonGroupToLayout(
            self._left if portType == sNode.PortType.In else self._right, portIndex + 1
        )

        # Trigger changes in the model
        self._model.addPort(self._nodeId, portType, portIndex + 1)

        self.adjustSize()

    def onMinusClicked(self):
        # index of the minus button in the QHBoxLayout
        minusButtonIndex = 1
        (portType, portIndex) = self.findWhichPortWasClicked(
            self.sender(), minusButtonIndex
        )

        self.removeButtonGroupFromLayout(
            self._left if portType == sNode.PortType.In else self._right, portIndex
        )

        # Trigger changes in the model
        self._model.removePort(self._nodeId, portType, portIndex)

        self.adjustSize()

    def findWhichPortWasClicked(self, sender, buttonIndex):
        portType: sNode.PortType | None = None

        def checkOneSide(sideLayout: QtWidgets.QVBoxLayout) -> int:
            for i in range(sideLayout.count()):
                layoutItem = sideLayout.itemAt(i)

                if not isinstance(layoutItem, QtWidgets.QHBoxLayout):
                    continue

                widget = layoutItem.itemAt(buttonIndex).widget()

                if sender == widget:
                    return i

        portIndex = checkOneSide(self._left)
        if portIndex is None:
            portIndex = sNode.InvalidPortIndex

        if portIndex != sNode.InvalidPortIndex:
            portType = sNode.PortType.In
        else:
            portIndex = checkOneSide(self._right)

            if portIndex != sNode.InvalidPortIndex:
                portType = sNode.PortType.Out

        return portType, portIndex
