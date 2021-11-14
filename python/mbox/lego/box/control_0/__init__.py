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
from mgear.core import primitive, icon


class Objects(AbstractObjects):

    def __init__(self, block):
        super(Objects, self).__init__(block=block)

    def process(self, context):
        super(Objects, self).process(context=context)
        n_kwargs = {"name": self.block["name"], "direction": self.block["direction"], "index": self.block["index"]}
        root_name = self.block.top.controls_name(**n_kwargs, description="", extension="root")
        npo_name = self.block.top.controls_name(**n_kwargs, description="", extension="npo")
        con_name = self.block.top.controls_name(**n_kwargs, description="", extension=self.block.top["controls_ext"])
        ref_name = self.block.top.controls_name(**n_kwargs, description="", extension="ref")

        root_m = self.parent_ins["ref"][self.block["controls_ref_index"]].getMatrix(worldSpace=True)
        m = pm.datatypes.Matrix(self.block["transforms"][0])

        # create
        root = primitive.addTransform(self.top_ins["blocks"], root_name, root_m)
        npo = primitive.addTransform(root, npo_name, m)
        con = icon.circle(npo, con_name, m=m)
        ref = primitive.addTransform(con, ref_name, m)

        self.ins["root"] = root # block root. use build connect network
        self.ins["controls"] = [con] # block controls. use build connect controllers
        self.ins["refs"] = [ref] # block reference transform. sub block parent matrix
        # self.ins["joints"] = [jnt] # block joint. use build connect joint


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

