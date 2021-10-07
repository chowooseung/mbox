# -*- coding:utf-8 -*-

# maya
import pymel.core as pm

# mbox
import mbox
from mbox import lego
from mbox.lego import blueprint, box
from mbox.core import utils, pyqt

#
import logging
import os

logger = logging.getLogger(__name__)


def draw_blueprint(bp, block, parent, showUI):
    """

    :param bp:
    :param block:
    :param parent:
    :param showUI:
    :return:
    """
    if bp:
        blueprint.draw_from_blueprint(bp)
        return

    if parent:
        selected = [pm.PyNode(parent)]
    else:
        selected = pm.selected(type="transform")

    if selected:
        if selected[0].hasAttr("isBlueprint") or selected[0].hasAttr("isBlueprintComponent"):
            blueprint.draw_block_selection(selected[0], block)
    else:
        blueprint.draw_block_no_selection(block)

    # TODO: showUI


def duplicate_blueprint_component(mirror=False, apply=True):
    """

    :param node:
    :param mirror:
    :param apply:
    :return:
    """
    node = pm.selected(type="transform")
    if not len(node):
        logger.info("plz select blueprint root or component")
        return

    node = node[0]
    if int(node.hasAttr("isBlueprint")) + int(node.hasAttr("isBlueprintComponent")) != 1:
        logger.info("plz select blueprint root or component")
        return

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


def inspect_settings():
    oSel = pm.selected(type="transform")
    if oSel:
        root = oSel[0]
    else:
        pm.displayWarning(
            "please select one object from the component guide")
        return

    comp_type = False
    guide_root = False
    while root:
        if pm.attributeQuery("isBlueprintComponent", node=root, exists=True):
            network = root.message.outputs(type="network")[0]
            comp_type = network.attr("component").get()
            break
        elif pm.attributeQuery("isBlueprint", node=root, exists=True):
            guide_root = root
            break
        root = root.getParent()
        pm.select(root)

    if comp_type:
        mod = load_blocks_blueprint(comp_type)
        wind = pyqt.show_dialog(mod.componentSettings, dockable=True)
        wind.tabs.setCurrentIndex(0)

    elif guide_root:
        module_name = "mbox.lego.box.settings"
        mod = __import__(module_name, globals(), locals(), ["*"], -1)
        wind = pyqt.show_dialog(mod.guideSettings, dockable=True)
        wind.tabs.setCurrentIndex(0)

    else:
        pm.displayError("The selected object is not part of component guide")


def build(bp, selected=None, window=True, step="all"):
    """build rig from selection node

    :param bp:
    :param selected:
    :param window:
    :param step:
    :return:
    """
    if window:
        log_window()
    mbox.log_information()

    if selected:
        logger.info("selected node : {0}".format(selected.name()))
        bp = blueprint.get_blueprint_from_hierarchy(selected)
    else:
        logger.info("no selection")
    lego.lego(bp, step)


def log_window():
    """show build log console

    from mgear

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


def get_blocks_directory():
    return utils.gather_custom_module_directories(
        "MBOX_CUSTOM_BOX_PATH",
        [os.path.join(os.path.dirname(box.__file__))])


def load_blocks_blueprint(block):
    """Import the Component """
    dirs = get_blocks_directory()
    defFmt = "mbox.lego.box.{}.settings"
    customFmt = "{}.settings"

    mod = utils.import_from_standard_or_custom_directories(dirs, defFmt, customFmt, block)
    return mod


def load_blocks_init(block):
    dirs = get_blocks_directory()
    defFmt = "mbox.lego.box.{}"
    customFmt = "{}"

    mod = utils.import_from_standard_or_custom_directories(dirs, defFmt, customFmt, block)
    return mod
