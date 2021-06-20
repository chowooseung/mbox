# -*- coding:utf-8 -*-

#
from collections import OrderedDict
import time

# maya
import pymel.core as pm

# mbox
from mbox import version
from mbox.core import attribute, primitive


def initialize_():
    """ initialize blueprint root network data

    :return: root blueprint
    """
    data = OrderedDict()
    data["name"] = "rig"
    data["process"] = "WIP"
    data["component"] = "lego"
    data["version"] = version
    data["schemaVersion"] = "blueprint-1"
    data["direction"] = ["C", "L", "R"]
    data["nameRule"] = OrderedDict()
    data["nameRule"]["jointExp"] = "jnt"
    data["nameRule"]["controllerExp"] = "con"
    data["nameRule"]["jointDescriptionLetterCase"] = "default"
    data["nameRule"]["controllerDescriptionLetterCase"] = "default"
    data["nameRule"]["convention"] = OrderedDict()
    data["nameRule"]["convention"]["joint"] = "{name}_{direction}{index}_{description}_{extension}"
    data["nameRule"]["convention"]["common"] = "{name}_{direction}{index}_{description}_{extension}"
    data["runPreScripts"] = False
    data["preScripts"] = list()
    data["runPostScripts"] = False
    data["postScripts"] = list()
    data["blocks"] = list()
    t = time.localtime()
    data["notes"] = "{year}-{month}-{day} {hour}:{minute}:{second}".format(year=t.tm_year,
                                                                           month=t.tm_mon,
                                                                           day=t.tm_mday,
                                                                           hour=t.tm_hour,
                                                                           minute=t.tm_min,
                                                                           second=t.tm_sec)

    return data


def initialize(bp):
    """ guide initialize(root)
    - guide >> network
        - controller_shapes

    :param bp: root blueprint
    :return: guide node
    """
    network = pm.createNode("network")
    attribute.add(network, "schemaVersion", "string", bp["schemaVersion"])
    network.attr("schemaVersion").lock()
    attribute.add(network, "guide", "message")
    attribute.add(network, "rig", "message")
    attribute.add(network, "name", "string", bp["name"])
    attribute.add_enum(network, "process", bp["process"], ["WIP", "PUB"], keyable=False)
    attribute.add(network, "component", "string", bp["component"])
    attribute.add(network, "version", "string", bp["version"])
    attribute.add(network, "direction", "string", multi=True)
    network.direction[0].set(bp["direction"][0])
    network.direction[1].set(bp["direction"][1])
    network.direction[2].set(bp["direction"][2])
    attribute.add(network, "jointExp", "string", bp["nameRule"]["jointExp"])
    attribute.add(network, "controllerExp", "string", bp["nameRule"]["controllerExp"])
    attribute.add(network, "jointConvention", "string", bp["nameRule"]["convention"]["joint"])
    attribute.add(network, "commonConvention", "string", bp["nameRule"]["convention"]["common"])
    attribute.add_enum(network,
                       "jointDescriptionLetterCase",
                       bp["nameRule"]["jointDescriptionLetterCase"],
                       ["default", "lower", "upper", "capitalize"],
                       keyable=False)
    attribute.add_enum(network,
                       "controllerDescriptionLetterCase",
                       bp["nameRule"]["controllerDescriptionLetterCase"],
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
    guide = primitive.add_transform(None, "guide")
    shapes = primitive.add_transform(guide, "controller_shapes")
    attribute.add(guide, "isBlueprint", "bool", keyable=False)
    attribute.lock(guide, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"])
    attribute.hide(guide, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"])
    attribute.lock(shapes, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"])
    attribute.hide(shapes, ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"])

    network = initialize(bp)
    guide.message >> network.guide
    return guide
