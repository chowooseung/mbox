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
        self["component"] = TYPE
        self["version"] = "{}. {}. {}".format(*VERSION)
        self["name"] = NAME
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

        root_name = f"{self['name']}_{self['direction']}{self['index']}_root"
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


class BlockSettings(MayaQWidgetDockableMixin, settings.BlockSettings):

    def __init__(self, parent=None):
        super(BlockSettings, self).__init__(parent=parent)
