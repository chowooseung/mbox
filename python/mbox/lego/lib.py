# -*- coding:utf-8 -*-

# maya
import pymel.core as pm

# mbox
from mbox import version
from mbox.lego import blueprint
from mbox.lego import lego

#
import logging

logger = logging.getLogger(__name__)


def draw_blueprint(bp, block):
    """

    :param bp:
    :param block:
    :return:
    """
    if bp:
        blueprint.draw_from_blueprint(bp)
        return

    selected = pm.selected(type="transform")

    if selected:
        if selected[0].hasAttr("isBlueprint") or selected[0].hasAttr("isBlueprintComponent"):
            blueprint.draw_block_selection(selected[0], block)
    else:
        blueprint.draw_block_no_selection(block)


def duplicate_blueprint_component(node, mirror=False, apply=True):
    """

    :param node:
    :param mirror:
    :param apply:
    :return:
    """
    orig_bp = blueprint.get_blueprint_from_hierarchy(node.getParent(generations=-1))

    network = node.worldMatrix.outputs(type="network")[0]
    name = network.attr("name").get()
    direction = network.attr("direction").getEnums().key(network.attr("direction").get())
    index = network.attr("index").get()
    specific_block = blueprint.get_specific_block_blueprint(orig_bp,
                                                            "{name}_{direction}_{index}".format(name=name,
                                                                                                direction=direction,
                                                                                                index=index))
    blueprint.duplicate_blueprint(node.getParent(generations=-1), specific_block, mirror=mirror, apply=apply)


def build_lego_from_blueprint(bp):
    """build rig

    :param bp:
    :return:
    """
    log_window()
    logger.info(version.version_info)

    lego.lego(bp)


def build_lego_from_selection(node):
    """build rig from selection node

    :param node:
    :return:
    """
    if node.hasAttr("isBlueprint") or node.hasAttr("isBlueprintComponent"):
        logger.info("selected node : {0}".format(node.name()))
        bp = blueprint.get_blueprint_from_hierarchy(node)
        build_lego_from_blueprint(bp)


def log_window():
    """mgear shifter log window

    :return:
    """
    log_window_name = "mbox_lego_build_log_window"
    log_window_field_reporter = "mbox_lego_build_log_field_reporter"
    if not pm.window(log_window_name, exists=True):
        logWin = pm.window(log_window_name, title="Lego Build Log", iconName="Shifter Log")
        pm.columnLayout(adjustableColumn=True)
        pm.cmdScrollFieldReporter(log_window_field_reporter, width=800, height=500, clear=True)
        pm.button(label="Close",
                  command=("import pymel.core as pm\npm.deleteUI('{logWin}', window=True)".format(logWin=logWin)))
        pm.setParent('..')
        pm.showWindow(logWin)
    else:
        pm.cmdScrollFieldReporter(log_window_field_reporter, edit=True, clear=True)
        pm.showWindow(log_window_name)


