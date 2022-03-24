# -*- coding: utf-8 -*-

# mbox
from . import actions, common_settings_ui

# qt.py
from mgear.vendor.Qt import QtWidgets, QtCore, QtGui


class CommonSettings(common_settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(CommonSettings, self).__init__(parent=parent)
        self.setupUi(self)


class Settings(QtWidgets.QDialog, actions.Actions):

    def __init(self, parent=None):
        super(Settings, self).__init__(parent=parent)
        self.common_settings_ui = CommonSettings()

        self.setup_window()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        self.populate_widgets()

    def setup_window(self):
        pass

    def create_widgets(self):
        pass

    def create_layouts(self):
        pass

    def create_connections(self):
        pass

    def populate_widgets(self):
        pass
