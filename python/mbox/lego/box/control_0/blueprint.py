# -*- coding:utf-8 -*-

#
from collections import OrderedDict

# maya
import pymel.core as pm

# mbox
from mbox.lego import lib, box
from mbox.core import primitive, attribute, icon


def initialize():
    data = OrderedDict()
    data["id"] = "control_0"
    data["version"] = "0.0.0"
    data["name"] = "control"
    data["side"] = "center"
    data["index"] = 0
    data["transforms"] = [pm.datatypes.Matrix()]
    data["mirror"] = False
    data["joint"] = True
    data["primaryAxis"] = "x"
    data["secondaryAxis"] = "y"
    data["children"] = list()
    data["meta"] = OrderedDict()
    data["meta"]["asWorld"] = False
    data["meta"]["worldOrientAxis"] = False
    data["meta"]["keyableAttrs"] = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]

    return data


def create_network(bp):
    network = pm.createNode("network")
    attribute.add(network, "guide", "message")
    attribute.add(network, "rig", "message")
    attribute.add(network, "id", "string", bp["id"])
    attribute.add(network, "version", "string", bp["version"])
    attribute.add(network, "component", "string", bp["name"])
    attribute.add_enum(network, "side", bp["side"], ["center", "right", "left"], keyable=False)
    attribute.add(network, "index", "string", bp["index"])
    attribute.add(network, "mirror", "bool", bp["mirror"], keyable=False)
    attribute.add(network, "joint", "bool", bp["joint"], keyable=False)
    attribute.add(network, "primaryAxis", "string", bp["primaryAxis"])
    attribute.add(network, "secondaryAxis", "string", bp["secondaryAxis"])
    attribute.add(network, "asWorld", "bool", bp["meta"]["asWorld"], keyable=False)
    attribute.add(network, "worldOrientAxis", "bool", bp["meta"]["worldOrientAxis"], keyable=False)
    [attribute.add(network, attr, "bool", True if attr in bp["meta"]["keyableAttrs"] else False, keyable=False)
     for attr in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]]

    return network


def blueprint(bp):
    """

    :param bp:
    :return:
    """
    parent = box.blueprint()
    index = lib.blueprint_find_index(parent.getParent(generations=-1), bp["name"], bp["side"])

    # create
    root = icon.guide_root_icon(parent,
                                "{name}_{side}{index}_root".format(name=bp["name"],
                                                                   side=bp["side"],
                                                                   index=index),
                                m=bp["transforms"][0])
    root.t.set(0, 0, 0)
    network = primitive.add_block_network(root,
                                          bp["id"],
                                          bp["version"],
                                          bp["name"],
                                          bp["side"],
                                          index)

    # attribute
    attribute.hide(root, "v")
    attribute.lock(root, "v")
    root.message >> root.guides[0]

    key_attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]
    [attribute.add(network, attr, "bool", True, keyable=False) for attr in key_attrs]
    attribute.add(network, "asWorld", "bool", False, keyable=False)
    attribute.add(network, "worldOrientAxis", "bool", False, keyable=False)
