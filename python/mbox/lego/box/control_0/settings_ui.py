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
        Form.resize(283, 482)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.joint_checkBox = QCheckBox(self.groupBox)
        self.joint_checkBox.setObjectName(u"joint_checkBox")

        self.verticalLayout_4.addWidget(self.joint_checkBox)

        self.leafJoint_checkBox = QCheckBox(self.groupBox)
        self.leafJoint_checkBox.setObjectName(u"leafJoint_checkBox")
        self.leafJoint_checkBox.setEnabled(False)

        self.verticalLayout_4.addWidget(self.leafJoint_checkBox)

        self.uniScale_checkBox = QCheckBox(self.groupBox)
        self.uniScale_checkBox.setObjectName(u"uniScale_checkBox")

        self.verticalLayout_4.addWidget(self.uniScale_checkBox)

        self.neutralRotation_checkBox = QCheckBox(self.groupBox)
        self.neutralRotation_checkBox.setObjectName(u"neutralRotation_checkBox")

        self.verticalLayout_4.addWidget(self.neutralRotation_checkBox)

        self.mirrorBehaviour_checkBox = QCheckBox(self.groupBox)
        self.mirrorBehaviour_checkBox.setObjectName(u"mirrorBehaviour_checkBox")

        self.verticalLayout_4.addWidget(self.mirrorBehaviour_checkBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.ctlSize_label = QLabel(self.groupBox)
        self.ctlSize_label.setObjectName(u"ctlSize_label")

        self.horizontalLayout_3.addWidget(self.ctlSize_label)

        self.ctlSize_doubleSpinBox = QDoubleSpinBox(self.groupBox)
        self.ctlSize_doubleSpinBox.setObjectName(u"ctlSize_doubleSpinBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ctlSize_doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.ctlSize_doubleSpinBox.setSizePolicy(sizePolicy)
        self.ctlSize_doubleSpinBox.setWrapping(False)
        self.ctlSize_doubleSpinBox.setAlignment(Qt.AlignCenter)
        self.ctlSize_doubleSpinBox.setButtonSymbols(QAbstractSpinBox.PlusMinus)
        self.ctlSize_doubleSpinBox.setMinimum(0.010000000000000)
        self.ctlSize_doubleSpinBox.setMaximum(20000.000000000000000)
        self.ctlSize_doubleSpinBox.setValue(1.000000000000000)

        self.horizontalLayout_3.addWidget(self.ctlSize_doubleSpinBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.controlShape_label = QLabel(self.groupBox)
        self.controlShape_label.setObjectName(u"controlShape_label")
        self.controlShape_label.setText(u"Control Shape")

        self.horizontalLayout_2.addWidget(self.controlShape_label)

        self.controlShape_comboBox = QComboBox(self.groupBox)
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.addItem("")
        self.controlShape_comboBox.setObjectName(u"controlShape_comboBox")
        sizePolicy.setHeightForWidth(self.controlShape_comboBox.sizePolicy().hasHeightForWidth())
        self.controlShape_comboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.controlShape_comboBox)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.keyable_groupBox = QGroupBox(Form)
        self.keyable_groupBox.setObjectName(u"keyable_groupBox")
        self.gridLayout_4 = QGridLayout(self.keyable_groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.translate_pushButton = QPushButton(self.keyable_groupBox)
        self.translate_pushButton.setObjectName(u"translate_pushButton")

        self.verticalLayout.addWidget(self.translate_pushButton)

        self.tx_checkBox = QCheckBox(self.keyable_groupBox)
        self.tx_checkBox.setObjectName(u"tx_checkBox")

        self.verticalLayout.addWidget(self.tx_checkBox)

        self.ty_checkBox = QCheckBox(self.keyable_groupBox)
        self.ty_checkBox.setObjectName(u"ty_checkBox")

        self.verticalLayout.addWidget(self.ty_checkBox)

        self.tz_checkBox = QCheckBox(self.keyable_groupBox)
        self.tz_checkBox.setObjectName(u"tz_checkBox")

        self.verticalLayout.addWidget(self.tz_checkBox)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetMinimumSize)
        self.rotate_pushButton = QPushButton(self.keyable_groupBox)
        self.rotate_pushButton.setObjectName(u"rotate_pushButton")

        self.verticalLayout_2.addWidget(self.rotate_pushButton)

        self.rx_checkBox = QCheckBox(self.keyable_groupBox)
        self.rx_checkBox.setObjectName(u"rx_checkBox")

        self.verticalLayout_2.addWidget(self.rx_checkBox)

        self.ry_checkBox = QCheckBox(self.keyable_groupBox)
        self.ry_checkBox.setObjectName(u"ry_checkBox")

        self.verticalLayout_2.addWidget(self.ry_checkBox)

        self.rz_checkBox = QCheckBox(self.keyable_groupBox)
        self.rz_checkBox.setObjectName(u"rz_checkBox")

        self.verticalLayout_2.addWidget(self.rz_checkBox)

        self.ro_checkBox = QCheckBox(self.keyable_groupBox)
        self.ro_checkBox.setObjectName(u"ro_checkBox")

        self.verticalLayout_2.addWidget(self.ro_checkBox)

        self.ro_comboBox = QComboBox(self.keyable_groupBox)
        self.ro_comboBox.addItem("")
        self.ro_comboBox.addItem("")
        self.ro_comboBox.addItem("")
        self.ro_comboBox.addItem("")
        self.ro_comboBox.addItem("")
        self.ro_comboBox.addItem("")
        self.ro_comboBox.setObjectName(u"ro_comboBox")

        self.verticalLayout_2.addWidget(self.ro_comboBox)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.scale_pushButton = QPushButton(self.keyable_groupBox)
        self.scale_pushButton.setObjectName(u"scale_pushButton")

        self.verticalLayout_3.addWidget(self.scale_pushButton)

        self.sx_checkBox = QCheckBox(self.keyable_groupBox)
        self.sx_checkBox.setObjectName(u"sx_checkBox")

        self.verticalLayout_3.addWidget(self.sx_checkBox)

        self.sy_checkBox = QCheckBox(self.keyable_groupBox)
        self.sy_checkBox.setObjectName(u"sy_checkBox")

        self.verticalLayout_3.addWidget(self.sy_checkBox)

        self.sz_checkBox = QCheckBox(self.keyable_groupBox)
        self.sz_checkBox.setObjectName(u"sz_checkBox")

        self.verticalLayout_3.addWidget(self.sz_checkBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_3)


        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.keyable_groupBox, 1, 0, 1, 1)

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


        self.gridLayout.addWidget(self.ikRefArray_groupBox, 2, 0, 1, 1)


        self.retranslateUi(Form)
        self.translate_pushButton.clicked.connect(self.tx_checkBox.toggle)
        self.translate_pushButton.clicked.connect(self.ty_checkBox.toggle)
        self.translate_pushButton.clicked.connect(self.tz_checkBox.toggle)
        self.rotate_pushButton.clicked.connect(self.rx_checkBox.toggle)
        self.rotate_pushButton.clicked.connect(self.ry_checkBox.toggle)
        self.rotate_pushButton.clicked.connect(self.rz_checkBox.toggle)
        self.rotate_pushButton.clicked.connect(self.ro_checkBox.toggle)
        self.scale_pushButton.clicked.connect(self.sx_checkBox.toggle)
        self.scale_pushButton.clicked.connect(self.sy_checkBox.toggle)
        self.scale_pushButton.clicked.connect(self.sz_checkBox.toggle)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.joint_checkBox.setText(QCoreApplication.translate("Form", u"Joint", None))
#if QT_CONFIG(tooltip)
        self.leafJoint_checkBox.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>When &quot;<span style=\" font-weight:600;\">is Leaf Joint</span>&quot; is checked, the component will create only the joint without the controls</p><p>As the name indicates this option is meant to create leaf joints, but you can use it also to create &quot;branches&quot;</p><p>Leaf joint can be used as a deformation helpers or/and games pipelines</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.leafJoint_checkBox.setText(QCoreApplication.translate("Form", u"is Leaf Joint (Beta)", None))
        self.uniScale_checkBox.setText(QCoreApplication.translate("Form", u"Uniform Scale", None))
#if QT_CONFIG(tooltip)
        self.neutralRotation_checkBox.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>If is active, it will align the control with world space</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.neutralRotation_checkBox.setText(QCoreApplication.translate("Form", u"World Space Orientation Align", None))
#if QT_CONFIG(tooltip)
        self.mirrorBehaviour_checkBox.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>If is active, the control will have symmetrical behaviour on Left and Right side.</p><p><br/></p><p>WARNING: There is a bug in Maya 2018 and 2018.1 that will result in an incorrect behaviour, because this option will negate one of the axis. Other Maya version should be ok.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.mirrorBehaviour_checkBox.setText(QCoreApplication.translate("Form", u"Mirror Behaviour L and R", None))
        self.ctlSize_label.setText(QCoreApplication.translate("Form", u"Ctl Size", None))
        self.controlShape_comboBox.setItemText(0, QCoreApplication.translate("Form", u"Arrow", None))
        self.controlShape_comboBox.setItemText(1, QCoreApplication.translate("Form", u"Circle", None))
        self.controlShape_comboBox.setItemText(2, QCoreApplication.translate("Form", u"Compas", None))
        self.controlShape_comboBox.setItemText(3, QCoreApplication.translate("Form", u"Cross", None))
        self.controlShape_comboBox.setItemText(4, QCoreApplication.translate("Form", u"Crossarrow", None))
        self.controlShape_comboBox.setItemText(5, QCoreApplication.translate("Form", u"Cube", None))
        self.controlShape_comboBox.setItemText(6, QCoreApplication.translate("Form", u"Cubewithpeak", None))
        self.controlShape_comboBox.setItemText(7, QCoreApplication.translate("Form", u"Cylinder", None))
        self.controlShape_comboBox.setItemText(8, QCoreApplication.translate("Form", u"Diamond", None))
        self.controlShape_comboBox.setItemText(9, QCoreApplication.translate("Form", u"Flower", None))
        self.controlShape_comboBox.setItemText(10, QCoreApplication.translate("Form", u"Null", None))
        self.controlShape_comboBox.setItemText(11, QCoreApplication.translate("Form", u"Pyramid", None))
        self.controlShape_comboBox.setItemText(12, QCoreApplication.translate("Form", u"Sphere", None))
        self.controlShape_comboBox.setItemText(13, QCoreApplication.translate("Form", u"Square", None))

        self.keyable_groupBox.setTitle(QCoreApplication.translate("Form", u"Keyable", None))
        self.translate_pushButton.setText(QCoreApplication.translate("Form", u"Translate", None))
        self.tx_checkBox.setText(QCoreApplication.translate("Form", u"tx", None))
        self.ty_checkBox.setText(QCoreApplication.translate("Form", u"ty", None))
        self.tz_checkBox.setText(QCoreApplication.translate("Form", u"tz", None))
        self.rotate_pushButton.setText(QCoreApplication.translate("Form", u"Rotate", None))
        self.rx_checkBox.setText(QCoreApplication.translate("Form", u"rx", None))
        self.ry_checkBox.setText(QCoreApplication.translate("Form", u"ry", None))
        self.rz_checkBox.setText(QCoreApplication.translate("Form", u"rz", None))
        self.ro_checkBox.setText(QCoreApplication.translate("Form", u"ro", None))
        self.ro_comboBox.setItemText(0, QCoreApplication.translate("Form", u"XYZ", None))
        self.ro_comboBox.setItemText(1, QCoreApplication.translate("Form", u"YZX", None))
        self.ro_comboBox.setItemText(2, QCoreApplication.translate("Form", u"ZXY", None))
        self.ro_comboBox.setItemText(3, QCoreApplication.translate("Form", u"XZY", None))
        self.ro_comboBox.setItemText(4, QCoreApplication.translate("Form", u"YXZ", None))
        self.ro_comboBox.setItemText(5, QCoreApplication.translate("Form", u"ZYX", None))

        self.scale_pushButton.setText(QCoreApplication.translate("Form", u"Scale", None))
        self.sx_checkBox.setText(QCoreApplication.translate("Form", u"sx", None))
        self.sy_checkBox.setText(QCoreApplication.translate("Form", u"sy", None))
        self.sz_checkBox.setText(QCoreApplication.translate("Form", u"sz", None))
        self.ikRefArray_groupBox.setTitle(QCoreApplication.translate("Form", u"IK Reference Array", None))
        self.ikRefArrayAdd_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
        self.ikRefArrayRemove_pushButton.setText(QCoreApplication.translate("Form", u">>", None))
    # retranslateUi

