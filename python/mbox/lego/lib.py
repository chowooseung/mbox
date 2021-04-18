# -*- coding:utf-8 -*-

# maya
import pymel.core as pm
import maya.cmds as mc

#
from collections import OrderedDict
import sys
import os


def get_blueprint_graph(graph, data=None):
    """

    :param graph:
    :param data:
    :return:
    """
    if data is None:
        root = graph.keys()[0]
        info = get_root_info(root)
        info["children"] = list()
        get_blueprint_graph(graph[graph.keys()[0]], info["children"])
        return info
    elif isinstance(data, list) and graph is not None:
        for key in graph.keys():
            info = get_block_info(key)
            data.append(info)
            if graph[key]:
                info["children"] = list()
                get_blueprint_graph(graph[key], info["children"])
            else:
                info["children"] = None


def get_dag_graph(selection):
    """

    :param selection:
    :return:
    """
    try:
        selected = pm.selected(type="transform")[0]
        if selected.hasAttr("isLego"):
            return __recursive(selected, OrderedDict())
        else:
            selected = pm.selected(type="transform")[0].message.outputs(type="transform")[0]
            root = selected.getParent(generations=-1)
        if selection:
            data = OrderedDict()
            data[root] = __recursive(selected, OrderedDict())
            return data
        else:
            return __recursive(root, OrderedDict())
    except Exception as error:
        sys.stdout.write(error)
        return None


def __recursive(node, data):
    """

    :param node:
    :param data:
    :return:
    """
    guides = [node] if node.hasAttr("isLego") else node.guides.inputs(type="transform")
    children = [y for x in guides for y in x.getChildren(type="transform") if y.hasAttr("isGuide")]

    child = OrderedDict().fromkeys(children, None)
    data[node] = child if child else None

    for child in children:
        __recursive(child, data[node])
    return data


def get_root_info(node):
    """

    :param node:
    :return:
    """
    # network = node.message.outputs(type="network")[0]
    # pre = network.preScripts.get()
    # post = network.postScripts.get()
    # joint_exp = network.jointExp.get()
    # controller_exp = network.controllerExp.get()
    # common_convention = network.commonConvention.get()
    # joint_convention = network.jointConvention.get()

    data = OrderedDict()
    data["preScripts"] = list()
    data["postScripts"] = list()
    data["nameRule"] = OrderedDict()
    data["nameRule"]["jointExp"] = str()
    data["nameRule"]["controllerExp"] = str()
    data["nameRule"]["convention"] = OrderedDict()
    data["nameRule"]["convention"]["common"] = str()
    data["nameRule"]["convention"]["joint"] = str()

    return data


def get_block_info(node):
    """

    :param node:
    :return:
    """
    # network = node.message.outputs(type="network")[0]
    # network.blockID.get()
    # network.blockVersion.get()
    # network.transforms.get()
    # network.direction.get()
    # network.children.get()
    # network.mirror.get()
    # network.jointAxis.get()
    # network.joint.get()

    data = OrderedDict()
    data["blockID"] = str()
    data["blockVersion"] = str()
    data["transforms"] = list()
    data["direction"] = ["", "", ""]
    data["mirror"] = True
    data["jointAxis"] = list()
    data["joint"] = True
    data["meta"] = dict()

    return data
