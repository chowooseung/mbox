# -*- coding: utf-8 -*-

# built-in
import importlib.util
import os

# maya
import pymel.core as pm

# mbox
from mbox.lego.lib import (
    draw_specify_component_guide,
    inspect_settings,
    AbstractBlock,
    Context,
    blueprint_from_guide,
    AdditionalFunc,
    PreScript,
    PostScript,
    logger
)
from mbox.lego import utils


def guide(blueprint, block, parent, showUI):
    if blueprint:
        blueprint.guide()
    else:
        try:
            selected = pm.PyNode(parent) if parent else utils.select_guide()
            draw_specify_component_guide(selected, block)
        except AssertionError:
            draw_specify_component_guide(None, block)

        if showUI:
            inspect_settings()


def duplicate_guide():
    """TODO: build/ duplicate guide """
    selected = utils.select_guide()


def mirror_guide():
    """TODO: build/ mirror guide"""
    selected = utils.select_guide()


def rig(blueprint: AbstractBlock or None) -> Context:
    if not blueprint:
        blueprint = blueprint_from_guide(utils.select_guide())

    context = Context(blueprint)
    pre_scripts = list()
    objects = list()
    attributes = list()
    operators = list()
    connection = list()
    add_func = AdditionalFunc()
    additional_func = [add_func]
    post_scripts = list()

    def get_build_step(_blueprint: AbstractBlock):
        _objects, _attributes, _operators, _connection = _blueprint.build_step
        objects.append(_objects)
        attributes.append(_attributes)
        operators.append(_operators)
        connection.append(_connection)
        for sub_block in _blueprint["blocks"]:
            get_build_step(sub_block)

    get_build_step(blueprint)

    for path in blueprint["pre_custom_step"] + blueprint["post_custom_step"]:
        name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        for cls_name in dir(mod):
            cls = getattr(mod, cls_name)
            ins = cls()
            if issubclass(type(cls), PreScript):
                pre_scripts.append(ins)
            elif issubclass(type(cls), PostScript):
                post_scripts.append(ins)

    logger.debug("mbox build system")
    logger.debug("counting ... [???/???]")

    total = 0
    total += len(pre_scripts) + len(post_scripts)
    total += len(objects) + len(attributes) + len(operators) + len(connection) + len(additional_func)
    count = 0

    logger.debug(f"total count : [{count}/{total}]")

    process = [pre_scripts, objects, attributes, operators, connection, additional_func, post_scripts]
    stop_point = ["prescripts", "objects", "attributes", "operators", "connection", "additionalFunc", "postScripts"]
    for index, step in enumerate(process):
        for runner in step:
            count += 1
            runner.process(context)
            logger.debug("{0:<30}".format(runner.msg) + f" [{count}/{total}]")
        if stop_point[index] == blueprint["step"]:
            logger.debug(f"{stop_point[index]} Stop")
            break

    logger.debug("Build Success")
    return context
