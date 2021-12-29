# -*- coding: utf-8 -*-

# maya
import pymel.core as pm
from maya.app.general.mayaMixin import MayaQDockWidget
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

# Built-in
from functools import partial
import os
import sys
import json
import shutil
import subprocess

# mbox
from . import naming_rules_ui as name_ui
from . import custom_step_ui as custom_step_ui
from . import root_settings_ui as root_ui
from . import block_settings_ui as block_ui
from . import joint_names_ui as joint_name_ui
from mbox.lego import naming, lib

# mgear
from mgear.core import pyqt, string
from mgear.vendor.Qt import QtCore, QtWidgets, QtGui
from mgear.anim_picker.gui import MAYA_OVERRIDE_COLOR

ROOT_TYPE = "mbox_guide_root"
BLOCK_TYPE = "mbox_guide_block"


class RootMainTabUI(QtWidgets.QDialog, root_ui.Ui_Form):

    def __init__(self, parent=None):
        super(RootMainTabUI, self).__init__(parent)
        self.setupUi(self)


class RootCustomStepTabUI(QtWidgets.QDialog, custom_step_ui.Ui_Form):

    def __init__(self, parent=None):
        super(RootCustomStepTabUI, self).__init__(parent)
        self.setupUi(self)


class RootNameTabUI(QtWidgets.QDialog, name_ui.Ui_Form):

    def __init__(self, parent=None):
        super(RootNameTabUI, self).__init__(parent)
        self.setupUi(self)


class HelperSlots:

    def __init__(self):
        self._network = None # 

    def update_host_ui(self, l_edit, target_attr):
        guide = lib.get_component_guide(pm.selected(type="transform")[0])
        if guide:
            network = guide[0].message.outputs(type="network")[0]
            l_edit.setText(guide[0].name())
            self._network.attr(target_attr).set("{},{}".format(guide[0].name(), network.attr("oid").get()))
        else:
            if l_edit.text():
                l_edit.clear()
                self._network.attr(target_attr).set("")
                pm.displayWarning("")

    def update_line_edit(self, l_edit, target_attr):
        name = string.removeInvalidCharacter(l_edit.text())
        l_edit.setText(name)
        self._network.attr(target_attr).set(name)

    def update_line_edit2(self, l_edit, target_attr):
        # nomralize the text to be Maya naming compatible
        # replace invalid characters with "_"
        name = string.normalize2(l_edit.text())
        l_edit.setText(name)
        self._network.attr(target_attr).set(name)

    def update_text_edit(self, l_edit, target_attr):
        self._network.attr(target_attr).set(l_edit.toPlainText())

    def update_line_edit_path(self, l_edit, target_attr):
        self._network.attr(target_attr).set(l_edit.text())

    def update_name_rule_line_edit(self, l_edit, target_attr):
        # nomralize the text to be Maya naming compatible
        # replace invalid characters with "_"
        name = naming.normalize_name_rule(l_edit.text())
        l_edit.setText(name)
        self._network.attr(target_attr).set(name)
        self.naming_rule_validator(l_edit)

    def naming_rule_validator(self, l_edit, log=True):
        Palette = QtGui.QPalette()
        if not naming.name_rule_validator(l_edit.text(),
                                          naming.NAMING_RULE_TOKENS,
                                          log=log):

            Palette.setBrush(QtGui.QPalette.Text, self.red_brush)
        else:
            Palette.setBrush(QtGui.QPalette.Text, self.white_down_brush)
        l_edit.setPalette(Palette)

    def add_item_to_list_widget(self, list_widget, target_attr=None):

        items = pm.selected()
        items_list = [i.text() for i in list_widget.findItems(
            "", QtCore.Qt.MatchContains)]
        # Quick clean the first empty item
        if items_list and not items_list[0]:
            list_widget.takeItem(0)

        for item in items:
            if len(item.name().split("|")) != 1:
                pm.displayWarning("Not valid obj: %s, name is not unique." %
                                  item.name())
                continue

            if item.name() not in items_list:
                if item.hasAttr("is_guide_component") or item.hasAttr("is_guide_root"):
                    list_widget.addItem(item.name())

                else:
                    pm.displayWarning(
                        "The object: %s, is not a valid"
                        " reference, Please select only guide componet"
                        " roots and guide locators." % item.name())
            else:
                pm.displayWarning("The object: %s, is already in the list." %
                                  item.name())

        if target_attr:
            self.update_list_attr(list_widget, target_attr)

    def remove_selected_from_list_widget(self, list_widget, target_attr=None):
        for item in list_widget.selectedItems():
            list_widget.takeItem(list_widget.row(item))
        if target_attr:
            self.update_list_attr(list_widget, target_attr)

    def move_from_list_widget_to_list_widget(self, source_list_widget, target_list_widget,
                                             target_attr_list_widget, target_attr=None):
        # Quick clean the first empty item
        items_list = [i.text() for i in target_attr_list_widget.findItems(
            "", QtCore.Qt.MatchContains)]
        if items_list and not items_list[0]:
            target_attr_list_widget.takeItem(0)

        for item in source_list_widget.selectedItems():
            target_list_widget.addItem(item.text())
            source_list_widget.takeItem(source_list_widget.row(item))

        if target_attr:
            self.update_list_attr(target_attr_list_widget, target_attr)

    def copy_from_list_widget(self, source_list_widget, target_list_widget,
                              target_attr=None):
        target_list_widget.clear()
        items_list = [i.text() for i in source_list_widget.findItems(
            "", QtCore.Qt.MatchContains)]
        for item in items_list:
            target_list_widget.addItem(item)
        if target_attr:
            self.update_list_attr(source_list_widget, target_attr)

    def update_list_attr(self, source_list_widget, target_attr):
        """Update the string attribute with values separated by commas"""
        new_value = ",".join([i.text() for i in source_list_widget.findItems(
            "", QtCore.Qt.MatchContains)])
        self._network.attr(target_attr).set(new_value)

    def update_component_name(self):
        with pm.UndoChunk():
            side_set = ["center", "left", "right"]

            line_name = self.main_tab.name_lineEdit.text()
            new_name = string.normalize2(line_name)
            if line_name != new_name:
                self.main_tab.name_lineEdit.setText(new_name)
                return

            side_index = self.main_tab.side_comboBox.currentIndex()
            new_side = side_set[side_index]

            index = self.main_tab.componentIndex_spinBox.value()
            blueprint = lib.blueprint_from_guide(self._guide.getParent(generations=-1))
            block = blueprint.find_block_with_oid(self._network.attr("oid").get())
            new_index = blueprint.solve_index(new_name, new_side, index, block)

            rename_check = False
            if (self._network.attr("comp_name").get() != new_name) \
                    or (self._network.attr("comp_side").get(asString=True) != new_side) \
                    or (self._network.attr("comp_index").get() != new_index) \
                    or (self._network.attr("comp_index").get() == index
                        and self._network.attr("comp_name").get() == new_name
                        and self._network.attr("comp_side").get() == new_side):
                rename_check = True
            print(self._network.attr("comp_index").get() == index, self._network.attr("comp_index").get(), index)
            print(self._network.attr("comp_name").get() == self._network.attr("comp_name").get(), new_name)
            print(self._network.attr("comp_side").get() == self._network.attr("comp_side").get(), new_side)
            if rename_check:
                block["comp_name"] = new_name
                block["comp_side"] = new_side
                block["comp_index"] = new_index
                block.to_network()
                block.update_guide()

            if self._network.attr("comp_index").get() != self.main_tab.componentIndex_spinBox.value():
                self.main_tab.componentIndex_spinBox.setValue(self._network.attr("comp_index").get())

    def update_connector(self, source_widget, items_list, *args):
        self._network.attr("connector").set(items_list[source_widget.currentIndex()])

    def populate_check(self, target_widget, source_attr, *args):
        if self._network.attr(source_attr).get():
            target_widget.setCheckState(QtCore.Qt.Checked)
        else:
            target_widget.setCheckState(QtCore.Qt.Unchecked)

    def update_check(self, source_widget, target_attr, *args):
        self._network.attr(target_attr).set(source_widget.isChecked())

    def update_spin_box(self, source_widget, target_attr, *args):
        self._network.attr(target_attr).set(source_widget.value())
        return True

    def update_slider(self, source_widget, target_attr, *args):
        self._network.attr(target_attr).set(float(source_widget.value()) / 100)

    def update_combo_box(self, source_widget, target_attr, *args):
        self._network.attr(target_attr).set(source_widget.currentIndex())

    def update_control_shape(self, source_widget, ctl_list, target_attr, *args):
        current_index = source_widget.currentIndex()
        self._network.attr(target_attr).set(ctl_list[current_index])

    def update_index_color_widgets(
            self, source_widget, target_attr, color_widget, *args):
        self.update_spin_box(source_widget, target_attr)
        self.update_widget_style_sheet(
            color_widget,
            (i / 255.0 for i in MAYA_OVERRIDE_COLOR[source_widget.value()]))

    def update_rgb_color_widgets(self, button_widget, rgb, slider_widget):
        self.update_widget_style_sheet(button_widget, rgb)
        slider_widget.blockSignals(True)
        slider_widget.setValue(sorted(rgb)[2] * 255)
        slider_widget.blockSignals(False)

    def update_widget_style_sheet(self, source_widget, rgb):
        color = ', '.join(str(i * 255) for i in pm.colorManagementConvert(toDisplaySpace=rgb))
        source_widget.setStyleSheet(
            "* {background-color: rgb(" + color + ")}")

    def rgb_slider_value_changed(self, button_widget, target_attr, value):
        rgb = self._network.attr(target_attr).get()
        hsv_value = sorted(rgb)[2]
        if hsv_value:
            new_rgb = tuple(i / (hsv_value / 1.0) * (value / 255.0)
                            for i in rgb)
        else:
            new_rgb = tuple((1.0 * (value / 255.0), 1.0
                             * (value / 255.0), 1.0 * (value / 255.0)))
        self.update_widget_style_sheet(button_widget, new_rgb)
        self._network.attr(target_attr).set(new_rgb)

    def rgb_color_editor(self, source_widget, target_attr, slider_widget, *args):
        pm.colorEditor(rgb=self._network.attr(target_attr).get())
        if pm.colorEditor(query=True, result=True):
            rgb = pm.colorEditor(query=True, rgb=True)
            self._network.attr(target_attr).set(rgb)
            self.update_rgb_color_widgets(source_widget, rgb, slider_widget)

    def toggle_rgb_index_widgets(self, check_box, idx_widgets, rgb_widgets, target_attr, checked):
        show_widgets, hide_widgets = (
            rgb_widgets, idx_widgets) if checked else (
            idx_widgets, rgb_widgets)
        for widget in show_widgets:
            widget.show()
        for widget in hide_widgets:
            widget.hide()
        self.update_check(check_box, target_attr)

    def set_profile(self):
        pm.select(self._network, r=True)
        pm.runtime.GraphEditor()

    def get_cs_file_fullpath(self, cs_data):
        filepath = cs_data.split("|")[-1][1:]
        if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
            fullpath = os.path.join(
                os.environ.get(
                    "MBOX_CUSTOM_STEP_PATH", ""), filepath)
        else:
            fullpath = filepath

        return fullpath

    def edit_file(self, widgetList):
        try:
            cs_data = widgetList.selectedItems()[0].text()
            fullpath = self.get_cs_file_fullpath(cs_data)

            if fullpath:
                if sys.platform.startswith('darwin'):
                    subprocess.call(('open', fullpath))
                elif os.name == 'nt':
                    os.startfile(fullpath)
                elif os.name == 'posix':
                    subprocess.call(('xdg-open', fullpath))
            else:
                pm.displayWarning("Please select one item from the list")
        except Exception:
            pm.displayError("The step can't be find or does't exists")

    def format_info(self, data):
        data_parts = data.split("|")
        cs_name = data_parts[0]
        if cs_name.startswith("*"):
            cs_status = "Deactivated"
            cs_name = cs_name[1:]
        else:
            cs_status = "Active"

        cs_fullpath = self.get_cs_file_fullpath(data)
        if "_shared" in data:
            cs_shared_owner = self.shared_owner(cs_fullpath)
            cs_shared_status = "Shared"
        else:
            cs_shared_status = "Local"
            cs_shared_owner = "None"

        info = '<html><head/><body><p><span style=" font-weight:600;">\
        {0}</span></p><p>------------------</p><p><span style=" \
        font-weight:600;">Status</span>: {1}</p><p><span style=" \
        font-weight:600;">Shared Status:</span> {2}</p><p><span \
        style=" font-weight:600;">Shared Owner:</span> \
        {3}</p><p><span style=" font-weight:600;">Full Path</span>: \
        {4}</p></body></html>'.format(cs_name,
                                      cs_status,
                                      cs_shared_status,
                                      cs_shared_owner,
                                      cs_fullpath)
        return info

    def shared_owner(self, cs_fullpath):

        scan_dir = os.path.abspath(os.path.join(cs_fullpath, os.pardir))
        while not scan_dir.endswith("_shared"):
            scan_dir = os.path.abspath(os.path.join(scan_dir, os.pardir))
            # escape infinite loop
            if scan_dir == '/':
                break
        scan_dir = os.path.abspath(os.path.join(scan_dir, os.pardir))
        return os.path.split(scan_dir)[1]

    @classmethod
    def get_steps_dict(self, itemsList):
        stepsDict = {}
        stepsDict["itemsList"] = itemsList
        for item in itemsList:
            step = open(item, "r")
            data = step.read()
            stepsDict[item] = data
            step.close()

        return stepsDict

    @classmethod
    def runStep(self, stepPath, customStepDic):
        try:
            with pm.UndoChunk():
                pm.displayInfo(
                    "EXEC: Executing custom step: %s" % stepPath)
                # use forward slash for OS compatibility
                if sys.platform.startswith('darwin'):
                    stepPath = stepPath.replace('\\', '/')

                fileName = os.path.split(stepPath)[1].split(".")[0]

                if os.environ.get(MGEAR_SHIFTER_CUSTOMSTEP_KEY, ""):
                    runPath = os.path.join(
                        os.environ.get(
                            MGEAR_SHIFTER_CUSTOMSTEP_KEY, ""), stepPath)
                else:
                    runPath = stepPath

                customStep = imp.load_source(fileName, runPath)
                if hasattr(customStep, "CustomShifterStep"):
                    argspec = inspect.getargspec(
                        customStep.CustomShifterStep.__init__)
                    if "stored_dict" in argspec.args:
                        cs = customStep.CustomShifterStep(customStepDic)
                        cs.setup()
                        cs.run()
                    else:
                        cs = customStep.CustomShifterStep()
                        cs.run(customStepDic)
                    customStepDic[cs.name] = cs
                    pm.displayInfo(
                        "SUCCEED: Custom Shifter Step Class: %s. "
                        "Succeed!!" % stepPath)
                else:
                    pm.displayInfo(
                        "SUCCEED: Custom Step simple script: %s. "
                        "Succeed!!" % stepPath)

        except Exception as ex:
            template = "An exception of type {0} occurred. "
            "Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            pm.displayError(message)
            pm.displayError(traceback.format_exc())
            cont = pm.confirmBox(
                "FAIL: Custom Step Fail",
                "The step:%s has failed. Continue with next step?"
                % stepPath
                + "\n\n"
                + message
                + "\n\n"
                + traceback.format_exc(),
                "Continue", "Stop Build", "Try Again!")
            if cont == "Stop Build":
                # stop Build
                return True
            elif cont == "Try Again!":
                try:  # just in case there is nothing to undo
                    pm.undo()
                except Exception:
                    pass
                pm.displayInfo("Trying again! : {}".format(stepPath))
                inception = self.runStep(stepPath, customStepDic)
                if inception:  # stops build from the recursion loop.
                    return True
            else:
                return False

    def run_manual_step(self, widgetList):
        selItems = widgetList.selectedItems()
        for item in selItems:
            self.runStep(item.text().split("|")[-1][1:], customStepDic={})

    def close_settings(self):
        self.close()
        pyqt.deleteInstances(self, MayaQDockWidget)


