# -*- coding:utf-8 -*-

#
from collections import OrderedDict
from functools import partial

# maya
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.app.general.mayaMixin import MayaQDockWidget

# mbox
from mbox.core.attribute import add_attribute
from mbox.lego.blueprint import get_block_index
from mbox.core import icon
from mbox.lego.box import element

# mgear
from mgear.core import pyqt
from mgear.vendor.Qt import QtWidgets, QtCore


class Block(element.Blocks):
    AUTHOR = "cho wooseoung"
    URL = None
    EMAIL = "chowooseoung@gmail.com"
    VERSION = [0, 0, 1]
    TYPE = "control_0"
    NAME = "control"
    DESCRIPTION = ""

    def __init__(self):
        super(Block, self).__init__()
        self.component = self.TYPE
        self.version = "{}. {}. {}".format(*self.VERSION)
        self.name = self.NAME
        self.transforms = [pm.datatypes.Matrix().tolist()]

        # component data
        self.asWorld = False
        self.mirrorBehaviour = False
        self.worldOrientAxis = True
        self.keyAbleAttrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]

    def print(self):
        common_msg = super(Block, self).print()
        msg = (f"       asWorld : {self.asWorld}\n"
               f"       mirrorBehaviour : {self.mirrorBehaviour}\n"
               f"       worldOrientAxis : {self.worldOrientAxis}\n"
               f"       keyAbleAttrs : {self.keyAbleAttrs}\n")
        return common_msg + msg

    def guide(self, parent):
        # name
        root_name = f"{self.name}_{self.direction}{self.index}_root"

        # create
        root = icon.guide_root_icon(parent, root_name, m=pm.datatypes.Matrix(self.transforms[0]))

        network = pm.createNode("network")
        add_attribute(network, "guide", "message")
        add_attribute(network, "rig", "message")
        add_attribute(network, "component", "string", self.component)
        add_attribute(network, "version", "string", self.version)
        add_attribute(network, "name", "string", self.name)
        add_attribute(network, "direction", self.direction, ["center", "right", "left"], keyable=False)
        add_attribute(network, "index", "string", self.index)
        add_attribute(network, "joint", "bool", self.joint, keyable=False)
        add_attribute(network, "primaryAxis", "string", self.jointAxis[0])
        add_attribute(network, "secondaryAxis", "string", self.jointAxis[1])
        add_attribute(network, "transforms", "matrix", multi=True)
        add_attribute(network, "asWorld", "bool", self.asWorld, keyable=False)
        add_attribute(network, "mirrorBehaviour", "bool", self.mirrorBehaviour, keyable=False)
        add_attribute(network, "worldOrientAxis", "bool", self.worldOrientAxis, keyable=False)
        for attr in ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "ro"]:
            add_attribute(network, attr, "bool", True if attr in self.keyAbleAttrs else False, keyable=False)
        add_attribute(network, "parent", "string")
        add_attribute(network, "priority", "long", self.priority, keyable=False, minValue=0)

        # attribute
        parent.getParent(generations=-1).message.outputs(type="network")[0].affects[0] >> network.affectsBy[0]
        root.message >> network.guide
        root.worldMatrix >> network.transforms[0]


class componentSettings(MayaQWidgetDockableMixin, guide.componentMainSettings):
    """from mgear.shifter_classic_components.control_01.guide.componentSettings"""

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
