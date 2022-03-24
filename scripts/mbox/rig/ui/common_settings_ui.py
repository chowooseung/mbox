# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'common_settings_ui.ui'
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
        Form.resize(512, 533)
        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 50, 133, 22))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.layoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.spinBox_2 = QSpinBox(self.layoutWidget)
        self.spinBox_2.setObjectName(u"spinBox_2")

        self.horizontalLayout_4.addWidget(self.spinBox_2)

        self.spinBox_3 = QSpinBox(self.layoutWidget)
        self.spinBox_3.setObjectName(u"spinBox_3")

        self.horizontalLayout_4.addWidget(self.spinBox_3)

        self.checkBox_14 = QCheckBox(Form)
        self.checkBox_14.setObjectName(u"checkBox_14")
        self.checkBox_14.setGeometry(QRect(280, 130, 201, 31))
        self.checkBox_13 = QCheckBox(Form)
        self.checkBox_13.setObjectName(u"checkBox_13")
        self.checkBox_13.setGeometry(QRect(280, 100, 201, 31))
        self.checkBox_12 = QCheckBox(Form)
        self.checkBox_12.setObjectName(u"checkBox_12")
        self.checkBox_12.setGeometry(QRect(280, 70, 201, 31))
        self.layoutWidget_2 = QWidget(Form)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(20, 10, 211, 24))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.horizontalSlider = QSlider(self.layoutWidget_2)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.horizontalSlider)

        self.spinBox_5 = QSpinBox(self.layoutWidget_2)
        self.spinBox_5.setObjectName(u"spinBox_5")

        self.horizontalLayout_3.addWidget(self.spinBox_5)

        self.checkBox_11 = QCheckBox(Form)
        self.checkBox_11.setObjectName(u"checkBox_11")
        self.checkBox_11.setGeometry(QRect(280, 40, 201, 31))
        self.layoutWidget_3 = QWidget(Form)
        self.layoutWidget_3.setObjectName(u"layoutWidget_3")
        self.layoutWidget_3.setGeometry(QRect(260, 250, 214, 152))
        self.formLayout = QFormLayout(self.layoutWidget_3)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label_4 = QLabel(self.layoutWidget_3)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.comboBox_2 = QComboBox(self.layoutWidget_3)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox_2)

        self.label_5 = QLabel(self.layoutWidget_3)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.spinBox = QSpinBox(self.layoutWidget_3)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setLayoutDirection(Qt.LeftToRight)
        self.spinBox.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinBox.setMinimum(1)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.spinBox)

        self.label_6 = QLabel(self.layoutWidget_3)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_6)

        self.comboBox_3 = QComboBox(self.layoutWidget_3)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBox_3)

        self.label_7 = QLabel(self.layoutWidget_3)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_7)

        self.spinBox_4 = QSpinBox(self.layoutWidget_3)
        self.spinBox_4.setObjectName(u"spinBox_4")
        self.spinBox_4.setLayoutDirection(Qt.LeftToRight)
        self.spinBox_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinBox_4.setMinimum(1)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.spinBox_4)

        self.label_8 = QLabel(self.layoutWidget_3)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_8)

        self.label_9 = QLabel(self.layoutWidget_3)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_9)

        self.spinBox_6 = QSpinBox(self.layoutWidget_3)
        self.spinBox_6.setObjectName(u"spinBox_6")
        self.spinBox_6.setLayoutDirection(Qt.LeftToRight)
        self.spinBox_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinBox_6.setMinimum(1)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.spinBox_6)

        self.spinBox_7 = QSpinBox(self.layoutWidget_3)
        self.spinBox_7.setObjectName(u"spinBox_7")
        self.spinBox_7.setLayoutDirection(Qt.LeftToRight)
        self.spinBox_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.spinBox_7.setMinimum(1)

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.spinBox_7)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(-10, 230, 251, 181))
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.pushButton_3 = QPushButton(self.groupBox_2)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout_4.addWidget(self.pushButton_3)

        self.checkBox = QCheckBox(self.groupBox_2)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setChecked(True)

        self.verticalLayout_4.addWidget(self.checkBox)

        self.checkBox_2 = QCheckBox(self.groupBox_2)
        self.checkBox_2.setObjectName(u"checkBox_2")
        self.checkBox_2.setChecked(True)

        self.verticalLayout_4.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.groupBox_2)
        self.checkBox_3.setObjectName(u"checkBox_3")
        self.checkBox_3.setChecked(True)

        self.verticalLayout_4.addWidget(self.checkBox_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_4)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.pushButton_4 = QPushButton(self.groupBox_2)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.verticalLayout_2.addWidget(self.pushButton_4)

        self.checkBox_4 = QCheckBox(self.groupBox_2)
        self.checkBox_4.setObjectName(u"checkBox_4")
        self.checkBox_4.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_4)

        self.checkBox_6 = QCheckBox(self.groupBox_2)
        self.checkBox_6.setObjectName(u"checkBox_6")
        self.checkBox_6.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_6)

        self.checkBox_5 = QCheckBox(self.groupBox_2)
        self.checkBox_5.setObjectName(u"checkBox_5")
        self.checkBox_5.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_5)

        self.checkBox_10 = QCheckBox(self.groupBox_2)
        self.checkBox_10.setObjectName(u"checkBox_10")
        self.checkBox_10.setChecked(True)

        self.verticalLayout_2.addWidget(self.checkBox_10)

        self.comboBox = QComboBox(self.groupBox_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_2.addWidget(self.comboBox)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.pushButton_5 = QPushButton(self.groupBox_2)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.verticalLayout_3.addWidget(self.pushButton_5)

        self.checkBox_9 = QCheckBox(self.groupBox_2)
        self.checkBox_9.setObjectName(u"checkBox_9")
        self.checkBox_9.setChecked(True)

        self.verticalLayout_3.addWidget(self.checkBox_9)

        self.checkBox_8 = QCheckBox(self.groupBox_2)
        self.checkBox_8.setObjectName(u"checkBox_8")
        self.checkBox_8.setChecked(True)

        self.verticalLayout_3.addWidget(self.checkBox_8)

        self.checkBox_7 = QCheckBox(self.groupBox_2)
        self.checkBox_7.setObjectName(u"checkBox_7")
        self.checkBox_7.setChecked(True)

        self.verticalLayout_3.addWidget(self.checkBox_7)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(-10, 420, 281, 171))
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.listWidget = QListWidget(self.groupBox)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout_5.addWidget(self.listWidget)

        self.pushButton_6 = QPushButton(self.groupBox)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.verticalLayout_5.addWidget(self.pushButton_6)


        self.horizontalLayout.addLayout(self.verticalLayout_5)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Divisions", None))
        self.checkBox_14.setText(QCoreApplication.translate("Form", u"Joint", None))
        self.checkBox_13.setText(QCoreApplication.translate("Form", u"Leaf Joint", None))
        self.checkBox_12.setText(QCoreApplication.translate("Form", u"World Orient Axis", None))
        self.label.setText(QCoreApplication.translate("Form", u"IK/FK Blend", None))
        self.checkBox_11.setText(QCoreApplication.translate("Form", u"Mirror Behaviour R Side", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Connector", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Ctl Size", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Ctl Shape", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Jnt Numbers", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"FK Ctl Numbers", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"IK Ctl Numbers", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Keyable", None))
        self.pushButton_3.setText(QCoreApplication.translate("Form", u"Translate", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"tx", None))
        self.checkBox_2.setText(QCoreApplication.translate("Form", u"ty", None))
        self.checkBox_3.setText(QCoreApplication.translate("Form", u"tz", None))
        self.pushButton_4.setText(QCoreApplication.translate("Form", u"Rotate", None))
        self.checkBox_4.setText(QCoreApplication.translate("Form", u"rx", None))
        self.checkBox_6.setText(QCoreApplication.translate("Form", u"ry", None))
        self.checkBox_5.setText(QCoreApplication.translate("Form", u"rz", None))
        self.checkBox_10.setText(QCoreApplication.translate("Form", u"ro", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"XYZ", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"\uc0c8 \ud56d\ubaa9", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Form", u"\uc0c8 \ud56d\ubaa9", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Form", u"\uc0c8 \ud56d\ubaa9", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Form", u"\uc0c8 \ud56d\ubaa9", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Form", u"\uc0c8 \ud56d\ubaa9", None))

        self.pushButton_5.setText(QCoreApplication.translate("Form", u"Scale", None))
        self.checkBox_9.setText(QCoreApplication.translate("Form", u"sx", None))
        self.checkBox_8.setText(QCoreApplication.translate("Form", u"sy", None))
        self.checkBox_7.setText(QCoreApplication.translate("Form", u"sz", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Cns Array", None))
        self.pushButton_6.setText(QCoreApplication.translate("Form", u"Copy", None))
        self.pushButton_2.setText(QCoreApplication.translate("Form", u"<<", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u">>", None))
    # retranslateUi

