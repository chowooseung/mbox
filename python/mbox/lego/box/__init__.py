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
        world_ctl = self.block.create_ctl(context=context,
                                          parent=world_root,
                                          m=pm.datatypes.Matrix(),
                                          parent_ctl=None,
                                          color=(0, 0, 0))
        world_ref = self.block.create_ref(context=context,
                                          parent=world_ctl,
                                          m=pm.datatypes.Matrix())
        if False:
            world_jnt = self.block.create_jnt(context=context,
                                              parent=joints,
                                              ref=world_ref)

        self.ins["root"] = root
        self.ins["geo_root"] = geo
        self.ins["blocks_root"] = blocks
        self.ins["joints_root"] = joints
        self.ins["root_set"] = pm.sets(name=f"{self.block['name']}_set")
        self.ins["geo_set"] = pm.sets(name="geo_set")
        self.ins["controller_set"] = pm.sets(name="controller_set")
        self.ins["deformer_set"] = pm.sets(name="deformer_set")
        pm.sets(self.ins["root_set"], addElement=(self.ins["geo_set"],
                                                  self.ins["controller_set"],
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

        attribute.lockAttribute(self.ins["root"])
        attribute.lockAttribute(self.ins["geo_root"])
        attribute.lockAttribute(self.ins["blocks_root"])
        attribute.lockAttribute(self.ins["joints_root"])


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
        tag = pm.controller(self.ins["controls"][0], query=True)[0]
        condition = pm.createNode("condition")
        pm.connectAttr(self.ins["root"].attr("controls_mouseover"), condition.attr("firstTerm"))
        condition.attr("secondTerm").set(1)
        condition.attr("operation").set(0)
        condition.attr("colorIfTrueR").set(2)
        condition.attr("colorIfFalseR").set(0)
        pm.connectAttr(condition.attr("outColorR"), tag.attr("visibilityMode"))


