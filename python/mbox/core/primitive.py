# -*- coding:utf-8 -*-

# maya
import pymel.core as pm

# mbox
from mbox.core import transform
from mbox.core import attribute


def add_root_network(dag):
    """

    :return:
    """
    network = pm.createNode("network")
    attribute.add(network, "guide", "message")
    dag.message >> network.guide
    attribute.add(network, "rig", "message")
    attribute.add(network, "id", "string", "root")
    attribute.add(network, "sideName", "string", multi=True)
    network.sideName[0].set("C")
    network.sideName[1].set("L")
    network.sideName[2].set("R")
    attribute.add(network, "jointExp", "string", "jnt")
    attribute.add(network, "controllerExp", "string", "con")
    attribute.add(network, "jointConvention", "string", "{name}_{side}{index}_{description}_{extension}")
    attribute.add(network, "commonConvention", "string", "{name}_{side}{index}_{description}_{extension}")
    attribute.add(network, "runPreScripts", "bool", False, keyable=False)
    attribute.add(network, "preScripts", "string", multi=True)
    attribute.add(network, "runPostScripts", "bool", False, keyable=False)
    attribute.add(network, "postScripts", "string", multi=True)
    attribute.add(network, "notes", "string")


def add_block_network(dag, id, version, component, side, index):
    """

    :param dag:
    :param id:
    :param version:
    :param component:
    :param side:
    :param index:
    :return:
    """
    network = pm.createNode("network")
    attribute.add(network, "guide", "message")
    dag.message >> network.guide
    attribute.add(network, "rig", "message")
    attribute.add(network, "id", "string", id)
    attribute.add(network, "version", "string", version)
    attribute.add(network, "component", "string", component)
    attribute.add_enum(network, "side", side, ["center", "right", "left"], keyable=False)
    attribute.add(network, "index", "string", index)
    attribute.add(network, "mirror", "bool", keyable=False)
    attribute.add(network, "joint", "bool", keyable=False)
    attribute.add(network, "primaryAxis", "string", "x")
    attribute.add(network, "secondaryAxis", "string", "y")

    return network


def add_transform(parent, name, m=pm.datatypes.Matrix()):
    """Create a transform dagNode.
    Arguments:
        parent (dagNode): The parent for the node.
        name (str): The Node name.
        m (matrix): The matrix for the node transformation (optional).
    Returns:
        dagNode: The newly created node.
    """
    node = pm.PyNode(pm.createNode("transform", name=name))
    node.setTransformation(m)

    if parent is not None:
        parent.addChild(node)

    return node


def add_transform_from_pos(parent, name, pos=pm.datatypes.Vector(0, 0, 0)):
    """Create a transform dagNode.
    Arguments:
        parent (dagNode): The parent for the node.
        name (str): The Node name.
        pos (vector): The vector for the node position (optional).
    Returns:
        dagNode: The newly created node.
    """
    node = pm.PyNode(pm.createNode("transform", name=name))
    node.setTranslation(pos, space="world")

    if parent is not None:
        parent.addChild(node)

    return node
