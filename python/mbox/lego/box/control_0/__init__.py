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
        else:
            if self.block["mirror_behaviour"] and self.block.negate:
                scl = [1, 1, -1]
            else:
                scl = [1, 1, 1]
            m = transform.setMatrixScale(pm.datatypes.Matrix(self.block["transforms"][1]), scl)

        # get ctl color
        ik_color = self.block.get_ctl_color("ik")
        parent_joint = self.parent_ins["jnts"][self.block["ref_index"]] \
            if self.parent_ins["jnts"] \
            else None
        # create
        if not self.block["leaf_joint"]:
            root = self.block.create_root(context=context, m=m)
            distance = vector.getDistance(pm.datatypes.Matrix(self.block["transforms"][0]).translate,
                                          pm.datatypes.Matrix(self.block["transforms"][1]).translate)
            ctl = self.block.create_ctl(context=context,
                                        parent=root,
                                        m=m,
                                        parent_ctl=None,
                                        color=ik_color,
                                        ctl_attr=self.block["key_able_attrs"],
                                        shape=self.block["icon"],
                                        size=self.block["ctl_size"] * distance)
            ref = self.block.create_ref(context=context,
                                        parent=ctl,
                                        description="",
                                        m=m)
            if self.block.top["joint_rig"] and self.block["joint_rig"]:
                jnt = self.block.create_jnt(context=context,
                                            parent=parent_joint,
                                            description="",
                                            ref=ref)
        else:
            if self.block.top["joint_rig"] and self.block["joint_rig"]:
                jnt = self.block.create_jnt(context=context,
                                            parent=parent_joint,
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


class Connection(AbstractConnection):

    def __init__(self, block):
        super(Connection, self).__init__(block=block)

    def process(self, context):
        super(Connection, self).process(context=context)
