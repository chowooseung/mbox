# -*- coding: utf-8 -*-

#

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
    PreScripts,
    PostScripts,
    logger
)


def guide(blueprint, block, parent, showUI):
    if blueprint:
        blueprint.guide()
    else:
        if parent:
            selected = [pm.PyNode(parent)]
        else:
            selected = pm.selected(type="transform")
        if selected:
            if selected[0].hasAttr("is_guide_root") \
                    or selected[0].hasAttr("is_guide_component") \
                    or selected[0].hasAttr("is_guide"):
                draw_specify_component_guide(selected[0], block)
        else:
            draw_specify_component_guide(None, block)

        if showUI:
            inspect_settings()


def duplicate_guide():
    selected = pm.selected(type="transform")
    assert len(selected) > 0
    assert isinstance(selected[0], pm.nodetypes.Transform)


def mirror_guide():
    selected = pm.selected(type="transform")
    assert len(selected) > 0
    assert isinstance(selected[0], pm.nodetypes.Transform)


def rig(blueprint: AbstractBlock or None) -> Context:
    if not blueprint:
        blueprint = blueprint_from_guide(pm.selected(type="transform"))
        if not blueprint:
            raise RuntimeError

    context = Context()
    pre_scripts = list()
    objects = list()
    attributes = list()
    operators = list()
    connection = list()
    additional_func = [AdditionalFunc(blueprint)]
    post_scripts = list()

    def get_build_step(_blueprint: AbstractBlock):
        _objects, _attributes, _operators, _connection = _blueprint.build_step()
        objects.append(_objects)
        attributes.append(_attributes)
        operators.append(_operators)
        connection.append(_connection)
        for sub_block in _blueprint["blocks"]:
            get_build_step(sub_block)

    get_build_step(blueprint)

    # for path in blueprint["scripts"]:
    #     mod = importlib.import_module(path)
    #     for cls_name in dir(mod):
    #         cls = getattr(mod, cls_name)
    #         if issubclass(type(cls), PreScripts):
    #             pre_scripts.append(cls())
    #         elif issubclass(type(cls), PostScripts):
    #             post_scripts.append(cls())

    pre_scripts.sort(key=lambda s: s.order)
    post_scripts.sort(key=lambda s: s.order)

    logger.debug("mbox build system")
    logger.debug("counting ... [???/???]")

    total_count = 0
    total_count += len(pre_scripts) + len(post_scripts)
    total_count += len(objects) + len(attributes) + len(operators) + len(connection) + len(additional_func)
    count = 0

    logger.debug(f"total count : [{count}/{total_count}]")

    process = [pre_scripts, objects, attributes, operators, connection, additional_func, post_scripts]
    stop_point = ["prescripts", "objects", "attributes", "operators", "connection", "additionalFunc", "postScripts"]
    for index, step in enumerate(process):
        for runner in step:
            count += 1
            runner.process(context)
            logger.debug("{0:<30}".format(runner.msg) + f" [{count}/{total_count}]")
        if stop_point[index] == blueprint["step"]:
            logger.debug(f"{stop_point[index]} Stop")
            break

    logger.debug("Build Success")
    return context
