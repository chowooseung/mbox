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
TYPE = "chain_0"
NAME = "chain"
DESCRIPTION = "chain 0"


class Block(SubBlock):

    CONNECTOR = []

    def __init__(self, parent):
        super(Block, self).__init__(parent=parent)
        self["version"] = "{}. {}. {}".format(*VERSION)
        self["comp_type"] = TYPE
        self["comp_name"] = NAME
        self["transforms"] = list()
        self["ik_ref_array"] = str()
        self["roll_offset"] = float()
        self["roll_rotation"] = list()

        # specify attr

    def from_network(self):
        # common attr pull
        super(Block, self).from_network()

        # specify attr pull
        self["transforms"] = list()
        for trans in self.network.attr("transforms").get():
            self["transforms"].append(trans.tolist())
        self["ik_ref_array"] = self.network.attr("ik_ref_array").get()
        self["roll_offset"] = self.network.attr("roll_offset").get()
        self["roll_x"] = self.network.attr("roll_x").get()
        self["roll_y"] = self.network.attr("roll_y").get()
        self["roll_z"] = self.network.attr("roll_z").get()

    def to_network(self):
        # common attr push
        super(Block, self).to_network()

        # specify attr push
        for index, node in enumerate(self.network.attr("transforms").inpus(type="transform")):
            m = pm.datatypes.Matrix(self["transforms"][index])
            node.setMatrix(m, worldSpace=True)
        blade = self.network.attr("roll_offset").input(type="transform")
        if blade:
            roll = blade[0]
        else:
            roll = self.network
        roll.attr("roll_offset").set(self["roll_offset"])
        roll.attr("roll_x").set(self["roll_x"])
        roll.attr("roll_y").set(self["roll_y"])
        roll.attr("roll_z").set(self["roll_z"])

    def guide(self):
        if not self["transforms"]:
            ui = exec_window()
            if ui:
                axis = ui.dir_axis
                offset = ui.spacing
                number = ui.sections_number
                if axis == 0:  # X
                    offVec = pm.datatypes.Vector(offset, 0, 0)
                elif axis == 3:  # -X
                    offVec = pm.datatypes.Vector(offset * -1, 0, 0)
                elif axis == 1:  # Y
                    offVec = pm.datatypes.Vector(0, offset, 0)
                elif axis == 4:  # -Y
                    offVec = pm.datatypes.Vector(0, offset * -1, 0)
                elif axis == 2:  # Z
                    offVec = pm.datatypes.Vector(0, 0, offset)
                elif axis == 5:  # -Z
                    offVec = pm.datatypes.Vector(0, 0, offset * -1)

                newPosition = pm.datatypes.Vector(0, 0, 0)
                pos_list = [newPosition]
                for i in range(number):
                    newPosition = offVec + newPosition
                    pos_list.append(newPosition)
                self["transforms"] = [transform.getTransformFromPos(x).tolist() for x in pos_list]
            else:
                return
        super(Block, self).guide()
        attribute.addAttribute(self.network, "ik_ref_array", "string", self["ik_ref_array"])
        attribute.addAttribute(self.network, "roll_offset", "float", self["roll_offset"], keyable=False)
        attribute.addAttribute(self.network, "roll_x", "doubleAngle", self["roll_x"], keyable=False)
        attribute.addAttribute(self.network, "roll_y", "doubleAngle", self["roll_y"], keyable=False)
        attribute.addAttribute(self.network, "roll_z", "doubleAngle", self["roll_z"], keyable=False)

        name_format = f"{self['comp_name']}_{self['comp_side']}{self['comp_index']}_%s"
        if isinstance(self.parent, RootBlock):
            parent = self.top.network.attr("guide").inputs(type="transform")[0]
        else:
            parent = self.parent.network.attr("transforms").inputs(type="transform")[-1]
        guide = icon.guide_root_icon(parent, name_format % "root", m=pm.datatypes.Matrix(self["transforms"][0]))
        pm.connectAttr(guide.attr("message"), self.network.attr("guide"))
        pm.connectAttr(guide.attr("worldMatrix")[0], self.network.attr("transforms")[0])
        parent = [guide]
        for index, trans in enumerate(self["transforms"][1:]):
            parent.append(icon.guide_locator_icon(parent[index], name_format % f"loc{index}", m=pm.datatypes.Matrix(trans)))
            pm.connectAttr(parent[index + 1].attr("worldMatrix")[0], self.network.attr("transforms")[index + 1])
        curve.add_cns_curve(parent[0], name_format % "display_crv", parent)
        blade = icon.guide_blade_icon(guide, parent[1], name_format % "blade")
        blade.attr("roll_offset").set(self["roll_offset"])
        pm.connectAttr(blade.attr("roll_offset"), self.network.attr("roll_offset"))
        pm.connectAttr(blade.attr("rx"), self.network.attr("roll_x"))
        pm.connectAttr(blade.attr("ry"), self.network.attr("roll_y"))
        pm.connectAttr(blade.attr("rz"), self.network.attr("roll_z"))

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

        if self._network.attr("ik_ref_array").get():
            ikRefArrayItems = self._network.attr("ik_ref_array").get().split(",")
            items = [x.split(" | ") for x in ikRefArrayItems]
            root = self._guide.getParent(generations=-1)
            blueprint = blueprint_from_guide(root)
            for index, oid in items:
                block = blueprint.find_block_with_oid(oid)
                if block is not None:
                    new_item = QtWidgets.QListWidgetItem()
                    new_item.setText(block.ins_name)
                    new_item.setData(QtCore.Qt.UserRole, f"{index} | {oid}")
                    self.settings_tab.ikRefArray_listWidget.addItem(new_item)

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
        self.settings_tab.ikRefArrayAdd_pushButton.clicked.connect(
            partial(self.add_item_to_list_widget_m,
                    self.settings_tab.ikRefArray_listWidget,
                    "ik_ref_array"))
        self.settings_tab.ikRefArrayRemove_pushButton.clicked.connect(
            partial(self.remove_selected_from_list_widget_m,
                    self.settings_tab.ikRefArray_listWidget,
                    "ik_ref_array"))
        self.settings_tab.ikRefArray_listWidget.installEventFilter(self)

        self.main_tab.connector_comboBox.currentIndexChanged.connect(
            partial(self.update_connector,
                    self.main_tab.connector_comboBox,
                    self.connector_items))

    def dockCloseEventTriggered(self):
        pyqt.deleteInstances(self, MayaQDockWidget)
