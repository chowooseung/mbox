# -*- coding: utf-8 -*-

#
from functools import partial

# maya
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget

# mbox
from mbox.core import (
        icon,
        curve)
from mbox.lego.lib import (
        RootBlock,
        SubBlock,
        blueprint_from_guide)
from mbox.lego.box import settings
from . import settings_ui

# mgear
from mgear.core import pyqt, attribute, primitive, transform
from mgear.core import icon as micon
from mgear.vendor.Qt import QtWidgets, QtCore

# block info
AUTHOR = "cho wooseoung"
URL = None
EMAIL = "chowooseoung@gmail.com"
VERSION = [0, 0, 1]
TYPE = "arm_2jnt_0"
NAME = "arm2jnt"
DESCRIPTION = "arm_2jnt 0"


class Block(SubBlock):

    CONNECTOR = []

    def __init__(self, parent):
        super(Block, self).__init__(parent=parent)
        self["version"] = "{}. {}. {}".format(*VERSION)
        self["comp_type"] = TYPE
        self["comp_name"] = NAME
        root_m = transform.getTransformFromPos([0, 0, 0]).tolist()
        arm0_m = transform.getTransformFromPos([3, 0, -.01]).tolist()
        arm1_m = transform.getTransformFromPos([6, 0, 0]).tolist()
        arm2_m = transform.getTransformFromPos([7, 0, 0]).tolist()
        self["transforms"] = [root_m, arm0_m, arm2_m, arm1_m]

        # specify attr
        self["ik_t_r"] = False
        self["blend"] = 0.0
        self["mirror_ik"] = True
        self["mirror_mid"] = True
        self["ik_ref_array"] = str()
        self["upv_ref_array"] = str()
        self["elbow_ref_array"] = str()
        self["div"] = 2

    def from_network(self):
        # common attr pull
        super(Block, self).from_network()

        # specify attr pull
        self["ik_t_r"] = self.network.attr("ik_t_r").get()
        self["blend"] = self.network.attr("blend").get()
        self["mirror_ik"] = self.network.attr("mirror_ik").get()
        self["mirror_mid"] = self.network.attr("mirror_mid").get()
        self["ik_ref_array"] = self.network.attr("ik_ref_array").get()
        self["upv_ref_array"] = self.network.attr("upv_ref_array").get()
        self["elbow_ref_array"] = self.network.attr("elbow_ref_array").get()
        self["div"] = self.network.attr("div").get()

    def to_network(self):
        # common attr push
        super(Block, self).to_network()

        # specify attr push
        self.network.attr("ik_t_r").set(self["ik_t_r"])
        self.network.attr("blend").set(self["blend"])
        self.network.attr("mirror_ik").set(self["mirror_ik"])
        self.network.attr("mirror_mid").set(self["mirror_mid"])
        self.network.attr("ik_ref_array").set(self["ik_ref_array"])
        self.network.attr("upv_ref_array").set(self["upv_ref_array"])
        self.network.attr("elbow_ref_array").set(self["elbow_ref_array"])
        self.network.attr("div").set(self["div"])

    def guide(self):
        super(Block, self).guide()
        attribute.addAttribute(self.network, "ik_t_r", "bool", self["ik_t_r"], keyable=False)
        attribute.addAttribute(self.network, "blend", "float", self["blend"], keyable=False)
        attribute.addAttribute(self.network, "mirror_ik", "bool", self["mirror_ik"], keyable=False)
        attribute.addAttribute(self.network, "mirror_mid", "bool", self["mirror_mid"], keyable=False)
        attribute.addAttribute(self.network, "ik_ref_array", "string", self["ik_ref_array"])
        attribute.addAttribute(self.network, "upv_ref_array", "string", self["upv_ref_array"])
        attribute.addAttribute(self.network, "elbow_ref_array", "string", self["elbow_ref_array"])
        attribute.addAttribute(self.network, "div", "long", self["div"], keyable=False)

        name_format = f"{self['comp_name']}_{self['comp_side']}{self['comp_index']}_%s"
        if isinstance(self.parent, RootBlock):
            parent = self.top.network.attr("guide").inputs(type="transform")[0]
        else:
            parent = self.parent.network.attr("transforms").inputs(type="transform")[-1]
        guide = icon.guide_root_icon(parent, name_format % "root", m=pm.datatypes.Matrix(self["transforms"][0]))
        arm0 = icon.guide_locator_icon(guide, name_format % "aim0", m=pm.datatypes.Matrix(self["transforms"][1]))
        arm1 = icon.guide_locator_icon(arm0, name_format % "aim1", m=pm.datatypes.Matrix(self["transforms"][3]))
        arm2 = icon.guide_locator_icon(arm1, name_format % "aim2", m=pm.datatypes.Matrix(self["transforms"][2]))
        curve.add_cns_curve(guide, name_format % "display_crv", [guide, arm0, arm1, arm2])

        pm.connectAttr(guide.attr("message"), self.network.attr("guide"))
        pm.connectAttr(guide.attr("worldMatrix")[0], self.network.attr("transforms")[0])
        pm.connectAttr(arm0.attr("worldMatrix")[0], self.network.attr("transforms")[1])
        pm.connectAttr(arm1.attr("worldMatrix")[0], self.network.attr("transforms")[3])
        pm.connectAttr(arm2.attr("worldMatrix")[0], self.network.attr("transforms")[2])

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

        self.settings_tab.ikfk_slider.setValue(
                int(self._network.attr("blend").get() * 100))
        self.settings_tab.ikfk_spinBox.setValue(
                int(self._network.attr("blend").get() * 100))
        self.populate_check(self.settings_tab.ikTR_checkBox, "ik_t_r")
        #  self.populate_check(
        #          self.settings_tab.guideOrientWrist_checkBox, "guideOrientWrist")
        self.populate_check(self.settings_tab.mirrorMid_checkBox, "mirror_mid")
        self.populate_check(self.settings_tab.mirrorIK_checkBox, "mirror_ik")
        self.settings_tab.div_spinBox.setValue(self._network.attr("div").get())

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

        items_list = [i.text() for i in self.settings_tab.upvRefArray_listWidget.findItems(
            "", QtCore.Qt.MatchContains)]
        # Quick clean the first empty item
        if items_list and not items_list[0]:
            self.settings_tab.upvRefArray_listWidget.takeItem(0)

        if self._network.attr("upv_ref_array").get():
            upvRefArrayItems = self._network.attr("upv_ref_array").get().split(",")
            items = [x.split(" | ") for x in upvRefArrayItems]
            root = self._guide.getParent(generations=-1)
            blueprint = blueprint_from_guide(root)
            for index, oid in items:
                block = blueprint.find_block_with_oid(oid)
                if block is not None:
                    new_item = QtWidgets.QListWidgetItem()
                    new_item.setText(block.ins_name)
                    new_item.setData(QtCore.Qt.UserRole, f"{index} | {oid}")
                    self.settings_tab.upvRefArray_listWidget.addItem(new_item)

        items_list = [i.text() for i in self.settings_tab.pinRefArray_listWidget.findItems(
            "", QtCore.Qt.MatchContains)]
        # Quick clean the first empty item
        if items_list and not items_list[0]:
            self.settings_tab.pinRefArray_listWidget.takeItem(0)

        if self._network.attr("elbow_ref_array").get():
            elbowRefArrayItems = self._network.attr("elbow_ref_array").get().split(",")
            items = [x.split(" | ") for x in elbowRefArrayItems]
            root = self._guide.getParent(generations=-1)
            blueprint = blueprint_from_guide(root)
            for index, oid in items:
                block = blueprint.find_block_with_oid(oid)
                if block is not None:
                    new_item = QtWidgets.QListWidgetItem()
                    new_item.setText(block.ins_name)
                    new_item.setData(QtCore.Qt.UserRole, f"{index} | {oid}")
                    self.settings_tab.pinRefArray_listWidget.addItem(new_item)

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
        self.settings_tab.ikfk_slider.valueChanged.connect(
                partial(self.update_slider, self.settings_tab.ikfk_slider, "blend"))
        self.settings_tab.ikfk_spinBox.valueChanged.connect(
                partial(self.update_slider, self.settings_tab.ikfk_spinBox, "blend"))

        self.settings_tab.div_spinBox.valueChanged.connect(
                partial(self.update_spin_box, self.settings_tab.div_spinBox, "div"))

        self.settings_tab.ikTR_checkBox.stateChanged.connect(
                partial(self.update_check, self.settings_tab.ikTR_checkBox, "ik_t_r"))

        #  self.settings_tab.guideOrientWrist_checkBox.stateChanged.connect(
        #          partial(self.update_check,
        #              self.settings_tab.guideOrientWrist_checkBox,
        #              "guideOrientWrist"))
        self.settings_tab.mirrorMid_checkBox.stateChanged.connect(
                partial(self.update_check,
                    self.settings_tab.mirrorMid_checkBox, "mirror_mid"))
        self.settings_tab.mirrorIK_checkBox.stateChanged.connect(
                partial(self.update_check,
                    self.settings_tab.mirrorIK_checkBox,
                    "mirror_ik"))
        self.settings_tab.ikRefArrayAdd_pushButton.clicked.connect(
                partial(self.add_item_to_list_widget_m,
                    self.settings_tab.ikRefArray_listWidget,
                    "ik_ref_array"))
        self.settings_tab.ikRefArrayRemove_pushButton.clicked.connect(
                partial(self.remove_selected_from_list_widget_m,
                    self.settings_tab.ikRefArray_listWidget,
                    "ik_ref_array"))
        self.settings_tab.ikRefArray_copyRef_pushButton.clicked.connect(
                partial(self.copy_from_list_widget_m,
                    self.settings_tab.upvRefArray_listWidget,
                    self.settings_tab.ikRefArray_listWidget,
                    "ik_ref_array"))

        self.settings_tab.ikRefArray_listWidget.installEventFilter(self)

        self.settings_tab.upvRefArrayAdd_pushButton.clicked.connect(
                partial(self.add_item_to_list_widget_m,
                    self.settings_tab.upvRefArray_listWidget,
                    "upv_ref_array"))
        self.settings_tab.upvRefArrayRemove_pushButton.clicked.connect(
                partial(self.remove_selected_from_list_widget_m,
                    self.settings_tab.upvRefArray_listWidget,
                    "upv_ref_array"))
        self.settings_tab.upvRefArray_copyRef_pushButton.clicked.connect(
                partial(self.copy_from_list_widget_m,
                    self.settings_tab.ikRefArray_listWidget,
                    self.settings_tab.upvRefArray_listWidget,
                    "upv_ref_array"))

        self.settings_tab.upvRefArray_listWidget.installEventFilter(self)

        self.settings_tab.pinRefArrayAdd_pushButton.clicked.connect(
                partial(self.add_item_to_list_widget_m,
                    self.settings_tab.pinRefArray_listWidget,
                    "elbow_ref_array"))
        self.settings_tab.pinRefArrayRemove_pushButton.clicked.connect(
                partial(self.remove_selected_from_list_widget_m,
                    self.settings_tab.pinRefArray_listWidget,
                    "elbow_ref_array"))
        self.settings_tab.pinRefArray_copyRef_pushButton.clicked.connect(
                partial(self.copy_from_list_widget_m,
                    self.settings_tab.ikRefArray_listWidget,
                    self.settings_tab.pinRefArray_listWidget,
                    "elbow_ref_array"))

        self.settings_tab.pinRefArray_listWidget.installEventFilter(self)

        self.main_tab.connector_comboBox.currentIndexChanged.connect(
                partial(self.update_connector,
                    self.main_tab.connector_comboBox,
                    self.connector_items))

    def eventFilter(self, sender, event):
        if event.type() == QtCore.QEvent.ChildRemoved:
            if sender == self.settings_tab.ikRefArray_listWidget:
                self.update_list_attr(sender, "ik_ref_array")
            elif sender == self.settings_tab.upvRefArray_listWidget:
                self.update_list_attr(sender, "upv_ref_array")
            elif sender == self.settings_tab.pinRefArray_listWidget:
                self.update_list_attr(sender, "elbow_ref_array")
            return True
        else:
            return QtWidgets.QDialog.eventFilter(self, sender, event)

    def dockCloseEventTriggered(self):
        pyqt.deleteInstances(self, MayaQDockWidget)
