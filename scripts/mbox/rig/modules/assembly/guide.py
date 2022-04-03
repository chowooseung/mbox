# -*- coding: utf-8 -*-

# mbox
from mbox.rig import blueprint
from . import Contributor

# mgear
from mgear.core import attribute, primitive

# maya
from pymel import core as pm


class Guide(blueprint.Component, Contributor):

    @property
    def is_assembly(self):
        return True

    def __init__(self, network=None, parent=None, data=None):
        # load schema
        super(Guide, self).__init__(network=network, parent=parent, data=data)

    def pull(self):
        if not self.network:
            return
        self["oid"] = self.network.attr("oid").get()
        self["name"] = self.network.attr("name").get()
        self["comp_type"] = self.network.attr("comp_type").get()
        self["comp_name"] = self.network.attr("comp_name").get()
        self["comp_side"] = self.network.attr("comp_side").get(asString=True)
        self["comp_index"] = int(self.network.attr("comp_index").get())
        self["process"] = self.network.attr("process").get(asString=True)
        self["step"] = self.network.attr("step").get(asString=True)
        self["jnt_L_name"] = self.network.attr("jnt_L_name").get()
        self["jnt_R_name"] = self.network.attr("jnt_R_name").get()
        self["jnt_C_name"] = self.network.attr("jnt_C_name").get()
        self["ctl_L_name"] = self.network.attr("ctl_L_name").get()
        self["ctl_R_name"] = self.network.attr("ctl_R_name").get()
        self["ctl_C_name"] = self.network.attr("ctl_C_name").get()
        self["jnt_name_ext"] = self.network.attr("jnt_name_ext").get()
        self["ctl_name_ext"] = self.network.attr("ctl_name_ext").get()
        self["jnt_name_rule"] = self.network.attr("jnt_name_rule").get()
        self["ctl_name_rule"] = self.network.attr("ctl_name_rule").get()
        self["jnt_description_letter_case"] = self.network.attr("jnt_description_letter_case").get(asString=True)
        self["ctl_description_letter_case"] = self.network.attr("ctl_description_letter_case").get(asString=True)
        self["jnt_index_padding"] = int(self.network.attr("jnt_index_padding").get())
        self["ctl_index_padding"] = int(self.network.attr("ctl_index_padding").get())
        self["world_ctl_name"] = self.network.attr("world_ctl_name").get()
        self["world_jnt_name"] = self.network.attr("world_jnt_name").get()
        self["connect_jnt"] = self.network.attr("connect_jnt").get()
        self["force_uni_scale"] = self.network.attr("force_uni_scale").get()
        self["run_pre_custom_step"] = self.network.attr("run_pre_custom_step").get()
        self["pre_custom_step"] = self.network.attr("pre_custom_step").get()
        self["run_post_custom_step"] = self.network.attr("run_post_custom_step").get()
        self["post_custom_step"] = self.network.attr("post_custom_step").get()
        self["l_color_fk"] = self.network.attr("l_color_fk").get()
        self["l_color_ik"] = self.network.attr("l_color_ik").get()
        self["r_color_fk"] = self.network.attr("r_color_fk").get()
        self["r_color_ik"] = self.network.attr("r_color_ik").get()
        self["c_color_fk"] = self.network.attr("c_color_fk").get()
        self["c_color_ik"] = self.network.attr("c_color_ik").get()
        self["use_RGB_color"] = self.network.attr("use_RGB_color").get()
        self["l_RGB_fk"] = self.network.attr("l_RGB_fk").get()
        self["l_RGB_ik"] = self.network.attr("l_RGB_ik").get()
        self["r_RGB_fk"] = self.network.attr("r_RGB_fk").get()
        self["r_RGB_ik"] = self.network.attr("r_RGB_ik").get()
        self["c_RGB_fk"] = self.network.attr("c_RGB_fk").get()
        self["c_RGB_ik"] = self.network.attr("c_RGB_ik").get()
        self["notes"] = self.network.attr("notes").get()

    def push(self):
        if not self.network:
            return
        self.network.attr("oid").set(self["oid"])
        self.network.attr("name").set(self["name"])
        self.network.attr("comp_type").set(self["comp_type"])
        self.network.attr("comp_name").set(self["comp_name"])
        self.network.attr("comp_side").set(self["comp_side"])
        self.network.attr("comp_index").set(self["comp_index"])
        self.network.attr("process").set(self["process"])
        self.network.attr("step").set(self["step"])
        self.network.attr("jnt_L_name").set(self["jnt_L_name"])
        self.network.attr("jnt_R_name").set(self["jnt_R_name"])
        self.network.attr("jnt_C_name").set(self["jnt_C_name"])
        self.network.attr("ctl_L_name").set(self["ctl_L_name"])
        self.network.attr("ctl_R_name").set(self["ctl_R_name"])
        self.network.attr("ctl_C_name").set(self["ctl_C_name"])
        self.network.attr("jnt_name_ext").set(self["jnt_name_ext"])
        self.network.attr("ctl_name_ext").set(self["ctl_name_ext"])
        self.network.attr("jnt_name_rule").set(self["jnt_name_rule"])
        self.network.attr("ctl_name_rule").set(self["ctl_name_rule"])
        self.network.attr("jnt_description_letter_case").set(self["jnt_description_letter_case"])
        self.network.attr("ctl_description_letter_case").set(self["ctl_description_letter_case"])
        self.network.attr("jnt_index_padding").set(self["jnt_index_padding"])
        self.network.attr("ctl_index_padding").set(self["ctl_index_padding"])
        self.network.attr("world_ctl_name").set(self["world_ctl_name"])
        self.network.attr("world_jnt_name").set(self["world_jnt_name"])
        self.network.attr("connect_jnt").set(self["connect_jnt"])
        self.network.attr("force_uni_scale").set(self["force_uni_scale"])
        self.network.attr("run_pre_custom_step").set(self["run_pre_custom_step"])
        self.network.attr("pre_custom_step").set(self["pre_custom_step"])
        self.network.attr("run_post_custom_step").set(self["run_post_custom_step"])
        self.network.attr("post_custom_step").set(self["post_custom_step"])
        self.network.attr("l_color_fk").set(self["l_color_fk"])
        self.network.attr("l_color_ik").set(self["l_color_ik"])
        self.network.attr("r_color_fk").set(self["r_color_fk"])
        self.network.attr("r_color_ik").set(self["r_color_ik"])
        self.network.attr("c_color_fk").set(self["c_color_fk"])
        self.network.attr("c_color_ik").set(self["c_color_ik"])
        self.network.attr("use_RGB_color").set(self["use_RGB_color"])
        self.network.attr("l_RGB_fk").set(self["l_RGB_fk"])
        self.network.attr("l_RGB_ik").set(self["l_RGB_ik"])
        self.network.attr("r_RGB_fk").set(self["r_RGB_fk"])
        self.network.attr("r_RGB_ik").set(self["r_RGB_ik"])
        self.network.attr("c_RGB_fk").set(self["c_RGB_fk"])
        self.network.attr("c_RGB_ik").set(self["c_RGB_ik"])
        self.network.attr("notes").set(self["notes"])

    def draw_network(self):
        self._network = pm.createNode("network")
        n = self.network
        attribute.addAttribute(n, "oid", "string", self["oid"])
        attribute.addAttribute(n, "guide", "message")
        attribute.addAttribute(n, "rig", "message")
        attribute.addAttribute(n, "name", "string", self["name"])
        attribute.addAttribute(n, "comp_type", "string", self["comp_type"])
        attribute.addAttribute(n, "comp_name", "string", self["comp_name"])
        attribute.addEnumAttribute(n, "comp_side", self["comp_side"], ["C", "L", "R"], keyable=False)
        attribute.addAttribute(n, "comp_index", "long", self["comp_index"], minValue=0, keyable=False)
        attribute.addEnumAttribute(n, "process", self["process"], ["WIP", "PUB"], keyable=False)
        attribute.addEnumAttribute(n, "step", self["step"],
                                   ["all", "preCustomStep", "objects", "feature", "connector", "cleanup",
                                    "postCustomStep"], keyable=False)
        attribute.addAttribute(n, "jnt_L_name", "string", self["jnt_L_name"])
        attribute.addAttribute(n, "jnt_R_name", "string", self["jnt_R_name"])
        attribute.addAttribute(n, "jnt_C_name", "string", self["jnt_C_name"])
        attribute.addAttribute(n, "ctl_L_name", "string", self["ctl_L_name"])
        attribute.addAttribute(n, "ctl_R_name", "string", self["ctl_R_name"])
        attribute.addAttribute(n, "ctl_C_name", "string", self["ctl_C_name"])
        attribute.addAttribute(n, "jnt_name_ext", "string", self["jnt_name_ext"])
        attribute.addAttribute(n, "ctl_name_ext", "string", self["ctl_name_ext"])
        attribute.addAttribute(n, "jnt_name_rule", "string", self["jnt_name_rule"])
        attribute.addAttribute(n, "ctl_name_rule", "string", self["ctl_name_rule"])
        attribute.addEnumAttribute(n, "jnt_description_letter_case", self["jnt_description_letter_case"],
                                   ["default", "lower", "upper", "capitalize"], keyable=False)
        attribute.addEnumAttribute(n, "ctl_description_letter_case", self["ctl_description_letter_case"],
                                   ["default", "lower", "upper", "capitalize"], keyable=False)
        attribute.addAttribute(n, "jnt_index_padding", "long", self["jnt_index_padding"], keyable=False)
        attribute.addAttribute(n, "ctl_index_padding", "long", self["ctl_index_padding"], keyable=False)
        attribute.addAttribute(n, "world_ctl_name", "string", self["world_ctl_name"])
        attribute.addAttribute(n, "world_jnt_name", "string", self["world_jnt_name"])
        attribute.addAttribute(n, "world_jnt", "bool", self["world_jnt"], keyable=False)
        attribute.addAttribute(n, "connect_jnt", "bool", self["connect_jnt"], keyable=False)
        attribute.addAttribute(n, "force_uni_scale", "bool", self["force_uni_scale"], keyable=False)
        attribute.addAttribute(n, "run_pre_custom_step", "bool", self["run_pre_custom_step"], keyable=False)
        attribute.addAttribute(n, "pre_custom_step", "string", self["pre_custom_step"])
        attribute.addAttribute(n, "run_post_custom_step", "bool", self["run_post_custom_step"], keyable=False)
        attribute.addAttribute(n, "post_custom_step", "string", self["post_custom_step"])
        attribute.addAttribute(n, "l_color_fk", "long", self["l_color_fk"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "l_color_ik", "long", self["l_color_ik"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "r_color_fk", "long", self["r_color_fk"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "r_color_ik", "long", self["r_color_ik"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "c_color_fk", "long", self["c_color_fk"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "c_color_ik", "long", self["c_color_ik"], minValue=0, maxValue=31, keyable=False)
        attribute.addAttribute(n, "use_RGB_color", "bool", self["use_RGB_color"], keyable=False)
        attribute.addColorAttribute(n, "l_RGB_fk", self["l_RGB_fk"], keyable=False)
        attribute.addColorAttribute(n, "l_RGB_ik", self["l_RGB_ik"], keyable=False)
        attribute.addColorAttribute(n, "r_RGB_fk", self["r_RGB_fk"], keyable=False)
        attribute.addColorAttribute(n, "r_RGB_ik", self["r_RGB_ik"], keyable=False)
        attribute.addColorAttribute(n, "c_RGB_fk", self["c_RGB_fk"], keyable=False)
        attribute.addColorAttribute(n, "c_RGB_ik", self["c_RGB_ik"], keyable=False)
        attribute.addAttribute(n, "notes", "string", self["notes"])
        pm.addAttr(n, longName="guide_transforms", type="message", multi=True)
        pm.addAttr(n, longName="ctls", type="message", multi=True)
        pm.addAttr(n, longName="jnts", type="message", multi=True)
        attribute.addAttribute(n, "script_node", "message")

    def draw_guide(self):
        if not self.network:
            self.draw_network()
        guide = primitive.addTransform(None, "guide", m=pm.datatypes.Matrix())
        attribute.addAttribute(guide, "is_guide", "bool", keyable=False)
        attribute.lockAttribute(guide, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
        attribute.setNotKeyableAttributes(guide, ["v"])
        pm.connectAttr(guide.attr("message"), self.network.attr("guide"), force=True)
        pm.connectAttr(guide.attr("worldMatrix")[0], self.network.attr("guide_transforms")[0], force=True)
        return guide
