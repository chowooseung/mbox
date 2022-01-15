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
TYPE = "control_0"
NAME = "control"
DESCRIPTION = "control 0"


class Block(SubBlock):

    def __init__(self, parent):
        super(Block, self).__init__(parent=parent)
        self["version"] = "{}. {}. {}".format(*VERSION)
        self["comp_type"] = TYPE
        self["comp_name"] = NAME
        self["transforms"] = [pm.datatypes.Matrix().tolist()]

        # specify attr
        self["joint_rig"] = True
        self["leaf_joint"] = False
        self["uni_scale"] = False
        self["mirror_behaviour"] = False
        self["neutral_rotation"] = True
        self["icon"] = "cube"
        self["key_able_attrs"] = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]
        self["default_rotate_order"] = 0
        self["ik_ref_array"] = str()
        self["ctl_size"] = 1

    def from_network(self):
        # common attr pull
        super(Block, self).from_network()

        # specify attr pull
        self["joint_rig"] = self.network.attr("joint_rig").get()
        self["leaf_joint"] = self.network.attr("leaf_joint").get()
        self["uni_scale"] = self.network.attr("uni_scale").get()
        self["icon"] = self.network.attr("icon").get()
        self["mirror_behaviour"] = self.network.attr("mirror_behaviour").get()
        self["neutral_rotation"] = self.network.attr("neutral_rotation").get()
        self["key_able_attrs"] = [k for k in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]
                                          if self.network.attr(k).get()]
        self["default_rotate_order"] = self.network.attr("default_rotate_order").get()
        self["ik_ref_array"] = self.network.attr("ik_ref_array").get()
        self["ctl_size"] = self.network.attr("ctl_size").get()

    def to_network(self):
        # common attr push
        super(Block, self).to_network()

        # specify attr push
        self.network.attr("joint_rig").set(self["joint_rig"])
        self.network.attr("leaf_joint").set(self["leaf_joint"])
        self.network.attr("uni_scale").set(self["uni_scale"])
        self.network.attr("icon").set(self["icon"])
        self.network.attr("mirror_behaviour").set(self["mirror_behaviour"])
        self.network.attr("neutral_rotation").set(self["neutral_rotation"])
        [self.network.attr(a).set(True if a in self["key_able_attrs"] else False)
         for a in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]]
        self.network.attr("default_rotate_order").set(self["default_rotate_order"])
        self.network.attr("ik_ref_array").set(self["ik_ref_array"])

    def guide(self):
        super(Block, self).guide()
        attribute.addAttribute(self.network, "joint_rig", "bool", self["joint_rig"], keyable=False)
        attribute.addAttribute(self.network, "leaf_joint", "bool", self["leaf_joint"], keyable=False)
        attribute.addAttribute(self.network, "uni_scale", "bool", self["uni_scale"], keyable=False)
        attribute.addAttribute(self.network, "mirror_behaviour", "bool", self["mirror_behaviour"], keyable=False)
        attribute.addAttribute(self.network, "neutral_rotation", "bool", self["neutral_rotation"], keyable=False)
        attribute.addAttribute(self.network, "icon", "string", self["icon"])
        for attr in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]:
            attribute.addAttribute(self.network, attr, "bool",
                                   True if attr in self["key_able_attrs"] else False, keyable=False)
        attribute.addAttribute(self.network, "default_rotate_order", "long", self["default_rotate_order"],
                               minValue=0, maxValue=5, keyable=False)
        attribute.addAttribute(self.network, "ik_ref_array", "string", self["ik_ref_array"])
        attribute.addAttribute(self.network, "ctl_size", "float", self["ctl_size"], keyable=False)

        name_format = f"{self['comp_name']}_{self['comp_side']}{self['comp_index']}_%s"
        if isinstance(self.parent, RootBlock):
            parent = self.parent.network.attr("guide").inputs(type="transform")[0]
        else:
            parent = self.parent.network.attr("transforms").inputs(type="transform")[-1]
        guide = icon.guide_root_icon(parent, name_format % "root", m=pm.datatypes.Matrix(self["transforms"][0]))
        size_ref_t = transform.getOffsetPosition(guide, [0, 0, 1])
        size_ref = primitive.addTransform(guide, name_format % "sizeRef", m=size_ref_t)
        attribute.lockAttribute(size_ref)
        attribute.addAttribute(size_ref, "is_guide", "bool", False, keyable=False)
        pm.connectAttr(guide.attr("message"), self.network.attr("guide"))
        pm.connectAttr(size_ref.attr("worldMatrix")[0], self.network.attr("transforms")[0])
        pm.connectAttr(guide.attr("worldMatrix")[0], self.network.attr("transforms")[1])

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

        self.iconsList = ['arrow',
                          'circle',
                          'compas',
                          'cross',
                          'crossarrow',
                          'cube',
                          'cubewithpeak',
                          'cylinder',
                          'diamond',
                          'flower',
                          'null',
                          'pyramid',
                          'sphere',
                          'square']

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

        self.populate_check(self.settings_tab.joint_checkBox, "joint_rig")
        self.enable_leaf_joint()
        self.populate_check(self.settings_tab.leafJoint_checkBox, "leaf_joint")
        self.populate_check(self.settings_tab.uniScale_checkBox, "uni_scale")
        self.populate_check(self.settings_tab.neutralRotation_checkBox,
                           "neutral_rotation")
        self.populate_check(self.settings_tab.mirrorBehaviour_checkBox,
                           "mirror_behaviour")
        self.settings_tab.ctlSize_doubleSpinBox.setValue(
            self._network.attr("ctl_size").get())
        sideIndex = self.iconsList.index(self._network.attr("icon").get())
        self.settings_tab.controlShape_comboBox.setCurrentIndex(sideIndex)

        self.populate_check(self.settings_tab.tx_checkBox, "tx")
        self.populate_check(self.settings_tab.ty_checkBox, "ty")
        self.populate_check(self.settings_tab.tz_checkBox, "tz")
        self.populate_check(self.settings_tab.rx_checkBox, "rx")
        self.populate_check(self.settings_tab.ry_checkBox, "ry")
        self.populate_check(self.settings_tab.rz_checkBox, "rz")
        self.populate_check(self.settings_tab.ro_checkBox, "ro")
        self.populate_check(self.settings_tab.sx_checkBox, "sx")
        self.populate_check(self.settings_tab.sy_checkBox, "sy")
        self.populate_check(self.settings_tab.sz_checkBox, "sz")

        self.settings_tab.ro_comboBox.setCurrentIndex(
            self._network.attr("default_rotate_order").get())

        ikRefArrayItems = self._network.attr("ik_ref_array").get().split(",")
        for item in ikRefArrayItems:
            self.settings_tab.ikRefArray_listWidget.addItem(item)

        # populate connections in main settings
        # for cnx in Guide.connectors:
        #     self.main_tab.connector_comboBox.addItem(cnx)
        # cBox = self.main_tab.connector_comboBox
        # self.connector_items = [cBox.itemText(i) for i in range(cBox.count())]
        # currentConnector = self._network.attr("connector").get()
        # if currentConnector not in self.connector_items:
        #     self.main_tab.connector_comboBox.addItem(currentConnector)
        #     self.connector_items.append(currentConnector)
        #     pm.displayWarning("The current connector: %s, is not a valid "
        #                       "connector for this component. "
        #                       "Build will Fail!!")
        # comboIndex = self.connector_items.index(currentConnector)
        # self.main_tab.connector_comboBox.setCurrentIndex(comboIndex)

    def create_component_layout(self):
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout.addWidget(self.tabs)
        self.settings_layout.addWidget(self.close_button)

        self.setLayout(self.settings_layout)

    def create_component_connections(self):
        self.settings_tab.joint_checkBox.stateChanged.connect(
            self.enable_leaf_joint)
        self.settings_tab.joint_checkBox.stateChanged.connect(
            partial(self.update_check,
                    self.settings_tab.joint_checkBox,
                    "joint_rig"))
        self.settings_tab.leafJoint_checkBox.stateChanged.connect(
            partial(self.update_check,
                    self.settings_tab.leafJoint_checkBox,
                    "leaf_joint"))
        self.settings_tab.uniScale_checkBox.stateChanged.connect(
            partial(self.update_check,
                    self.settings_tab.uniScale_checkBox,
                    "uni_scale"))
        self.settings_tab.neutralRotation_checkBox.stateChanged.connect(
            partial(self.update_check,
                    self.settings_tab.neutralRotation_checkBox,
                    "neutral_rotation"))
        self.settings_tab.mirrorBehaviour_checkBox.stateChanged.connect(
            partial(self.update_check,
                    self.settings_tab.mirrorBehaviour_checkBox,
                    "mirror_behaviour"))
        self.settings_tab.ctlSize_doubleSpinBox.valueChanged.connect(
            partial(self.update_spin_box,
                    self.settings_tab.ctlSize_doubleSpinBox,
                    "ctl_size"))
        self.settings_tab.controlShape_comboBox.currentIndexChanged.connect(
            partial(self.update_control_shape,
                    self.settings_tab.controlShape_comboBox,
                    self.iconsList, "icon"))

        self.settings_tab.tx_checkBox.stateChanged.connect(
            partial(self.update_check, self.settings_tab.tx_checkBox, "tx"))
        self.settings_tab.ty_checkBox.stateChanged.connect(
            partial(self.update_check, self.settings_tab.ty_checkBox, "ty"))
        self.settings_tab.tz_checkBox.stateChanged.connect(
            partial(self.update_check, self.settings_tab.tz_checkBox, "tz"))
        self.settings_tab.rx_checkBox.stateChanged.connect(
            partial(self.update_check, self.settings_tab.rx_checkBox, "rx"))
        self.settings_tab.ry_checkBox.stateChanged.connect(
            partial(self.update_check, self.settings_tab.ry_checkBox, "ry"))
        self.settings_tab.rz_checkBox.stateChanged.connect(
            partial(self.update_check, self.settings_tab.rz_checkBox, "rz"))
        self.settings_tab.ro_checkBox.stateChanged.connect(
            partial(self.update_check, self.settings_tab.ro_checkBox, "ro"))
        self.settings_tab.sx_checkBox.stateChanged.connect(
            partial(self.update_check, self.settings_tab.sx_checkBox, "sx"))
        self.settings_tab.sy_checkBox.stateChanged.connect(
            partial(self.update_check, self.settings_tab.sy_checkBox, "sy"))
        self.settings_tab.sz_checkBox.stateChanged.connect(
            partial(self.update_check, self.settings_tab.sz_checkBox, "sz"))

        self.settings_tab.ro_comboBox.currentIndexChanged.connect(
            partial(self.update_combo_box,
                    self.settings_tab.ro_comboBox,
                    "default_rotate_order"))

        self.settings_tab.ikRefArrayAdd_pushButton.clicked.connect(
            partial(self.add_item_to_list_widget,
                    self.settings_tab.ikRefArray_listWidget,
                    "ik_ref_array"))
        self.settings_tab.ikRefArrayRemove_pushButton.clicked.connect(
            partial(self.remove_selected_from_list_widget,
                    self.settings_tab.ikRefArray_listWidget,
                    "ik_ref_array"))
        self.settings_tab.ikRefArray_listWidget.installEventFilter(self)

        # self.main_tab.connector_comboBox.currentIndexChanged.connect(
        #     partial(self.update_connector,
        #             self.main_tab.connector_comboBox,
        #             self.connector_items))

    def enable_leaf_joint(self):
        state = self.settings_tab.joint_checkBox.isChecked()
        self.settings_tab.leafJoint_checkBox.setEnabled(state)

    def dockCloseEventTriggered(self):
        pyqt.deleteInstances(self, MayaQDockWidget)
