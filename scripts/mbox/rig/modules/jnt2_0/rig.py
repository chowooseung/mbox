# -*- coding: utf-8 -*-

# mbox
from mbox.rig import build
from . import Contributor

# mgear
from mgear.core import attribute, primitive, transform, vector, node, applyop

# maya
from pymel import core as pm


class Rig(build.Instance, Contributor):

    def objects(self):
        comp = self.component
        naming = comp.naming
        pos0_v, pos1_v, pos2_v, pos3_v = [pm.datatypes.Vector(x[-1][:-1]) for x in comp["guide_transforms"]]
        root = self.add_root(m=transform.getTransformFromPos(pos0_v))
        normal = vector.getPlaneNormal(pos0_v, pos1_v, pos2_v)
        fk_color = self.get_ctl_color("fk")
        ik_color = self.get_ctl_color("ik")
        fk_attr = ["tx", "ty", "tz", "rx", "ry", "rz", "ro"]
        kwargs = {"w": 1, "h": 1, "d": 1, "icon": "cube"}

        pos0_m = transform.getTransformLookingAt(pos0_v, pos1_v, normal, "xz", comp.negate)
        pos1_m = transform.getTransformLookingAt(pos1_v, pos2_v, normal, "xz", comp.negate)
        pos2_m = transform.getTransformLookingAt(pos2_v, pos3_v, normal, "xz", comp.negate)
        v = pos2_v - pos0_v
        v = normal ^ v
        v.normalize()
        v *= vector.getDistance(pos2_v, pos1_v) * .8
        v += pos1_v
        upv_m = transform.getTransformFromPos(v)
        self.fk0_jnt, self.fk1_jnt, self.fk2_jnt = primitive.add2DChain(root,
                                                                        naming.name(comp, False, "fk%s", "jnt"),
                                                                        [pos0_v, pos1_v, pos2_v],
                                                                        normal,
                                                                        comp.negate,
                                                                        False)
        self.ik0_jnt, self.ik1_jnt, self.ik2_jnt = primitive.add2DChain(root,
                                                                        naming.name(comp, False, "ik%s", "jnt"),
                                                                        [pos0_v, pos1_v, pos2_v],
                                                                        normal,
                                                                        comp.negate,
                                                                        False)
        self.blend0_jnt, self.blend1_jnt, self.blend2_jnt = primitive.add2DChain(root,
                                                                                 naming.name(comp,
                                                                                             False,
                                                                                             "blend%s",
                                                                                             "jnt"),
                                                                                 [pos0_v, pos1_v, pos2_v],
                                                                                 normal,
                                                                                 comp.negate,
                                                                                 False)

        self.fk0_ctl = self.add_ctl(root,
                                    None,
                                    fk_color,
                                    fk_attr,
                                    None,
                                    "fk0",
                                    False,
                                    m=pos0_m,
                                    **kwargs)
        self.fk0_loc = self.add_loc(self.fk0_ctl, "fk0", m=pos0_m)
        self.fk1_ctl = self.add_ctl(self.fk0_loc,
                                    self.fk0_ctl,
                                    fk_color,
                                    fk_attr,
                                    None,
                                    "fk1",
                                    False,
                                    m=pos1_m,
                                    **kwargs)
        self.fk1_loc = self.add_loc(self.fk1_ctl, "fk1", m=pos1_m)
        self.fk2_ctl = self.add_ctl(self.fk1_loc,
                                    self.fk1_ctl,
                                    fk_color,
                                    fk_attr,
                                    None,
                                    "fk2",
                                    False,
                                    m=pos2_m,
                                    **kwargs)
        self.fk2_loc = self.add_loc(self.fk2_ctl, "fk2", m=pos2_m)

        self.upper0_jnt, self.upper1_jnt = primitive.add2DChain(root,
                                                                naming.name(comp, False, "upper%sSC", "jnt"),
                                                                [pos0_v, pos1_v],
                                                                normal,
                                                                comp.negate,
                                                                False)
        self.lower_rot0_jnt, self.lower_rot1_jnt = primitive.add2DChain(self.upper1_jnt,
                                                                        naming.name(comp, False, "lowerRot%sSC", "jnt"),
                                                                        [pos1_v, pos2_v],
                                                                        normal,
                                                                        comp.negate,
                                                                        False)
        self.lower_fix0_jnt, self.lower_fix1_jnt = primitive.add2DChain(self.upper1_jnt,
                                                                        naming.name(comp, False, "lowerFix%sSC", "jnt"),
                                                                        [pos1_v, pos2_v],
                                                                        normal,
                                                                        comp.negate,
                                                                        False)
        m = transform.getTransformFromPos(pos0_v)
        self.ik0_ctl = self.add_ctl(root,
                                    None,
                                    ik_color,
                                    ["tx", "ty", "tz"],
                                    None,
                                    "ik0",
                                    False,
                                    m=m,
                                    **kwargs)
        self.ik0_loc = self.add_loc(self.ik0_ctl, "ik0", m=m)
        self.ik_upv_ctl = self.add_ctl(root,
                                       self.ik0_ctl,
                                       ik_color,
                                       ["tx", "ty", "tz"],
                                       None,
                                       "ikUpv",
                                       True if comp["upv_ref_array"] else False,
                                       m=upv_m,
                                       **kwargs)
        self.ik_upv_loc = self.add_loc(self.ik_upv_ctl, "ikUpv", m=upv_m)
        m = transform.getTransformFromPos(pos2_v)
        self.ik_ctl = self.add_ctl(root,
                                   self.ik_upv_ctl,
                                   ik_color,
                                   ["tx", "ty", "tz", "rx", "ry", "rz", "ro"],
                                   None,
                                   "ik",
                                   True if comp["ik_ref_array"] else False,
                                   m=m,
                                   **kwargs)
        self.ik_loc = self.add_loc(self.ik_ctl, "ik", m=m)

        index = 0
        ref = self.add_ref(root, description=f"{index}", m=pm.datatypes.Matrix())
        pm.parentConstraint(self.upper0_jnt, ref)
        pre_jnt = self.add_jnt(None, ref, naming.name(comp, True, f"{index}"), True)
        for i in range(int(comp["div"])):
            index = i + 1
            ref = self.add_ref(root, description=f"{index}", m=pm.datatypes.Matrix())
            cons = pm.parentConstraint(self.upper0_jnt, self.upper1_jnt, ref)
            cons.attr("interpType").set(2)
            weight1, weight2 = pm.parentConstraint(cons, query=True, weightAliasList=True)
            weight2.set((i + 1) / (int(comp["div"]) + 1))
            weight1.set(1 - ((i + 1) / (int(comp["div"]) + 1)))
            pre_jnt = self.add_jnt(pre_jnt, ref, naming.name(comp, True, f"{index}"), True)
        index += 1
        ref = self.add_ref(root, description=f"{index}", m=pm.datatypes.Matrix())
        pm.parentConstraint(self.lower_fix0_jnt, ref)
        pre_jnt = self.add_jnt(pre_jnt, ref, naming.name(comp, True, f"{index}"), True)
        for i in range(int(comp["div"])):
            index = i + 1 + comp["div"] + 2
            ref = self.add_ref(root, description=f"{index}", m=pm.datatypes.Matrix())
            cons = pm.parentConstraint(self.lower_fix0_jnt, self.lower_rot1_jnt, ref)
            cons.attr("interpType").set(2)
            weight1, weight2 = pm.parentConstraint(cons, query=True, weightAliasList=True)
            weight2.set((i + 1) / (int(comp["div"]) + 1))
            weight1.set(1 - ((i + 1) / (int(comp["div"]) + 1)))
            pre_jnt = self.add_jnt(pre_jnt, ref, naming.name(comp, True, f"{index}"), True)
        index += 1
        ref = self.add_ref(root, description=f"{index}", m=pm.datatypes.Matrix())
        pm.parentConstraint(self.blend2_jnt, ref)
        pre_jnt = self.add_jnt(pre_jnt, ref, naming.name(comp, True, f"{index}"), True)

    def attributes(self):
        ui_host = self.ui_host
        self.blend_attr = attribute.addAttribute(ui_host, "ik_fk_blend", "float", 0, minValue=0, maxValue=1,
                                                 keyable=True)

    def operators(self):
        naming = self.component.naming
        blend_rev = node.createReverseNode(self.blend_attr)
        node.createPairBlend(self.ik0_jnt, self.fk0_jnt, self.blend_attr, 1, self.blend0_jnt)
        node.createPairBlend(self.ik1_jnt, self.fk1_jnt, self.blend_attr, 1, self.blend1_jnt)
        node.createPairBlend(self.ik2_jnt, self.fk2_jnt, self.blend_attr, 1, self.blend2_jnt)
        for ctl in [self.fk0_ctl, self.fk1_ctl, self.fk2_ctl]:
            for shp in ctl.getShapes():
                pm.connectAttr(self.blend_attr, shp.attr("v"))
        for ctl in [self.ik_ctl, self.ik0_ctl, self.ik_upv_ctl]:
            for shp in ctl.getShapes():
                pm.connectAttr(blend_rev.attr("outputX"), shp.attr("v"))

        pm.parentConstraint(self.fk0_loc, self.fk0_jnt)
        pm.parentConstraint(self.fk1_loc, self.fk1_jnt)
        pm.parentConstraint(self.fk2_loc, self.fk2_jnt)
        pm.pointConstraint(self.ik0_loc, self.ik0_jnt)
        pm.orientConstraint(self.ik_loc, self.ik2_jnt, maintainOffset=True)

        self.ikh_rp = primitive.addIkHandle(self.ik_loc,
                                            naming.name(self.component,
                                                        False,
                                                        "RP",
                                                        "ikh"),
                                            [self.ik0_jnt, self.ik2_jnt],
                                            "ikRPsolver",
                                            self.ik_upv_loc)
        self.upper_ikh_sc = primitive.addIkHandle(self.root,
                                                  naming.name(self.component,
                                                              False,
                                                              "upperSC",
                                                              "ikh"),
                                                  [self.upper0_jnt, self.upper1_jnt],
                                                  "ikSCsolver")
        pm.pointConstraint(self.blend1_jnt, self.upper_ikh_sc)
        self.lower_rot_ikh_sc = primitive.addIkHandle(self.root,
                                                      naming.name(self.component,
                                                                  False,
                                                                  "lowerRotSC",
                                                                  "ikh"),
                                                      [self.lower_rot0_jnt, self.lower_rot1_jnt],
                                                      "ikSCsolver")
        pm.parentConstraint(self.blend2_jnt, self.lower_rot_ikh_sc)
        pm.pointConstraint(self.blend0_jnt, self.upper0_jnt)
        pm.orientConstraint(self.blend0_jnt, self.upper1_jnt)
        self.lower_fix_ikh_sc = primitive.addIkHandle(self.root,
                                                      naming.name(self.component,
                                                                  False,
                                                                  "lowerFixSC",
                                                                  "ikh"),
                                                      [self.lower_fix0_jnt, self.lower_fix1_jnt],
                                                      "ikSCsolver")
        pm.pointConstraint(self.blend2_jnt, self.lower_fix_ikh_sc)
        pm.orientConstraint(self.blend0_jnt, self.lower_fix_ikh_sc)

    def connector(self):
        """ specify parent component connector """
