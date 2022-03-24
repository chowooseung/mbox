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
    vector
)


class Objects(AbstractObjects):

    def __init__(self, block):
        super(Objects, self).__init__(block=block)

    def process(self, context):
        super(Objects, self).process(context=context)

        # matrix
        if self.block["neutral_rotation"]:
            m = transform.getTransformFromPos(pm.datatypes.Matrix(self.block["transforms"][1]).translate)
            root = self.create_root(context=context, m=m)
        else:
            if self.block["mirror_behaviour"] and self.block.negate:
                scl = [1, 1, -1]
            else:
                scl = [1, 1, 1]
            m = transform.getTransformFromPos(pm.datatypes.Matrix(self.block["transforms"][1]).translate)
            root = self.create_root(context=context, m=m)
            m = transform.setMatrixScale(pm.datatypes.Matrix(self.block["transforms"][1]), scl)

        # get ctl color
        ik_color = self.get_ctl_color("ik")

        # create
        if not self.block["leaf_joint"]:
            distance = vector.getDistance(pm.datatypes.Matrix(self.block["transforms"][0]).translate,
                                          pm.datatypes.Matrix(self.block["transforms"][1]).translate)
            ctl = self.create_ctl(context=context,
                                  parent=root,
                                  m=m,
                                  parent_ctl=None,
                                  color=ik_color,
                                  ctl_attr=self.block["key_able_attrs"],
                                  shape=self.block["icon"],
                                  size=self.block["ctl_size"] * distance,
                                  cns=True if self.block["ik_ref_array"] else False)
            ref = self.create_ref(context=context,
                                  parent=ctl,
                                  description="",
                                  m=m)
            if self.block.top["joint_rig"] and self.block["joint_rig"]:
                jnt = self.create_jnt(context=context,
                                      parent=None,
                                      description="",
                                      ref=ref)
        else:
            if self.block.top["joint_rig"] and self.block["joint_rig"]:
                jnt = self.create_jnt(context=context,
                                      parent=None,
                                      description="",
                                      ref=m)


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

        if self.block["ik_ref_array"] and not self.block["leaf_joint"]:
            self.space_switch(context=context, ctl=self.ins["ctls"][0], target=self.ins["ui_host"], attr_name="space_switch")


class Connection(AbstractConnection):

    def __init__(self, block):
        super(Connection, self).__init__(block=block)

    def process(self, context):
        super(Connection, self).process(context=context)
