# -*- coding: utf-8 -*-

# built-in
import os, sys, importlib

# maya
from pymel import core as pm

# mbox
from mbox import logger

# mbox.__init__.py
MBOX_ROOT = os.getenv("MBOX_ROOT")
MBOX_MODULES = os.getenv("MBOX_MODULES")
MBOX_CUSTOM_MODULES = os.getenv("MBOX_CUSTOM_MODULES")

# sys path append
# load_block_module import component
if MBOX_MODULES not in sys.path:
    sys.path.append(MBOX_MODULES)
for path in MBOX_CUSTOM_MODULES.split(";"):
    if path not in sys.path:
        sys.path.append(path)


def traversal(node, func1, get_child_func, result):
    result.append(func1(node))
    for child_node in get_child_func(node):
        traversal(child_node, func1, get_child_func, result)


def is_guide(node: pm.PyNode):
    return node if node.hasAttr("is_guide") else None


def is_rig(node: pm.PyNode):
    return node if node.hasAttr("is_rig") else None


def is_network(node: pm.PyNode):
    return node if node.hasAttr("comp_type") else None


def is_ctl(node: pm.PyNode):
    return node if node.hasAttr("is_ctl") else None


def is_jnt(node: pm.PyNode):
    return node if node.hasAttr("is_jnt") else None


def get_component_modules():
    result = dict()
    module_dir = [d for d in os.listdir(MBOX_MODULES)
                  if os.path.isdir(os.path.join(MBOX_MODULES, d)) and "__pycache__" not in d]
    clean_module_dir = list(set(module_dir))
    if len(clean_module_dir) != len(module_dir):
        logger.warning("Exists same module in MBOX_MODULES")
    result[MBOX_MODULES] = clean_module_dir
    if os.path.exists(MBOX_CUSTOM_MODULES):
        custom_module_dir = [d for d in os.listdir(MBOX_CUSTOM_MODULES)
                             if os.path.isdir(os.path.join(MBOX_CUSTOM_MODULES, d)) and "__pycache__" not in d]
        clean_custom_module_dir = list(set(custom_module_dir))
        if len(clean_custom_module_dir) != len(custom_module_dir):
            logger.warning("Exists same module in MBOX_CUSTOM_MODULES")
        if len(list(set(clean_custom_module_dir + clean_module_dir))) != len(module_dir + custom_module_dir):
            logger.warning("Exists same module")
        result[MBOX_CUSTOM_MODULES] = clean_custom_module_dir
    return result


def import_component_module(comp_type, guide):
    modules = get_component_modules()
    valid = False
    for modules_list in modules.values():
        if comp_type in modules_list:
            valid = True
    if not valid:
        logger.warning(f"{comp_type} is invalid")
    mod = importlib.import_module(f"{comp_type}.guide" if guide else f"{comp_type}.rig")
    return mod


class Naming:

    def __init__(self):
        pass


class Selection:

    @property
    def network(self):
        node = self.valid(self.node)
        if node:
            if is_network(node):
                return node
            network = node.attr("message").outputs(type="network")
            if network:
                return network[0]

    @property
    def oid(self):
        return self.network.attr("oid").get() if self.network else None

    @property
    def guides(self):
        guides = list()
        if self.network:
            guides = self.network.attr("transforms").inputs(type="transform")
        return guides

    @property
    def ui_host(self):
        node = None
        if is_network(self.node):
            node = self.node.attr("ctls").inputs(type="transform")
            if node:
                node = node[0]
        elif is_ctl(self.node):
            node = self.node
        if node:
            ui_host = node.attr("ui_host").inputs(type="transform")
            if ui_host:
                return ui_host[0]

    @property
    def ctl_hierarchy(self):
        result = list()
        if is_ctl(self.node):
            traversal(self.node,
                      lambda x: x,
                      lambda x: pm.controller(x, query=True, children=True) if pm.controller(x, query=True, children=True) else [],
                      result)
        return list(result)

    @property
    def jnt_hierarchy(self):
        result = list()
        if is_jnt(self.node):
            traversal(self.node,
                      lambda x: x,
                      lambda x: x.getChildren(type="joint"),
                      result)
        return list(result)

    def __init__(self, node):
        """self.node is guide or rig or network"""
        self.node = node if isinstance(node, pm.PyNode) else pm.PyNode(node)

    @staticmethod
    def valid(node):
        while node:
            if is_guide(node) or is_rig(node) or is_network(node):
                break
            node = node.getParent()
        return node
