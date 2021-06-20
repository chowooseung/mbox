# -*- coding:utf-8 -*-

# maya
import pymel.core as pm

# mbox
from mbox.lego import blueprint


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

