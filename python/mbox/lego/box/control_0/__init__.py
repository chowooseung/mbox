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
    transform
)


class Objects(AbstractObjects):

    def __init__(self, block):
        super(Objects, self).__init__(block=block)

    def process(self, context):
        super(Objects, self).process(context=context)

        # matrix
        if self.block["neutral_rotation"]:
            m = transform.getTransformFromPos(pm.datatypes.Matrix(self.block["transforms"][0]).translate)
        else:
            if self.block["mirror_behaviour"] and self.block.negate:
                scl = [1, 1, -1]
            else:
                scl = [1, 1, 1]
            m = transform.setMatrixScale(pm.datatypes.Matrix(self.block["transforms"][0]), scl)

        # get ctl color
        ik_color = self.block.get_ctl_color("ik")

        # create
        root = self.block.create_root(context=context, m=m)
        ctl = self.block.create_ctl(context=context,
                                    parent=root,
                                    m=m,
                                    parent_ctl=None,
                                    color=ik_color,
                                    shape=self.block["icon"],
                                    size=self.block["ctl_size"])
        ref = self.block.create_ref(context=context,
                                    parent=ctl,
                                    m=m)
        if not self.block["leaf_joint"]:
            jnt = self.block.create_jnt(context=context,
                                        parent=self.parent_ins["joint"][self.block["ref_index"]],
                                        description="",
                                        ref=ref)


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
