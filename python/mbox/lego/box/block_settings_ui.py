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
        Form.resize(306, 445)
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

        self.label_2 = QLabel(self.mainSettings_groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_2)

        self.parent_ref_index_spinBox = QSpinBox(self.mainSettings_groupBox)
        self.parent_ref_index_spinBox.setObjectName(u"parent_ref_index_spinBox")
        sizePolicy.setHeightForWidth(self.parent_ref_index_spinBox.sizePolicy().hasHeightForWidth())
        self.parent_ref_index_spinBox.setSizePolicy(sizePolicy)
        self.parent_ref_index_spinBox.setMinimum(-1)
        self.parent_ref_index_spinBox.setMaximum(999)
        self.parent_ref_index_spinBox.setValue(-1)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.parent_ref_index_spinBox)


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
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.joint_names_label = QLabel(self.jointSettings_groupBox)
        self.joint_names_label.setObjectName(u"joint_names_label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.joint_names_label)

        self.joint_names_pushButton = QPushButton(self.jointSettings_groupBox)
        self.joint_names_pushButton.setObjectName(u"joint_names_pushButton")
        sizePolicy.setHeightForWidth(self.joint_names_pushButton.sizePolicy().hasHeightForWidth())
        self.joint_names_pushButton.setSizePolicy(sizePolicy)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.joint_names_pushButton)

        self.joint_rig_checkBox = QCheckBox(self.jointSettings_groupBox)
        self.joint_rig_checkBox.setObjectName(u"joint_rig_checkBox")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.joint_rig_checkBox)

        self.label_5 = QLabel(self.jointSettings_groupBox)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_5)


        self.gridLayout_3.addLayout(self.formLayout_2, 0, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.jointSettings_groupBox)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout = QGridLayout(self.groupBox_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_3 = QGroupBox(self.groupBox_4)
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


        self.gridLayout.addWidget(self.groupBox_3, 3, 0, 1, 2)

        self.primary_axis_comboBox = QComboBox(self.groupBox_4)
        self.primary_axis_comboBox.addItem("")
        self.primary_axis_comboBox.addItem("")
        self.primary_axis_comboBox.addItem("")
        self.primary_axis_comboBox.addItem("")
        self.primary_axis_comboBox.addItem("")
        self.primary_axis_comboBox.addItem("")
        self.primary_axis_comboBox.setObjectName(u"primary_axis_comboBox")

        self.gridLayout.addWidget(self.primary_axis_comboBox, 1, 1, 1, 1)

        self.label_4 = QLabel(self.groupBox_4)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.label_3 = QLabel(self.groupBox_4)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.secondary_axis_comboBox = QComboBox(self.groupBox_4)
        self.secondary_axis_comboBox.addItem("")
        self.secondary_axis_comboBox.addItem("")
        self.secondary_axis_comboBox.addItem("")
        self.secondary_axis_comboBox.addItem("")
        self.secondary_axis_comboBox.addItem("")
        self.secondary_axis_comboBox.addItem("")
        self.secondary_axis_comboBox.setObjectName(u"secondary_axis_comboBox")

        self.gridLayout.addWidget(self.secondary_axis_comboBox, 2, 1, 1, 1)

        self.joint_index_comboBox = QComboBox(self.groupBox_4)
        self.joint_index_comboBox.setObjectName(u"joint_index_comboBox")

        self.gridLayout.addWidget(self.joint_index_comboBox, 0, 1, 1, 1)

        self.label_6 = QLabel(self.groupBox_4)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_4, 1, 0, 1, 1)


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

        self.index_label.setText(QCoreApplication.translate("Form", u"Component Index", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Parent Ref Index", None))
        self.jointSettings_groupBox.setTitle(QCoreApplication.translate("Form", u"Joint Settings", None))
        self.joint_names_label.setText(QCoreApplication.translate("Form", u"Joint Names", None))
        self.joint_names_pushButton.setText(QCoreApplication.translate("Form", u"Configure", None))
        self.joint_rig_checkBox.setText("")
        self.label_5.setText(QCoreApplication.translate("Form", u"Create Joint", None))
        self.groupBox_4.setTitle("")
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
        self.primary_axis_comboBox.setItemText(0, QCoreApplication.translate("Form", u"x", None))
        self.primary_axis_comboBox.setItemText(1, QCoreApplication.translate("Form", u"y", None))
        self.primary_axis_comboBox.setItemText(2, QCoreApplication.translate("Form", u"z", None))
        self.primary_axis_comboBox.setItemText(3, QCoreApplication.translate("Form", u"-x", None))
        self.primary_axis_comboBox.setItemText(4, QCoreApplication.translate("Form", u"-y", None))
        self.primary_axis_comboBox.setItemText(5, QCoreApplication.translate("Form", u"-z", None))

        self.label_4.setText(QCoreApplication.translate("Form", u"Secondary Axis", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Primary Axis", None))
        self.secondary_axis_comboBox.setItemText(0, QCoreApplication.translate("Form", u"x", None))
        self.secondary_axis_comboBox.setItemText(1, QCoreApplication.translate("Form", u"y", None))
        self.secondary_axis_comboBox.setItemText(2, QCoreApplication.translate("Form", u"z", None))
        self.secondary_axis_comboBox.setItemText(3, QCoreApplication.translate("Form", u"-x", None))
        self.secondary_axis_comboBox.setItemText(4, QCoreApplication.translate("Form", u"-y", None))
        self.secondary_axis_comboBox.setItemText(5, QCoreApplication.translate("Form", u"-z", None))

        self.secondary_axis_comboBox.setCurrentText(QCoreApplication.translate("Form", u"x", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Index", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Channels Host Settings", None))
        self.host_label.setText(QCoreApplication.translate("Form", u"Host:", None))
        self.host_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
    # retranslateUi

