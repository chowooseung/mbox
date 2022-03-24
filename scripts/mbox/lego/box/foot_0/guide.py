# -*- coding: utf-8 -*

#
from functools import partial

# maya
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget

# mbox
from mbox.core import (
    icon,
    curve
)

from mbox.lego.lib import (
    RootBlock,
    SubBlock,
    blueprint_from_guide
)
from mbox.lego.box import settings
from . import settings_ui
from mbox.lego.box.chain_guide_initializer import exec_window

# mgear
from mgear.core import pyqt, attribute, transform, vector
from mgear.vendor.Qt import QtWidgets, QtCore

# block info
AUTHOR = "cho wooseoung"
URL = None
EMAIL = "chowooseoung@gmail.com"
VERSION = [0, 0, 1]
TYPE = "foot_0"
NAME = "foot"
DESCRIPTION = "foot 0"


class Block(SubBlock):

    CONNECTOR = ["arm_2jnt_0"]

    def __init__(self, parent):
        super(Block, self).__init__(parent=parent)
        self["version"] = "{}. {}. {}".format(*VERSION)
        self["comp_type"] = TYPE
        self["comp_name"] = NAME
        root_m = transform.getTransformFromPos([0, 0, 0]).tolist()
        inner_m = transform.getTransformFromPos([-1, -1, 1]).tolist()
        outer_m = transform.getTransformFromPos([1, -1, 1]).tolist()
        heel_m = transform.getTransformFromPos([0, -1, -1]).tolist()
        ball_m = transform.getTransformFromPos([0, -0.5, 1]).tolist()
        toe_m = transform.getTransformFromPos([0, -0.5, 2]).tolist()
        self["transforms"] = [root_m, inner_m, outer_m, heel_m, ball_m, toe_m]

        # specify attr

    def from_network(self):
        # common attr pull
        super(Block, self).from_network()

        # specify attr pull
        self["transforms"] = list()
        for trans in self.network.attr("transforms").get():
            self["transforms"].append(trans.tolist())

    def to_network(self):
        # common attr push
        super(Block, self).to_network()

        # specify attr push
        for index, node in enumerate(self.network.attr("transforms").inputs(type="transform")):
            m = pm.datatypes.Matrix(self["transforms"][index])
            node.setMatrix(m, worldSpace=True)

    def guide(self):
        super(Block, self).guide()

        name_format = f"{self['comp_name']}_{self['comp_side']}{self['comp_index']}_%s"
        if isinstance(self.parent, RootBlock):
            parent = self.top.network.attr("guide").inputs(type="transform")[0]
        else:
            parent = self.parent.network.attr("transforms").inputs(type="transform")[-1]
        guide = icon.guide_root_icon(parent, name_format % "root", m=pm.datatypes.Matrix(self["transforms"][0]))
        pm.connectAttr(guide.attr("message"), self.network.attr("guide"))
        pm.connectAttr(guide.attr("worldMatrix")[0], self.network.attr("transforms")[0])
        heel = icon.guide_locator_icon(guide, name_format % "heel", m=pm.datatypes.Matrix(self["transforms"][3]))
        pm.connectAttr(heel.attr("worldMatrix")[0], self.network.attr("transforms")[3])
        inner = icon.guide_locator_icon(heel, name_format % "inner", m=pm.datatypes.Matrix(self["transforms"][1]))
        pm.connectAttr(inner.attr("worldMatrix")[0], self.network.attr("transforms")[1])
        outer = icon.guide_locator_icon(heel, name_format % "outer", m=pm.datatypes.Matrix(self["transforms"][2]))
        pm.connectAttr(outer.attr("worldMatrix")[0], self.network.attr("transforms")[2])
        ball = icon.guide_locator_icon(guide, name_format % "ball", m=pm.datatypes.Matrix(self["transforms"][4]))
        pm.connectAttr(ball.attr("worldMatrix")[0], self.network.attr("transforms")[4])
        toe = icon.guide_locator_icon(ball, name_format % "toe", m=pm.datatypes.Matrix(self["transforms"][5]))
        pm.connectAttr(toe.attr("worldMatrix")[0], self.network.attr("transforms")[5])

        curve.add_cns_curve(guide, name_format % "display0_crv", [guide, heel])
        curve.add_cns_curve(guide, name_format % "display1_crv", [inner, heel, outer])
        curve.add_cns_curve(guide, name_format % "display2_crv", [guide, ball, toe])

        return guide


class BlockSettingsUI(QtWidgets.QDialog, settings_ui.Ui_Form):

    def __init__(self, parent=None):
        super(BlockSettingsUI, self).__init__(parent)
        self.setupUi(self)


class BlockSettings(MayaQWidgetDockableMixin, settings.BlockSettings):

    def __init__(self, parent=None):
        self.toolName = TYPE
        # Delete old instances of the componet settings window.
        pyqt.deleteInstances(self, MayaQDockWidget)

        super(BlockSettings, self).__init__(parent=parent)
        self.settings_tab = BlockSettingsUI()

        self.setup_component_setting_window()
        self.populate_component_controls()
        self.create_component_layout()
        self.create_component_connections()

    def setup_component_setting_window(self):
        self.mayaMainWindow = pyqt.maya_main_window()

        self.setObjectName(self.toolName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(TYPE)

    def populate_component_controls(self):
        """Populate Controls

        Populate the controls values from the custom attributes of the
        component.

        """
        # populate tab
        self.tabs.insertTab(1, self.settings_tab, "Component Settings")

        items_list = [i.text() for i in self.settings_tab.ikRefArray_listWidget.findItems(
            "", QtCore.Qt.MatchContains)]
        # Quick clean the first empty item
        if items_list and not items_list[0]:
            self.settings_tab.ikRefArray_listWidget.takeItem(0)

        # populate connections in main settings
        for cnx in Block.CONNECTOR:
            self.main_tab.connector_comboBox.addItem(cnx)
        cBox = self.main_tab.connector_comboBox
        self.connector_items = [cBox.itemText(i) for i in range(cBox.count())]
        currentConnector = self._network.attr("connector").get()
        if currentConnector not in self.connector_items:
            self.main_tab.connector_comboBox.addItem(currentConnector)
            self.connector_items.append(currentConnector)
            pm.displayWarning("The current connector: %s, is not a valid "
                              "connector for this component. "
                              "Build will Fail!!")
        comboIndex = self.connector_items.index(currentConnector)
        self.main_tab.connector_comboBox.setCurrentIndex(comboIndex)

    def create_component_layout(self):
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout.addWidget(self.tabs)
        self.settings_layout.addWidget(self.close_button)

        self.setLayout(self.settings_layout)

    def create_component_connections(self):
        self.main_tab.connector_comboBox.currentIndexChanged.connect(
            partial(self.update_connector,
                    self.main_tab.connector_comboBox,
                    self.connector_items))

    def dockCloseEventTriggered(self):
        pyqt.deleteInstances(self, MayaQDockWidget)
