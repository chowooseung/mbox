# -*- coding: utf-8 -*-

# mbox
from mbox.rig import blueprint
from . import Contributor

# maya
from pymel import core as pm

# mgear
from mgear.core import attribute, primitive


class Guide(blueprint.Component, Contributor):

    def __init__(self, network=None, parent=None, data=None):
        # load schema
        super(Guide, self).__init__(network=network, parent=parent, data=data)

        # specify attribute setup
        self["guide_transforms"].append(pm.datatypes.Matrix().tolist())

    def pull(self):
        # if no network
        if not self.network:
            return

        # common attribute pull
        super(Guide, self).pull()

        # specify attribute pull
        self["jnt_rig"] = self.network.attr("jnt_rig").get()
        self["leaf_jnt"] = self.network.attr("leaf_jnt").get()
        self["uni_scale"] = self.network.attr("uni_scale").get()
        self["mirror_behaviour"] = self.network.attr("mirror_behaviour").get()
        self["neutral_rotation"] = self.network.attr("neutral_rotation").get()
        self["icon"] = self.network.attr("icon").get()
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "ro", "sx", "sy", "sz"]
        self["key_able_attrs"] = [k for k in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]
                                  if self.network.attr(k).get()]
        self["default_rotate_order"] = self.network.attr("default_rotate_order").get()
        self["ik_ref_array"] = self.network.attr("ik_ref_array").get()
        self["ctl_size"] = self.network.attr("ctl_size").get()

    def push(self):
        # if no network
        if not self.network:
            return

        # common attribute push
        super(Guide, self).push()

        # specify attribute push
        self.network.attr("jnt_rig").set(self["jnt_rig"])
        self.network.attr("leaf_jnt").set(self["leaf_jnt"])
        self.network.attr("uni_scale").set(self["uni_scale"])
        self.network.attr("mirror_behaviour").set(self["mirror_behaviour"])
        self.network.attr("neutral_rotation").set(self["neutral_rotation"])
        self.network.attr("icon").set(self["icon"])
        [self.network.attr(a).set(True if a in self["key_able_attrs"] else False)
         for a in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]]
        self.network.attr("default_rotate_order").set(self["default_rotate_order"])
        self.network.attr("ik_ref_array").set(self["ik_ref_array"])
        self.network.attr("ctl_size").set(self["ctl_size"])

    def draw_network(self):
        # new network, add common attribute
        super(Guide, self).draw_network()
        n = self.network

        # specify attribute create
        attribute.addAttribute(n, "jnt_rig", "bool", self["jnt_rig"], keyable=False)
        attribute.addAttribute(n, "leaf_jnt", "bool", self["leaf_jnt"], keyable=False)
        attribute.addAttribute(n, "uni_scale", "bool", self["uni_scale"], keyable=False)
        attribute.addAttribute(n, "mirror_behaviour", "bool", self["mirror_behaviour"], keyable=False)
        attribute.addAttribute(n, "neutral_rotation", "bool", self["neutral_rotation"], keyable=False)
        attribute.addAttribute(n, "icon", "string", self["icon"], keyable=False)
        for attr in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]:
            attribute.addAttribute(self.network, attr, "bool",
                                   True if attr in self["key_able_attrs"] else False, keyable=False)
        attribute.addAttribute(n, "default_rotate_order", "long", self["default_rotate_order"], keyable=False)
        attribute.addAttribute(n, "ik_ref_array", "string", self["ik_ref_array"])
        attribute.addAttribute(n, "ctl_size", "float", self["ctl_size"], keyable=False)

    def draw_guide(self):
        # If self._network is None, add network
        super(Guide, self).draw_guide()

        # draw guide
        guide = self.add_root(m=pm.datatypes.Matrix(self["guide_transforms"][0]))
        size_ref = primitive.addTransform(guide, guide.nodeName().replace("root", "sizeRef"))
        size_ref.attr("t").set((0, 0, 1))
        size_ref.attr("r").set((0, 0, 0))
        size_ref.attr("s").set((1, 1, 1))
        attribute.lockAttribute(size_ref)
        return guide
