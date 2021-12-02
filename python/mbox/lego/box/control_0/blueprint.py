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
    TopBlock,
    SubBlock
)
from mbox.lego.box import settings
from . import settings_ui

# mgear
from mgear.core import pyqt, attribute
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
        self["meta"] = dict()
        self["meta"]["as_world"] = False
        self["meta"]["mirror_behaviour"] = False
        self["meta"]["world_orient_axis"] = True
        self["meta"]["key_able_attrs"] = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]

    def guide(self):
        super(Block, self).guide()
        meta = self["meta"]
        attribute.addAttribute(self.network, "as_world", "bool", meta["as_world"], keyable=False)
        attribute.addAttribute(self.network, "mirror_behaviour", "bool", meta["mirror_behaviour"], keyable=False)
        attribute.addAttribute(self.network, "world_orient_axis", "bool", meta["world_orient_axis"], keyable=False)
        for attr in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]:
            attribute.addAttribute(self.network, attr, "bool",
                                   True if attr in meta["key_able_attrs"] else False, keyable=False)

        root_name = f"{self['comp_name']}_{self['comp_direction']}{self['comp_index']}_root"
        if isinstance(self.parent, TopBlock):
            parent = self.parent.network.attr("guide").inputs(type="transform")[0]
        else:
            parent = self.parent.network.attr("transforms").inputs(type="transform")[-1]
        guide = icon.guide_root_icon(parent, root_name, m=pm.datatypes.Matrix(self["transforms"][0]))
        pm.connectAttr(guide.attr("message"), self.network.attr("guide"))
        pm.connectAttr(guide.attr("worldMatrix")[0], self.network.attr("transforms")[0])

        return guide

    def from_network(self):
        # common attr pull
        super(Block, self).from_network()

        # specify attr pull
        self["meta"]["as_world"] = self.network.attr("as_world").get()
        self["meta"]["mirror_behaviour"] = self.network.attr("mirror_behaviour").get()
        self["meta"]["world_orient_axis"] = self.network.attr("world_orient_axis").get()
        self["meta"]["key_able_attrs"] = [k for k in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]
                                          if self.network.attr(k).get()]

    def to_network(self):
        # common attr push
        super(Block, self).to_network()

        # specify attr push
        self.network.attr("as_world").set(self["meta"]["as_world"])
        self.network.attr("mirror_behaviour").set(self["meta"]["mirror_behaviour"])
        self.network.attr("world_orient_axis").set(self["meta"]["world_orient_axis"])
        [self.network.attr(a).set(True if a in self["meta"]["key_able_attrs"] else False)
         for a in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]]


class BlockSettingsUI(QtWidgets.QDialog, settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(BlockSettingsUI, self).__init__(parent)
        self.setupUi(self)


class BlockSettings(MayaQWidgetDockableMixin, settings.BlockSettings):

    def __init__(self, parent=None):
        self.toolName = TYPE
        # Delete old instances of the componet settings window.
        pyqt.deleteInstances(self, MayaQDockWidget)

        super(self.__class__, self).__init__(parent=parent)
        self.settings_tab = BlockSettingsUI()

        self.populate_block_controls()

    def populate_block_controls(self):
        """Populate Controls

        Populate the controls values from the custom attributes of the
        component.

        """
        # populate tab
        self.tabs.insertTab(1, self.settings_tab, "Component Settings")