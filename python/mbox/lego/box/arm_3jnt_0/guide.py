# -*- coding: utf-8 -*

#
from functools import partial

# maya
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget

# mbox
from mbox.core import icon
from mbox.lego.lib import (
    RootBlock,
    SubBlock
)
from mbox.lego.box import settings
from . import settings_ui

# mgear
from mgear.core import pyqt, attribute, primitive, transform
from mgear.vendor.Qt import QtWidgets, QtCore

# block info
AUTHOR = "cho wooseoung"
URL = None
EMAIL = "chowooseoung@gmail.com"
VERSION = [0, 0, 1]
TYPE = "arm_3jnt_0"
NAME = "arm_3jnt"
DESCRIPTION = "arm_3jnt 0"


