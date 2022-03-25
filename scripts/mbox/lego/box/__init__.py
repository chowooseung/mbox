# -*- coding: utf-8 -*-

# mgear
from mgear.core import (
    attribute,
    primitive,
    icon,
    node)

# mbox
from mbox.lego.lib import (
    AbstractObjects,
    AbstractAttributes,
    AbstractOperators,
    AbstractConnection)

# maya
import pymel.core as pm


class Objects(AbstractObjects):

    def __init__(self, block):
        super(Objects, self).__init__(block=block)

    def process(self, context):
        super(Objects, self).process(context=context)

        m = pm.datatypes.Matrix()
        root = self.create_root(context, m=pm.datatypes.Matrix())
        geo = primitive.addTransform(root, "geo", m=m)
        blocks = primitive.addTransform(root, "blocks", m=m)
        joints = primitive.addTransform(root, "joints", m=m)

        world_root = primitive.addTransform(blocks, "world_root", m=m)
        world_npo = primitive.addTransform(world_root, "world_npo", m=m)
        attribute.setKeyableAttributes(world_npo, [])
        world_ctl = icon.create(world_npo, "world_ctl", m=m, icon="circle", color=(0, 1, 1))
        attribute.setKeyableAttributes(world_ctl, ["tx", "ty", "tz", "ro", "rx", "ry", "rz", "sx", "sy", "sz"])
        attribute.addAttribute(world_ctl, "is_ctl", "bool", keyable=False)
        tag = node.add_controller_tag(world_ctl, None)
        world_ref = primitive.addTransform(world_ctl, "world_ref", m=m)
        attribute.setKeyableAttributes(world_ref, [])
        attribute.addAttribute(world_ref, "is_ref", "bool", keyable=False)
        self.ins["root"] = root
        self.ins["geo_root"] = geo
        self.ins["blocks_root"] = blocks
        self.ins["joints_root"] = joints
        self.ins["ctls"] = [world_ctl]
        self.ins["refs"] = [world_ref]
        self.ins["jnts"] = None
        self.ins["root_set"] = pm.sets(name=f"{self.block['name']}_set", empty=True)
        self.ins["geo_set"] = pm.sets(name="geo_set", empty=True)
        self.ins["controls_set"] = pm.sets(name="controls_set", empty=True)
        self.ins["deformer_set"] = pm.sets(name="deformer_set", empty=True)
        pm.sets(self.ins["root_set"], addElement=(self.ins["geo_set"],
                                                  self.ins["controls_set"],
                                                  self.ins["deformer_set"]))
        pm.sets(self.ins["geo_set"], addElement=geo)

        attribute.addEnumAttribute(self.ins["root"], "controls_switch", 0, [" "])
        attribute.addAttribute(self.ins["root"], "controls_vis", "bool", True)
        attribute.addAttribute(self.ins["root"], "controls_mouseover", "bool", False)
        attribute.addAttribute(self.ins["root"], "controls_on_playback_vis", "bool", False)
        attribute.addAttribute(self.ins["root"], "controls_x_ray", "bool", False)
        attribute.addEnumAttribute(self.ins["root"], "joints_switch", 0, [" "])
        attribute.addAttribute(self.ins["root"], "joints_vis", "bool", False)
        attribute.addAttribute(self.ins["root"], "joints_label_vis", "bool", False)

        pm.connectAttr(self.ins["root"].attr("controls_vis"), self.ins["blocks_root"].attr("v"))
        pm.connectAttr(self.ins["root"].attr("controls_on_playback_vis"),
                       self.ins["blocks_root"].attr("hideOnPlayback"))
        pm.connectAttr(self.ins["root"].attr("joints_vis"), self.ins["joints_root"].attr("v"))
        condition = pm.createNode("condition")
        pm.connectAttr(self.ins["root"].attr("controls_mouseover"), condition.attr("firstTerm"))
        condition.attr("secondTerm").set(1)
        condition.attr("operation").set(0)
        condition.attr("colorIfTrueR").set(2)
        condition.attr("colorIfFalseR").set(0)
        pm.connectAttr(condition.attr("outColorR"), tag.attr("visibilityMode"))

        attribute.lockAttribute(self.ins["root"])
        attribute.setNotKeyableAttributes(self.ins["root"], ["controls_switch",
                                                             "controls_vis",
                                                             "controls_mouseover",
                                                             "controls_on_playback_vis",
                                                             "controls_x_ray",
                                                             "joints_switch",
                                                             "joints_vis",
                                                             "joints_label_vis"])
        attribute.lockAttribute(self.ins["geo_root"])
        attribute.lockAttribute(self.ins["blocks_root"])
        attribute.lockAttribute(self.ins["joints_root"])


class Attributes(AbstractAttributes):

    def __init__(self, block):
        super(Attributes, self).__init__(block=block)

    def process(self, context):
        super(Attributes, self).process(context=context)


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
