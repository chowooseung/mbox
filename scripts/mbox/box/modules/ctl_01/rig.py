# -*- coding: utf-8 -*-

# mbox
from mbox.box import build
from . import Contributor

# maya
from pymel import core as pm

# mgear
from mgear.core import transform


class Rig(build.Instance, Contributor):

    def objects(self):
        naming = self.component.naming

        # matrix
        if self.component["neutral_rotation"]:
            m = transform.getTransformFromPos(pm.datatypes.Matrix(self.component["guide_transforms"][0]).translate)
            root = self.add_root(m=m)
        else:
            if self.component["mirror_behaviour"] and self.component.negate:
                scl = [1, 1, -1]
            else:
                scl = [1, 1, 1]
            m = transform.getTransformFromPos(pm.datatypes.Matrix(self.component["guide_transforms"][0]).translate)
            root = self.add_root(m=m)
            m = transform.setMatrixScale(pm.datatypes.Matrix(self.component["guide_transforms"][0]), scl)

        # get ctl color
        ik_color = self.get_ctl_color("ik")

        # create
        jnt_names = [""]
        if self.component["jnt_names"]:
            jnt_names = self.component["jnt_names"].split(",")
        if not self.component["leaf_jnt"]:
            distance = pm.datatypes.Matrix(self.component["guide_transforms"][0]).scale[2]
            uni_scale = True if self.component["uni_scale"] else False
            if self.component.assembly["force_uni_scale"]:
                uni_scale = True

            ctl = self.add_ctl(root,
                               None,
                               ik_color,
                               self.component["key_able_attrs"],
                               None,
                               "",
                               True if self.component["ik_ref_array"] else False,
                               m,
                               icon=self.component["icon"],
                               w=self.component["ctl_size"] * distance,
                               d=self.component["ctl_size"] * distance,
                               h=self.component["ctl_size"] * distance)
            ref = self.add_ref(ctl,
                               "",
                               m)
            if self.component["jnt_rig"]:
                jnt = self.add_jnt(None,
                                   ref,
                                   jnt_names[0] if jnt_names[0] else naming.name(self.component, True),
                                   uni_scale)
        else:
            if self.component["jnt_rig"]:
                jnt = self.add_jnt(None,
                                   pm.datatypes.Matrix(self.component["guide_transforms"][0]),
                                   jnt_names[0] if jnt_names[0] else naming.name(self.component, True),
                                   False)

    def attributes(self):
        pass

    def operators(self):
        """ rig feature create """

    def connector(self):
        """ specify parent component connector """
