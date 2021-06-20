# -*- coding:utf-8 -*-

#
from collections import OrderedDict

# maya
import pymel.core as pm

# mbox
from mbox.lego.blueprint import get_block_index
from mbox.core import attribute, icon


def initialize_(bp, parent, priority):
    data = OrderedDict()
    data["component"] = "control_0"
    data["version"] = "0.0.0"
    data["name"] = "control"
    data["direction"] = "center"
    data["index"] = get_block_index(bp, data["name"], data["direction"])
    data["transforms"] = [pm.datatypes.Matrix().tolist()]
    data["mirror"] = False
    data["joint"] = True
    data["jointAxis"] = ["x", "y"]
    data["meta"] = OrderedDict()
    data["meta"]["asWorld"] = False
    data["meta"]["worldOrientAxis"] = False
    data["meta"]["keyAbleAttrs"] = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]
    data["parent"] = parent
    data["priority"] = priority

    return data


def initialize(affects, bp):
    network = pm.createNode("network")
    attribute.add(network, "guide", "message")
    attribute.add(network, "rig", "message")
    attribute.add(network, "component", "string", bp["component"])
    attribute.add(network, "version", "string", bp["version"])
    attribute.add(network, "name", "string", bp["name"])
    attribute.add_enum(network, "direction", bp["direction"], ["center", "right", "left"], keyable=False)
    attribute.add(network, "index", "string", bp["index"])
    attribute.add(network, "parent", "string", bp["parent"])
    attribute.add(network, "mirror", "bool", bp["mirror"], keyable=False)
    attribute.add(network, "joint", "bool", bp["joint"], keyable=False)
    attribute.add(network, "primaryAxis", "string", bp["jointAxis"][0])
    attribute.add(network, "secondaryAxis", "string", bp["jointAxis"][1])
    attribute.add(network, "asWorld", "bool", bp["meta"]["asWorld"], keyable=False)
    attribute.add(network, "worldOrientAxis", "bool", bp["meta"]["worldOrientAxis"], keyable=False)
    for attr in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]:
        attribute.add(network, attr, "bool", True if attr in bp["meta"]["keyAbleAttrs"] else False, keyable=False)
    attribute.add(network, "transforms", "matrix", multi=True)
    for index, transform in enumerate(bp["transforms"]):
        network.attr("transforms")[index].set(pm.datatypes.Matrix(transform))
    attribute.add(network, "priority", "long", bp["priority"], keyable=False)

    affects >> network.affectedBy[0]
    return network


def blueprint(parent, bp):
    """

    :param parent:
    :param bp:
    :return:
    """
    # name
    root_n = "{name}_{direction}{index}_root".format(name=bp["name"], direction=bp["direction"], index=bp["index"])

    # create
    root = icon.guide_root_icon(parent, root_n, m=pm.datatypes.Matrix(bp["transforms"][0]))
    network = initialize(parent.getParent(generations=-1).message.outputs(type="network")[0].affects[0], bp)

    # attribute
    attribute.hide(root, "v")
    attribute.lock(root, "v")
    root.message >> network.guide
    root.worldMatrix >> network.transforms[0]


def get_block_info(node):
    """ get specific block meta info

    :param node: network node
    :return: meta data
    """
    data = OrderedDict()
    data["asWorld"] = node.attr("asWorld").get()
    data["worldOrientAxis"] = node.attr("worldOrientAxis").get()
    data["keyAbleAttrs"] = \
        [a for a in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"] if node.attr(a).get()]

    return data
