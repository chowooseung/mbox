# -*- coding: utf-8 -*-

# mbox
from mbox.box import build
from . import Contributor

# mgear
from mgear.core import attribute, primitive

# maya
from pymel import core as pm


class Rig(build.Instance, Contributor):

    def __init__(self, context, component):
        super(Rig, self).__init__(context=context, component=component)

    def objects(self):
        root = self.add_root()
        attribute.addAttribute(root, "ctl_vis", "bool", True)
        attribute.addAttribute(root, "ctl_mouseover", "bool", False)
        attribute.addAttribute(root, "ctl_on_playback_vis", "bool", False)
        attribute.addAttribute(root, "ctl_x_ray", "bool", False)
        attribute.addAttribute(root, "jnt_vis", "bool", False)
        attribute.addAttribute(root, "jnt_label_vis", "bool", False)
        attribute.addAttribute(root, "character_sets", "message")

        self.geo = primitive.addTransform(root, "geo")
        self.control_rigs = primitive.addTransform(root, "controls")
        self.jnts_grp = primitive.addTransform(root, "deform")
        self.character_sets = pm.sets(name=f"{self.component['name']}_sets", empty=True)
        geo_sets = pm.sets(name="geo_sets", empty=True)
        ctls_sets = pm.sets(name="controllers_sets", empty=True)
        jnts_sets = pm.sets(name="deforms_sets", empty=True)
        pm.sets(self.character_sets, addElement=jnts_sets)
        pm.sets(self.character_sets, addElement=ctls_sets)
        pm.sets(self.character_sets, addElement=geo_sets)
        pm.sets(geo_sets, addElement=self.geo)
        ik_color = self.get_ctl_color("ik")
        kwargs = {"icon": "circle", "w": 1, "h": 1, "d": 1}
        if self.component["world_ctl_name"]:
            kwargs.update(name=self.component["world_ctl_name"])
        self.ctl = self.add_ctl(self.control_rigs,
                                None,
                                ik_color,
                                None,
                                None,
                                "",
                                False,
                                pm.datatypes.Matrix(),
                                **kwargs)
        ref = self.add_ref(self.ctl, "", pm.datatypes.Matrix())
        if self.component["world_jnt"]:
            self.add_jnt(None, ref, self.component.jnt_names[0], True)

    def attributes(self):
        attribute.lockAttribute(self.root)
        attribute.setNotKeyableAttributes(self.root, ["ctl_vis",
                                                      "ctl_mouseover",
                                                      "ctl_on_playback_vis",
                                                      "ctl_x_ray",
                                                      "jnt_vis",
                                                      "jnt_label_vis"])

    def operators(self):
        pm.connectAttr(self.root.attr("ctl_vis"), self.control_rigs.attr("v"))
        pm.connectAttr(self.root.attr("ctl_on_playback_vis"), self.control_rigs.attr("hideOnPlayback"))
        pm.connectAttr(self.root.attr("jnt_vis"), self.jnts_grp.attr("v"))
        attribute.lockAttribute(self.geo)
        attribute.lockAttribute(self.control_rigs)
        attribute.lockAttribute(self.jnts_grp)
        tag = pm.PyNode(pm.controller(self.ctl, query=True)[0])
        condition = pm.createNode("condition")
        pm.connectAttr(self.root.attr("ctl_mouseover"), condition.attr("firstTerm"))
        condition.attr("secondTerm").set(1)
        condition.attr("operation").set(0)
        condition.attr("colorIfTrueR").set(2)
        condition.attr("colorIfFalseR").set(0)
        pm.connectAttr(condition.attr("outColorR"), tag.attr("visibilityMode"))
        pm.connectAttr(self.character_sets.attr("message"), self.root.attr("character_sets"))

    def connector(self):
        """ specify parent component connector """
