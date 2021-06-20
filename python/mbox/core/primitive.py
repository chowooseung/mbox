# -*- coding:utf-8 -*-

# maya
import pymel.core as pm

# mbox
from mbox.core import transform
from mbox.core import attribute


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
