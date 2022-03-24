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

        positions = [pm.datatypes.Matrix(x) for x in self.block["transforms"]]

        blade = vector.Blade(pm.datatypes.Matrix(self.block["roll_m"]))
        normal = blade.z * -1
        binormal = blade.x

        root = self.create_root(context, m=transform.getTransformFromPos(positions[0].translate))
        parent = root
        ctl_parent = None
        jnt_parent = None
        fk_color = self.get_ctl_color("fk")
        for index, t in enumerate(transform.getChainTransform([x.translate for x in positions], normal, self.block.negate)):
            ctl = self.create_ctl(context, root if not ctl_parent else ctl_parent, m=t, parent_ctl=ctl_parent, description=f"fk{index}", color=fk_color, ctl_attr=["rx", "ry", "rz", "ro"])
            ref = self.create_ref(context, parent=ctl, description=f"fk{index}Ref", m=t)
            jnt = self.create_jnt(context, parent=jnt_parent, description=f"fk{index}", ref=ref)
            ctl_parent = ref
            jnt_parent = jnt


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
