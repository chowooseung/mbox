# -*- coding:utf-8 -*-

# mbox
from mbox.lego import boxui, editorui
from mbox.vendor.Qt import QtCore, QtWidgets
from mbox.core import pyqt

# maya
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


# guides manager UI

class LegoBox(MayaQWidgetDockableMixin, QtWidgets.QDialog):

    def __init__(self, parent=None):
        self.toolName = "LegoBox"
        super(LegoBox, self).__init__(parent=parent)

        self.box_ui = boxui.Blocks()
        self.editor_ui = editorui.Blueprint()
        self.installEventFilter(self)
        self.create_window()
        self.create_layout()

    def keyPressEvent(self, event):
        if not event.key() == QtCore.Qt.Key_Escape:
            super(LegoBox, self).keyPressEvent(event)

    def create_window(self):
        self.setObjectName(self.toolName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Lego Box")
        self.resize(280, 750)

    def create_layout(self):
        self.gm_layout = QtWidgets.QVBoxLayout()
        self.gm_layout.setContentsMargins(3, 3, 3, 3)
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setObjectName("legobox_tab")
        self.tabs.insertTab(0, self.box_ui, "Lego Components")
        self.tabs.insertTab(1, self.editor_ui, "Editor")

        self.gm_layout.addWidget(self.tabs)

        self.setLayout(self.gm_layout)


def show_guide_manager(*args):
    pyqt.showDialog(LegoBox, dockable=True)