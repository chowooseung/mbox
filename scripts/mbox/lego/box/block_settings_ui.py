# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'block_settings_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(452, 518)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 0, 1, 1)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.host_label = QLabel(self.groupBox)
        self.host_label.setObjectName(u"host_label")

        self.horizontalLayout_2.addWidget(self.host_label)

        self.host_lineEdit = QLineEdit(self.groupBox)
        self.host_lineEdit.setObjectName(u"host_lineEdit")

        self.horizontalLayout_2.addWidget(self.host_lineEdit)

        self.host_pushButton = QPushButton(self.groupBox)
        self.host_pushButton.setObjectName(u"host_pushButton")

        self.horizontalLayout_2.addWidget(self.host_pushButton)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 1)

        self.groupBox_4 = QGroupBox(Form)
        self.groupBox_4.setObjectName(u"groupBox_4")
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.gridLayout_8 = QGridLayout(self.groupBox_4)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.color_fk_label = QLabel(self.groupBox_4)
        self.color_fk_label.setObjectName(u"color_fk_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.color_fk_label.sizePolicy().hasHeightForWidth())
        self.color_fk_label.setSizePolicy(sizePolicy1)
        self.color_fk_label.setMinimumSize(QSize(0, 0))

        self.gridLayout_9.addWidget(self.color_fk_label, 0, 1, 1, 1)

        self.color_fk_spinBox = QSpinBox(self.groupBox_4)
        self.color_fk_spinBox.setObjectName(u"color_fk_spinBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.color_fk_spinBox.sizePolicy().hasHeightForWidth())
        self.color_fk_spinBox.setSizePolicy(sizePolicy2)
        self.color_fk_spinBox.setMaximum(31)

        self.gridLayout_9.addWidget(self.color_fk_spinBox, 0, 2, 1, 1)

        self.RGB_fk_pushButton = QPushButton(self.groupBox_4)
        self.RGB_fk_pushButton.setObjectName(u"RGB_fk_pushButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.RGB_fk_pushButton.sizePolicy().hasHeightForWidth())
        self.RGB_fk_pushButton.setSizePolicy(sizePolicy3)
        self.RGB_fk_pushButton.setMaximumSize(QSize(16777215, 16777215))
        self.RGB_fk_pushButton.setLayoutDirection(Qt.LeftToRight)
        self.RGB_fk_pushButton.setStyleSheet(u"")

        self.gridLayout_9.addWidget(self.RGB_fk_pushButton, 0, 3, 1, 1)

        self.RGB_fk_slider = QSlider(self.groupBox_4)
        self.RGB_fk_slider.setObjectName(u"RGB_fk_slider")
        self.RGB_fk_slider.setMaximum(255)
        self.RGB_fk_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_9.addWidget(self.RGB_fk_slider, 0, 4, 1, 1)

        self.fk_label_2 = QLabel(self.groupBox_4)
        self.fk_label_2.setObjectName(u"fk_label_2")

        self.gridLayout_9.addWidget(self.fk_label_2, 0, 0, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_9, 1, 0, 1, 1)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.color_ik_spinBox = QSpinBox(self.groupBox_4)
        self.color_ik_spinBox.setObjectName(u"color_ik_spinBox")
        sizePolicy2.setHeightForWidth(self.color_ik_spinBox.sizePolicy().hasHeightForWidth())
        self.color_ik_spinBox.setSizePolicy(sizePolicy2)
        self.color_ik_spinBox.setMaximum(31)

        self.gridLayout_10.addWidget(self.color_ik_spinBox, 0, 2, 1, 1)

        self.color_ik_label = QLabel(self.groupBox_4)
        self.color_ik_label.setObjectName(u"color_ik_label")
        sizePolicy1.setHeightForWidth(self.color_ik_label.sizePolicy().hasHeightForWidth())
        self.color_ik_label.setSizePolicy(sizePolicy1)
        self.color_ik_label.setMinimumSize(QSize(0, 0))

        self.gridLayout_10.addWidget(self.color_ik_label, 0, 1, 1, 1)

        self.RGB_ik_pushButton = QPushButton(self.groupBox_4)
        self.RGB_ik_pushButton.setObjectName(u"RGB_ik_pushButton")
        sizePolicy3.setHeightForWidth(self.RGB_ik_pushButton.sizePolicy().hasHeightForWidth())
        self.RGB_ik_pushButton.setSizePolicy(sizePolicy3)
        self.RGB_ik_pushButton.setMaximumSize(QSize(16777215, 16777215))
        self.RGB_ik_pushButton.setLayoutDirection(Qt.LeftToRight)
        self.RGB_ik_pushButton.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.RGB_ik_pushButton, 0, 3, 1, 1)

        self.RGB_ik_slider = QSlider(self.groupBox_4)
        self.RGB_ik_slider.setObjectName(u"RGB_ik_slider")
        self.RGB_ik_slider.setMaximum(255)
        self.RGB_ik_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_10.addWidget(self.RGB_ik_slider, 0, 4, 1, 1)

        self.ik_label = QLabel(self.groupBox_4)
        self.ik_label.setObjectName(u"ik_label")

        self.gridLayout_10.addWidget(self.ik_label, 0, 0, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_10, 1, 1, 1, 1)

        self.overrideColors_checkBox = QCheckBox(self.groupBox_4)
        self.overrideColors_checkBox.setObjectName(u"overrideColors_checkBox")

        self.gridLayout_7.addWidget(self.overrideColors_checkBox, 0, 0, 1, 1)

        self.useRGB_checkBox = QCheckBox(self.groupBox_4)
        self.useRGB_checkBox.setObjectName(u"useRGB_checkBox")

        self.gridLayout_7.addWidget(self.useRGB_checkBox, 0, 1, 1, 1)


        self.gridLayout_8.addLayout(self.gridLayout_7, 2, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_4, 4, 0, 1, 1)

        self.mainSettings_groupBox = QGroupBox(Form)
        self.mainSettings_groupBox.setObjectName(u"mainSettings_groupBox")
        self.gridLayout_4 = QGridLayout(self.mainSettings_groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.name_label = QLabel(self.mainSettings_groupBox)
        self.name_label.setObjectName(u"name_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.name_label)

        self.name_lineEdit = QLineEdit(self.mainSettings_groupBox)
        self.name_lineEdit.setObjectName(u"name_lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.name_lineEdit)

        self.side_label = QLabel(self.mainSettings_groupBox)
        self.side_label.setObjectName(u"side_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.side_label)

        self.side_comboBox = QComboBox(self.mainSettings_groupBox)
        self.side_comboBox.addItem("")
        self.side_comboBox.addItem("")
        self.side_comboBox.addItem("")
        self.side_comboBox.setObjectName(u"side_comboBox")
        sizePolicy2.setHeightForWidth(self.side_comboBox.sizePolicy().hasHeightForWidth())
        self.side_comboBox.setSizePolicy(sizePolicy2)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.side_comboBox)

        self.componentIndex_label = QLabel(self.mainSettings_groupBox)
        self.componentIndex_label.setObjectName(u"componentIndex_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.componentIndex_label)

        self.componentIndex_spinBox = QSpinBox(self.mainSettings_groupBox)
        self.componentIndex_spinBox.setObjectName(u"componentIndex_spinBox")
        sizePolicy2.setHeightForWidth(self.componentIndex_spinBox.sizePolicy().hasHeightForWidth())
        self.componentIndex_spinBox.setSizePolicy(sizePolicy2)
        self.componentIndex_spinBox.setMaximum(999)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.componentIndex_spinBox)

        self.conector_label = QLabel(self.mainSettings_groupBox)
        self.conector_label.setObjectName(u"conector_label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.conector_label)

        self.connector_comboBox = QComboBox(self.mainSettings_groupBox)
        self.connector_comboBox.addItem("")
        self.connector_comboBox.setObjectName(u"connector_comboBox")
        sizePolicy2.setHeightForWidth(self.connector_comboBox.sizePolicy().hasHeightForWidth())
        self.connector_comboBox.setSizePolicy(sizePolicy2)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.connector_comboBox)


        self.gridLayout_4.addLayout(self.formLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.mainSettings_groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.gridLayout_5 = QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.subGroup_lineEdit = QLineEdit(self.groupBox_2)
        self.subGroup_lineEdit.setObjectName(u"subGroup_lineEdit")

        self.horizontalLayout_3.addWidget(self.subGroup_lineEdit)


        self.gridLayout_5.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox_2, 3, 0, 1, 1)

        self.jointSettings_groupBox = QGroupBox(Form)
        self.jointSettings_groupBox.setObjectName(u"jointSettings_groupBox")
        sizePolicy.setHeightForWidth(self.jointSettings_groupBox.sizePolicy().hasHeightForWidth())
        self.jointSettings_groupBox.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QGridLayout(self.jointSettings_groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.useJointIndex_checkBox = QCheckBox(self.jointSettings_groupBox)
        self.useJointIndex_checkBox.setObjectName(u"useJointIndex_checkBox")

        self.horizontalLayout_5.addWidget(self.useJointIndex_checkBox)

        self.parentJointIndex_spinBox = QSpinBox(self.jointSettings_groupBox)
        self.parentJointIndex_spinBox.setObjectName(u"parentJointIndex_spinBox")
        sizePolicy2.setHeightForWidth(self.parentJointIndex_spinBox.sizePolicy().hasHeightForWidth())
        self.parentJointIndex_spinBox.setSizePolicy(sizePolicy2)
        self.parentJointIndex_spinBox.setMinimum(-1)
        self.parentJointIndex_spinBox.setMaximum(999999)
        self.parentJointIndex_spinBox.setValue(-1)

        self.horizontalLayout_5.addWidget(self.parentJointIndex_spinBox)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.jointNames_label = QLabel(self.jointSettings_groupBox)
        self.jointNames_label.setObjectName(u"jointNames_label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.jointNames_label.sizePolicy().hasHeightForWidth())
        self.jointNames_label.setSizePolicy(sizePolicy4)
        self.jointNames_label.setMinimumSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.jointNames_label)

        self.jointNames_pushButton = QPushButton(self.jointSettings_groupBox)
        self.jointNames_pushButton.setObjectName(u"jointNames_pushButton")
        sizePolicy2.setHeightForWidth(self.jointNames_pushButton.sizePolicy().hasHeightForWidth())
        self.jointNames_pushButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.jointNames_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox_3 = QGroupBox(self.jointSettings_groupBox)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.joint_offset_x_doubleSpinBox = QDoubleSpinBox(self.groupBox_3)
        self.joint_offset_x_doubleSpinBox.setObjectName(u"joint_offset_x_doubleSpinBox")
        self.joint_offset_x_doubleSpinBox.setMinimum(-360.000000000000000)
        self.joint_offset_x_doubleSpinBox.setMaximum(360.000000000000000)
        self.joint_offset_x_doubleSpinBox.setSingleStep(90.000000000000000)

        self.horizontalLayout_4.addWidget(self.joint_offset_x_doubleSpinBox)

        self.joint_offset_y_doubleSpinBox = QDoubleSpinBox(self.groupBox_3)
        self.joint_offset_y_doubleSpinBox.setObjectName(u"joint_offset_y_doubleSpinBox")
        self.joint_offset_y_doubleSpinBox.setMinimum(-360.000000000000000)
        self.joint_offset_y_doubleSpinBox.setMaximum(360.000000000000000)
        self.joint_offset_y_doubleSpinBox.setSingleStep(90.000000000000000)

        self.horizontalLayout_4.addWidget(self.joint_offset_y_doubleSpinBox)

        self.joint_offset_z_doubleSpinBox = QDoubleSpinBox(self.groupBox_3)
        self.joint_offset_z_doubleSpinBox.setObjectName(u"joint_offset_z_doubleSpinBox")
        self.joint_offset_z_doubleSpinBox.setMinimum(-360.000000000000000)
        self.joint_offset_z_doubleSpinBox.setMaximum(360.000000000000000)
        self.joint_offset_z_doubleSpinBox.setSingleStep(90.000000000000000)

        self.horizontalLayout_4.addWidget(self.joint_offset_z_doubleSpinBox)


        self.verticalLayout.addWidget(self.groupBox_3)


        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.jointSettings_groupBox, 1, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Channels Host Settings", None))
        self.host_label.setText(QCoreApplication.translate("Form", u"Host:", None))
        self.host_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"Color Settings", None))
        self.color_fk_label.setText("")
        self.RGB_fk_pushButton.setText("")
        self.fk_label_2.setText(QCoreApplication.translate("Form", u"FK", None))
        self.color_ik_label.setText("")
        self.RGB_ik_pushButton.setText("")
        self.ik_label.setText(QCoreApplication.translate("Form", u"IK", None))
        self.overrideColors_checkBox.setText(QCoreApplication.translate("Form", u"Override Colors", None))
        self.useRGB_checkBox.setText(QCoreApplication.translate("Form", u"Use RGB Colors", None))
        self.mainSettings_groupBox.setTitle("")
        self.name_label.setText(QCoreApplication.translate("Form", u"Name:", None))
        self.side_label.setText(QCoreApplication.translate("Form", u"Side:", None))
        self.side_comboBox.setItemText(0, QCoreApplication.translate("Form", u"Center", None))
        self.side_comboBox.setItemText(1, QCoreApplication.translate("Form", u"Left", None))
        self.side_comboBox.setItemText(2, QCoreApplication.translate("Form", u"Right", None))

        self.componentIndex_label.setText(QCoreApplication.translate("Form", u"Component Index:", None))
        self.conector_label.setText(QCoreApplication.translate("Form", u"Connector:", None))
        self.connector_comboBox.setItemText(0, QCoreApplication.translate("Form", u"standard", None))

        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Custom Controllers Group", None))
#if QT_CONFIG(tooltip)
        self.subGroup_lineEdit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Name for a custom controllers Group (Maya set) for the component controllers.</p><p align=\"center\"><span style=\" font-weight:600;\">i.e</span>: Setting the name &quot;arm&quot; will create a sub group (sub set in Mayas terminology) with the name &quot;rig_arm_grp&quot;. This group will be under the &quot;rig_controllers_grp&quot;</p><p>Leave this option empty for the default behaviour.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.jointSettings_groupBox.setTitle(QCoreApplication.translate("Form", u"Joint Settings", None))
        self.useJointIndex_checkBox.setText(QCoreApplication.translate("Form", u"Parent Joint Index", None))
        self.jointNames_label.setText(QCoreApplication.translate("Form", u"Joint Names", None))
        self.jointNames_pushButton.setText(QCoreApplication.translate("Form", u"Configure", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"Orientation Offset XYZ", None))
#if QT_CONFIG(tooltip)
        self.joint_offset_x_doubleSpinBox.setToolTip(QCoreApplication.translate("Form", u"Rotation Offset X", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.joint_offset_y_doubleSpinBox.setToolTip(QCoreApplication.translate("Form", u"Rotation Offset Y", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.joint_offset_z_doubleSpinBox.setToolTip(QCoreApplication.translate("Form", u"Rotation Offset Z", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

