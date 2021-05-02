# -*- coding:utf-8 -*-

# maya
import pymel.core as pm

# json
from mbox.vendor import jsonschema
import json

# mbox
from mbox.lego.lib import get_dag_graph, get_blueprint_graph
from mbox.lego import box

#
import os
import importlib
from collections import OrderedDict


def get_blueprint_from_hierarchy(selection):
    """

    :return:
    """
    dag = get_dag_graph(selection)
    if not dag:
        return None
    with open(os.path.join(os.path.dirname(__file__), "schema", "blueprint-1.json"), "r") as f:
        schema = json.load(f)
    data = get_blueprint_graph(dag)
    jsonschema.validate(data, schema)

    return data


def get_blueprint_from_file(path):
    """

    :return:
    """
    with open(path, "r") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)
    with open(os.path.join(os.path.dirname(__file__), "schema", "blueprint-1.json"), "r") as f:
        schema = json.load(f, object_pairs_hook=OrderedDict)
    jsonschema.validate(data, schema)
    return data


def draw(blueprint, context):
    """

    :return:
    """
    if "blockID" not in blueprint:
        box.blueprint(blueprint, context)
    else:
        mod = importlib.import_module("mbox.lego.box.{0}.blueprint".format(blueprint["blockID"]))
        importlib.reload(mod)
        if blueprint["blockVersion"] != mod.version:
            pass
        mod.blueprint(blueprint, context)
    for child in blueprint["children"]:
        draw(child)


def save(blueprint, path):
    """

    :return:
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(blueprint, f, ensure_ascii=False, sort_keys=False, indent=2)


def insert_blueprint(a, b, parent):
    """

    :param a:
    :param b:
    :param parent:
    :return:
    """