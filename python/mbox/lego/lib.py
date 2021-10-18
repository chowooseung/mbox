# -*- coding: utf-8 -*-

# maya
import pymel.core as pm

# mbox
import mbox
from mbox import lego
from mbox.lego import blueprint

#
import logging

# mgear
from mbox.lego.utils import load_block_blueprint
from mgear.core import pyqt

logger = logging.getLogger(__name__)


def draw_blueprint(bp, block, parent, showUI):
    """"""
    if bp:
        blueprint.draw_guide_from_blueprint()
        return
    if parent:
        selected = [pm.PyNode(parent)]
    else:
        selected = pm.selected(type="transform")
    if selected:
        if selected[0].hasAttr("isGuideRoot") or selected[0].hasAttr("isGuideComponent"):
            blueprint.draw_block_selection(selected[0], block)
        elif selected[0].hasAttr("isGuide"):
            blueprint.draw_block_selection(selected[0], block)
    else:
        blueprint.draw_block_no_selection(block)

    # TODO: showUI


def duplicate_blueprint_component(mirror=False, apply=True):
    """"""
    selected = pm.selected(type="transform")
    try:
        selected = selected[0]
        if selected.hasAttr("isGuide"):
            selected = selected.worldMatrix[0].outputs(type="network")[0].guide.get()
        network = selected.message.outputs(type="network")[0]
    except Exception as e:
        pm.displayWarning("select mbox component")
        return

    root_block = blueprint.get_blueprint_graph(selected.getParent(generations=-1))
    block = root_block.get_specify_block(network.attr("name"), network.attr("direction"), network.attr("index"))
    # todo


def inspect_settings():
    # todo
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
        mod = load_block_blueprint(comp_type)
        wind = pyqt.showDialog(mod.componentSettings, dockable=True)
        wind.tabs.setCurrentIndex(0)

    elif guide_root:
        module_name = "mbox.lego.box.settings"
        mod = __import__(module_name, globals(), locals(), ["*"], -1)
        wind = pyqt.showDialog(mod.guideSettings, dockable=True)
        wind.tabs.setCurrentIndex(0)

    else:
        pm.displayError("The selected object is not part of component guide")


def build(bp, selected=None, window=True, step="all"):
    """"""
    if window:
        log_window()
    mbox.log_information()

    if selected:
        logger.info("selected node : {0}".format(selected.naming()))
        bp = blueprint.blueprint_from_guide(selected)
    else:
        logger.info("no selection")


def log_window():
    """"""
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


def export_blueprint(node, path):
    """blueprint json file export"""
    if not path:
        path = _file_dialog(path, mode=0)
        if not path:
            pm.displayWarning("File path None")
            return
    if not node:
        try:
            selected = pm.selected(type="transform")[0]
            if not selected.hasAttr("isGuideRoot"):
                raise RuntimeError("select mbox root guide")
        except IndexError as e:
            pm.displayWarning(e)
            return
        except RuntimeError as e:
            pm.displayWarning(e)
            return
    else:
        selected = node

    root_block = blueprint.blueprint_from_guide(selected)
    root_block.save(root_block, path)


def import_blueprint(path, draw=True):
    """blueprint json file import"""
    if not path:
        path = _file_dialog(path, mode=1)
        if not path:
            pm.displayWarning("File path None")
            return

    root_block = blueprint.blueprint_from_file(path)
    if draw:
        root_block.draw_guide()

    return root_block


def _file_dialog(path=None, mode=0):
    """from mgear.shifter.io._get_file
    mode [0:save, 1:open]"""
    file_path = pm.fileDialog2(
        startingDirectory=path if path else pm.workspace(query=True, rootDirectory=True),
        fileMode=mode,
        fileFilter='mBox Guide Template .mbox (*%s)' % ".mbox")

    if not file_path:
        return

    return file_path[0]
