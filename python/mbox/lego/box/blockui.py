# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'blockui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from mgear.vendor.Qt.QtCore import *
from mgear.vendor.Qt.QtGui import *
from mgear.vendor.Qt.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(306, 482)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
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

        self.direction_comboBox = QComboBox(self.mainSettings_groupBox)
        self.direction_comboBox.addItem("")
        self.direction_comboBox.addItem("")
        self.direction_comboBox.addItem("")
        self.direction_comboBox.setObjectName(u"direction_comboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.direction_comboBox.sizePolicy().hasHeightForWidth())
        self.direction_comboBox.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.direction_comboBox)

        self.index_label = QLabel(self.mainSettings_groupBox)
        self.index_label.setObjectName(u"index_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.index_label)

        self.index_spinBox = QSpinBox(self.mainSettings_groupBox)
        self.index_spinBox.setObjectName(u"index_spinBox")
        sizePolicy.setHeightForWidth(self.index_spinBox.sizePolicy().hasHeightForWidth())
        self.index_spinBox.setSizePolicy(sizePolicy)
        self.index_spinBox.setMinimum(0)
        self.index_spinBox.setMaximum(999)
        self.index_spinBox.setValue(0)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.index_spinBox)

        self.connector_label = QLabel(self.mainSettings_groupBox)
        self.connector_label.setObjectName(u"connector_label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.connector_label)

        self.connector_comboBox = QComboBox(self.mainSettings_groupBox)
        self.connector_comboBox.addItem("")
        self.connector_comboBox.setObjectName(u"connector_comboBox")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.connector_comboBox)

        self.label_2 = QLabel(self.mainSettings_groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_2)

        self.root_ref_index_spinBox = QSpinBox(self.mainSettings_groupBox)
        self.root_ref_index_spinBox.setObjectName(u"root_ref_index_spinBox")
        self.root_ref_index_spinBox.setMinimum(-1)
        self.root_ref_index_spinBox.setMaximum(999)
        self.root_ref_index_spinBox.setValue(-1)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.root_ref_index_spinBox)


        self.gridLayout_4.addLayout(self.formLayout, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.mainSettings_groupBox)

        self.jointSettings_groupBox = QGroupBox(Form)
        self.jointSettings_groupBox.setObjectName(u"jointSettings_groupBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.jointSettings_groupBox.sizePolicy().hasHeightForWidth())
        self.jointSettings_groupBox.setSizePolicy(sizePolicy1)
        self.gridLayout_3 = QGridLayout(self.jointSettings_groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
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


        self.gridLayout_3.addWidget(self.groupBox_3, 1, 0, 1, 1)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label = QLabel(self.jointSettings_groupBox)
        self.label.setObjectName(u"label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label)

        self.joint_ref_index_spinBox = QSpinBox(self.jointSettings_groupBox)
        self.joint_ref_index_spinBox.setObjectName(u"joint_ref_index_spinBox")
        self.joint_ref_index_spinBox.setMinimum(-1)
        self.joint_ref_index_spinBox.setMaximum(999)
        self.joint_ref_index_spinBox.setValue(-1)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.joint_ref_index_spinBox)

        self.label_3 = QLabel(self.jointSettings_groupBox)
        self.label_3.setObjectName(u"label_3")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.primary_axis_comboBox = QComboBox(self.jointSettings_groupBox)
        self.primary_axis_comboBox.addItem("")
        self.primary_axis_comboBox.addItem("")
        self.primary_axis_comboBox.addItem("")
        self.primary_axis_comboBox.addItem("")
        self.primary_axis_comboBox.addItem("")
        self.primary_axis_comboBox.addItem("")
        self.primary_axis_comboBox.setObjectName(u"primary_axis_comboBox")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.primary_axis_comboBox)

        self.label_4 = QLabel(self.jointSettings_groupBox)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.secondary_axis_comboBox = QComboBox(self.jointSettings_groupBox)
        self.secondary_axis_comboBox.addItem("")
        self.secondary_axis_comboBox.addItem("")
        self.secondary_axis_comboBox.addItem("")
        self.secondary_axis_comboBox.addItem("")
        self.secondary_axis_comboBox.addItem("")
        self.secondary_axis_comboBox.addItem("")
        self.secondary_axis_comboBox.setObjectName(u"secondary_axis_comboBox")

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.secondary_axis_comboBox)

        self.label_5 = QLabel(self.jointSettings_groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.create_joint_checkBox = QCheckBox(self.jointSettings_groupBox)
        self.create_joint_checkBox.setObjectName(u"create_joint_checkBox")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.create_joint_checkBox)


        self.gridLayout_3.addLayout(self.formLayout_2, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.jointSettings_groupBox)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy1.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy1)
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


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.gridLayout_5 = QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.subGroup_lineEdit = QLineEdit(self.groupBox_2)
        self.subGroup_lineEdit.setObjectName(u"subGroup_lineEdit")

        self.horizontalLayout_3.addWidget(self.subGroup_lineEdit)


        self.gridLayout_5.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.mainSettings_groupBox.setTitle("")
        self.name_label.setText(QCoreApplication.translate("Form", u"Name", None))
        self.side_label.setText(QCoreApplication.translate("Form", u"Direction", None))
        self.direction_comboBox.setItemText(0, QCoreApplication.translate("Form", u"center", None))
        self.direction_comboBox.setItemText(1, QCoreApplication.translate("Form", u"left", None))
        self.direction_comboBox.setItemText(2, QCoreApplication.translate("Form", u"right", None))

        self.index_label.setText(QCoreApplication.translate("Form", u"Index", None))
        self.connector_label.setText(QCoreApplication.translate("Form", u"Connector", None))
        self.connector_comboBox.setItemText(0, QCoreApplication.translate("Form", u"None", None))

        self.label_2.setText(QCoreApplication.translate("Form", u"Root Ref Index", None))
        self.jointSettings_groupBox.setTitle(QCoreApplication.translate("Form", u"Joint Settings", None))
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
        self.label.setText(QCoreApplication.translate("Form", u"Joint Ref Index", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Primary Axis", None))
        self.primary_axis_comboBox.setItemText(0, QCoreApplication.translate("Form", u"x", None))
        self.primary_axis_comboBox.setItemText(1, QCoreApplication.translate("Form", u"y", None))
        self.primary_axis_comboBox.setItemText(2, QCoreApplication.translate("Form", u"z", None))
        self.primary_axis_comboBox.setItemText(3, QCoreApplication.translate("Form", u"-x", None))
        self.primary_axis_comboBox.setItemText(4, QCoreApplication.translate("Form", u"-y", None))
        self.primary_axis_comboBox.setItemText(5, QCoreApplication.translate("Form", u"-z", None))

        self.label_4.setText(QCoreApplication.translate("Form", u"Secondary Axis", None))
        self.secondary_axis_comboBox.setItemText(0, QCoreApplication.translate("Form", u"x", None))
        self.secondary_axis_comboBox.setItemText(1, QCoreApplication.translate("Form", u"y", None))
        self.secondary_axis_comboBox.setItemText(2, QCoreApplication.translate("Form", u"z", None))
        self.secondary_axis_comboBox.setItemText(3, QCoreApplication.translate("Form", u"-x", None))
        self.secondary_axis_comboBox.setItemText(4, QCoreApplication.translate("Form", u"-y", None))
        self.secondary_axis_comboBox.setItemText(5, QCoreApplication.translate("Form", u"-z", None))

        self.secondary_axis_comboBox.setCurrentText(QCoreApplication.translate("Form", u"y", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Create Joint", None))
        self.create_joint_checkBox.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Channels Host Settings", None))
        self.host_label.setText(QCoreApplication.translate("Form", u"Host:", None))
        self.host_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Custom Controllers Group", None))
#if QT_CONFIG(tooltip)
        self.subGroup_lineEdit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Name for a custom controllers Group (Maya set) for the component controllers.</p><p align=\"center\"><span style=\" font-weight:600;\">i.e</span>: Setting the name &quot;arm&quot; will create a sub group (sub set in Mayas terminology) with the name &quot;rig_arm_grp&quot;. This group will be under the &quot;rig_controllers_grp&quot;</p><p>Leave this option empty for the default behaviour.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