class RootSettings(MayaQWidgetDockableMixin, QtWidgets.QDialog, HelperSlots):
    green_brush = QtGui.QColor(0, 160, 0)
    red_brush = QtGui.QColor(180, 0, 0)
    white_brush = QtGui.QColor(255, 255, 255)
    white_down_brush = QtGui.QColor(160, 160, 160)
    orange_brush = QtGui.QColor(240, 160, 0)

    def __init__(self):
        self.toolName = ROOT_TYPE
        # Delete old instances of the componet settings window.
        pyqt.deleteInstances(self, MayaQDockWidget)
        # super(self.__class__, self).__init__(parent=parent)
        super(RootSettings, self).__init__()
        # the inspectSettings function set the current selection to the
        # component root before open the settings dialog
        self._network = pm.selected(type="transform")[0].message.outputs(type="network")[0]

        self.main_tab = RootMainTabUI()
        self.custom_step_tab = RootCustomStepTabUI()
        self.naming_rule_tab = RootNameTabUI()

        self.mayaMainWindow = pyqt.maya_main_window()

        self.setObjectName(self.toolName)
        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle(ROOT_TYPE)
        self.resize(500, 615)

        self.create_controls()
        self.populate_controls()
        self.create_layout()
        self.create_connections()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        # hover info
        self.pre_cs = self.custom_step_tab.preCustomStep_listWidget
        self.pre_cs.setMouseTracking(True)
        self.pre_cs.entered.connect(self.pre_info)

        self.post_cs = self.custom_step_tab.postCustomStep_listWidget
        self.post_cs.setMouseTracking(True)
        self.post_cs.entered.connect(self.post_info)

    def pre_info(self, index):
        self.hover_info_item_entered(self.pre_cs, index)

    def post_info(self, index):
        self.hover_info_item_entered(self.post_cs, index)

    def hover_info_item_entered(self, view, index):
        if index.isValid():
            info_data = self.format_info(index.data())
            QtWidgets.QToolTip.showText(
                QtGui.QCursor.pos(),
                info_data,
                view.viewport(),
                view.visualRect(index))

    def create_controls(self):
        """Create the controls for the component base"""
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setObjectName("settings_tab")

        # Close Button
        self.close_button = QtWidgets.QPushButton("Close")

    def populate_controls(self):
        """Populate the controls values
            from the custom attributes of the component.

        """
        # populate tab
        self.tabs.insertTab(0, self.main_tab, "Guide Settings")
        self.tabs.insertTab(1, self.custom_step_tab, "Custom Steps")
        self.tabs.insertTab(2, self.naming_rule_tab, "Naming Rules")

        # populate main settings
        self.main_tab.rigName_lineEdit.setText(
            self._network.attr("name").get())
        self.main_tab.mode_comboBox.setCurrentIndex(
            self._network.attr("process").get())
        self.main_tab.step_comboBox.setCurrentIndex(
            self._network.attr("step").get())
        # self.populateCheck(
        #     self.main_tab.proxyChannels_checkBox, "proxyChannels")

        self.populate_check(self.main_tab.worldCtl_checkBox, "world_ctl")
        self.main_tab.worldCtl_lineEdit.setText(
            self._network.attr("world_ctl_name").get())

        # self.populateCheck(
        #     self.main_tab.classicChannelNames_checkBox,
        #     "classicChannelNames")
        # self.populateCheck(
        #     self.main_tab.attrPrefix_checkBox,
        #     "attrPrefixName")
        # self.populateCheck(
        #     self.main_tab.importSkin_checkBox, "importSkin")
        # self.main_tab.skin_lineEdit.setText(
        #     self._network.attr("skin").get())
        # self.populateCheck(
        #     self.main_tab.dataCollector_checkBox, "data_collector")
        # self.main_tab.dataCollectorPath_lineEdit.setText(
        #     self._network.attr("data_collector_path").get())
        self.populate_check(
            self.main_tab.jointRig_checkBox, "joint_rig")
        self.populate_check(
            self.main_tab.force_uniScale_checkBox, "force_uni_scale")
        self.populate_check(
            self.main_tab.connect_joints_checkBox, "connect_joints")
        # self.populateAvailableSynopticTabs()

        # for item in self._network.attr("synoptic").get().split(","):
        #     self.main_tab.rigTabs_listWidget.addItem(item)

        tap = self.main_tab

        index_widgets = ((tap.L_color_fk_spinBox,
                          tap.L_color_fk_label,
                          "l_color_fk"),
                         (tap.L_color_ik_spinBox,
                          tap.L_color_ik_label,
                          "l_color_ik"),
                         (tap.C_color_fk_spinBox,
                          tap.C_color_fk_label,
                          "c_color_fk"),
                         (tap.C_color_ik_spinBox,
                          tap.C_color_ik_label,
                          "c_color_ik"),
                         (tap.R_color_fk_spinBox,
                          tap.R_color_fk_label,
                          "r_color_fk"),
                         (tap.R_color_ik_spinBox,
                          tap.R_color_ik_label,
                          "r_color_ik"))

        rgb_widgets = ((tap.L_RGB_fk_pushButton,
                        tap.L_RGB_fk_slider,
                        "l_RGB_fk"),
                       (tap.L_RGB_ik_pushButton,
                        tap.L_RGB_ik_slider,
                        "l_RGB_ik"),
                       (tap.C_RGB_fk_pushButton,
                        tap.C_RGB_fk_slider,
                        "c_RGB_fk"),
                       (tap.C_RGB_ik_pushButton,
                        tap.C_RGB_ik_slider,
                        "c_RGB_ik"),
                       (tap.R_RGB_fk_pushButton,
                        tap.R_RGB_fk_slider,
                        "r_RGB_fk"),
                       (tap.R_RGB_ik_pushButton,
                        tap.R_RGB_ik_slider,
                        "r_RGB_ik"))

        for spinBox, label, source_attr in index_widgets:
            color_index = self._network.attr(source_attr).get()
            spinBox.setValue(color_index)
            self.update_widget_style_sheet(
                label, [i / 255.0 for i in MAYA_OVERRIDE_COLOR[color_index]])

        for button, slider, source_attr in rgb_widgets:
            self.update_rgb_color_widgets(
                button, self._network.attr(source_attr).get(), slider)

        # forceing the size of the color buttons/label to keep ui clean
        for widget in tuple(i[0] for i in rgb_widgets) + tuple(
                i[1] for i in index_widgets):
            widget.setFixedSize(pyqt.dpi_scale(30), pyqt.dpi_scale(20))

        self.populate_check(tap.useRGB_checkBox, "use_RGB_color")
        self.toggle_rgb_index_widgets(tap.useRGB_checkBox,
                                      (w for i in index_widgets for w in i[:2]),
                                      (w for i in rgb_widgets for w in i[:2]),
                                      "use_RGB_color",
                                      tap.useRGB_checkBox.checkState())

        tap.notes_textEdit.setText(self._network.attr("notes").get())

        # pupulate custom steps sttings
        self.populate_check(
            self.custom_step_tab.preCustomStep_checkBox, "run_pre_custom_step")
        for item in self._network.attr("pre_custom_step").get().split(","):
            self.custom_step_tab.preCustomStep_listWidget.addItem(item)
        self.refresh_status_color(self.custom_step_tab.preCustomStep_listWidget)

        self.populate_check(
            self.custom_step_tab.postCustomStep_checkBox, "run_post_custom_step")
        for item in self._network.attr("post_custom_step").get().split(","):
            self.custom_step_tab.postCustomStep_listWidget.addItem(item)
        self.refresh_status_color(self.custom_step_tab.postCustomStep_listWidget)

        self.populate_naming_controls()

    def populate_naming_controls(self):
        # populate name settings
        self.naming_rule_tab.ctl_name_rule_lineEdit.setText(
            self._network.attr("ctl_name_rule").get())
        self.naming_rule_validator(
            self.naming_rule_tab.ctl_name_rule_lineEdit)
        self.naming_rule_tab.joint_name_rule_lineEdit.setText(
            self._network.attr("joint_name_rule").get())
        self.naming_rule_validator(
            self.naming_rule_tab.joint_name_rule_lineEdit)

        self.naming_rule_tab.side_left_name_lineEdit.setText(
            self._network.attr("ctl_left_name").get())
        self.naming_rule_tab.side_right_name_lineEdit.setText(
            self._network.attr("ctl_right_name").get())
        self.naming_rule_tab.side_center_name_lineEdit.setText(
            self._network.attr("ctl_center_name").get())

        self.naming_rule_tab.side_joint_left_name_lineEdit.setText(
            self._network.attr("joint_left_name").get())
        self.naming_rule_tab.side_joint_right_name_lineEdit.setText(
            self._network.attr("joint_right_name").get())
        self.naming_rule_tab.side_joint_center_name_lineEdit.setText(
            self._network.attr("joint_center_name").get())

        self.naming_rule_tab.ctl_name_ext_lineEdit.setText(
            self._network.attr("ctl_name_ext").get())
        self.naming_rule_tab.joint_name_ext_lineEdit.setText(
            self._network.attr("joint_name_ext").get())

        self.naming_rule_tab.ctl_des_letter_case_comboBox.setCurrentIndex(
            self._network.attr("ctl_description_letter_case").get())

        self.naming_rule_tab.joint_des_letter_case_comboBox.setCurrentIndex(
            self._network.attr("joint_description_letter_case").get())

        self.naming_rule_tab.ctl_padding_spinBox.setValue(
            self._network.attr("ctl_index_padding").get())
        self.naming_rule_tab.joint_padding_spinBox.setValue(
            self._network.attr("joint_index_padding").get())

    def create_layout(self):
        """
        Create the layout for the component base settings

        """
        self.settings_layout = QtWidgets.QVBoxLayout()
        self.settings_layout.addWidget(self.tabs)
        self.settings_layout.addWidget(self.close_button)

        self.setLayout(self.settings_layout)

    def create_connections(self):
        """Create the slots connections to the controls functions"""
        self.close_button.clicked.connect(self.close_settings)

        # Setting Tab
        tap = self.main_tab
        tap.rigName_lineEdit.editingFinished.connect(
            partial(self.update_line_edit,
                    tap.rigName_lineEdit,
                    "name"))
        tap.mode_comboBox.currentIndexChanged.connect(
            partial(self.update_combo_box,
                    tap.mode_comboBox,
                    "process"))
        tap.step_comboBox.currentIndexChanged.connect(
            partial(self.update_combo_box,
                    tap.step_comboBox,
                    "step"))
        # tap.proxyChannels_checkBox.stateChanged.connect(
        #     partial(self.update_check,
        #             tap.proxyChannels_checkBox,
        #             "proxyChannels"))
        tap.worldCtl_checkBox.stateChanged.connect(
            partial(self.update_check,
                    tap.worldCtl_checkBox,
                    "world_ctl"))
        tap.worldCtl_lineEdit.editingFinished.connect(
            partial(self.update_line_edit2,
                    tap.worldCtl_lineEdit,
                    "world_ctl_name"))
        # tap.classicChannelNames_checkBox.stateChanged.connect(
        #     partial(self.updateCheck,
        #             tap.classicChannelNames_checkBox,
        #             "classicChannelNames"))
        # tap.attrPrefix_checkBox.stateChanged.connect(
        #     partial(self.updateCheck,
        #             tap.attrPrefix_checkBox,
        #             "attrPrefixName"))
        # tap.dataCollector_checkBox.stateChanged.connect(
        #     partial(self.updateCheck,
        #             tap.dataCollector_checkBox,
        #             "data_collector"))
        # tap.dataCollectorPath_lineEdit.editingFinished.connect(
        #     partial(self.updateLineEditPath,
        #             tap.dataCollectorPath_lineEdit,
        #             "data_collector_path"))
        tap.jointRig_checkBox.stateChanged.connect(
            partial(self.update_check,
                    tap.jointRig_checkBox,
                    "joint_rig"))
        tap.force_uniScale_checkBox.stateChanged.connect(
            partial(self.update_check,
                    tap.force_uniScale_checkBox,
                    "force_uni_scale"))
        tap.connect_joints_checkBox.stateChanged.connect(
            partial(self.update_check,
                    tap.connect_joints_checkBox,
                    "connect_joints"))
        # tap.addTab_pushButton.clicked.connect(
        #     partial(self.moveFromListWidget2ListWidget,
        #             tap.available_listWidget,
        #             tap.rigTabs_listWidget,
        #             tap.rigTabs_listWidget,
        #             "synoptic"))
        # tap.removeTab_pushButton.clicked.connect(
        #     partial(self.moveFromListWidget2ListWidget,
        #             tap.rigTabs_listWidget,
        #             tap.available_listWidget,
        #             tap.rigTabs_listWidget,
        #             "synoptic"))
        # tap.loadSkinPath_pushButton.clicked.connect(
        #     self.skinLoad)
        # tap.dataCollectorPath_pushButton.clicked.connect(
        #     self.data_collector_path)
        # tap.rigTabs_listWidget.installEventFilter(self)

        # colors connections
        index_widgets = ((tap.L_color_fk_spinBox,
                          tap.L_color_fk_label, "l_color_fk"),
                         (tap.L_color_ik_spinBox,
                          tap.L_color_ik_label, "l_color_ik"),
                         (tap.C_color_fk_spinBox,
                          tap.C_color_fk_label, "c_color_fk"),
                         (tap.C_color_ik_spinBox,
                          tap.C_color_ik_label, "c_color_ik"),
                         (tap.R_color_fk_spinBox,
                          tap.R_color_fk_label, "r_color_fk"),
                         (tap.R_color_ik_spinBox,
                          tap.R_color_ik_label, "r_color_ik"))

        rgb_widgets = ((tap.L_RGB_fk_pushButton,
                        tap.L_RGB_fk_slider, "l_RGB_fk"),
                       (tap.L_RGB_ik_pushButton,
                        tap.L_RGB_ik_slider, "l_RGB_ik"),
                       (tap.C_RGB_fk_pushButton,
                        tap.C_RGB_fk_slider, "c_RGB_fk"),
                       (tap.C_RGB_ik_pushButton,
                        tap.C_RGB_ik_slider, "c_RGB_ik"),
                       (tap.R_RGB_fk_pushButton,
                        tap.R_RGB_fk_slider, "r_RGB_fk"),
                       (tap.R_RGB_ik_pushButton,
                        tap.R_RGB_ik_slider, "r_RGB_ik"))

        for spinBox, label, source_attr in index_widgets:
            spinBox.valueChanged.connect(
                partial(self.update_index_color_widgets,
                        spinBox,
                        source_attr,
                        label))

        for button, slider, source_attr in rgb_widgets:
            button.clicked.connect(
                partial(self.rgb_color_editor, button, source_attr, slider))
            slider.valueChanged.connect(
                partial(self.rgb_slider_value_changed, button, source_attr))

        tap.useRGB_checkBox.stateChanged.connect(
            partial(self.toggle_rgb_index_widgets,
                    tap.useRGB_checkBox,
                    tuple(w for i in index_widgets for w in i[:2]),
                    tuple(w for i in rgb_widgets for w in i[:2]),
                    "use_RGB_color"))

        tap.notes_textEdit.textChanged.connect(
            partial(self.update_text_edit,
                    tap.notes_textEdit,
                    "notes"))

        # custom Step Tab
        csTap = self.custom_step_tab
        csTap.preCustomStep_checkBox.stateChanged.connect(
            partial(self.update_check,
                    csTap.preCustomStep_checkBox,
                    "run_pre_custom_step"))
        csTap.preCustomStepAdd_pushButton.clicked.connect(
            self.add_custom_step)
        csTap.preCustomStepNew_pushButton.clicked.connect(
            self.new_custom_step)
        csTap.preCustomStepDuplicate_pushButton.clicked.connect(
            self.duplicate_custom_step)
        csTap.preCustomStepExport_pushButton.clicked.connect(
            self.export_custom_step)
        csTap.preCustomStepImport_pushButton.clicked.connect(
            self.import_custom_step)
        csTap.preCustomStepRemove_pushButton.clicked.connect(
            partial(self.remove_selected_from_list_widget,
                    csTap.preCustomStep_listWidget,
                    "pre_custom_step"))
        csTap.preCustomStep_listWidget.installEventFilter(self)
        csTap.preCustomStepRun_pushButton.clicked.connect(
            partial(self.run_manual_step,
                    csTap.preCustomStep_listWidget))
        csTap.preCustomStepEdit_pushButton.clicked.connect(
            partial(self.edit_file,
                    csTap.preCustomStep_listWidget))

        csTap.postCustomStep_checkBox.stateChanged.connect(
            partial(self.update_check,
                    csTap.postCustomStep_checkBox,
                    "run_post_custom_step"))
        csTap.postCustomStepAdd_pushButton.clicked.connect(
            partial(self.add_custom_step, False))
        csTap.postCustomStepNew_pushButton.clicked.connect(
            partial(self.new_custom_step, False))
        csTap.postCustomStepDuplicate_pushButton.clicked.connect(
            partial(self.duplicate_custom_step, False))
        csTap.postCustomStepExport_pushButton.clicked.connect(
            partial(self.export_custom_step, False))
        csTap.postCustomStepImport_pushButton.clicked.connect(
            partial(self.import_custom_step, False))
        csTap.postCustomStepRemove_pushButton.clicked.connect(
            partial(self.remove_selected_from_list_widget,
                    csTap.postCustomStep_listWidget,
                    "post_custom_step"))
        csTap.postCustomStep_listWidget.installEventFilter(self)
        csTap.postCustomStepRun_pushButton.clicked.connect(
            partial(self.run_manual_step,
                    csTap.postCustomStep_listWidget))
        csTap.postCustomStepEdit_pushButton.clicked.connect(
            partial(self.edit_file,
                    csTap.postCustomStep_listWidget))

        # right click menus
        csTap.preCustomStep_listWidget.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        csTap.preCustomStep_listWidget.customContextMenuRequested.connect(
            self.pre_custom_step_menu)
        csTap.postCustomStep_listWidget.setContextMenuPolicy(
            QtCore.Qt.CustomContextMenu)
        csTap.postCustomStep_listWidget.customContextMenuRequested.connect(
            self.post_custom_step_menu)

        # search hightlight
        csTap.preSearch_lineEdit.textChanged.connect(
            self.pre_highlight_search)
        csTap.postSearch_lineEdit.textChanged.connect(
            self.post_highlight_search)

        # Naming Tab
        tap = self.naming_rule_tab

        # names rules
        tap.ctl_name_rule_lineEdit.editingFinished.connect(
            partial(self.update_name_rule_line_edit,
                    tap.ctl_name_rule_lineEdit,
                    "ctl_name_rule"))
        tap.joint_name_rule_lineEdit.editingFinished.connect(
            partial(self.update_name_rule_line_edit,
                    tap.joint_name_rule_lineEdit,
                    "joint_name_rule"))

        # sides names
        tap.side_left_name_lineEdit.editingFinished.connect(
            partial(self.update_line_edit2,
                    tap.side_left_name_lineEdit,
                    "ctl_left_name"))
        tap.side_right_name_lineEdit.editingFinished.connect(
            partial(self.update_line_edit2,
                    tap.side_right_name_lineEdit,
                    "ctl_right_name"))
        tap.side_center_name_lineEdit.editingFinished.connect(
            partial(self.update_line_edit2,
                    tap.side_center_name_lineEdit,
                    "ctl_center_name"))

        tap.side_joint_left_name_lineEdit.editingFinished.connect(
            partial(self.update_line_edit2,
                    tap.side_joint_left_name_lineEdit,
                    "joint_left_name"))
        tap.side_joint_right_name_lineEdit.editingFinished.connect(
            partial(self.update_line_edit2,
                    tap.side_joint_right_name_lineEdit,
                    "joint_right_name"))
        tap.side_joint_center_name_lineEdit.editingFinished.connect(
            partial(self.update_line_edit2,
                    tap.side_joint_center_name_lineEdit,
                    "joint_center_name"))

        # names extensions
        tap.ctl_name_ext_lineEdit.editingFinished.connect(
            partial(self.update_line_edit2,
                    tap.ctl_name_ext_lineEdit,
                    "ctl_name_ext"))
        tap.joint_name_ext_lineEdit.editingFinished.connect(
            partial(self.update_line_edit2,
                    tap.joint_name_ext_lineEdit,
                    "joint_name_ext"))

        # description letter case
        tap.ctl_des_letter_case_comboBox.currentIndexChanged.connect(
            partial(self.update_combo_box,
                    tap.ctl_des_letter_case_comboBox,
                    "ctl_description_letter_case"))
        tap.joint_des_letter_case_comboBox.currentIndexChanged.connect(
            partial(self.update_combo_box,
                    tap.joint_des_letter_case_comboBox,
                    "joint_description_letter_case"))

        # reset naming rules
        tap.reset_ctl_name_rule_pushButton.clicked.connect(
            partial(self.reset_naming_rule,
                    tap.ctl_name_rule_lineEdit,
                    "ctl_name_rule"))
        tap.reset_joint_name_rule_pushButton.clicked.connect(
            partial(self.reset_naming_rule,
                    tap.joint_name_rule_lineEdit,
                    "joint_name_rule"))

        # reset naming sides
        tap.reset_side_name_pushButton.clicked.connect(
            self.reset_naming_sides)

        tap.reset_joint_side_name_pushButton.clicked.connect(
            self.reset_joint_naming_sides)

        # reset naming extension
        tap.reset_name_ext_pushButton.clicked.connect(
            self.reset_naming_extension)

        # index padding
        tap.ctl_padding_spinBox.valueChanged.connect(
            partial(self.update_spin_box,
                    tap.ctl_padding_spinBox,
                    "ctl_index_padding"))
        tap.joint_padding_spinBox.valueChanged.connect(
            partial(self.update_spin_box,
                    tap.joint_padding_spinBox,
                    "joint_index_padding"))

        # import name configuration
        tap.load_naming_configuration_pushButton.clicked.connect(
            self.import_name_config)

        # export name configuration
        tap.save_naming_configuration_pushButton.clicked.connect(
            self.export_name_config)

    def eventFilter(self, sender, event):
        if event.type() == QtCore.QEvent.ChildRemoved:
            # if sender == self.main_tab.rigTabs_listWidget:
            #     self.updateListAttr(sender, "synoptic")
            if sender == self.custom_step_tab.preCustomStep_listWidget:
                self.update_list_attr(sender, "pre_custom_step")
            elif sender == self.custom_step_tab.postCustomStep_listWidget:
                self.update_list_attr(sender, "post_custom_step")
            return True
        else:
            return QtWidgets.QDialog.eventFilter(self, sender, event)

        # Slots ########################################################

    def export_name_config(self, file_path=None):
        # set focus to the save button to ensure all values are updated
        # if the cursor stay in other lineEdit since the edition is not
        # finished will not take the last edition

        self.naming_rule_tab.save_naming_configuration_pushButton.setFocus(
            QtCore.Qt.MouseFocusReason)

        config = dict()
        config["ctl_name_rule"] = self._network.attr(
            "ctl_name_rule").get()
        config["joint_name_rule"] = self._network.attr(
            "joint_name_rule").get()
        config["ctl_left_name"] = self._network.attr(
            "ctl_left_name").get()
        config["ctl_right_name"] = self._network.attr(
            "ctl_right_name").get()
        config["ctl_center_name"] = self._network.attr(
            "ctl_center_name").get()
        config["joint_left_name"] = self._network.attr(
            "joint_left_name").get()
        config["joint_right_name"] = self._network.attr(
            "joint_right_name").get()
        config["joint_center_name"] = self._network.attr(
            "joint_center_name").get()
        config["ctl_name_ext"] = self._network.attr(
            "ctl_name_ext").get()
        config["joint_name_ext"] = self._network.attr(
            "joint_name_ext").get()
        config["ctl_description_letter_case"] = self._network.attr(
            "ctl_description_letter_case").get()
        config["joint_description_letter_case"] = self._network.attr(
            "joint_description_letter_case").get()
        config["ctl_index_padding"] = self._network.attr(
            "ctl_index_padding").get()
        config["joint_index_padding"] = self._network.attr(
            "joint_index_padding").get()

        if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
            startDir = os.environ.get("MBOX_CUSTOM_STEP_PATH", "")
        else:
            startDir = pm.workspace(q=True, rootDirectory=True)
        data_string = json.dumps(config, indent=4, sort_keys=True)
        if not file_path:
            file_path = pm.fileDialog2(
                fileMode=0,
                startingDirectory=startDir,
                fileFilter='Naming Configuration .naming (*%s)' % ".naming")
        if not file_path:
            return
        if not isinstance(file_path, str):
            file_path = file_path[0]
        f = open(file_path, 'w')
        f.write(data_string)
        f.close()

    def import_name_config(self, file_path=None):
        if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
            startDir = os.environ.get("MBOX_CUSTOM_STEP_PATH", "")
        else:
            startDir = pm.workspace(q=True, rootDirectory=True)
        if not file_path:
            file_path = pm.fileDialog2(
                fileMode=1,
                startingDirectory=startDir,
                fileFilter='Naming Configuration .naming (*%s)' % ".naming")
        if not file_path:
            return
        if not isinstance(file_path, str):
            file_path = file_path[0]
        config = json.load(open(file_path))
        for key in config.keys():
            self._network.attr(key).set(config[key])
        self.populate_naming_controls()

    def reset_naming_rule(self, rule_lineEdit, target_attr):
        rule_lineEdit.setText(naming.DEFAULT_NAMING_RULE)
        self.update_name_rule_line_edit(rule_lineEdit, target_attr)

    def reset_naming_sides(self):
        self.naming_rule_tab.side_left_name_lineEdit.setText(
            naming.DEFAULT_SIDE_L_NAME)
        self.naming_rule_tab.side_right_name_lineEdit.setText(
            naming.DEFAULT_SIDE_R_NAME)
        self.naming_rule_tab.side_center_name_lineEdit.setText(
            naming.DEFAULT_SIDE_C_NAME)
        self._network.attr("ctl_left_name").set(naming.DEFAULT_SIDE_L_NAME)
        self._network.attr("ctl_right_name").set(naming.DEFAULT_SIDE_R_NAME)
        self._network.attr("ctl_center_name").set(naming.DEFAULT_SIDE_C_NAME)

    def reset_joint_naming_sides(self):
        self.naming_rule_tab.side_joint_left_name_lineEdit.setText(
            naming.DEFAULT_JOINT_SIDE_L_NAME)
        self.naming_rule_tab.side_joint_right_name_lineEdit.setText(
            naming.DEFAULT_JOINT_SIDE_R_NAME)
        self.naming_rule_tab.side_joint_center_name_lineEdit.setText(
            naming.DEFAULT_JOINT_SIDE_C_NAME)
        self._network.attr("joint_left_name").set(
            naming.DEFAULT_JOINT_SIDE_L_NAME)
        self._network.attr("joint_right_name").set(
            naming.DEFAULT_JOINT_SIDE_R_NAME)
        self._network.attr("joint_center_name").set(
            naming.DEFAULT_JOINT_SIDE_C_NAME)

    def reset_naming_extension(self):
        self.naming_rule_tab.ctl_name_ext_lineEdit.setText(
            naming.DEFAULT_CTL_EXT_NAME)
        self.naming_rule_tab.joint_name_ext_lineEdit.setText(
            naming.DEFAULT_JOINT_EXT_NAME)
        self._network.attr("ctl_name_ext").set(naming.DEFAULT_CTL_EXT_NAME)
        self._network.attr("joint_name_ext").set(naming.DEFAULT_JOINT_EXT_NAME)

    # def populateAvailableSynopticTabs(self):
    #
    #     import mgear.shifter as shifter
    #     defPath = os.environ.get("MGEAR_SYNOPTIC_PATH", None)
    #     if not defPath or not os.path.isdir(defPath):
    #         defPath = shifter.SYNOPTIC_PATH
    #
    #     # Sanity check for folder existence.
    #     if not os.path.isdir(defPath):
    #         return
    #
    #     tabsDirectories = [name for name in os.listdir(defPath) if
    #                        os.path.isdir(os.path.join(defPath, name))]
    #     # Quick clean the first empty item
    #     if tabsDirectories and not tabsDirectories[0]:
    #         self.main_tab.available_listWidget.takeItem(0)
    #
    #     itemsList = self._network.attr("synoptic").get().split(",")
    #     for tab in sorted(tabsDirectories):
    #         if tab not in itemsList:
    #             self.main_tab.available_listWidget.addItem(tab)
    #
    # def skinLoad(self, *args):
    #     startDir = self._network.attr("skin").get()
    #     filePath = pm.fileDialog2(
    #         fileMode=1,
    #         startingDirectory=startDir,
    #         okc="Apply",
    #         fileFilter='mGear skin (*%s)' % skin.FILE_EXT)
    #     if not filePath:
    #         return
    #     if not isinstance(filePath, str):
    #         filePath = filePath[0]
    #
    #     self._network.attr("skin").set(filePath)
    #     self.main_tab.skin_lineEdit.setText(filePath)
    #
    # def _data_collector_path(self, *args):
    #     ext_filter = 'Shifter Collected data (*{})'.format(DATA_COLLECTOR_EXT)
    #     filePath = pm.fileDialog2(
    #         fileMode=0,
    #         fileFilter=ext_filter)
    #     if not filePath:
    #         return
    #     if not isinstance(filePath, str):
    #         filePath = filePath[0]
    #
    #     return filePath
    #
    # def data_collector_path(self, *args):
    #     filePath = self._data_collector_path()
    #
    #     if filePath:
    #         self._network.attr("data_collector_path").set(filePath)
    #         self.main_tab.dataCollectorPath_lineEdit.setText(filePath)

    def add_custom_step(self, pre=True, *args):
        """Add a new custom step

        Arguments:
            pre (bool, optional): If true adds the steps to the pre step list
            *args: Maya's Dummy

        Returns:
            None: None
        """

        if pre:
            stepAttr = "pre_custom_step"
            stepWidget = self.custom_step_tab.preCustomStep_listWidget
        else:
            stepAttr = "post_custom_step"
            stepWidget = self.custom_step_tab.postCustomStep_listWidget

        # Check if we have a custom env for the custom steps initial folder
        if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
            startDir = os.environ.get("MBOX_CUSTOM_STEP_PATH", "")
        else:
            startDir = self._network.attr(stepAttr).get()

        filePath = pm.fileDialog2(
            fileMode=1,
            startingDirectory=startDir,
            okc="Add",
            fileFilter='Custom Step .py (*.py)')
        if not filePath:
            return
        if not isinstance(filePath, str):
            filePath = filePath[0]

        # Quick clean the first empty item
        itemsList = [i.text() for i in stepWidget.findItems(
            "", QtCore.Qt.MatchContains)]
        if itemsList and not itemsList[0]:
            stepWidget.takeItem(0)

        if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
            filePath = os.path.abspath(filePath)
            baseReplace = os.path.abspath(os.environ.get(
                "MBOX_CUSTOM_STEP_PATH", ""))
            filePath = filePath.replace(baseReplace, "")[1:]

        fileName = os.path.split(filePath)[1].split(".")[0]
        stepWidget.addItem(fileName + " | " + filePath)
        self.updateListAttr(stepWidget, stepAttr)
        self.refresh_status_color(stepWidget)

    def new_custom_step(self, pre=True, *args):
        """Creates a new custom step

        Arguments:
            pre (bool, optional): If true adds the steps to the pre step list
            *args: Maya's Dummy

        Returns:
            None: None
        """

        if pre:
            stepAttr = "pre_custom_step"
            stepWidget = self.custom_step_tab.preCustomStep_listWidget
        else:
            stepAttr = "post_custom_step"
            stepWidget = self.custom_step_tab.postCustomStep_listWidget

        # Check if we have a custom env for the custom steps initial folder
        if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
            startDir = os.environ.get("MBOX_CUSTOM_STEP_PATH", "")
        else:
            startDir = self._network.attr(stepAttr).get()

        filePath = pm.fileDialog2(
            fileMode=0,
            startingDirectory=startDir,
            okc="New",
            fileFilter='Custom Step .py (*.py)')
        if not filePath:
            return
        if not isinstance(filePath, str):
            filePath = filePath[0]

        n, e = os.path.splitext(filePath)
        stepName = os.path.split(n)[-1]
        # raw custome step string
        rawString = r'''import mbox.lego.lib as lib 


class CustomStep(lib.{pre_post}):
    """Custom Step description
    """

    def process(self):
        """Run method.

        Returns:
            None: None
        """
        return'''.format(pre_post="PreScript" if pre else "PostScript")
        f = open(filePath, 'w')
        f.write(rawString + "\n")
        f.close()

        # Quick clean the first empty item
        itemsList = [i.text() for i in stepWidget.findItems(
            "", QtCore.Qt.MatchContains)]
        if itemsList and not itemsList[0]:
            stepWidget.takeItem(0)

        if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
            filePath = os.path.abspath(filePath)
            baseReplace = os.path.abspath(os.environ.get(
                "MBOX_CUSTOM_STEP_PATH", ""))
            filePath = filePath.replace(baseReplace, "")[1:]

        fileName = os.path.split(filePath)[1].split(".")[0]
        stepWidget.addItem(fileName + " | " + filePath)
        self.update_list_attr(stepWidget, stepAttr)
        self.refresh_status_color(stepWidget)

    def duplicate_custom_step(self, pre=True, *args):
        """Duplicate the selected step

        Arguments:
            pre (bool, optional): If true adds the steps to the pre step list
            *args: Maya's Dummy

        Returns:
            None: None
        """

        if pre:
            stepAttr = "pre_custom_step"
            stepWidget = self.custom_step_tab.preCustomStep_listWidget
        else:
            stepAttr = "post_custom_step"
            stepWidget = self.custom_step_tab.postCustomStep_listWidget

        # Check if we have a custom env for the custom steps initial folder
        if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
            startDir = os.environ.get("MBOX_CUSTOM_STEP_PATH", "")
        else:
            startDir = self._network.attr(stepAttr).get()

        if stepWidget.selectedItems():
            sourcePath = stepWidget.selectedItems()[0].text().split(
                "|")[-1][1:]

        filePath = pm.fileDialog2(
            fileMode=0,
            startingDirectory=startDir,
            okc="New",
            fileFilter='Custom Step .py (*.py)')
        if not filePath:
            return
        if not isinstance(filePath, str):
            filePath = filePath[0]

        if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
            sourcePath = os.path.join(startDir, sourcePath)
        shutil.copy(sourcePath, filePath)

        # Quick clean the first empty item
        itemsList = [i.text() for i in stepWidget.findItems(
            "", QtCore.Qt.MatchContains)]
        if itemsList and not itemsList[0]:
            stepWidget.takeItem(0)

        if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
            filePath = os.path.abspath(filePath)
            baseReplace = os.path.abspath(os.environ.get(
                "MBOX_CUSTOM_STEP_PATH", ""))
            filePath = filePath.replace(baseReplace, "")[1:]

        fileName = os.path.split(filePath)[1].split(".")[0]
        stepWidget.addItem(fileName + " | " + filePath)
        self.update_list_attr(stepWidget, stepAttr)
        self.refresh_status_color(stepWidget)

    def export_custom_step(self, pre=True, *args):
        """Export custom steps to a json file

        Arguments:
            pre (bool, optional): If true takes the steps from the
                pre step list
            *args: Maya's Dummy

        Returns:
            None: None

        """

        if pre:
            stepWidget = self.custom_step_tab.preCustomStep_listWidget
        else:
            stepWidget = self.custom_step_tab.postCustomStep_listWidget

        # Quick clean the first empty item
        itemsList = [i.text() for i in stepWidget.findItems(
            "", QtCore.Qt.MatchContains)]
        if itemsList and not itemsList[0]:
            stepWidget.takeItem(0)

        # Check if we have a custom env for the custom steps initial folder
        if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
            startDir = os.environ.get("MBOX_CUSTOM_STEP_PATH", "")
            itemsList = [os.path.join(startDir, i.text().split("|")[-1][1:])
                         for i in stepWidget.findItems(
                    "", QtCore.Qt.MatchContains)]
        else:
            itemsList = [i.text().split("|")[-1][1:]
                         for i in stepWidget.findItems(
                    "", QtCore.Qt.MatchContains)]
            if itemsList:
                startDir = os.path.split(itemsList[-1])[0]
            else:
                pm.displayWarning("No custom steps to export.")
                return
        stepsDict = self.get_steps_dict(itemsList)

        data_string = json.dumps(stepsDict, indent=4, sort_keys=True)
        filePath = pm.fileDialog2(
            fileMode=0,
            startingDirectory=startDir,
            fileFilter='Lego Custom Steps .lcs (*%s)' % ".lcs")
        if not filePath:
            return
        if not isinstance(filePath, str):
            filePath = filePath[0]
        f = open(filePath, 'w')
        f.write(data_string)
        f.close()

    def import_custom_step(self, pre=True, *args):
        """Import custom steps from a json file

        Arguments:
            pre (bool, optional): If true import to pre steps list
            *args: Maya's Dummy

        Returns:
            None: None

        """

        if pre:
            stepAttr = "pre_custom_step"
            stepWidget = self.custom_step_tab.preCustomStep_listWidget
        else:
            stepAttr = "post_custom_step"
            stepWidget = self.custom_step_tab.postCustomStep_listWidget

        # option import only paths or unpack steps
        option = pm.confirmDialog(
            title='Lego Custom Step Import Style',
            message='Do you want to import only the path or'
                    ' unpack and import?',
            button=['Only Path', 'Unpack', 'Cancel'],
            defaultButton='Only Path',
            cancelButton='Cancel',
            dismissString='Cancel')

        if option in ['Only Path', 'Unpack']:
            if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
                startDir = os.environ.get("MBOX_CUSTOM_STEP_PATH", "")
            else:
                startDir = pm.workspace(q=True, rootDirectory=True)

            filePath = pm.fileDialog2(
                fileMode=1,
                startingDirectory=startDir,
                fileFilter='Shifter Custom Steps .scs (*%s)' % ".scs")
            if not filePath:
                return
            if not isinstance(filePath, str):
                filePath = filePath[0]
            stepDict = json.load(open(filePath))
            stepsList = []

        if option == 'Only Path':
            for item in stepDict["itemsList"]:
                stepsList.append(item)

        elif option == 'Unpack':
            unPackDir = pm.fileDialog2(
                fileMode=2,
                startingDirectory=startDir)
            if not filePath:
                return
            if not isinstance(unPackDir, str):
                unPackDir = unPackDir[0]

            for item in stepDict["itemsList"]:
                fileName = os.path.split(item)[1]
                fileNewPath = os.path.join(unPackDir, fileName)
                stepsList.append(fileNewPath)
                f = open(fileNewPath, 'w')
                f.write(stepDict[item])
                f.close()

        if option in ['Only Path', 'Unpack']:

            for item in stepsList:
                # Quick clean the first empty item
                itemsList = [i.text() for i in stepWidget.findItems(
                    "", QtCore.Qt.MatchContains)]
                if itemsList and not itemsList[0]:
                    stepWidget.takeItem(0)

                if os.environ.get("MBOX_CUSTOM_STEP_PATH", ""):
                    item = os.path.abspath(item)
                    baseReplace = os.path.abspath(os.environ.get(
                        "MBOX_CUSTOM_STEP_PATH", ""))
                    item = item.replace(baseReplace, "")[1:]

                fileName = os.path.split(item)[1].split(".")[0]
                stepWidget.addItem(fileName + " | " + item)
                self.update_list_attr(stepWidget, stepAttr)

    def _custom_step_menu(self, cs_listWidget, stepAttr, QPos):
        "right click context menu for custom step"
        currentSelection = cs_listWidget.currentItem()
        if currentSelection is None:
            return
        self.csMenu = QtWidgets.QMenu()
        parentPosition = cs_listWidget.mapToGlobal(QtCore.QPoint(0, 0))
        menu_item_01 = self.csMenu.addAction("Toggle Custom Step")
        self.csMenu.addSeparator()
        menu_item_02 = self.csMenu.addAction("Turn OFF Selected")
        menu_item_03 = self.csMenu.addAction("Turn ON Selected")
        self.csMenu.addSeparator()
        menu_item_04 = self.csMenu.addAction("Turn OFF All")
        menu_item_05 = self.csMenu.addAction("Turn ON All")

        menu_item_01.triggered.connect(partial(self.toggle_status_custom_step,
                                               cs_listWidget,
                                               stepAttr))
        menu_item_02.triggered.connect(partial(self.set_status_custom_step,
                                               cs_listWidget,
                                               stepAttr,
                                               False))
        menu_item_03.triggered.connect(partial(self.set_status_custom_step,
                                               cs_listWidget,
                                               stepAttr,
                                               True))
        menu_item_04.triggered.connect(partial(self.set_status_custom_step,
                                               cs_listWidget,
                                               stepAttr,
                                               False,
                                               False))
        menu_item_05.triggered.connect(partial(self.set_status_custom_step,
                                               cs_listWidget,
                                               stepAttr,
                                               True,
                                               False))

        self.csMenu.move(parentPosition + QPos)
        self.csMenu.show()

    def pre_custom_step_menu(self, QPos):
        self._custom_step_menu(self.custom_step_tab.preCustomStep_listWidget,
                               "pre_custom_step",
                               QPos)

    def post_custom_step_menu(self, QPos):
        self._custom_step_menu(self.custom_step_tab.postCustomStep_listWidget,
                               "post_custom_step",
                               QPos)

    def toggle_status_custom_step(self, cs_listWidget, stepAttr):
        items = cs_listWidget.selectedItems()
        for item in items:
            if item.text().startswith("*"):
                item.setText(item.text()[1:])
                item.setForeground(self.white_down_brush)
            else:
                item.setText("*" + item.text())
                item.setForeground(self.red_brush)

        self.update_list_attr(cs_listWidget, stepAttr)
        self.refresh_status_color(cs_listWidget)

    def set_status_custom_step(
            self, cs_listWidget, stepAttr, status=True, selected=True):
        if selected:
            items = cs_listWidget.selectedItems()
        else:
            items = self.get_all_items(cs_listWidget)
        for item in items:
            off = item.text().startswith("*")
            if status and off:
                item.setText(item.text()[1:])
            elif not status and not off:
                item.setText("*" + item.text())
            self.set_status_color(item)
        self.update_list_attr(cs_listWidget, stepAttr)
        self.refresh_status_color(cs_listWidget)

    def get_all_items(self, cs_listWidget):
        return [cs_listWidget.item(i) for i in range(cs_listWidget.count())]

    def set_status_color(self, item):
        if item.text().startswith("*"):
            item.setForeground(self.red_brush)
        elif "_shared" in item.text():
            item.setForeground(self.green_brush)
        else:
            item.setForeground(self.white_down_brush)

    def refresh_status_color(self, cs_listWidget):
        items = self.get_all_items(cs_listWidget)
        for i in items:
            self.set_status_color(i)

        # Highligter filter

    def _highlight_search(self, cs_listWidget, searchText):
        items = self.get_all_items(cs_listWidget)
        for i in items:
            if searchText and searchText.lower() in i.text().lower():
                i.setBackground(QtGui.QColor(128, 128, 128, 255))
            else:
                i.setBackground(QtGui.QColor(255, 255, 255, 0))

    def pre_highlight_search(self):
        searchText = self.custom_step_tab.preSearch_lineEdit.text()
        self._highlight_search(self.custom_step_tab.preCustomStep_listWidget,
                               searchText)

    def post_highlight_search(self):
        searchText = self.custom_step_tab.postSearch_lineEdit.text()
        self._highlight_search(self.custom_step_tab.postCustomStep_listWidget,
                               searchText)


