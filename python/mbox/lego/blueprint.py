# -*- coding:utf-8 -*-
""" blueprint(bp) module"""

# maya
import pymel.core as pm

# json
from mbox.vendor import jsonschema
import json

# mbox
from mbox.lego.box import blueprint

#
import os
import sys
import copy
import logging
import importlib
from collections import OrderedDict

logger = logging.getLogger(__name__)


def get_blueprint_graph(graph, data=None, priority=0):
    """

    :param graph:
    :param data:
    :param priority:
    :return:
    """
    if graph:
        root = [x for x in graph.keys() if x.hasAttr("isBlueprint")]
    else:
        return None

    # root info get
    if root:
        info = get_root_info(root[0].message.outputs(type="network")[0])
        if graph[root[0]]:
            info["blocks"] = list()
            get_blueprint_graph(graph[root[0]], info["blocks"], priority)
        else:
            info["blocks"] = None
        return info
    # block info get
    else:
        priority += 1
        for key in graph.keys():
            info = get_block_info(key.message.outputs(type="network")[0])
            data.append(info)
            info["priority"] = priority
            get_blueprint_graph(graph[key], data, priority)
        priority -= 1


def get_dag_graph(node):
    """

    :param node:
    :return:
    """
    try:
        if node.hasAttr("isBlueprint"):
            return _get_dag_graph(node, OrderedDict())
        elif node.hasAttr("isBlueprintComponent"):
            data = OrderedDict()
            data[node.getParent(generations=-1)] = _get_dag_graph(node, OrderedDict())
            return data
    except Exception as error:
        sys.stdout.write(error)
        return None


def _get_dag_graph(node, data):
    """

    :param node:
    :param data:
    :return:
    """
    guides = [node] if node.hasAttr("isBlueprint") \
        else [node.worldMatrix.outputs(type="network")[0].transforms.inputs(type="transform")[0]]
    children = [y for x in guides for y in x.getChildren(type="transform") if y.hasAttr("isBlueprintComponent")]

    child = OrderedDict().fromkeys(children, None)
    data[node] = child if child else None

    for child in children:
        _get_dag_graph(child, data[node])
    return data


def get_root_info(node):
    """

    :param node:
    :return:
    """
    data = OrderedDict()
    data["schemaVersion"] = node.attr("schemaVersion").get()
    data["component"] = node.attr("component").get()
    data["version"] = node.attr("version").get()
    data["name"] = node.attr("name").get()
    data["process"] = node.attr("process").getEnums().key(node.attr("process").get())
    data["direction"] = node.attr("direction").get()
    data["runPreScripts"] = node.attr("runPreScripts").get()
    data["runPostScripts"] = node.attr("runPostScripts").get()
    data["preScripts"] = node.attr("preScripts").get() if node.attr("preScripts").get() else list()
    data["postScripts"] = node.attr("postScripts").get() if node.attr("postScripts").get() else list()
    data["nameRule"] = OrderedDict()
    data["nameRule"]["direction"] = node.attr("direction").get()
    data["nameRule"]["jointExp"] = node.attr("jointExp").get()
    data["nameRule"]["controllerExp"] = node.attr("controllerExp").get()
    data["nameRule"]["convention"] = OrderedDict()
    data["nameRule"]["convention"]["common"] = node.attr("commonConvention").get()
    data["nameRule"]["convention"]["joint"] = node.attr("jointConvention").get()
    data["nameRule"]["jointDescriptionLetterCase"] = \
        node.attr("jointDescriptionLetterCase").getEnums().key(node.attr("jointDescriptionLetterCase").get())
    data["nameRule"]["controllerDescriptionLetterCase"] = \
        node.attr("controllerDescriptionLetterCase").getEnums().key(node.attr("controllerDescriptionLetterCase").get())
    data["blocks"] = node.attr("affects")[0].outputs(type="network") \
        if node.attr("affects").outputs(type="network") else None
    data["notes"] = node.attr("notes").get()

    return data


def get_block_info(node):
    """

    :param node:
    :return:
    """
    data = OrderedDict()
    data["component"] = node.attr("component").get()
    data["version"] = node.attr("version").get()
    data["name"] = node.attr("name").get()
    data["direction"] = node.attr("direction").getEnums().key(node.attr("direction").get())
    data["index"] = node.attr("index").get()
    data["transforms"] = [x.tolist() for x in node.attr("transforms").get()]
    data["mirror"] = node.attr("mirror").get()
    data["joint"] = node.attr("joint").get()
    data["jointAxis"] = [node.attr("primaryAxis").get(), node.attr("secondaryAxis").get()]
    data["priority"] = node.attr("priority").get()
    data["parent"] = node.attr("parent").get()

    mod = importlib.import_module("mbox.lego.box.{block}.blueprint".format(block=data["component"]))
    data["meta"] = mod.get_block_info(node)

    return data


def get_blueprint_from_hierarchy(node):
    """ get mbox blueprint graph from maya hierarchy

    explanation
    1. get graph
    2. validate the graph with a schema
    3. return graph

    :return:
    """
    dag = get_dag_graph(node)
    if not dag:
        return None
    data = get_blueprint_graph(dag)
    schema_version = "{schema}.json".format(schema=data["schemaVersion"])
    with open(os.path.join(os.path.dirname(__file__), "schema", schema_version), "r") as f:
        schema = json.load(f)
    jsonschema.validate(data, schema)

    return data


def get_blueprint_from_file(path):
    """ get mbox blueprint graph from file

    explanation
    1. load blueprint file
    2. load schema file
    3. validate graph
    4. return graph

    :return:
    """
    with open(path, "r") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    schema_version = "{schema}.json".format(schema=data["schemaVersion"])
    with open(os.path.join(os.path.dirname(__file__), "schema", schema_version), "r") as f:
        schema = json.load(f, object_pairs_hook=OrderedDict)
    jsonschema.validate(data, schema)
    return data


