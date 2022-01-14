# -*- coding: utf-8 -*-

# mgear
from mgear.core import attribute, primitive, icon

# mbox
from mbox.lego.lib import (
    AbstractObjects,
    AbstractAttributes,
    AbstractOperators,
    AbstractConnection
)

# maya
import pymel.core as pm


class Objects(AbstractObjects):

    def __init__(self, block):
        super(Objects, self).__init__(block=block)

    def process(self, context):
        super(Objects, self).process(context=context)

        root = primitive.addTransform(None, self.block["name"])
        geo = primitive.addTransform(root, "geo")
        blocks = primitive.addTransform(root, "blocks")
        joints = primitive.addTransform(root, "joints")

        world_root = primitive.addTransform(blocks, "world_root")
        world_npo = primitive.addTransform(world_root, "world_npo")
        world_ctl = icon.create(world_npo, "world_ctl", icon="circle")
        pm.controller(world_ctl)
        world_ref = primitive.addTransform(world_ctl, "world_ref")

        self.ins["root"] = root
        self.ins["geo_root"] = geo
        self.ins["blocks_root"] = blocks
        self.ins["joints_root"] = joints
        self.ins["controls"] = [world_ctl]
        self.ins["refs"] = [world_ref]
        self.ins["joints"] = [joints]
        self.ins["root_set"] = pm.sets(name=f"{self.block['name']}_set")
        self.ins["geo_set"] = pm.sets(name="geo_set")
        self.ins["controls_set"] = pm.sets(name="controls_set")
        self.ins["deformer_set"] = pm.sets(name="deformer_set")
        pm.sets(self.ins["root_set"], addElement=(self.ins["geo_set"],
                                                  self.ins["controls_set"],
                                                  self.ins["deformer_set"]))
        pm.sets(self.ins["geo_set"], addElement=geo)


class Attributes(AbstractAttributes):

    def __init__(self, block):
        super(Attributes, self).__init__(block=block)

    def process(self, context):
        super(Attributes, self).process(context=context)

        attribute.addAttribute(self.ins["root"], "controls_vis", "bool", True)
        attribute.addAttribute(self.ins["root"], "controls_mouseover", "bool", False)
        attribute.addAttribute(self.ins["root"], "controls_on_playback_vis", "bool", False)
        attribute.addAttribute(self.ins["root"], "joints_vis", "bool", False)
        attribute.addAttribute(self.ins["root"], "joints_label_vis", "bool", False)
        attribute.addAttribute(self.ins["root"], "is_rig_root", "bool", keyable=False)


class Operators(AbstractOperators):

    def __init__(self, block):
        super(Operators, self).__init__(block=block)

    def process(self, context):
        super(Operators, self).process(context=context)


class Connection(AbstractConnection):

    def __init__(self, block):
        super(Connection, self).__init__(block=block)

    def process(self, context):
        super(Connection, self).process(context=context)
        pm.connectAttr(self.ins["root"].attr("controls_vis"), self.ins["blocks_root"].attr("v"))
        pm.connectAttr(self.ins["root"].attr("controls_on_playback_vis"), self.ins["blocks_root"].attr("hideOnPlayback"))
        pm.connectAttr(self.ins["root"].attr("joints_vis"), self.ins["joints_root"].attr("v"))
        tag = pm.PyNode(pm.controller(self.ins["controls"][0], query=True)[0])
        condition = pm.createNode("condition")
        pm.connectAttr(self.ins["root"].attr("controls_mouseover"), condition.attr("firstTerm"))
        condition.attr("secondTerm").set(1)
        condition.attr("operation").set(0)
        condition.attr("colorIfTrueR").set(2)
        condition.attr("colorIfFalseR").set(0)
        pm.connectAttr(condition.attr("outColorR"), tag.attr("visibilityMode"))

        attribute.lockAttribute(self.ins["root"])
        attribute.lockAttribute(self.ins["geo_root"])
        attribute.lockAttribute(self.ins["blocks_root"])
        attribute.lockAttribute(self.ins["joints_root"])


