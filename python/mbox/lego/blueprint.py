# -*- coding: utf-8 -*-

# maya
import pymel.core as pm

# json
from mbox.vendor import jsonschema
import json

# mbox
from mbox.lego.box import blueprint
from mbox.lego import utils

# mgear
from mgear.core import transform

#
import os
import copy
import logging
import importlib
from collections import OrderedDict

logger = logging.getLogger(__name__)


def get_blueprint_graph(graph):
    """node tree graph를 기준으로 blueprint graph를 생성해 return"""
    if graph:
        root = [x for x in graph.keys() if x.hasAttr("isGuideRoot")]
    else:
        return None

    # root info get
    root_block = blueprint.Root()
    blueprint.get_info_from_guide(root_block, root[0].message.outputs(type="network")[0])

    return root_block


def get_dag_graph(node):
    """선택한 노드를 기준으로 tree구조를 return. node tree 중간을 선택했다면 최상위를 포함해 중간부터 return"""
    try:
        if node.hasAttr("isGuideRoot"):
            return _get_dag_graph(node, OrderedDict())
        elif node.hasAttr("isGuideComponent"):
            data = OrderedDict()
            data[node.getParent(generations=-1)] = _get_dag_graph(node, OrderedDict())
            return data
        elif node.hasAttr("isGuide"):
            guide_component = node.worldMatrix.outputs(type="network")[0].transforms.inputs(type="transform")[0]
            return get_dag_graph(guide_component)
    except Exception as error:
        logger.error(error)


def _get_dag_graph(node, data):
    """선택한 node가 속한 component를 기준으로 하위 component를 찾고 data[node]에 추가"""
    guides = [node] if node.hasAttr("isGuideRoot") \
        else node.worldMatrix.outputs(type="network")[0].transforms.inputs(type="transform")
    children = [y for x in guides for y in x.getChildren(type="transform") if y.hasAttr("isGuideComponent")]

    child = OrderedDict().fromkeys(children, None)
    data[node] = child if child else None

    for child in children:
        _get_dag_graph(child, data[node])
    return data


def blueprint_from_guide(node):
    """"""
    dag = get_dag_graph(node)
    if not dag:
        return None
    bp = get_blueprint_graph(dag)

    return bp


def blueprint_from_network(network):
    pass


def blueprint_from_rig():
    # get network from rig
    # blueprint_from_network(network)
    pass


def blueprint_from_file(path):
    """"""
    check = True
    if not os.path.exists(path):
        logger.info(f"Don't exists path : {path}")
    elif os.path.splitext(path)[-1] != ".mbox":
        logger.info(f"This file not .mbox ext")
    else:
        check = False

    if check:
        return

    with open(path, "r") as f:
        data = json.load(f)

    bp = blueprint.Root.load(blueprint.Root(), data)
    return bp


def draw_block_selection(node, block):
    """"""
    block_tree = blueprint_from_guide(node.getParent(generations=-1))

    mod = utils.load_block_blueprint(block)
    block = mod.Block()
    index = block_tree.get_component_index(block.naming, block.direction)
    block.set(index=index)

    # translation offset
    offset_t = node.getTranslation(space="world")
    for index, t in enumerate(block.transforms):
        block.transforms[index] = transform.setMatrixPosition(t, offset_t)

    p_network = node.message.outputs(type="network")[0]
    if p_network.hasAttr("component"):
        p_name = p_network.attr("name").get()
        p_direction = p_network.attr("direction").get(asString=True)
        p_index = p_network.attr("index").get()
        p_block = block_tree.get_specify_block(p_name, p_direction, p_index)
        parent = p_network.transforms.inputs(type="transform")[-1]
    else:
        p_block = block_tree
        parent = p_network.guide.inputs(type="transform")[0]
    p_block.blocks.append(block)
    block.draw_guide(parent=parent, parentNetwork=p_network)
    block_tree.print()

    components = [x for x in node.getChildren(type="transform") if x.hasAttr("isGuideComponent")]
    for component in components:
        network = component.message.outputs(type="network")[0]
        if block.naming == network.attr("name").get() \
                and block.direction == network.attr("direction").get(asString=True) \
                and block.index == network.attr("index").get():
            pm.select(component)
            break


def draw_block_no_selection(block):
    """"""
    root = blueprint.Root()
    mod = utils.load_block_blueprint(block=block)
    block = mod.Block()

    root.blocks.append(block)
    guide = root.draw_guide()
    root.print()

    components = [x for x in guide.getChildren(type="transform") if x.hasAttr("isGuideComponent")]
    for component in components:
        network = component.message.outputs(type="network")[0]
        if block.naming == network.attr("name").get() \
                and block.direction == network.attr("direction").get(asString=True) \
                and block.index == network.attr("index").get():
            pm.select(component)
            break


def draw_specify_component_guide(parent, component):
    if not parent:
        # root block
        root_block = blueprint.Root()

        # component block
        block_mod = utils.load_block_blueprint(component)
        block = block_mod()

        # append
        root_block.blocks.append(block)

        pm.select(root_block.draw_guide())
        return

    block_tree = blueprint_from_guide(parent.getParent(generations=-1))

    mod = utils.load_block_blueprint(component)
    block = mod.Block()
    index = block_tree.get_component_index(block.naming, block.direction)
    block.set(index=index)

    # translation offset
    offset_t = parent.getTranslation(space="world")
    for index, t in enumerate(block.transforms):
        block.transforms[index] = transform.setMatrixPosition(t, offset_t)

    p_network = parent.message.outputs(type="network")[0]
    if p_network.hasAttr("component"):
        p_name = p_network.attr("name").get()
        p_direction = p_network.attr("direction").get(asString=True)
        p_index = p_network.attr("index").get()
        p_block = block_tree.get_specify_block(p_name, p_direction, p_index)
        parent = p_network.transforms.inputs(type="transform")[-1]
    else:
        p_block = block_tree
        parent = p_network.guide.inputs(type="transform")[0]
    p_block.blocks.append(block)
    block.draw_guide(parent=parent, parentNetwork=p_network)
    block_tree.print()


def draw_rig_from_guide():
    pass


def draw_rig_from_blueprint():
    pass