class BlockMainTabUI(QtWidgets.QDialog, block_ui.Ui_Form):

    def __init__(self):
        super(BlockMainTabUI, self).__init__()
        self.setupUi(self)


class BlockSettings(QtWidgets.QDialog, HelperSlots):

    valueChanged = QtCore.Signal(int)

    def __init__(self, parent=None):
        super(BlockSettings, self).__init__()
        # the inspectSettings function set the current selection to the
        # component root before open the settings dialog
        self._guide = lib.get_component_guide(pm.selected(type="transform")[0])[0]
        self._network = self._guide.message.outputs(type="network")[0]

        self.main_tab = BlockMainTabUI()

        self.create_controls()
        self.populate_controls()
        self.create_layout()
        self.create_connections()

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

    def create_controls(self):
        """
        Create the controls for the component base

        """
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setObjectName("block_settings_tab")

        # Close Button
        self.close_button = QtWidgets.QPushButton("Close")

    def populate_controls(self):
        """Populate Controls attribute values

        Populate the controls values from the custom attributes
        of the component.

        """
        # populate tab
        self.tabs.insertTab(0, self.main_tab, "Main Settings")

        # populate main settings
        self.main_tab.name_lineEdit.setText(
            self._network.attr("comp_name").get())
        sideSet = ["center", "left", "right"]
        sideIndex = sideSet.index(self._network.attr("comp_side").get(asString=True))
        self.main_tab.side_comboBox.setCurrentIndex(sideIndex)
        self.main_tab.componentIndex_spinBox.setValue(
            self._network.attr("comp_index").get())
        # if self._network.attr("useIndex").get():
        #     self.main_tab.useJointIndex_checkBox.setCheckState(
        #         QtCore.Qt.Checked)
        # else:
        #     self.main_tab.useJointIndex_checkBox.setCheckState(
        #         QtCore.Qt.Unchecked)
        # self.main_tab.parentJointIndex_spinBox.setValue(
        #     self._network.attr("parentJointIndex").get())
        self.main_tab.host_lineEdit.setText(
            self._network.attr("ui_host").get().split(",")[0])
        # self.main_tab.subGroup_lineEdit.setText(
        #     self._network.attr("ctlGrp").get())
        # self.main_tab.joint_offset_x_doubleSpinBox.setValue(
        #     self._network.attr("joint_rot_offset_x").get())
        # self.main_tab.joint_offset_y_doubleSpinBox.setValue(
        #     self._network.attr("joint_rot_offset_y").get())
        # self.main_tab.joint_offset_z_doubleSpinBox.setValue(
        #     self._network.attr("joint_rot_offset_z").get())

        # testing adding custom color per component
        self.main_tab.overrideColors_checkBox.setCheckState(
            QtCore.Qt.Checked if self._network.attr("override_color").get()
            else QtCore.Qt.Unchecked)

        self.main_tab.useRGB_checkBox.setCheckState(
            QtCore.Qt.Checked if self._network.attr("use_RGB_color").get()
            else QtCore.Qt.Unchecked)

        tab = self.main_tab

        index_widgets = ((tab.color_fk_spinBox,
                          tab.color_fk_label,
                          "color_fk"),
                         (tab.color_ik_spinBox,
                          tab.color_ik_label,
                          "color_ik"))

        rgb_widgets = ((tab.RGB_fk_pushButton, tab.RGB_fk_slider, "RGB_fk"),
                       (tab.RGB_ik_pushButton, tab.RGB_ik_slider, "RGB_ik"))

        for spinBox, label, source_attr in index_widgets:
            color_index = self._network.attr(source_attr).get()
            spinBox.setValue(color_index)
            self.update_widget_style_sheet(
                label, [i / 255.0 for i in MAYA_OVERRIDE_COLOR[color_index]])

        for button, slider, source_attr in rgb_widgets:
            self.update_rgb_color_widgets(
                button, self._network.attr(source_attr).get(), slider)

        # forceing the size of the color buttons/label to keep ui clean
        for widget in tuple(i[0] for i in rgb_widgets) + tuple(
                i[1] for i in index_widgets):
            widget.setFixedSize(pyqt.dpi_scale(30), pyqt.dpi_scale(20))

        self.toggle_rgb_index_widgets(tab.useRGB_checkBox,
                                      (w for i in index_widgets for w in i[:2]),
                                      (w for i in rgb_widgets for w in i[:2]),
                                      "use_RGB_color",
                                      tab.useRGB_checkBox.checkState())

        self.refresh_controls()

    def refresh_controls(self):
        joint_names = [name.strip() for name in
                       self._network.attr("joint_names").get().split(",")]
        if any(joint_names):
            summary = "<b>({0} set)</b>".format(sum(map(bool, joint_names)))
        else:
            summary = "(None)"
        self.main_tab.jointNames_label.setText("Joint Names " + summary)

    def create_layout(self):
        """
        Create the layout for the component base settings

        """
        return

    def create_connections(self):
        """
        Create the slots connections to the controls functions

        """
        self.close_button.clicked.connect(self.close_settings)

        self.main_tab.name_lineEdit.editingFinished.connect(
            self.update_component_name)
        self.main_tab.side_comboBox.currentIndexChanged.connect(
            self.update_component_name)
        self.main_tab.componentIndex_spinBox.valueChanged.connect(
            self.update_component_name)
        # self.main_tab.useJointIndex_checkBox.stateChanged.connect(
        #     partial(self.update_check,
        #             self.main_tab.useJointIndex_checkBox,
        #             "useIndex"))
        # self.main_tab.parentJointIndex_spinBox.valueChanged.connect(
        #     partial(self.update_spin_box,
        #             self.main_tab.parentJointIndex_spinBox,
        #             "parentJointIndex"))
        self.main_tab.host_pushButton.clicked.connect(
            partial(self.update_host_ui,
                    self.main_tab.host_lineEdit,
                    "ui_host"))
        # self.main_tab.subGroup_lineEdit.editingFinished.connect(
        #     partial(self.update_line_edit,
        #             self.main_tab.subGroup_lineEdit,
        #             "ctlGrp"))
        self.main_tab.jointNames_pushButton.clicked.connect(
            self.joint_names_dialog)

        # self.main_tab.joint_offset_x_doubleSpinBox.valueChanged.connect(
        #     partial(self.update_spin_box,
        #             self.main_tab.joint_offset_x_doubleSpinBox,
        #             "joint_rot_offset_x"))
        # self.main_tab.joint_offset_y_doubleSpinBox.valueChanged.connect(
        #     partial(self.update_spin_box,
        #             self.main_tab.joint_offset_y_doubleSpinBox,
        #             "joint_rot_offset_y"))
        # self.main_tab.joint_offset_z_doubleSpinBox.valueChanged.connect(
        #     partial(self.update_spin_box,
        #             self.main_tab.joint_offset_z_doubleSpinBox,
        #             "joint_rot_offset_z"))

        tab = self.main_tab

        index_widgets = ((tab.color_fk_spinBox,
                          tab.color_fk_label,
                          "color_fk"),
                         (tab.color_ik_spinBox,
                          tab.color_ik_label,
                          "color_ik"))

        rgb_widgets = ((tab.RGB_fk_pushButton, tab.RGB_fk_slider, "RGB_fk"),
                       (tab.RGB_ik_pushButton, tab.RGB_ik_slider, "RGB_ik"))

        for spinBox, label, source_attr in index_widgets:
            spinBox.valueChanged.connect(
                partial(self.update_index_color_widgets,
                        spinBox,
                        source_attr,
                        label))

        for button, slider, source_attr in rgb_widgets:
            button.clicked.connect(
                partial(self.rgb_color_editor, button, source_attr, slider))
            slider.valueChanged.connect(
                partial(self.rgb_slider_value_changed, button, source_attr))

        tab.useRGB_checkBox.stateChanged.connect(
            partial(self.toggle_rgb_index_widgets,
                    tab.useRGB_checkBox,
                    tuple(w for i in index_widgets for w in i[:2]),
                    tuple(w for i in rgb_widgets for w in i[:2]),
                    "use_RGB_color"))

        tab.overrideColors_checkBox.stateChanged.connect(
            partial(self.update_check,
                    tab.overrideColors_checkBox,
                    "override_color"))

    def joint_names_dialog(self):
        dialog = JointNames(self._network, self)
        dialog.setWindowTitle(self.windowTitle())
        dialog.attributeChanged.connect(self.refresh_controls)
        dialog.show()


