# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rootui.ui'
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
        Form.resize(448, 376)
        self.gridLayout_2 = QGridLayout(Form)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.groupBox_7 = QGroupBox(Form)
        self.groupBox_7.setObjectName(u"groupBox_7")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy)
        self.horizontalLayout_9 = QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.world_control_checkBox = QCheckBox(self.groupBox_7)
        self.world_control_checkBox.setObjectName(u"world_control_checkBox")

        self.horizontalLayout_9.addWidget(self.world_control_checkBox)

        self.world_control_lineEdit = QLineEdit(self.groupBox_7)
        self.world_control_lineEdit.setObjectName(u"world_control_lineEdit")

        self.horizontalLayout_9.addWidget(self.world_control_lineEdit)


        self.gridLayout_2.addWidget(self.groupBox_7, 1, 0, 1, 1)

        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.gridLayout_5 = QGridLayout(self.groupBox_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.force_uniScale_checkBox = QCheckBox(self.groupBox_3)
        self.force_uniScale_checkBox.setObjectName(u"force_uniScale_checkBox")

        self.gridLayout_5.addWidget(self.force_uniScale_checkBox, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_3, 2, 0, 1, 1)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_3 = QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.rigName_label = QLabel(self.groupBox)
        self.rigName_label.setObjectName(u"rigName_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.rigName_label)

        self.name_lineEdit = QLineEdit(self.groupBox)
        self.name_lineEdit.setObjectName(u"name_lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.name_lineEdit)

        self.mode_label = QLabel(self.groupBox)
        self.mode_label.setObjectName(u"mode_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.mode_label)

        self.process_comboBox = QComboBox(self.groupBox)
        self.process_comboBox.addItem("")
        self.process_comboBox.addItem("")
        self.process_comboBox.setObjectName(u"process_comboBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.process_comboBox)

        self.step_label = QLabel(self.groupBox)
        self.step_label.setObjectName(u"step_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.step_label)

        self.step_comboBox = QComboBox(self.groupBox)
        self.step_comboBox.addItem("")
        self.step_comboBox.addItem("")
        self.step_comboBox.addItem("")
        self.step_comboBox.addItem("")
        self.step_comboBox.addItem("")
        self.step_comboBox.setObjectName(u"step_comboBox")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.step_comboBox)


        self.gridLayout_3.addLayout(self.formLayout, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_5 = QGroupBox(Form)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_7 = QGridLayout(self.groupBox_5)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.useRGB_checkBox = QCheckBox(self.groupBox_5)
        self.useRGB_checkBox.setObjectName(u"useRGB_checkBox")

        self.gridLayout_7.addWidget(self.useRGB_checkBox, 1, 0, 1, 1)

        self.gridLayout_9 = QGridLayout()
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.label_3 = QLabel(self.groupBox_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.label_3, 0, 2, 1, 1)

        self.label_2 = QLabel(self.groupBox_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.label_2, 0, 1, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.fk_label_2 = QLabel(self.groupBox_5)
        self.fk_label_2.setObjectName(u"fk_label_2")

        self.gridLayout.addWidget(self.fk_label_2, 0, 0, 1, 1)

        self.C_color_fk_label = QLabel(self.groupBox_5)
        self.C_color_fk_label.setObjectName(u"C_color_fk_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.C_color_fk_label.sizePolicy().hasHeightForWidth())
        self.C_color_fk_label.setSizePolicy(sizePolicy1)
        self.C_color_fk_label.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.C_color_fk_label, 0, 1, 1, 1)

        self.C_color_fk_spinBox = QSpinBox(self.groupBox_5)
        self.C_color_fk_spinBox.setObjectName(u"C_color_fk_spinBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.C_color_fk_spinBox.sizePolicy().hasHeightForWidth())
        self.C_color_fk_spinBox.setSizePolicy(sizePolicy2)
        self.C_color_fk_spinBox.setMaximum(31)

        self.gridLayout.addWidget(self.C_color_fk_spinBox, 0, 2, 1, 1)

        self.C_RGB_fk_pushButton = QPushButton(self.groupBox_5)
        self.C_RGB_fk_pushButton.setObjectName(u"C_RGB_fk_pushButton")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.C_RGB_fk_pushButton.sizePolicy().hasHeightForWidth())
        self.C_RGB_fk_pushButton.setSizePolicy(sizePolicy3)
        self.C_RGB_fk_pushButton.setMaximumSize(QSize(16777215, 16777215))
        self.C_RGB_fk_pushButton.setLayoutDirection(Qt.LeftToRight)
        self.C_RGB_fk_pushButton.setStyleSheet(u"")

        self.gridLayout.addWidget(self.C_RGB_fk_pushButton, 0, 3, 1, 1)

        self.C_RGB_fk_slider = QSlider(self.groupBox_5)
        self.C_RGB_fk_slider.setObjectName(u"C_RGB_fk_slider")
        self.C_RGB_fk_slider.setMaximum(255)
        self.C_RGB_fk_slider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.C_RGB_fk_slider, 0, 4, 1, 1)

        self.ik_label_2 = QLabel(self.groupBox_5)
        self.ik_label_2.setObjectName(u"ik_label_2")

        self.gridLayout.addWidget(self.ik_label_2, 1, 0, 1, 1)

        self.C_color_ik_label = QLabel(self.groupBox_5)
        self.C_color_ik_label.setObjectName(u"C_color_ik_label")
        sizePolicy1.setHeightForWidth(self.C_color_ik_label.sizePolicy().hasHeightForWidth())
        self.C_color_ik_label.setSizePolicy(sizePolicy1)
        self.C_color_ik_label.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.C_color_ik_label, 1, 1, 1, 1)

        self.C_color_ik_spinBox = QSpinBox(self.groupBox_5)
        self.C_color_ik_spinBox.setObjectName(u"C_color_ik_spinBox")
        sizePolicy2.setHeightForWidth(self.C_color_ik_spinBox.sizePolicy().hasHeightForWidth())
        self.C_color_ik_spinBox.setSizePolicy(sizePolicy2)
        self.C_color_ik_spinBox.setMaximum(31)

        self.gridLayout.addWidget(self.C_color_ik_spinBox, 1, 2, 1, 1)

        self.C_RGB_ik_pushButton = QPushButton(self.groupBox_5)
        self.C_RGB_ik_pushButton.setObjectName(u"C_RGB_ik_pushButton")
        sizePolicy3.setHeightForWidth(self.C_RGB_ik_pushButton.sizePolicy().hasHeightForWidth())
        self.C_RGB_ik_pushButton.setSizePolicy(sizePolicy3)
        self.C_RGB_ik_pushButton.setMaximumSize(QSize(16777215, 16777215))
        self.C_RGB_ik_pushButton.setLayoutDirection(Qt.LeftToRight)
        self.C_RGB_ik_pushButton.setStyleSheet(u"")

        self.gridLayout.addWidget(self.C_RGB_ik_pushButton, 1, 3, 1, 1)

        self.C_RGB_ik_slider = QSlider(self.groupBox_5)
        self.C_RGB_ik_slider.setObjectName(u"C_RGB_ik_slider")
        self.C_RGB_ik_slider.setMaximum(255)
        self.C_RGB_ik_slider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.C_RGB_ik_slider, 1, 4, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout, 1, 1, 1, 1)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.fk_label_3 = QLabel(self.groupBox_5)
        self.fk_label_3.setObjectName(u"fk_label_3")

        self.gridLayout_10.addWidget(self.fk_label_3, 0, 0, 1, 1)

        self.R_color_fk_label = QLabel(self.groupBox_5)
        self.R_color_fk_label.setObjectName(u"R_color_fk_label")
        sizePolicy1.setHeightForWidth(self.R_color_fk_label.sizePolicy().hasHeightForWidth())
        self.R_color_fk_label.setSizePolicy(sizePolicy1)
        self.R_color_fk_label.setMinimumSize(QSize(0, 0))

        self.gridLayout_10.addWidget(self.R_color_fk_label, 0, 1, 1, 1)

        self.R_color_fk_spinBox = QSpinBox(self.groupBox_5)
        self.R_color_fk_spinBox.setObjectName(u"R_color_fk_spinBox")
        sizePolicy2.setHeightForWidth(self.R_color_fk_spinBox.sizePolicy().hasHeightForWidth())
        self.R_color_fk_spinBox.setSizePolicy(sizePolicy2)
        self.R_color_fk_spinBox.setMaximum(31)

        self.gridLayout_10.addWidget(self.R_color_fk_spinBox, 0, 2, 1, 1)

        self.R_RGB_fk_pushButton = QPushButton(self.groupBox_5)
        self.R_RGB_fk_pushButton.setObjectName(u"R_RGB_fk_pushButton")
        sizePolicy3.setHeightForWidth(self.R_RGB_fk_pushButton.sizePolicy().hasHeightForWidth())
        self.R_RGB_fk_pushButton.setSizePolicy(sizePolicy3)
        self.R_RGB_fk_pushButton.setMaximumSize(QSize(16777215, 16777215))
        self.R_RGB_fk_pushButton.setLayoutDirection(Qt.LeftToRight)
        self.R_RGB_fk_pushButton.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.R_RGB_fk_pushButton, 0, 3, 1, 1)

        self.R_RGB_fk_slider = QSlider(self.groupBox_5)
        self.R_RGB_fk_slider.setObjectName(u"R_RGB_fk_slider")
        self.R_RGB_fk_slider.setMaximum(255)
        self.R_RGB_fk_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_10.addWidget(self.R_RGB_fk_slider, 0, 4, 1, 1)

        self.ik_label_3 = QLabel(self.groupBox_5)
        self.ik_label_3.setObjectName(u"ik_label_3")

        self.gridLayout_10.addWidget(self.ik_label_3, 1, 0, 1, 1)

        self.R_color_ik_label = QLabel(self.groupBox_5)
        self.R_color_ik_label.setObjectName(u"R_color_ik_label")
        sizePolicy1.setHeightForWidth(self.R_color_ik_label.sizePolicy().hasHeightForWidth())
        self.R_color_ik_label.setSizePolicy(sizePolicy1)
        self.R_color_ik_label.setMinimumSize(QSize(0, 0))

        self.gridLayout_10.addWidget(self.R_color_ik_label, 1, 1, 1, 1)

        self.R_color_ik_spinBox = QSpinBox(self.groupBox_5)
        self.R_color_ik_spinBox.setObjectName(u"R_color_ik_spinBox")
        sizePolicy2.setHeightForWidth(self.R_color_ik_spinBox.sizePolicy().hasHeightForWidth())
        self.R_color_ik_spinBox.setSizePolicy(sizePolicy2)
        self.R_color_ik_spinBox.setMaximum(31)

        self.gridLayout_10.addWidget(self.R_color_ik_spinBox, 1, 2, 1, 1)

        self.R_RGB_ik_pushButton = QPushButton(self.groupBox_5)
        self.R_RGB_ik_pushButton.setObjectName(u"R_RGB_ik_pushButton")
        self.R_RGB_ik_pushButton.setEnabled(True)
        sizePolicy3.setHeightForWidth(self.R_RGB_ik_pushButton.sizePolicy().hasHeightForWidth())
        self.R_RGB_ik_pushButton.setSizePolicy(sizePolicy3)
        self.R_RGB_ik_pushButton.setMaximumSize(QSize(16777215, 16777215))
        self.R_RGB_ik_pushButton.setLayoutDirection(Qt.LeftToRight)
        self.R_RGB_ik_pushButton.setStyleSheet(u"")

        self.gridLayout_10.addWidget(self.R_RGB_ik_pushButton, 1, 3, 1, 1)

        self.R_RGB_ik_slider = QSlider(self.groupBox_5)
        self.R_RGB_ik_slider.setObjectName(u"R_RGB_ik_slider")
        self.R_RGB_ik_slider.setMaximum(255)
        self.R_RGB_ik_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_10.addWidget(self.R_RGB_ik_slider, 1, 4, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_10, 1, 2, 1, 1)

        self.label = QLabel(self.groupBox_5)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout_9.addWidget(self.label, 0, 0, 1, 1)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.fk_label = QLabel(self.groupBox_5)
        self.fk_label.setObjectName(u"fk_label")

        self.gridLayout_11.addWidget(self.fk_label, 0, 0, 1, 1)

        self.L_color_fk_label = QLabel(self.groupBox_5)
        self.L_color_fk_label.setObjectName(u"L_color_fk_label")
        sizePolicy1.setHeightForWidth(self.L_color_fk_label.sizePolicy().hasHeightForWidth())
        self.L_color_fk_label.setSizePolicy(sizePolicy1)
        self.L_color_fk_label.setMinimumSize(QSize(0, 0))

        self.gridLayout_11.addWidget(self.L_color_fk_label, 0, 1, 1, 1)

        self.L_color_fk_spinBox = QSpinBox(self.groupBox_5)
        self.L_color_fk_spinBox.setObjectName(u"L_color_fk_spinBox")
        sizePolicy2.setHeightForWidth(self.L_color_fk_spinBox.sizePolicy().hasHeightForWidth())
        self.L_color_fk_spinBox.setSizePolicy(sizePolicy2)
        self.L_color_fk_spinBox.setMaximum(31)

        self.gridLayout_11.addWidget(self.L_color_fk_spinBox, 0, 2, 1, 1)

        self.L_RGB_fk_pushButton = QPushButton(self.groupBox_5)
        self.L_RGB_fk_pushButton.setObjectName(u"L_RGB_fk_pushButton")
        sizePolicy3.setHeightForWidth(self.L_RGB_fk_pushButton.sizePolicy().hasHeightForWidth())
        self.L_RGB_fk_pushButton.setSizePolicy(sizePolicy3)
        self.L_RGB_fk_pushButton.setMaximumSize(QSize(16777215, 16777215))
        self.L_RGB_fk_pushButton.setLayoutDirection(Qt.LeftToRight)
        self.L_RGB_fk_pushButton.setStyleSheet(u"")

        self.gridLayout_11.addWidget(self.L_RGB_fk_pushButton, 0, 3, 1, 1)

        self.L_RGB_fk_slider = QSlider(self.groupBox_5)
        self.L_RGB_fk_slider.setObjectName(u"L_RGB_fk_slider")
        self.L_RGB_fk_slider.setMaximum(255)
        self.L_RGB_fk_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_11.addWidget(self.L_RGB_fk_slider, 0, 4, 1, 1)

        self.ik_label = QLabel(self.groupBox_5)
        self.ik_label.setObjectName(u"ik_label")

        self.gridLayout_11.addWidget(self.ik_label, 1, 0, 1, 1)

        self.L_color_ik_label = QLabel(self.groupBox_5)
        self.L_color_ik_label.setObjectName(u"L_color_ik_label")
        sizePolicy1.setHeightForWidth(self.L_color_ik_label.sizePolicy().hasHeightForWidth())
        self.L_color_ik_label.setSizePolicy(sizePolicy1)
        self.L_color_ik_label.setMinimumSize(QSize(0, 0))

        self.gridLayout_11.addWidget(self.L_color_ik_label, 1, 1, 1, 1)

        self.L_color_ik_spinBox = QSpinBox(self.groupBox_5)
        self.L_color_ik_spinBox.setObjectName(u"L_color_ik_spinBox")
        sizePolicy2.setHeightForWidth(self.L_color_ik_spinBox.sizePolicy().hasHeightForWidth())
        self.L_color_ik_spinBox.setSizePolicy(sizePolicy2)
        self.L_color_ik_spinBox.setMaximum(31)

        self.gridLayout_11.addWidget(self.L_color_ik_spinBox, 1, 2, 1, 1)

        self.L_RGB_ik_pushButton = QPushButton(self.groupBox_5)
        self.L_RGB_ik_pushButton.setObjectName(u"L_RGB_ik_pushButton")
        sizePolicy3.setHeightForWidth(self.L_RGB_ik_pushButton.sizePolicy().hasHeightForWidth())
        self.L_RGB_ik_pushButton.setSizePolicy(sizePolicy3)
        self.L_RGB_ik_pushButton.setMaximumSize(QSize(16777215, 16777215))
        self.L_RGB_ik_pushButton.setLayoutDirection(Qt.LeftToRight)
        self.L_RGB_ik_pushButton.setStyleSheet(u"")

        self.gridLayout_11.addWidget(self.L_RGB_ik_pushButton, 1, 3, 1, 1)

        self.L_RGB_ik_slider = QSlider(self.groupBox_5)
        self.L_RGB_ik_slider.setObjectName(u"L_RGB_ik_slider")
        self.L_RGB_ik_slider.setMaximum(255)
        self.L_RGB_ik_slider.setOrientation(Qt.Horizontal)

        self.gridLayout_11.addWidget(self.L_RGB_ik_slider, 1, 4, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_11, 1, 0, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_9, 0, 0, 1, 1)


        self.gridLayout_2.addWidget(self.groupBox_5, 3, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 4, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("Form", u"Base Rig Control", None))
#if QT_CONFIG(tooltip)
        self.world_control_checkBox.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Shifter creates by default a Base control called &quot;<span style=\" font-weight:600;\">global_C0_ctl</span>&quot;. </p><p>Since this control is not accesible from any guide locator. Is not possible to add it as a space reference.</p><p>If this option is active, The base control will be named &quot;<span style=\" font-weight:600;\">world_ctl</span>&quot; and we can add &quot;<span style=\" font-weight:600;\">global_C0_ctl</span>&quot; as a regular &quot;Control_01&quot; component. </p><p>This way we can use it as space reference.</p><p>The biped guide template is configured with this structure.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.world_control_checkBox.setText(QCoreApplication.translate("Form", u"Use World Ctl or Custom Name", None))
        self.world_control_lineEdit.setText(QCoreApplication.translate("Form", u"world_con", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"Joint Settings", None))
        self.force_uniScale_checkBox.setText(QCoreApplication.translate("Form", u"Force uniform scaling in all joints by connection all axis to Z axis", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Rig Settings", None))
        self.rigName_label.setText(QCoreApplication.translate("Form", u"Name", None))
        self.mode_label.setText(QCoreApplication.translate("Form", u"Process", None))
        self.process_comboBox.setItemText(0, QCoreApplication.translate("Form", u"PUB", None))
        self.process_comboBox.setItemText(1, QCoreApplication.translate("Form", u"WIP", None))

        self.step_label.setText(QCoreApplication.translate("Form", u"Build Steps:", None))
        self.step_comboBox.setItemText(0, QCoreApplication.translate("Form", u"all", None))
        self.step_comboBox.setItemText(1, QCoreApplication.translate("Form", u"prepare", None))
        self.step_comboBox.setItemText(2, QCoreApplication.translate("Form", u"objects", None))
        self.step_comboBox.setItemText(3, QCoreApplication.translate("Form", u"attributes", None))
        self.step_comboBox.setItemText(4, QCoreApplication.translate("Form", u"operate", None))

        self.groupBox_5.setTitle(QCoreApplication.translate("Form", u"Color Settings", None))
        self.useRGB_checkBox.setText(QCoreApplication.translate("Form", u"Use RBG Colors", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Right", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Center", None))
        self.fk_label_2.setText(QCoreApplication.translate("Form", u"FK", None))
        self.C_color_fk_label.setText("")
        self.C_RGB_fk_pushButton.setText("")
        self.ik_label_2.setText(QCoreApplication.translate("Form", u"IK", None))
        self.C_color_ik_label.setText("")
        self.C_RGB_ik_pushButton.setText("")
        self.fk_label_3.setText(QCoreApplication.translate("Form", u"FK", None))
        self.R_color_fk_label.setText("")
        self.R_RGB_fk_pushButton.setText("")
        self.ik_label_3.setText(QCoreApplication.translate("Form", u"IK", None))
        self.R_color_ik_label.setText("")
        self.R_RGB_ik_pushButton.setText("")
        self.label.setText(QCoreApplication.translate("Form", u"Left", None))
        self.fk_label.setText(QCoreApplication.translate("Form", u"FK", None))
        self.L_color_fk_label.setText("")
        self.L_RGB_fk_pushButton.setText("")
        self.ik_label.setText(QCoreApplication.translate("Form", u"IK", None))
        self.L_color_ik_label.setText("")
        self.L_RGB_ik_pushButton.setText("")
    # retranslateUi

