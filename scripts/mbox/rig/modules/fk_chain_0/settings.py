# -*- coding: utf-8 -*-

# mbox
from .. import common_settings
from . import settings_ui

# maya
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget
from pymel import core as pm

# qt.py
from mgear.vendor.Qt import QtWidgets, QtCore, QtGui


class SettingsUI(QtWidgets.QDialog, settings_ui.Ui_From):

    def __init__(self, parent=None):
        super(SettingsUI, self).__init__(parent=parent)
        self.setupUi(self)


class Settings(MayaQWidgetDockableMixin, common_settings.Settings):

    def __init(self, parent=None):
        super(Settings, self).__init__(parent=parent)
        self.settings_ui = SettingsUI()

        self.setup_window()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.populate_widgets()

    def setup_window(self):
        super(Settings, self).setup_window()

    def create_widgets(self):
        super(Settings, self).create_widgets()

    def create_layouts(self):
        super(Settings, self).create_layouts()

    def create_connections(self):
        super(Settings, self).create_connections()

    def populate_widgets(self):
        super(Settings, self).populate_widgets()