class JointNames(QtWidgets.QDialog, joint_name_ui.Ui_Form):
    attributeChanged = QtCore.Signal()

    def __init__(self, network, parent=None):
        super(JointNames, self).__init__(parent)
        self._network = network

        self.setupUi(self)

        self.populate_controls()
        self.apply_names()
        self.create_connections()

    def populate_controls(self):
        jointNames = self._network.attr("joint_names").get().split(",")
        if jointNames[-1]:
            jointNames.append("")

        self.jointNamesList.clearContents()
        self.jointNamesList.setRowCount(0)

        for i, name in enumerate(jointNames):
            self.jointNamesList.insertRow(i)
            item = QtWidgets.QTableWidgetItem(name.strip())
            self.jointNamesList.setItem(i, 0, item)

    def create_connections(self):
        self.jointNamesList.cellChanged.connect(self.update_name)
        self.jointNamesList.itemActivated.connect(self.jointNamesList.editItem)

        self.add_pushButton.clicked.connect(self.add)
        self.remove_pushButton.clicked.connect(self.remove)
        self.removeAll_pushButton.clicked.connect(self.remove_all)

        self.moveUp_pushButton.clicked.connect(lambda: self.move(-1))
        self.moveDown_pushButton.clicked.connect(lambda: self.move(1))

    def apply_names(self):
        jointNames = []
        for i in range(self.jointNamesList.rowCount()):
            item = self.jointNamesList.item(i, 0)
            jointNames.append(item.text())

        value = ",".join(jointNames[0:-1])
        self._network.attr("joint_names").set(value)

        self.jointNamesList.setVerticalHeaderLabels(
            [str(i) for i in range(len(jointNames))])

        self.attributeChanged.emit()

    def add(self):
        row = max(0, self.jointNamesList.currentRow() or 0)
        self.jointNamesList.insertRow(row)
        item = QtWidgets.QTableWidgetItem("")
        self.jointNamesList.setItem(row, 0, item)
        self.jointNamesList.setCurrentCell(row, 0)
        self.apply_names()

    def remove(self):
        row = self.jointNamesList.currentRow()
        if row + 1 < self.jointNamesList.rowCount() > 1:
            self.jointNamesList.removeRow(row)
            self.apply_names()
            self.jointNamesList.setCurrentCell(row, 0)

    def remove_all(self):
        self.jointNamesList.clearContents()
        self.jointNamesList.setRowCount(0)
        self.jointNamesList.insertRow(0)
        self.jointNamesList.setItem(0, 0, QtWidgets.QTableWidgetItem(""))
        self.jointNamesList.setCurrentCell(0, 0)
        self.apply_names()

    def move(self, step):
        row = self.jointNamesList.currentRow()
        if row + step < 0:
            return
        item1 = self.jointNamesList.item(row, 0).text()
        item2 = self.jointNamesList.item(row + step, 0).text()
        self.jointNamesList.item(row, 0).setText(item2)
        self.jointNamesList.item(row + step, 0).setText(item1)
        self.jointNamesList.setCurrentCell(row + step, 0)

    def update_name(self, row, column):
        item = self.jointNamesList.item(row, column)
        if row == self.jointNamesList.rowCount() - 1 and item.text():
            self.jointNamesList.insertRow(row + 1)
            self.jointNamesList.setItem(
                row + 1, 0, QtWidgets.QTableWidgetItem(""))
        self.apply_names()
        self.jointNamesList.setCurrentCell(row + 1, 0)
        self.jointNamesList.editItem(self.jointNamesList.currentItem())

    def keyPressEvent(self):
        pass
