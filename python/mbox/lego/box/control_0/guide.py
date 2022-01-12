# -*- coding: utf-8 -*

#
from functools import partial

# maya
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget

# mbox
from mbox.core import icon
from mbox.lego.lib import (
    RootBlock,
    SubBlock
)
from mbox.lego.box import settings
from . import settings_ui

# mgear
from mgear.core import pyqt, attribute, primitive, transform
from mgear.vendor.Qt import QtWidgets, QtCore

# block info
AUTHOR = "cho wooseoung"
URL = None
EMAIL = "chowooseoung@gmail.com"
VERSION = [0, 0, 1]
TYPE = "control_0"
NAME = "control"
DESCRIPTION = "control 0"


class Block(SubBlock):

    def __init__(self, parent):
        super(Block, self).__init__(parent=parent)
        self["version"] = "{}. {}. {}".format(*VERSION)
        self["comp_type"] = TYPE
        self["comp_name"] = NAME
        self["transforms"] = [pm.datatypes.Matrix().tolist()]

        # specify attr
        self["as_world"] = False
        self["leaf_joint"] = False
        self["uni_scale"] = False
        self["mirror_behaviour"] = False
        self["neutral_rotation"] = True
        self["icon"] = "cube"
        self["key_able_attrs"] = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]
        self["default_rotate_order"] = 0
        self["ik_ref_array"] = str()
        self["ctl_size"] = 1

    def guide(self):
        super(Block, self).guide()
        attribute.addAttribute(self.network, "as_world", "bool", self["as_world"], keyable=False)
        attribute.addAttribute(self.network, "leaf_joint", "bool", self["leaf_joint"], keyable=False)
        attribute.addAttribute(self.network, "uni_scale", "bool", self["uni_scale"], keyable=False)
        attribute.addAttribute(self.network, "mirror_behaviour", "bool", self["mirror_behaviour"], keyable=False)
        attribute.addAttribute(self.network, "neutral_rotation", "bool", self["neutral_rotation"], keyable=False)
        attribute.addAttribute(self.network, "icon", "string", self["icon"])
        for attr in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]:
            attribute.addAttribute(self.network, attr, "bool",
                                   True if attr in self["key_able_attrs"] else False, keyable=False)
        attribute.addAttribute(self.network, "default_rotate_order", "long", self["default_rotate_order"],
                               minValue=0, maxValue=5, keyable=False)
        attribute.addAttribute(self.network, "ik_ref_array", "string", self["ik_ref_array"])
        attribute.addAttribute(self.network, "ctl_size", "float", self["ctl_size"], keyable=False)

        name_format = f"{self['comp_name']}_{self['comp_side']}{self['comp_index']}_%s"
        if isinstance(self.parent, RootBlock):
            parent = self.parent.network.attr("guide").inputs(type="transform")[0]
        else:
            parent = self.parent.network.attr("transforms").inputs(type="transform")[-1]
        guide = icon.guide_root_icon(parent, name_format % "root", m=pm.datatypes.Matrix(self["transforms"][0]))
        size_ref_t = transform.getOffsetPosition(guide, [0, 0, 1])
        size_ref = primitive.addTransform(guide, name_format % "sizeRef", m=size_ref_t)
        attribute.lockAttribute(size_ref)
        attribute.addAttribute(size_ref, "is_guide", "bool", False, keyable=False)
        pm.connectAttr(guide.attr("message"), self.network.attr("guide"))
        pm.connectAttr(size_ref.attr("worldMatrix")[0], self.network.attr("transforms")[0])
        pm.connectAttr(guide.attr("worldMatrix")[0], self.network.attr("transforms")[1])

        return guide

    def from_network(self):
        # common attr pull
        super(Block, self).from_network()

        # specify attr pull
        self["as_world"] = self.network.attr("as_world").get()
        self["leaf_joint"] = self.network.attr("leaf_joint").get()
        self["uni_scale"] = self.network.attr("uni_scale").get()
        self["icon"] = self.network.attr("icon").get()
        self["mirror_behaviour"] = self.network.attr("mirror_behaviour").get()
        self["neutral_rotation"] = self.network.attr("neutral_rotation").get()
        self["key_able_attrs"] = [k for k in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]
                                          if self.network.attr(k).get()]
        self["default_rotate_order"] = self.network.attr("default_rotate_order").get()
        self["ik_ref_array"] = self.network.attr("ik_ref_array").get()
        self["ctl_size"] = self.network.attr("ctl_size").get()

    def to_network(self):
        # common attr push
        super(Block, self).to_network()

        # specify attr push
        self.network.attr("as_world").set(self["as_world"])
        self.network.attr("leaf_joint").set(self["leaf_joint"])
        self.network.attr("uni_scale").set(self["uni_scale"])
        self.network.attr("icon").set(self["icon"])
        self.network.attr("mirror_behaviour").set(self["mirror_behaviour"])
        self.network.attr("neutral_rotation").set(self["neutral_rotation"])
        [self.network.attr(a).set(True if a in self["key_able_attrs"] else False)
         for a in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]]
        self.network.attr("default_rotate_order").set(self["default_rotate_order"])
        self.network.attr("ik_ref_array").set(self["ik_ref_array"])


class BlockSettingsUI(QtWidgets.QDialog, settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(BlockSettingsUI, self).__init__(parent)
        self.setupUi(self)


class BlockSettings(MayaQWidgetDockableMixin, settings.BlockSettings):

    def __init__(self, parent=None):
        self.toolName = TYPE
        # Delete old instances of the componet settings window.
        pyqt.deleteInstances(self, MayaQDockWidget)

        super(BlockSettings, self).__init__(parent=parent)
        self.settings_tab = BlockSettingsUI()

        self.setup_component_setting_window()
        self.populate_block_controls()
        self.create_component_layout()

    def setup_component_setting_window(self):
        self.mayaMainWindow = pyqt.maya_main_window()

        self.setObjectName(self.toolName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(TYPE)

    def populate_block_controls(self):
        """Populate Controls

        Populate the controls values from the custom attributes of the
        component.

        """
        # populate tab
        self.tabs.insertTab(1, self.settings_tab, "Component Settings")

    def create_component_layout(self):
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout.addWidget(self.tabs)
        self.settings_layout.addWidget(self.close_button)

        self.setLayout(self.settings_layout)

    def dockCloseEventTriggered(self):
        pyqt.deleteInstances(self, MayaQDockWidget)