def get_specific_block_blueprint(graph, name):
    """get specific block blueprint

    :param graph:
    :param name: name_direction_index ex)arm_left_0
    :return:
    """
    context = None
    for child in graph["blocks"]:
        context_name = "{name}_{direction}_{index}".format(name=child["name"],
                                                           direction=child["direction"],
                                                           index=child["index"])
        if context_name == name:
            context = child
    return context if context else None


def get_block_index(bp, name, direction):
    """

    :param bp:
    :param name:
    :param direction:
    :return:
    """
    block_name = "{name}{direction}".format(name=name, direction=direction)
    names = OrderedDict()
    for block in bp["blocks"]:
        name = "{name}{direction}".format(name=block["name"], direction=block["direction"])
        if name not in names:
            names[name] = list()
        names[name].append(block["index"])

    if block_name not in names:
        return "0"

    for index, number in enumerate(sorted(names[block_name])):
        if str(index) != str(number):
            return str(index)

    return str(max([int(x) for x in names[block_name]]) + 1)


def get_specific_dag_node(root, name):
    dags = pm.ls(root, dagObjects=True)
    parent = [dag for dag in dags if name in dag.nodeName()]
    return parent[0] if parent else root


def draw_block_selection(node, block):
    """ Add a block to an already existing dag list

    explanation
    1. get original blueprint from node hierarchy
    2. get parent context from original blueprint
    3. get new block blueprint
    4. insert blueprint to original blueprint
    5. add block to node hierarchy

    :param node:
    :param block:
    :return:
    """
    orig_bp = get_blueprint_from_hierarchy(node.getParent(generations=-1))

    mod = importlib.import_module("mbox.lego.box.{block}.blueprint".format(block=block))
    priority = 1 if node.hasAttr("isBlueprint") else node.message.outputs(type="network")[0].attr("priority").get() + 1
    block_bp = mod.initialize_(orig_bp, node.nodeName(), priority)

    insert_blueprint(orig_bp["blocks"], block_bp, node.getParent(generations=-1), orig_bp)


def draw_block_no_selection(block):
    """ draw new single block

    explanation
    1. init guide root block
    2. insert block blueprint to guide root blueprint
    3. create node hierarchy

    :param block:
    :return:
    """
    init_bp = blueprint.initialize_()
    guide = blueprint.blueprint(init_bp)
    mod = importlib.import_module("mbox.lego.box.{block}.blueprint".format(block=block))
    block_bp = mod.initialize_(init_bp, "guide", 1)

    insert_blueprint(init_bp["blocks"], block_bp, guide, init_bp)


def draw_from_blueprint(bp):
    """ draw node hierarchy from bp

    explanation
    1. bp is root - root guide
       bp is block - block guide
    2. recursive

    :param bp:
    :return:
    """
    root = blueprint.blueprint(bp)
    p = max([int(x["priority"]) for x in bp["blocks"]])
    p_list = [list() for x in range(p)]
    for block in bp["blocks"]:
        p_list[block["priority"]-1].append(block)

    for priority in p_list:
        for block in priority:
            mod = importlib.import_module("mbox.lego.box.{block}.blueprint".format(block=block["component"]))
            mod.blueprint(get_specific_dag_node(root, block["parent"]), block)


def synchronize(root, bp):
    """

    :param root:
    :param bp:
    :return:
    """
    orig = get_blueprint_from_hierarchy(root)
    orig_blocks = ["{name}_{direction}_{index}".format(name=x["name"],
                                                       direction=x["direction"],
                                                       index=x["index"]) for x in orig["blocks"]] if orig["blocks"] else list()
    new_blocks = ["{name}_{direction}_{index}".format(name=x["name"],
                                                      direction=x["direction"],
                                                      index=x["index"]) for x in bp["blocks"]] if bp["blocks"] else list()
    generated_blocks = list(set(new_blocks) - set(orig_blocks))
    disappeared_blocks = list(set(orig_blocks) - set(new_blocks))

    for g_block in generated_blocks:
        block_bp = get_specific_block_blueprint(bp, g_block)
        mod = importlib.import_module("mbox.lego.box.{block}.blueprint".format(block=block_bp["component"]))
        mod.blueprint(get_specific_dag_node(root, block_bp["parent"]), block_bp)


def insert_blueprint(parent, child, root=None, bp=None):
    """ insert blueprint graph to blueprint graph

    :param parent: parent block children list
    :param child: child block blueprint
    :param root: root node
    :param bp: root blueprint
    :return:
    """
    parent.append(child)
    if root and bp:
        synchronize(root, bp)


def delete_blueprint(bp, root=None, node=False):
    """ delete a part of blueprint graph

    :return:
    """
    name = bp["name"]
    side = bp["side"]
    index = bp["index"]

    if node:
        remove = None
        guides = [x for x in pm.ls(root, dagObjects=True) if x.hasAttr("isBlueprintComponent") or x.hasAttr("isBlueprint")]
        for guide in guides:
            network = guide.message.outputs(type="network")[0]
            if (name == network.attr("name")) and (side == network.attr("side")) and (index == network.attr("index")):
                remove = guide
        if remove:
            pm.delete(remove)
    del bp


def duplicate_blueprint(root, parent, bp, mirror=False):
    """

    :param root:
    :param parent:
    :param bp:
    :param mirror:
    :return:
    """
    dup_bp = copy.deepcopy(bp)
    parent.append(dup_bp)


def save(bp, path):
    """

    :param bp:
    :param path:
    :return:
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(bp, f, ensure_ascii=False, sort_keys=False, indent=2)
