# -*- coding:utf-8 -*-

# maya
import pymel.core as pm

# json
from mbox.vendor import jsonschema
import json

# mbox
from mbox.lego.lib import get_dag_graph, get_blueprint_graph

#
import os
from collections import OrderedDict


def get_blueprint_from_hierarchy(selection):
    """

    :return:
    """
    dag = get_dag_graph(selection)
    if not dag:
        return None
    with open(os.path.join(os.path.dirname(__file__), "schema", "blueprint.json"), "r") as f:
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
    with open(os.path.join(os.path.dirname(__file__), "schema", "blueprint.json"), "r") as f:
        schema = json.load(f)
    jsonschema.validate(data, schema)
    return data


def draw(blueprint):
    """

    :return:
    """
    for child in blueprint["children"]:
        draw(child)


def save(blueprint, path):
    """

    :return:
    """
    with open(path, "w") as f:
        json.dump(blueprint)


def insert_blueprint(a, b, parent):
    """

    :param a:
    :param b:
    :param parent:
    :return:
    """