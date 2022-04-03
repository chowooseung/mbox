# -*- coding: utf-8 -*-

# mbox
from mbox.rig import blueprint
from . import Contributor

# mgear
from mgear.core import attribute, primitive, transform

# maya
from pymel import core as pm


class Guide(blueprint.Component, Contributor):

    def __init__(self, network=None, parent=None, data=None, chain_number=0):
        # if chain self["guide_transforms"] = "#"

        # load schema
        super(Guide, self).__init__(network=network, parent=parent, data=data, chain_number=chain_number)

        # specify attribute setup
        root_m = transform.getTransformFromPos([0, 0, 0]).tolist()
        arm0_m = transform.getTransformFromPos([3, 0, -.01]).tolist()
        arm1_m = transform.getTransformFromPos([6, 0, 0]).tolist()
        arm2_m = transform.getTransformFromPos([7, 0, 0]).tolist()
        self["guide_transforms"] = [root_m, arm0_m, arm1_m, arm2_m]

    def pull(self):
        # if no network
        if not self.network:
            return

        # common attribute pull
        super(Guide, self).pull()

        # specify attribute pull
        self["ik_t_r"] = self.network.attr("ik_t_r").get()
        self["blend"] = self.network.attr("blend").get()
        self["mirror_ik"] = self.network.attr("mirror_ik").get()
        self["mirror_mid"] = self.network.attr("mirror_mid").get()
        self["ik_ref_array"] = self.network.attr("ik_ref_array").get()
        self["upv_ref_array"] = self.network.attr("upv_ref_array").get()
        self["elbow_ref_array"] = self.network.attr("elbow_ref_array").get()
        self["div"] = self.network.attr("div").get()

    def push(self):
        # if no network
        if not self.network:
            return

        # common attribute push
        super(Guide, self).push()

        # specify attribute push
        self.network.attr("ik_t_r").set(self["ik_t_r"])
        self.network.attr("blend").set(self["blend"])
        self.network.attr("mirror_ik").set(self["mirror_ik"])
        self.network.attr("mirror_mid").set(self["mirror_mid"])
        self.network.attr("ik_ref_array").set(self["ik_ref_array"])
        self.network.attr("upv_ref_array").set(self["upv_ref_array"])
        self.network.attr("elbow_ref_array").set(self["elbow_ref_array"])
        self.network.attr("div").set(self["div"])

    def draw_network(self):
        # new network, add common attribute
        super(Guide, self).draw_network()

        # specify attribute create
        attribute.addAttribute(self.network, "ik_t_r", "bool", self["ik_t_r"], keyable=False)
        attribute.addAttribute(self.network, "blend", "float", self["blend"], keyable=False)
        attribute.addAttribute(self.network, "mirror_ik", "bool", self["mirror_ik"], keyable=False)
        attribute.addAttribute(self.network, "mirror_mid", "bool", self["mirror_mid"], keyable=False)
        attribute.addAttribute(self.network, "ik_ref_array", "string", self["ik_ref_array"])
        attribute.addAttribute(self.network, "upv_ref_array", "string", self["upv_ref_array"])
        attribute.addAttribute(self.network, "elbow_ref_array", "string", self["elbow_ref_array"])
        attribute.addAttribute(self.network, "div", "long", self["div"], keyable=False)

    def draw_guide(self):
        # If self._network is None, add network
        super(Guide, self).draw_guide()

        # draw guide
        guide = self.add_root(m=pm.datatypes.Matrix(self["guide_transforms"][0]))
        elbow = self.add_loc(guide, m=pm.datatypes.Matrix(self["guide_transforms"][1]))
        lower = self.add_loc(elbow, m=pm.datatypes.Matrix(self["guide_transforms"][2]))
        hand = self.add_loc(lower, m=pm.datatypes.Matrix(self["guide_transforms"][3]))
        self.add_display_curve(guide, [guide, elbow, lower, hand])
        return guide
