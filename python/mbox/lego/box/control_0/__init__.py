# -*- coding:utf-8 -*-

# maya
import pymel.core as pm

# mbox
from mbox.core import string

# mgear
from mgear.core import attribute, primitive, icon

#
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


def objects(block, context):
    """"""
    # current context
    context_name = f"{block.naming}_{block.direction}{block.index}"
    context[context_name] = OrderedDict()
    ct = context[context_name]

    # parent context
    p_network = block.__class__.NETWORK.affedtedBy[0].get()
    p_context_name = \
        f"{p_network.attr('name').get()}_{p_network.attr('direction').get()}{p_network.attr('index').get()}"
    p_ct = context[p_context_name]

    # name
    c_convention = context["controlsConvention"]
    j_convention = context["jointConvention"]
    con_ext = context["controlsExt"]
    jnt_ext = context["jointExt"]
    con_padding = context["controlsPadding"]
    jnt_padding = context["jointPadding"]
    name_dict = {"name": block.naming, "direction": block.direction, "index": block.index}

    root_name = string.naming(c_convention, padding=con_padding, **name_dict, extension="root")
    npo_name = string.naming(c_convention, padding=con_padding, **name_dict, extension="npo")
    con_name = string.naming(c_convention, padding=con_padding, **name_dict, extension=con_ext)
    ref_name = string.naming(c_convention, padding=con_padding, **name_dict, extension="ref")
    jnt_name = string.naming(j_convention, padding=jnt_padding, **name_dict, extension=jnt_ext)

    # create
    root = primitive.addTransform(context["root"]["blocks"], root_name, p_ct["ref"][-1].getMatrix(worldSpace=True))
    npo = primitive.addTransform(root, npo_name, pm.datatypes.Matrix(block.transform[0]))
    con = primitive.addTransform(npo, con_name)
    ref = primitive.addTransform(con, ref_name)
    jnt = primitive.addJoint(context["root"]["joints"], jnt_name, pm.datatypes.Matrix(block.transforms[0]))

    # controls
    pm.controller(con, p_ct["con"][-1], parent=True)

    ct["root"] = root
    ct["controls"] = [con]
    ct["ref"] = [ref]
    ct["joints"] = [jnt]


def attributes(block, context):
    """"""
    # current context
    context_name = f"{block.naming}_{block.direction}{block.index}"
    ct = context[context_name]


def connections(block, context):
    """"""
    # current context
    context_name = f"{block.naming}_{block.direction}{block.index}"
    ct = context[context_name]

    ct["root"].message >> block.__class__.NETWORK.rig
