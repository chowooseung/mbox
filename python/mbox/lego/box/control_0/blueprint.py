# -*- coding: utf-8 -*

#
import logging
from functools import partial

# maya
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget

# mbox
from mbox.core import icon
from mbox.lego.box import blueprint, settings

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

logger = logging.getLogger(__name__)


class Block(blueprint.Blocks):

    def __init__(self, guide=None, network=None, rig=None):
        super(Block, self).__init__(guide=guide, network=network, rig=rig)
        self.component = TYPE
        self.version = "{}. {}. {}".format(*VERSION)
        self.name = NAME
        self.transforms = [pm.datatypes.Matrix().tolist()]

        # specify attr
        self.asWorld = False
        self.mirrorBehaviour = False
        self.worldOrientAxis = True
        self.keyAbleAttrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]

    def draw_guide(self, parent):
        # network
        if not self.NETWORK:
            self.draw_network()

        # name
        root_name = f"{self.name}_{self.direction}{self.index}_root"

        # create
        self.GUIDE = icon.guide_root_icon(parent, root_name, m=pm.datatypes.Matrix(self.transforms[0]))

        # attribute

        # connection
        pm.connectAttr(self.GUIDE.worldMatrix[0], self.NETWORK.transforms[0], force=True)

        # recursive
        super(Block, self).draw_guide(parent=self.GUIDE)

        return self.GUIDE

    def draw_network(self):
        super(Block, self).draw_network()
        attribute.addAttribute(self.NETWORK, "asWorld", "bool", self.asWorld, keyable=False)
        attribute.addAttribute(self.NETWORK, "mirrorBehaviour", "bool", self.mirrorBehaviour, keyable=False)
        attribute.addAttribute(self.NETWORK, "worldOrientAxis", "bool", self.worldOrientAxis, keyable=False)
        for attr in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]:
            attribute.addAttribute(self.NETWORK, attr, "bool",
                                   True if attr in self.keyAbleAttrs else False, keyable=False)

    def draw_rig(self, context, step, **kwargs):
        from .. import control_0 as rig
        super(Block, self).draw_rig(context, step, rig)
        pm.connectAttr(self.RIG.message, self.NETWORK.rig, force=True)

    def update_network_to_blueprint(self):
        # common attr pull
        super(Block, self).update_network_to_blueprint()

        # specify attr pull
        self.asWorld = self.NETWORK.attr("asWorld").get()
        self.mirrorBehaviour = self.NETWORK.attr("mirrorBehaviour").get()
        self.worldOrientAxis = self.NETWORK.attr("worldOrientAxis").get()
        self.keyAbleAttrs = [k for k in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]
                             if self.NETWORK.attr(k).get()]

    def update_blueprint_to_network(self):
        # common attr push
        super(Block, self).update_blueprint_to_network()

        # specify attr push
        self.NETWORK.attr("asWorld").set(self.asWorld)
        self.NETWORK.attr("mirrorBehaviour").set(self.mirrorBehaviour)
        self.NETWORK.attr("worldOrientAxis").set(self.worldOrientAxis)
        [self.NETWORK.attr(a).set(True if a in self.keyAbleAttrs else False)
         for a in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]]


class BlockSettings(MayaQWidgetDockableMixin, settings.BlockSettings):

    def __init__(self, parent=None):
        super(BlockSettings, self).__init__(parent=parent)
