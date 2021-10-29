# -*- coding: utf-8 -*-

# maya
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQDockWidget
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# Built-in
from functools import partial
import os

# mbox
from . import rootnameui as name_ui
from . import rootcustomstepui as custom_step_ui
from . import rootui as root_ui
from . import blockui as block_ui

# mgear
from mgear.core import pyqt
from mgear.vendor.Qt import QtCore, QtWidgets, QtGui


MBOX_CUSTOMSTEP_PATH = ""
ROOT_TYPE = "mbox_guide_root"
BLOCK_TYPE = "mbox_guide_block"


class RootMainTab(QtWidgets.QDialog, root_ui.Ui_Form):

    def __init__(self, parent=None):
        super(RootMainTab, self).__init__(parent)
        self.setupUi(self)


class RootCustomStepTab(QtWidgets.QDialog, custom_step_ui.Ui_Form):

    def __init__(self, parent=None):
        super(RootCustomStepTab, self).__init__(parent)
        self.setupUi(self)


class RootNameTab(QtWidgets.QDialog, name_ui.Ui_Form):

    def __init__(self, parent=None):
        super(RootNameTab, self).__init__(parent)
        self.setupUi(self)


class HelperSlots:

    def update_line_edit(self):
        pass

    def update_combo_box(self):
        pass

    def update_push_button(self):
        pass

    def update_spin_box(self):
        pass

    def close_settings(self):
        self.close()
        pyqt.deleteInstances(self, MayaQDockWidget)


class RootSettings(MayaQWidgetDockableMixin, QtWidgets.QDialog, HelperSlots):

    @property
    def guide(self):
        return self._guide

    @guide.setter
    def guide(self, guide):
        self._guide = guide

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network

    def __init__(self, parent=None):
        pyqt.deleteInstances(self, MayaQDockWidget)
        super(RootSettings, self).__init__(parent=parent)
        self.toolName = ROOT_TYPE
        self.setObjectName(self.toolName)
        self.mayaMainWindow = pyqt.maya_main_window()

        self._guide = None
        self._network = None

        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(self.toolName)
        self.resize(500, 615)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.root_tab = RootMainTab()
        self.custom_step_tab = RootCustomStepTab()
        self.name_tab = RootNameTab()

        self.create_controls()
        self.create_layouts()
        self.create_connections()
        self.populate_controls()

        # hover info
        self.cs_list_widget = self.custom_step_tab.customStep_listWidget
        self.cs_list_widget.setMouseTracking(True)
        self.cs_list_widget.entered.connect(self.info)

    def info(self, index):
        self.hover_info_item_entered(self.cs_list_widget, index)

    def hover_info_item_entered(self, view, index):
        if index.isValid():
            info_data = self.format_info(index.data())
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(),
                info_data,
                view.viewport(),
                view.visualRect(index))

    def format_info(self, data):
        data_parts = data.split("|")
        cs_name = data_parts[0]
        if cs_name.startswith("*"):
            cs_status = "Deactivated"
            cs_name = cs_name[1:]
        else:
            cs_status = "Active"

        cs_fullpath = self.get_cs_file_fullpath(data)
        if "_shared" in data:
            cs_shared_owner = self.shared_owner(cs_fullpath)
            cs_shared_status = "Shared"
        else:
            cs_shared_status = "Local"
            cs_shared_owner = "None"

        info = '<html><head/><body><p><span style=" font-weight:600;">\
                        {0}</span></p><p>------------------</p><p><span style=" \
                        font-weight:600;">Status</span>: {1}</p><p><span style=" \
                        font-weight:600;">Shared Status:</span> {2}</p><p><span \
                        style=" font-weight:600;">Shared Owner:</span> \
                        {3}</p><p><span style=" font-weight:600;">Full Path</span>: \
                        {4}</p></body></html>'.format(cs_name,
                                                      cs_status,
                                                      cs_shared_status,
                                                      cs_shared_owner,
                                                      cs_fullpath)
        return info

    def get_cs_file_fullpath(self, cs_data):
        filepath = cs_data.split("|")[-1][1:]
        if os.environ.get(MGEAR_SHIFTER_CUSTOMSTEP_KEY, ""):
            fullpath = os.path.join(
                os.environ.get(
                    MGEAR_SHIFTER_CUSTOMSTEP_KEY, ""), filepath)
        else:
            fullpath = filepath

        return fullpath

    def shared_owner(self, cs_fullpath):

        scan_dir = os.path.abspath(os.path.join(cs_fullpath, os.pardir))
        while not scan_dir.endswith("_shared"):
            scan_dir = os.path.abspath(os.path.join(scan_dir, os.pardir))
            # escape infinite loop
            if scan_dir == '/':
                break
        scan_dir = os.path.abspath(os.path.join(scan_dir, os.pardir))
        return os.path.split(scan_dir)[1]

    def create_controls(self):
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setObjectName("root_settings_tab")

        self.tabs.insertTab(0, self.root_tab, "Root Main Settings")
        self.tabs.insertTab(1, self.custom_step_tab, "Custom Steps")
        self.tabs.insertTab(2, self.name_tab, "Naming Rules")

    def populate_controls(self):
        pass

    def create_layouts(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tabs)

        self.close_button = QtWidgets.QPushButton("Close")
        self.layout.addWidget(self.close_button)
        self.setLayout(self.layout)

    def create_connections(self):
        self.close_button.clicked.connect(self.close_settings)


class BlockMainTab(QtWidgets.QDialog, block_ui.Ui_Form):

    def __init__(self):
        super(BlockMainTab, self).__init__()
        self.setupUi(self)


class BlockSettings(QtWidgets.QDialog, HelperSlots):

    @property
    def guide(self):
        return self._guide

    @guide.setter
    def guide(self, guide):
        self._guide = guide

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network

    def __init__(self, parent=None):
        pyqt.deleteInstances(self, MayaQDockWidget)
        super(BlockSettings, self).__init__(parent=parent)
        self.toolName = BLOCK_TYPE
        self.setObjectName(self.toolName)
        self.mayaMainWindow = pyqt.maya_main_window()

        self._guide = None
        self._network = None

        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(self.toolName)

        self.main_tab = BlockMainTab()

        self.create_controls()
        self.create_layouts()
        self.create_connections()

    def create_controls(self):
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setObjectName("block_settings_tab")

        self.tabs.insertTab(0, self.main_tab, "Block Main Settings")

    def populate_controls(self):
        pass

    def create_layouts(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tabs)

        self.close_button = QtWidgets.QPushButton("Close")
        self.layout.addWidget(self.close_button)
        self.setLayout(self.layout)

    def create_connections(self):
        self.close_button.clicked.connect(self.close_settings)
