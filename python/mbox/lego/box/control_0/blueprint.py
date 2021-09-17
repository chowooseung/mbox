# -*- coding:utf-8 -*-
AUTHOR = "chowooseoung"
TYPE = "control_0"
VERSION = "0.0.0"
NAME = "control"
DIRECTION = "center"
URL = ""
DESCRIPTION = "1 controller"

#
from collections import OrderedDict
from functools import partial

# maya
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget

# mbox
from mbox.lego.blueprint import get_block_index
from mbox.core import attribute, icon, pyqt
from mbox.vendor.Qt import QtWidgets, QtCore

from .settingui import sui

def initialize_(bp, parent):
    data = OrderedDict()
    data["component"] = TYPE
    data["version"] = VERSION
    data["name"] = NAME
    data["direction"] = DIRECTION
    data["index"] = get_block_index(bp, data["name"], data["direction"])
    data["joint"] = True
    data["jointAxis"] = ["x", "y"]
    data["transforms"] = [pm.datatypes.Matrix().tolist()]
    data["priority"] = 1
    data["parent"] = parent
    data["meta"] = OrderedDict()
    data["meta"]["asWorld"] = False
    data["meta"]["mirrorBehaviour"] = False
    data["meta"]["worldOrientAxis"] = True
    data["meta"]["keyAbleAttrs"] = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]

    return data


def initialize(affects, bp):
    network = pm.createNode("network")
    attribute.add(network, "guide", "message")
    attribute.add(network, "rig", "message")
    attribute.add(network, "component", "string", bp["component"])
    attribute.add(network, "version", "string", bp["version"])
    attribute.add(network, "name", "string", bp["name"])
    attribute.add_enum(network, "direction", bp["direction"], ["center", "right", "left"], keyable=False)
    attribute.add(network, "index", "string", bp["index"])
    attribute.add(network, "joint", "bool", bp["joint"], keyable=False)
    attribute.add(network, "primaryAxis", "string", bp["jointAxis"][0])
    attribute.add(network, "secondaryAxis", "string", bp["jointAxis"][1])
    attribute.add(network, "transforms", "matrix", multi=True)
    for index, transform in enumerate(bp["transforms"]):
        network.attr("transforms")[index].set(pm.datatypes.Matrix(transform))
    attribute.add(network, "asWorld", "bool", bp["meta"]["asWorld"], keyable=False)
    attribute.add(network, "mirrorBehaviour", "bool", bp["meta"]["mirrorBehaviour"], keyable=False)
    attribute.add(network, "worldOrientAxis", "bool", bp["meta"]["worldOrientAxis"], keyable=False)
    for attr in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]:
        attribute.add(network, attr, "bool", True if attr in bp["meta"]["keyAbleAttrs"] else False, keyable=False)
    affects >> network.affectedBy[0]
    attribute.add(network, "parent", "string", bp["parent"])
    attribute.add(network, "priority", "long", bp["priority"], keyable=False, minValue=0)

    return network


def blueprint(parent, bp):
    """

    :param parent:
    :param bp:
    :return:
    """
    # name
    root_n = "{name}_{direction}{index}_root".format(name=bp["name"], direction=bp["direction"], index=bp["index"])

    # create
    root = icon.guide_root_icon(parent, root_n, m=pm.datatypes.Matrix(bp["transforms"][0]))
    network = initialize(parent.getParent(generations=-1).message.outputs(type="network")[0].affects[0], bp)

    # attribute
    attribute.hide(root, "v")
    attribute.lock(root, "v")
    root.message >> network.guide
    root.worldMatrix >> network.transforms[0]


