# -*- coding:utf-8 -*-

#
from collections import OrderedDict

# maya
import pymel.core as pm

# mbox
from mbox import version
from mbox.core import attribute, primitive, icon


def objects(bp, context, contextName):
    """

    :param bp:
    :param context:
    :param contextName:
    :return:
    """
    data = context[contextName]

    root = primitive.add_transform(None, bp["name"])
    model = primitive.add_transform(root, "model")
    blocks = primitive.add_transform(root, "blocks")
    joints = primitive.add_transform(root, "joints")
    wip = primitive.add_transform(root, "WIP")

    world_root = primitive.add_transform(blocks, "world_root")
    world_npo = primitive.add_transform(world_root, "world_npo")
    world_con = icon.create(world_npo, "world_{0}".format(bp["controllerExp"]), color=17, icon="compas")
    world_ref = primitive.add_transform(world_con, "world_ref")
    world_output = primitive.add_transform(world_root, "world_output")

    data["rig"] = root
    data["model"] = model
    data["blocks"] = blocks
    data["joints"] = joints
    data["WIP"] = wip
    data["world"] = [world_root, world_npo, world_con, world_ref, world_output]
    data["output"] = [world_output]


def attributes(bp, context, contextName):
    """

    :param bp:
    :param context:
    :param contextName:
    :return:
    """
    data = context[contextName]
    root, model, blocks, joints, wip, _ = data
    attribute.add(root, "controllersVis", "bool", True)
    attribute.add(root, "controllersOnPlaybackVis", "bool", False)
    attribute.add(root, "jointsVis", "bool", False)


def connections(bp, context, contextName):
    """

    :param bp:
    :param context:
    :param contextName:
    :return:
    """
    data = context[contextName]
    root, model, blocks, joints, wip, _ = data
    root.controllersVis >> blocks.v
    root.controllersOnPlaybackVis >> blocks.hideOnPlayback
    root.jointsVis >> joints.v
    attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
    [attribute.lock(node, attrs) for node in [root, model, blocks, joints, wip]]
    [attribute.hide(node, attrs) for node in [root, model, blocks, joints, wip]]
    if bp["process"] == "PUB":
        pm.delete(wip)
