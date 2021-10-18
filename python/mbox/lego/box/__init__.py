# -*- coding: utf-8 -*-

# mgear
from mgear.core import attribute, primitive, icon

#
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


def objects(block, context):
    """"""
    # root context
    context_name = "root"
    context[context_name] = OrderedDict()
    ct = context[context_name]

    root = primitive.addTransform(None, block.naming)
    geo = primitive.addTransform(root, "geo")
    blocks = primitive.addTransform(root, "blocks")
    joints = primitive.addTransform(root, "joints")

    world_root = primitive.addTransform(blocks, "world_root")
    world_npo = primitive.addTransform(world_root, "world_npo")
    world_con = icon.create(world_npo, "world_con")
    world_ref = primitive.addTransform(world_con, "world_ref")
    world_jnt = primitive.addJoint(joints, "world_jnt")

    ct["rig"] = root
    ct["geo_root"] = geo
    ct["blocks_root"] = blocks
    ct["joints_root"] = joints
    ct["ref"] = [world_ref]
    ct["controls"] = [world_con]
    ct["joints"] = [world_jnt]


def attributes(block, context):
    """"""
    # root context
    context_name = "root"
    ct = context[context_name]

    root = ct[0]
    attribute.addAttribute(root, "controlsVis", "bool", True)
    attribute.addAttribute(root, "controlsOnPlaybackVis", "bool", False)
    attribute.addAttribute(root, "jointsVis", "bool", False)

    [attribute.setKeyableAttributes(con) for con in ct["controls"]]


def connections(block, context):
    """"""
    # root context
    context_name = "root"
    ct = context[context_name]

    root, geo, blocks, joints, _ = ct
    root.controlsVis >> blocks.v
    root.controlsOnPlaybackVis >> blocks.hideOnPlayback
    root.jointsVis >> joints.v
    root.message >> block.__class__.NETWORK.rig
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
    [attribute.lockAttribute(node, attrs) for node in [root, geo, blocks, joints]]
    [attribute.setNotKeyableAttributes(node, attrs) for node in [root, geo, blocks, joints]]
