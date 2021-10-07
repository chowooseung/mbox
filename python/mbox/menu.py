# -*- coding:utf-8 -*-
"""from mgear.menu"""

# maya
import pymel.core as pm

import logging

logger = logging.getLogger(__name__)


def create(menuId):
    """from mgear.menu.create"""
    if pm.menu(menuId, exists=True):
        pm.deleteUI(menuId)

    pm.menu(menuId,
            parent="MayaWindow",
            tearOff=True,
            allowOptionBoxes=True,
            label=menuId)

    return menuId


def install_help(menuId):
    """from mgear.menu.install_help_menu"""
    pm.setParent(menuId, menu=True)
    pm.menuItem(divider=True)
    pm.menuItem(parent=menuId, subMenu=True, tearOff=True, label="Help")
    pm.menuItem(label="About", command=str_about)


str_about = """
import mbox
mbox.about()"""