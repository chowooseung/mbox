# -*- coding: utf-8 -*-

# built-in
import importlib.util
import os
import sys

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
    logger,
    log_window
)
from mbox.lego import utils


def guide(blueprint, block, parent, showUI):
    if blueprint:
        blueprint.guide()
    else:
        try:
            selected = pm.PyNode(parent) if parent else utils.select_guides()[0]
            draw_specify_component_guide(selected, block)
        except:
            draw_specify_component_guide(None, block)

        if showUI:
            inspect_settings()


def duplicate_guide(blueprint=None, block=None):
    if blueprint is None and block is None:
        guides = utils.select_guides()
        if not guides:
            return
        root = guides[0].getParent(generations=-1)
        blueprint = blueprint_from_guide(root)
        network = guides[0].attr("message").outputs(type="network")[0]
        block = blueprint.find_block_with_oid(network.attr("oid").get())
    parent = block.parent
    pm.select(block.duplicate(blueprint, parent, mirror=False))


def mirror_guide(blueprint=None, block=None):
    if blueprint is None and block is None:
        guides = utils.select_guides()
        if not guides:
            return
        root = guides[0].getParent(generations=-1)
        blueprint = blueprint_from_guide(root)
        network = guides[0].attr("message").outputs(type="network")[0]
        block = blueprint.find_block_with_oid(network.attr("oid").get())
    parent = block.parent
    pm.select(block.duplicate(blueprint, parent, mirror=True))


def rig(blueprint: AbstractBlock or None) -> Context:
    if not blueprint:
        if utils.select_guides():
            blueprint = blueprint_from_guide(utils.select_guides()[0])

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

    bp_pre_custom_step = list()
    if blueprint["pre_custom_step"]:
        bp_pre_custom_step = [x.split(" | ")[1] for x in blueprint["pre_custom_step"].split(",") if not x.startswith("*")]
    bp_post_custom_step = list()
    if blueprint["post_custom_step"]:
        bp_post_custom_step = [x.split(" | ")[1] for x in blueprint["post_custom_step"].split(",") if not x.startswith("*")]

    custom_path = os.environ["MBOX_CUSTOM_STEP_PATH"]
    if custom_path and custom_path not in sys.path:
        sys.path.append(custom_path)

    for path in bp_pre_custom_step + bp_post_custom_step:
        name = os.path.splitext(os.path.basename(path))[0]
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if issubclass(mod.CustomStep, PreScript):
            ins = mod.CustomStep()
            pre_scripts.append(ins)
        elif issubclass(moc.CustomStep, PostScript):
            ins = mod.CustomStep()
            post_scripts.append(ins)

    log_window()
    logger.info("mbox build system")
    logger.info("counting ... [???/???]")

    total = 0
    total += len(pre_scripts) + len(post_scripts)
    total += len(objects) + len(attributes) + len(operators) + len(connection) + len(additional_func)
    count = 0

    logger.info(f"total count : [{count}/{total}]")

    try:
        with pm.UndoChunk():
            process = [pre_scripts, objects, attributes, operators, connection, additional_func, post_scripts]
            stop_point = ["prescripts", "objects", "attributes", "operators", "connection", "additionalFunc", "postScripts"]
            for index, step in enumerate(process):
                for runner in step:
                    count += 1
                    logger.info("{0:<50}".format(runner.msg) + f" [{count}/{total}]")
                    runner.process(context)
                if stop_point[index] == blueprint["step"]:
                    logger.info(f"{stop_point[index]} Stop")
                    break
    except Exception as e:
        pm.undo()
        logger.error(e)
        logger.info("Build Fail")
        return context

    logger.info("Build Success")
    return context