def get_block_info(node):
    """ get specific block meta info

    :param node: network node
    :return: meta data
    """
    data = OrderedDict()
    data["asWorld"] = node.attr("asWorld").get()
    data["mirrorBehaviour"] = node.attr("mirrorBehaviour").get()
    data["worldOrientAxis"] = node.attr("worldOrientAxis").get()
    data["keyAbleAttrs"] = \
        [a for a in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"] if node.attr(a).get()]

    return data


class componentSettings(MayaQWidgetDockableMixin, guide.componentMainSettings):
    """Create the component setting window"""

    def __init__(self, parent=None):
        self.toolName = TYPE
        # Delete old instances of the componet settings window.
        pyqt.deleteInstances(self, MayaQDockWidget)

        super(self.__class__, self).__init__(parent=parent)
        self.settingsTab = settingsTab()

        self.setup_componentSettingWindow()
        self.create_componentControls()
        self.populate_componentControls()
        self.create_componentLayout()
        self.create_componentConnections()

    def setup_componentSettingWindow(self):
        self.mayaMainWindow = pyqt.maya_main_window()

        self.setObjectName(self.toolName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(TYPE)
        self.resize(280, 780)

    def create_componentControls(self):
        return

    def populate_componentControls(self):
        """Populate Controls

        Populate the controls values from the custom attributes of the
        component.

        """
        # populate tab
        self.tabs.insertTab(1, self.settingsTab, "Component Settings")

        # populate component settings
        self.settingsTab.ikfk_slider.setValue(
            int(self.root.attr("blend").get() * 100))
        self.settingsTab.ikfk_spinBox.setValue(
            int(self.root.attr("blend").get() * 100))
        self.settingsTab.maxStretch_spinBox.setValue(
            self.root.attr("maxstretch").get())
        self.populateCheck(self.settingsTab.ikTR_checkBox, "ikTR")
        self.populateCheck(self.settingsTab.supportJoints_checkBox,
                           "supportJoints")
        self.populateCheck(self.settingsTab.mirrorMid_checkBox, "mirrorMid")
        self.populateCheck(self.settingsTab.mirrorIK_checkBox, "mirrorIK")
        self.populateCheck(self.settingsTab.extraTweak_checkBox, "extraTweak")
        self.settingsTab.div0_spinBox.setValue(self.root.attr("div0").get())
        self.settingsTab.div1_spinBox.setValue(self.root.attr("div1").get())
        ikRefArrayItems = self.root.attr("ikrefarray").get().split(",")

        for item in ikRefArrayItems:
            self.settingsTab.ikRefArray_listWidget.addItem(item)

        upvRefArrayItems = self.root.attr("upvrefarray").get().split(",")
        for item in upvRefArrayItems:
            self.settingsTab.upvRefArray_listWidget.addItem(item)

        pinRefArrayItems = self.root.attr("pinrefarray").get().split(",")
        for item in pinRefArrayItems:
            self.settingsTab.pinRefArray_listWidget.addItem(item)

        # populate connections in main settings
        self.c_box = self.mainSettingsTab.connector_comboBox
        for cnx in Guide.connectors:
            self.c_box.addItem(cnx)
        self.connector_items = [self.c_box.itemText(i) for i in
                                range(self.c_box.count())]

        currentConnector = self.root.attr("connector").get()
        if currentConnector not in self.connector_items:
            self.c_box.addItem(currentConnector)
            self.connector_items.append(currentConnector)
            pm.displayWarning(
                "The current connector: %s, is not a valid connector for this"
                " component. Build will Fail!!")
        comboIndex = self.connector_items.index(currentConnector)
        self.c_box.setCurrentIndex(comboIndex)

    def create_componentLayout(self):

        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout.addWidget(self.tabs)
        self.settings_layout.addWidget(self.close_button)

        self.setLayout(self.settings_layout)

    def create_componentConnections(self):

        self.settingsTab.ikfk_slider.valueChanged.connect(
            partial(self.updateSlider, self.settingsTab.ikfk_slider, "blend"))

        self.settingsTab.ikfk_spinBox.valueChanged.connect(
            partial(self.updateSlider, self.settingsTab.ikfk_spinBox, "blend"))

        self.settingsTab.maxStretch_spinBox.valueChanged.connect(
            partial(self.updateSpinBox,
                    self.settingsTab.maxStretch_spinBox, "maxstretch"))

        self.settingsTab.div0_spinBox.valueChanged.connect(
            partial(self.updateSpinBox, self.settingsTab.div0_spinBox, "div0"))

        self.settingsTab.div1_spinBox.valueChanged.connect(
            partial(self.updateSpinBox, self.settingsTab.div1_spinBox, "div1"))

        self.settingsTab.squashStretchProfile_pushButton.clicked.connect(
            self.setProfile)

        self.settingsTab.ikTR_checkBox.stateChanged.connect(
            partial(self.updateCheck, self.settingsTab.ikTR_checkBox, "ikTR"))

        self.settingsTab.supportJoints_checkBox.stateChanged.connect(
            partial(self.updateCheck,
                    self.settingsTab.supportJoints_checkBox,
                    "supportJoints"))

        self.settingsTab.mirrorMid_checkBox.stateChanged.connect(
            partial(self.updateCheck,
                    self.settingsTab.mirrorMid_checkBox, "mirrorMid"))

        self.settingsTab.extraTweak_checkBox.stateChanged.connect(
            partial(self.updateCheck,
                    self.settingsTab.extraTweak_checkBox, "extraTweak"))

        self.settingsTab.mirrorIK_checkBox.stateChanged.connect(
            partial(self.updateCheck,
                    self.settingsTab.mirrorIK_checkBox,
                    "mirrorIK"))

        self.settingsTab.ikRefArrayAdd_pushButton.clicked.connect(
            partial(self.addItem2listWidget,
                    self.settingsTab.ikRefArray_listWidget,
                    "ikrefarray"))

        self.settingsTab.ikRefArrayRemove_pushButton.clicked.connect(
            partial(self.removeSelectedFromListWidget,
                    self.settingsTab.ikRefArray_listWidget,
                    "ikrefarray"))

        self.settingsTab.ikRefArray_copyRef_pushButton.clicked.connect(
            partial(self.copyFromListWidget,
                    self.settingsTab.upvRefArray_listWidget,
                    self.settingsTab.ikRefArray_listWidget,
                    "ikrefarray"))

        self.settingsTab.ikRefArray_listWidget.installEventFilter(self)

        self.settingsTab.upvRefArrayAdd_pushButton.clicked.connect(
            partial(self.addItem2listWidget,
                    self.settingsTab.upvRefArray_listWidget,
                    "upvrefarray"))

        self.settingsTab.upvRefArrayRemove_pushButton.clicked.connect(
            partial(self.removeSelectedFromListWidget,
                    self.settingsTab.upvRefArray_listWidget,
                    "upvrefarray"))

        self.settingsTab.upvRefArray_copyRef_pushButton.clicked.connect(
            partial(self.copyFromListWidget,
                    self.settingsTab.ikRefArray_listWidget,
                    self.settingsTab.upvRefArray_listWidget,
                    "upvrefarray"))

        self.settingsTab.upvRefArray_listWidget.installEventFilter(self)

        self.settingsTab.pinRefArrayAdd_pushButton.clicked.connect(
            partial(self.addItem2listWidget,
                    self.settingsTab.pinRefArray_listWidget,
                    "pinrefarray"))

        self.settingsTab.pinRefArrayRemove_pushButton.clicked.connect(
            partial(self.removeSelectedFromListWidget,
                    self.settingsTab.pinRefArray_listWidget,
                    "pinrefarray"))

        self.settingsTab.pinRefArray_copyRef_pushButton.clicked.connect(
            partial(self.copyFromListWidget,
                    self.settingsTab.ikRefArray_listWidget,
                    self.settingsTab.pinRefArray_listWidget,
                    "pinrefarray"))

        self.settingsTab.pinRefArray_listWidget.installEventFilter(self)

        self.mainSettingsTab.connector_comboBox.currentIndexChanged.connect(
            partial(self.updateConnector,
                    self.mainSettingsTab.connector_comboBox,
                    self.connector_items))

    def eventFilter(self, sender, event):
        if event.type() == QtCore.QEvent.ChildRemoved:
            if sender == self.settingsTab.ikRefArray_listWidget:
                self.updateListAttr(sender, "ikrefarray")
            elif sender == self.settingsTab.upvRefArray_listWidget:
                self.updateListAttr(sender, "upvrefarray")
            elif sender == self.settingsTab.pinRefArray_listWidget:
                self.updateListAttr(sender, "pinrefarray")
            return True
        else:
            return QtWidgets.QDialog.eventFilter(self, sender, event)

    def dockCloseEventTriggered(self):
        pyqt.deleteInstances(self, MayaQDockWidget)
