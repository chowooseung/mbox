# -*- coding: utf-8 -*-

# maya
import pymel.core as pm

# json
import json

# mbox
from mbox.lego.box import blueprint
from mbox.lego import utils

# mgear
from mgear.core import transform

#
import os
import logging
from collections import OrderedDict
import itertools


logger = logging.getLogger(__name__)


def blueprint_from_guide(selected):

    def hierarchy(component, data):
        children = blueprint.get_child_component(component)
        child = OrderedDict().fromkeys(children, None)
        data[component] = child if child else None

        for child in children:
            hierarchy(child, data[component])
        return data

    comp_hierarchy = None
    if selected.hasAttr("is_guide_root"):
        comp_hierarchy = hierarchy(selected, OrderedDict())
    elif selected.hasAttr("is_guide_component"):
        comp_hierarchy = OrderedDict()
        comp_hierarchy[selected.getParent(generations=-1)] = hierarchy(selected, OrderedDict())
    elif selected.hasAttr("is_guide"):
        selected = [x for x in blueprint.get_component_guide(selected) if x.hasAttr("is_guide_component")][0]
        comp_hierarchy = OrderedDict()
        comp_hierarchy[selected.getParent(generations=-1)] = hierarchy(selected, OrderedDict())

    # todo variable name change
    def get_blueprint(parent, guide, child):
        network = guide.message.outputs(type="network")[0]
        mod = utils.load_block_blueprint(network.attr("component").get())
        block = mod.Block(guide=guide, network=network)
        parent.blocks.append(block)
        if child:
            for key, value in child.items():
                get_blueprint(block, key, value)
    guide = next(itertools.islice(comp_hierarchy.keys(), 1))
    network = guide.message.outputs(type="network")[0]
    root = blueprint.Root(guide=guide, network=network)

    for key, value in comp_hierarchy[root.GUIDE].items():
        get_blueprint(root, key, value)
    root.update_network_to_blueprint()
    blueprint.connect_network(root)
    return root


def blueprint_from_network(network):

    def hierarchy():
        pass

    def get_blueprint():
        pass


def blueprint_from_rig():
    # get network from rig
    # blueprint_from_network(network)
    blueprint_from_network()


def blueprint_from_file(path):
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

    bp = blueprint.load(blueprint.Root(), data)
    return bp


def draw_specify_component_guide(parent, component):
    if not parent:
        # root block
        root_block = blueprint.Root()

        # component block
        block_mod = utils.load_block_blueprint(component)
        block = block_mod.Block()

        # append
        root_block.blocks.append(block)
        root_block.print()

        pm.select(root_block.draw_guide())
        return

    block_tree = blueprint_from_guide(parent.getParent(generations=-1))
    block_tree.update_blueprint_to_network()

    mod = utils.load_block_blueprint(component)
    block = mod.Block()
    index = blueprint.get_component_index(block_tree, block.name, block.direction)
    block.set(index=index)

    # translation offset
    offset_t = parent.getTranslation(space="world")
    for index, t in enumerate(block.transforms):
        block.transforms[index] = transform.setMatrixPosition(t, offset_t)

    p_network = parent.message.outputs(type="network")[0]
    if p_network.attr("component").get() != "mbox":
        p_name = p_network.attr("name").get()
        p_direction = p_network.attr("direction").get(asString=True)
        p_index = p_network.attr("index").get()
        p_block = blueprint.get_specify_block(block_tree, p_name, p_direction, p_index)
        parent = p_network.transforms.inputs(type="transform")[-1]
    else:
        p_block = block_tree
        parent = p_network.guide.inputs(type="transform")[0]
    p_block.blocks.append(block)
    pm.select(block.draw_guide(parent=parent))
    blueprint.connect_network(block_tree)
