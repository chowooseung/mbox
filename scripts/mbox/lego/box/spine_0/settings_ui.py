# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings_ui.ui'
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
        Form.resize(255, 290)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.mode_label = QLabel(self.groupBox)
        self.mode_label.setObjectName(u"mode_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.mode_label)

        self.mode_comboBox = QComboBox(self.groupBox)
        self.mode_comboBox.addItem("")
        self.mode_comboBox.addItem("")
        self.mode_comboBox.addItem("")
        self.mode_comboBox.setObjectName(u"mode_comboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mode_comboBox.sizePolicy().hasHeightForWidth())
        self.mode_comboBox.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.mode_comboBox)

        self.ikfk_label = QLabel(self.groupBox)
        self.ikfk_label.setObjectName(u"ikfk_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.ikfk_label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.ikfk_slider = QSlider(self.groupBox)
        self.ikfk_slider.setObjectName(u"ikfk_slider")
        self.ikfk_slider.setMinimumSize(QSize(0, 15))
        self.ikfk_slider.setMaximum(100)
        self.ikfk_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.ikfk_slider)

        self.ikfk_spinBox = QSpinBox(self.groupBox)
        self.ikfk_spinBox.setObjectName(u"ikfk_spinBox")
        self.ikfk_spinBox.setMaximum(100)

        self.horizontalLayout_3.addWidget(self.ikfk_spinBox)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_3)


        self.verticalLayout.addLayout(self.formLayout)

        self.neutralPose_checkBox = QCheckBox(self.groupBox)
        self.neutralPose_checkBox.setObjectName(u"neutralPose_checkBox")

        self.verticalLayout.addWidget(self.neutralPose_checkBox)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.ikRefArray_groupBox = QGroupBox(Form)
        self.ikRefArray_groupBox.setObjectName(u"ikRefArray_groupBox")
        self.gridLayout_3 = QGridLayout(self.ikRefArray_groupBox)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.ikRefArray_horizontalLayout = QHBoxLayout()
        self.ikRefArray_horizontalLayout.setObjectName(u"ikRefArray_horizontalLayout")
        self.ikRefArray_verticalLayout_1 = QVBoxLayout()
        self.ikRefArray_verticalLayout_1.setObjectName(u"ikRefArray_verticalLayout_1")
        self.ikRefArray_listWidget = QListWidget(self.ikRefArray_groupBox)
        self.ikRefArray_listWidget.setObjectName(u"ikRefArray_listWidget")
        self.ikRefArray_listWidget.setDragDropOverwriteMode(True)
        self.ikRefArray_listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.ikRefArray_listWidget.setDefaultDropAction(Qt.MoveAction)
        self.ikRefArray_listWidget.setAlternatingRowColors(True)
        self.ikRefArray_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ikRefArray_listWidget.setSelectionRectVisible(False)

        self.ikRefArray_verticalLayout_1.addWidget(self.ikRefArray_listWidget)


        self.ikRefArray_horizontalLayout.addLayout(self.ikRefArray_verticalLayout_1)

        self.ikRefArray_verticalLayout_2 = QVBoxLayout()
        self.ikRefArray_verticalLayout_2.setObjectName(u"ikRefArray_verticalLayout_2")
        self.ikRefArrayAdd_pushButton = QPushButton(self.ikRefArray_groupBox)
        self.ikRefArrayAdd_pushButton.setObjectName(u"ikRefArrayAdd_pushButton")

        self.ikRefArray_verticalLayout_2.addWidget(self.ikRefArrayAdd_pushButton)

        self.ikRefArrayRemove_pushButton = QPushButton(self.ikRefArray_groupBox)
        self.ikRefArrayRemove_pushButton.setObjectName(u"ikRefArrayRemove_pushButton")

        self.ikRefArray_verticalLayout_2.addWidget(self.ikRefArrayRemove_pushButton)

        self.ikRefArray_verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.ikRefArray_verticalLayout_2.addItem(self.ikRefArray_verticalSpacer)


        self.ikRefArray_horizontalLayout.addLayout(self.ikRefArray_verticalLayout_2)


        self.gridLayout_3.addLayout(self.ikRefArray_horizontalLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.ikRefArray_groupBox, 1, 0, 1, 1)


        self.retranslateUi(Form)
        self.ikfk_slider.sliderMoved.connect(self.ikfk_spinBox.setValue)
        self.ikfk_spinBox.valueChanged.connect(self.ikfk_slider.setValue)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.mode_label.setText(QCoreApplication.translate("Form", u"Mode:", None))
        self.mode_comboBox.setItemText(0, QCoreApplication.translate("Form", u"FK", None))
        self.mode_comboBox.setItemText(1, QCoreApplication.translate("Form", u"IK", None))
        self.mode_comboBox.setItemText(2, QCoreApplication.translate("Form", u"FK/IK", None))

        self.ikfk_label.setText(QCoreApplication.translate("Form", u"IK/FK Blend:", None))
        self.neutralPose_checkBox.setText(QCoreApplication.translate("Form", u"Nuetral pose", None))
        self.ikRefArray_groupBox.setTitle(QCoreApplication.translate("Form", u"IK Reference Array", None))
        self.ikRefArrayAdd_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
        self.ikRefArrayRemove_pushButton.setText(QCoreApplication.translate("Form", u">>", None))
    # retranslateUi

