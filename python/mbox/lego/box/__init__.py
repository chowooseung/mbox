# -*- coding:utf-8 -*-

#
from collections import OrderedDict

# maya
import pymel.core as pm

# mbox
from mbox import version
from mbox.core import attribute, primitive, icon


def initialize():
    data = OrderedDict()
    data["name"] = "rig"
    data["process"] = "WIP"
    data["id"] = "lego"
    data["version"] = version
    data["sideName"] = ["C", "L", "R"]
    data["jointExp"] = "jnt"
    data["controllerExp"] = "con"
    data["jointConvention"] = "{name}_{side}{index}_{description}_{extension}"
    data["commonConvention"] = "{name}_{side}{index}_{description}_{extension}"
    data["jointDescriptionLetterCase"] = "default"
    data["controllerDescriptionLetterCase"] = "default"
    data["runPreScripts"] = False
    data["preScripts"] = list()
    data["runPostScripts"] = False
    data["postScripts"] = list()
    data["notes"] = str()
    data["children"] = list()

    return data


def create_network(bp):
    """

    :return:
    """
    network = pm.createNode("network")
    attribute.add(network, "guide", "message")
    attribute.add(network, "rig", "message")
    attribute.add(network, "name", "string", bp["name"])
    attribute.add_enum(network, "process", bp["process"], ["WIP", "PUB"], keyable=False)
    attribute.add(network, "id", "string", bp["id"])
    attribute.add(network, "version", "string", bp["version"])
    attribute.add(network, "sideName", "string", multi=True)
    network.sideName[0].set(bp["sideName"][0])
    network.sideName[1].set(bp["sideName"][1])
    network.sideName[2].set(bp["sideName"][2])
    attribute.add(network, "jointExp", "string", bp["jointExp"])
    attribute.add(network, "controllerExp", "string", bp["controllerExp"])
    attribute.add(network, "jointConvention", "string", bp["jointConvention"])
    attribute.add(network, "commonConvention", "string", bp["commonConvention"])
    attribute.add_enum(network,
                       "jointDescriptionLetterCase",
                       bp["jointDescriptionLetterCase"],
                       ["default", "lower", "upper", "capitalize"],
                       keyable=False)
    attribute.add_enum(network,
                       "controllerDescriptionLetterCase",
                       bp["controllerDescriptionLetterCase"],
                       ["default", "lower", "upper", "capitalize"],
                       keyable=False)
    attribute.add(network, "runPreScripts", "bool", bp["runPreScripts"], keyable=False)
    attribute.add(network, "preScripts", "string", multi=True)
    [network.attr("preScripts")[index].set(script) for index, script in enumerate(bp["preScripts"])]
    attribute.add(network, "runPostScripts", "bool", bp["runPostScripts"], keyable=False)
    attribute.add(network, "postScripts", "string", multi=True)
    [network.attr("postScripts")[index].set(script) for index, script in enumerate(bp["postScripts"])]
    attribute.add(network, "notes", "string", bp["notes"])

    return network


def blueprint(bp):
    """

    :return:
    """
    guide = primitive.add_transform(None, "guide")
    shapes = primitive.add_transform(guide, "controller_shapes")
    attribute.add(guide, "isLego", "bool", keyable=False)
    attribute.lock(guide, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"])
    attribute.hide(guide, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"])
    attribute.lock(shapes, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"])
    attribute.hide(shapes, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"])
    network = create_network(bp)
    guide.message >> network.guide

    return guide


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
