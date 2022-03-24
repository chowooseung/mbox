# -*- coding: utf-8 -*-

# maya
import pymel.core as pm

# mbox
from mbox.lego.lib import (
    AbstractObjects,
    AbstractAttributes,
    AbstractOperators,
    AbstractConnection
)

# mgear
from mgear.core import (
    attribute,
    transform,
    vector,
    primitive
)


class Objects(AbstractObjects):

    def __init__(self, block):
        super(Objects, self).__init__(block=block)

    def process(self, context):
        super(Objects, self).process(context=context)

        root_v, arm0_v, arm2_v, arm1_v = [pm.datatypes.Vector(x[-1][:-1]) for x in self.block["transforms"]]
        root = self.create_root(context, m=transform.getTransformFromPos(root_v))
        ik_ctl_grp = pm.group(name=self.get_name(typ=False, description="ik_ctl", extension="grp"), empty=True)
        fk_ctl_grp = pm.group(name=self.get_name(typ=False, description="ik_ctl", extension="grp"), empty=True)
        pm.parent(ik_ctl_grp, fk_ctl_grp, root)
        ik_ctl_grp.attr("t").set((0, 0, 0))
        ik_ctl_grp.attr("r").set((0, 0, 0))
        fk_ctl_grp.attr("t").set((0, 0, 0))
        fk_ctl_grp.attr("r").set((0, 0, 0))
        self.ins["ik_ctl_grp"] = ik_ctl_grp
        self.ins["fk_ctl_grp"] = fk_ctl_grp

        normal = vector.getPlaneNormal(root_v, arm0_v, arm1_v)
        t = transform.getTransformLookingAt(root_v, arm0_v, normal, "xz", self.block.negate)
        fk_color = self.get_ctl_color("fk")
        fk_attr = ["tx", "ty", "tz", "rx", "ry", "rz", "ro"]
        fk0_jnt = primitive.addJoint(root, self.get_name(typ=False, description="fk0", extension="jnt"), m=t, vis=False)
        ik0_jnt = primitive.addJoint(root, self.get_name(typ=False, description="ik0", extension="jnt"), m=t, vis=False)
        fk0_ctl = self.create_ctl(context, fk_ctl_grp, m=t, parent_ctl=None, description="fk0", color=fk_color, ctl_attr=fk_attr)
        fk0_ref = self.create_ref(context, fk0_ctl, description="fk0", m=t)
        blend0_jnt = primitive.addJoint(root, self.get_name(typ=False, description="blend0", extension="jnt"), m=t, vis=False)
        upper0_jnt = primitive.addJoint(root, self.get_name(typ=False, description="upperSC0", extension="jnt"), m=t, vis=False)

        t = transform.getTransformLookingAt(arm0_v, arm1_v, normal, "xz", self.block.negate)
        fk1_jnt = primitive.addJoint(fk0_jnt, self.get_name(typ=False, description="fk1", extension="jnt"), m=t, vis=False)
        ik1_jnt = primitive.addJoint(ik0_jnt, self.get_name(typ=False, description="ik1", extension="jnt"), m=t, vis=False)
        fk1_ctl = self.create_ctl(context, fk0_ref, m=t, parent_ctl=fk0_ctl, description="fk1", color=fk_color, ctl_attr=fk_attr)
        fk1_ref = self.create_ref(context, fk1_ctl, description="fk1", m=t)
        blend1_jnt = primitive.addJoint(blend0_jnt, self.get_name(typ=False, description="blend1", extension="jnt"), m=t, vis=False)
        upper1_jnt = primitive.addJoint(upper0_jnt, self.get_name(typ=False, description="upperSC1", extension="jnt"), m=t, vis=False)
        lower_rot0_jnt = primitive.addJoint(root, self.get_name(typ=False, description="lowerRotSC0", extension="jnt"), m=t, vis=False)
        lower_fix0_jnt = primitive.addJoint(root, self.get_name(typ=False, description="lowerFixSC0", extension="jnt"), m=t, vis=False)

        t = transform.getTransformLookingAt(arm1_v, arm2_v, normal, "xz", self.block.negate)
        fk2_jnt = primitive.addJoint(fk1_jnt, self.get_name(typ=False, description="fk2Ref", extension="jnt"), m=t, vis=False)
        ik2_jnt = primitive.addJoint(ik1_jnt, self.get_name(typ=False, description="ik2Ref", extension="jnt"), m=t, vis=False)
        fk2_ctl = self.create_ctl(context, fk1_ref, m=t, parent_ctl=fk1_ctl, description="fk2", color=fk_color, ctl_attr=fk_attr)
        fk2_ref = self.create_ref(context, fk2_ctl, description="fk2", m=t)
        blend2_jnt = primitive.addJoint(blend1_jnt, self.get_name(typ=False, description="blend2Ref", extension="jnt"), m=t, vis=False)
        lower_rot1_jnt = primitive.addJoint(lower_rot0_jnt, self.get_name(typ=False, description="lowerRotSC1", extension="jnt"), m=t, vis=False)
        lower_fix1_jnt = primitive.addJoint(lower_fix0_jnt, self.get_name(typ=False, description="lowerFixSC1", extension="jnt"), m=t, vis=False)

        pm.makeIdentity(fk0_jnt, apply=True, rotate=True)
        pm.makeIdentity(ik0_jnt, apply=True, rotate=True)
        pm.makeIdentity(blend0_jnt, apply=True, rotate=True)
        pm.makeIdentity(upper0_jnt, apply=True, rotate=True)
        pm.makeIdentity(lower_rot0_jnt, apply=True, rotate=True)
        pm.makeIdentity(lower_fix0_jnt, apply=True, rotate=True)
        # fk2_jnt.attr("jointOrient").set((0, 0, 0))
        # ik2_jnt.attr("jointOrient").set((0, 0, 0))
        # blend2_jnt.attr("jointOrient").set((0, 0, 0))
        upper1_jnt.attr("jointOrient").set((0, 0, 0))
        lower_rot1_jnt.attr("jointOrient").set((0, 0, 0))
        lower_fix1_jnt.attr("jointOrient").set((0, 0, 0))
        pm.parent(lower_rot0_jnt, upper1_jnt)
        pm.parent(lower_fix0_jnt, upper1_jnt)

        t = transform.getTransformFromPos(root_v)
        ik_color = self.get_ctl_color("ik")
        ik0_ctl = self.create_ctl(context, ik_ctl_grp, m=t, parent_ctl=None, description="ik0", color=ik_color, ctl_attr=["tx", "ty", "tz"])
        ik0_ref = self.create_ref(context, ik0_ctl, description="ik0", m=t)

        v = arm1_v - root_v
        v = normal ^ v
        v.normalize()
        v *= vector.getDistance(arm1_v, arm0_v) * .8
        v += arm0_v
        t = transform.getTransformFromPos(v)
        cns = True if self.block["upv_ref_array"] else False
        ik_upv_ctl = self.create_ctl(context, ik_ctl_grp, m=t, parent_ctl=ik0_ctl, description="ikUpv", color=ik_color, ctl_attr=["tx", "ty", "tz"], cns=cns)
        ik_upv_ref = self.create_ref(context, ik_upv_ctl, description="ikUpv", m=t)

        t = transform.getTransformFromPos(arm1_v)
        cns = True if self.block["ik_ref_array"] else False
        ik_ctl = self.create_ctl(context, ik_ctl_grp, m=t, parent_ctl=ik_upv_ctl, description="ik", color=ik_color, ctl_attr=["tx", "ty", "tz", "rx", "ry", "rz", "ro"], cns=cns)
        ik_ref = self.create_ref(context, ik_ctl, m=t, description="ik")

        self.ins["pairblend"] = list()
        pairblend0 = pm.createNode("pairBlend")
        pm.connectAttr(ik0_jnt.attr("t"), pairblend0.attr("inTranslate1"))
        pm.connectAttr(ik0_jnt.attr("r"), pairblend0.attr("inRotate1"))
        pm.connectAttr(fk0_jnt.attr("t"), pairblend0.attr("inTranslate2"))
        pm.connectAttr(fk0_jnt.attr("r"), pairblend0.attr("inRotate2"))
        pm.connectAttr(pairblend0.attr("outTranslate"), blend0_jnt.attr("t"))
        pm.connectAttr(pairblend0.attr("outRotate"), blend0_jnt.attr("r"))

        pairblend1 = pm.createNode("pairBlend")
        pm.connectAttr(ik1_jnt.attr("t"), pairblend1.attr("inTranslate1"))
        pm.connectAttr(ik1_jnt.attr("r"), pairblend1.attr("inRotate1"))
        pm.connectAttr(fk1_jnt.attr("t"), pairblend1.attr("inTranslate2"))
        pm.connectAttr(fk1_jnt.attr("r"), pairblend1.attr("inRotate2"))
        pm.connectAttr(pairblend1.attr("outTranslate"), blend1_jnt.attr("t"))
        pm.connectAttr(pairblend1.attr("outRotate"), blend1_jnt.attr("r"))

        pairblend2 = pm.createNode("pairBlend")
        pm.connectAttr(ik2_jnt.attr("t"), pairblend2.attr("inTranslate1"))
        pm.connectAttr(ik2_jnt.attr("r"), pairblend2.attr("inRotate1"))
        pm.connectAttr(fk2_jnt.attr("t"), pairblend2.attr("inTranslate2"))
        pm.connectAttr(fk2_jnt.attr("r"), pairblend2.attr("inRotate2"))
        pm.connectAttr(pairblend2.attr("outTranslate"), blend2_jnt.attr("t"))
        pm.connectAttr(pairblend2.attr("outRotate"), blend2_jnt.attr("r"))

        self.ins["pairblend"].append(pairblend0)
        self.ins["pairblend"].append(pairblend1)
        self.ins["pairblend"].append(pairblend2)

        pm.parentConstraint(fk0_ref, fk0_jnt)
        pm.parentConstraint(fk1_ref, fk1_jnt)
        pm.parentConstraint(fk2_ref, fk2_jnt)
        pm.pointConstraint(ik0_ref, ik0_jnt)
        pm.orientConstraint(ik_ref, ik2_jnt, maintainOffset=True)

        ikh_rp, eff0 = pm.ikHandle(name=self.get_name(typ=False, description="rp", extension="ikh"), startJoint=ik0_jnt, endEffector=ik2_jnt, solver="ikRPsolver")
        ikh_rp.hide()
        pm.parent(ikh_rp, ik_ref)
        pm.poleVectorConstraint(ik_upv_ref, ikh_rp)
        upper_ikh_sc, eff1 = pm.ikHandle(name=self.get_name(typ=False, description="upperSc", extension="ikh"), startJoint=upper0_jnt, endEffector=upper1_jnt, solver="ikSCsolver")
        upper_ikh_sc.hide()
        pm.parent(upper_ikh_sc, root)
        pm.pointConstraint(blend1_jnt, upper_ikh_sc)
        lower_rot_ikh_sc, eff2 = pm.ikHandle(name=self.get_name(typ=False, description="lowerRotSc", extension="ikh"), startJoint=lower_rot0_jnt, endEffector=lower_rot1_jnt, solver="ikSCsolver")
        lower_rot_ikh_sc.hide()
        pm.parent(lower_rot_ikh_sc, root)
        pm.parentConstraint(blend2_jnt, lower_rot_ikh_sc)
        # pm.orientConstraint(blend2_jnt, lower1_jnt)
        pm.pointConstraint(blend0_jnt, upper0_jnt)
        pm.orientConstraint(blend0_jnt, upper1_jnt)
        lower_fix_ikh_sc, eff2 = pm.ikHandle(name=self.get_name(typ=False, description="lowerFixSc", extension="ikh"), startJoint=lower_fix0_jnt, endEffector=lower_fix1_jnt, solver="ikSCsolver")
        lower_fix_ikh_sc.hide()
        pm.parent(lower_fix_ikh_sc, root)
        pm.pointConstraint(blend2_jnt, lower_fix_ikh_sc)
        pm.orientConstraint(blend0_jnt, lower_fix_ikh_sc)

        index = 0
        ref = self.create_ref(context, root, description=f"{index}", m=pm.datatypes.Matrix())
        attribute.setKeyableAttributes(ref, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
        pm.parentConstraint(upper0_jnt, ref)
        pre_jnt = self.create_jnt(context, parent=None, description=f"{index}", ref=ref)
        for i in range(int(self.block["div"])):
            index = i + 1
            ref = self.create_ref(context, root, description=f"{index}", m=pm.datatypes.Matrix())
            attribute.setKeyableAttributes(ref, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
            cons = pm.parentConstraint(upper0_jnt, upper1_jnt, ref)
            cons.attr("interpType").set(2)
            weight1, weight2 = pm.parentConstraint(cons, query=True, weightAliasList=True)
            weight2.set((i + 1) / (int(self.block["div"]) + 1))
            weight1.set(1 - ((i + 1) / (int(self.block["div"]) + 1)))
            pre_jnt = self.create_jnt(context, parent=pre_jnt, description=f"{index}", ref=ref)
        index += 1
        ref = self.create_ref(context, root, description=f"{index}", m=pm.datatypes.Matrix())
        attribute.setKeyableAttributes(ref, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
        pm.parentConstraint(lower_fix0_jnt, ref)
        pre_jnt = self.create_jnt(context, parent=pre_jnt, description=f"{index}", ref=ref)
        for i in range(int(self.block["div"])):
            index = i + 1 + self.block["div"] + 2
            ref = self.create_ref(context, root, description=f"{index}", m=pm.datatypes.Matrix())
            attribute.setKeyableAttributes(ref, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
            cons = pm.parentConstraint(lower_fix0_jnt, lower_rot1_jnt, ref)
            cons.attr("interpType").set(2)
            weight1, weight2 = pm.parentConstraint(cons, query=True, weightAliasList=True)
            weight2.set((i + 1) / (int(self.block["div"]) + 1))
            weight1.set(1 - ((i + 1) / (int(self.block["div"]) + 1)))
            pre_jnt = self.create_jnt(context, parent=pre_jnt, description=f"{index}", ref=ref)
        index += 1
        ref = self.create_ref(context, root, description=f"{index}", m=pm.datatypes.Matrix())
        attribute.setKeyableAttributes(ref, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"])
        pm.parentConstraint(blend2_jnt, ref)
        pre_jnt = self.create_jnt(context, parent=pre_jnt, description=f"{index}", ref=ref)


class Attributes(AbstractAttributes):

    def __init__(self, block):
        super(Attributes, self).__init__(block=block)

    def process(self, context):
        super(Attributes, self).process(context=context)

        ikfk_attr = self.create_attr(context, longName="ikfk", attType="float", value=0, minValue=0, maxValue=1)
        pm.connectAttr(ikfk_attr, self.ins["pairblend"][0].attr("weight"))
        pm.connectAttr(ikfk_attr, self.ins["pairblend"][1].attr("weight"))
        pm.connectAttr(ikfk_attr, self.ins["pairblend"][2].attr("weight"))
        reverse = pm.createNode("reverse")
        pm.connectAttr(ikfk_attr, reverse.attr("inputX"))
        pm.connectAttr(reverse.attr("outputX"), self.ins["ik_ctl_grp"].attr("v"))
        pm.connectAttr(ikfk_attr, self.ins["fk_ctl_grp"].attr("v"))


class Operators(AbstractOperators):

    def __init__(self, block):
        super(Operators, self).__init__(block=block)

    def process(self, context):
        super(Operators, self).process(context=context)

        if self.block["ik_ref_array"]:
            self.space_switch(context=context, ctl=self.ins["ctls"][4], target=self.ins["ui_host"], attr_name="space_switch")
        if self.block["upv_ref_array"]:
            self.space_switch(context=context, ctl=self.ins["ctls"][5], target=self.ins["ui_host"], attr_name="space_switch")
        # if self.block["elbow_ref_array"]:
        #     self.space_switch(context=context, ctl=self.ins["ctls"][6], target=self.ins["ui_host"], attr_name="space_switch")


class Connection(AbstractConnection):

    def __init__(self, block):
        super(Connection, self).__init__(block=block)

    def process(self, context):
        super(Connection, self).process(context=context)
