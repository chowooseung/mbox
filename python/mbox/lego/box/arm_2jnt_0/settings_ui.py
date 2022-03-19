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
        Form.resize(280, 768)
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
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.ikfk_label = QLabel(self.groupBox)
        self.ikfk_label.setObjectName(u"ikfk_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.ikfk_label)

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


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.maxStretch_label = QLabel(self.groupBox)
        self.maxStretch_label.setObjectName(u"maxStretch_label")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maxStretch_label.sizePolicy().hasHeightForWidth())
        self.maxStretch_label.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.maxStretch_label)

        self.maxStretch_spinBox = QDoubleSpinBox(self.groupBox)
        self.maxStretch_spinBox.setObjectName(u"maxStretch_spinBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.maxStretch_spinBox.sizePolicy().hasHeightForWidth())
        self.maxStretch_spinBox.setSizePolicy(sizePolicy1)
        self.maxStretch_spinBox.setMinimum(1.000000000000000)
        self.maxStretch_spinBox.setValue(1.500000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.maxStretch_spinBox)

        self.maxStretch_label_2 = QLabel(self.groupBox)
        self.maxStretch_label_2.setObjectName(u"maxStretch_label_2")
        sizePolicy.setHeightForWidth(self.maxStretch_label_2.sizePolicy().hasHeightForWidth())
        self.maxStretch_label_2.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.maxStretch_label_2)

        self.elbowThickness_spinBox = QDoubleSpinBox(self.groupBox)
        self.elbowThickness_spinBox.setObjectName(u"elbowThickness_spinBox")
        sizePolicy1.setHeightForWidth(self.elbowThickness_spinBox.sizePolicy().hasHeightForWidth())
        self.elbowThickness_spinBox.setSizePolicy(sizePolicy1)
        self.elbowThickness_spinBox.setDecimals(3)
        self.elbowThickness_spinBox.setMinimum(0.000000000000000)
        self.elbowThickness_spinBox.setMaximum(1.000000000000000)
        self.elbowThickness_spinBox.setSingleStep(0.100000000000000)
        self.elbowThickness_spinBox.setValue(0.000000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.elbowThickness_spinBox)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.divisions_label = QLabel(self.groupBox)
        self.divisions_label.setObjectName(u"divisions_label")

        self.horizontalLayout.addWidget(self.divisions_label)

        self.div_spinBox = QSpinBox(self.groupBox)
        self.div_spinBox.setObjectName(u"div_spinBox")
        self.div_spinBox.setMinimum(0)
        self.div_spinBox.setValue(2)

        self.horizontalLayout.addWidget(self.div_spinBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.ikTR_checkBox = QCheckBox(self.groupBox)
        self.ikTR_checkBox.setObjectName(u"ikTR_checkBox")

        self.verticalLayout.addWidget(self.ikTR_checkBox)

        self.mirrorIK_checkBox = QCheckBox(self.groupBox)
        self.mirrorIK_checkBox.setObjectName(u"mirrorIK_checkBox")

        self.verticalLayout.addWidget(self.mirrorIK_checkBox)

        self.mirrorMid_checkBox = QCheckBox(self.groupBox)
        self.mirrorMid_checkBox.setObjectName(u"mirrorMid_checkBox")

        self.verticalLayout.addWidget(self.mirrorMid_checkBox)

        self.extraTweak_checkBox = QCheckBox(self.groupBox)
        self.extraTweak_checkBox.setObjectName(u"extraTweak_checkBox")

        self.verticalLayout.addWidget(self.extraTweak_checkBox)

        self.supportJoints_checkBox = QCheckBox(self.groupBox)
        self.supportJoints_checkBox.setObjectName(u"supportJoints_checkBox")
        self.supportJoints_checkBox.setChecked(True)

        self.verticalLayout.addWidget(self.supportJoints_checkBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.squashStretchProfile_pushButton = QPushButton(self.groupBox)
        self.squashStretchProfile_pushButton.setObjectName(u"squashStretchProfile_pushButton")

        self.horizontalLayout_2.addWidget(self.squashStretchProfile_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


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

        self.ikRefArray_copyRef_pushButton = QPushButton(self.ikRefArray_groupBox)
        self.ikRefArray_copyRef_pushButton.setObjectName(u"ikRefArray_copyRef_pushButton")

        self.ikRefArray_verticalLayout_1.addWidget(self.ikRefArray_copyRef_pushButton)


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

        self.upvRefArray_groupBox = QGroupBox(Form)
        self.upvRefArray_groupBox.setObjectName(u"upvRefArray_groupBox")
        self.gridLayout_5 = QGridLayout(self.upvRefArray_groupBox)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.upvRefArray_horizontalLayout = QHBoxLayout()
        self.upvRefArray_horizontalLayout.setObjectName(u"upvRefArray_horizontalLayout")
        self.upvRefArray_verticalLayout_1 = QVBoxLayout()
        self.upvRefArray_verticalLayout_1.setObjectName(u"upvRefArray_verticalLayout_1")
        self.upvRefArray_listWidget = QListWidget(self.upvRefArray_groupBox)
        self.upvRefArray_listWidget.setObjectName(u"upvRefArray_listWidget")
        self.upvRefArray_listWidget.setDragDropOverwriteMode(True)
        self.upvRefArray_listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.upvRefArray_listWidget.setDefaultDropAction(Qt.MoveAction)
        self.upvRefArray_listWidget.setAlternatingRowColors(True)
        self.upvRefArray_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.upvRefArray_listWidget.setSelectionRectVisible(False)

        self.upvRefArray_verticalLayout_1.addWidget(self.upvRefArray_listWidget)

        self.upvRefArray_copyRef_pushButton = QPushButton(self.upvRefArray_groupBox)
        self.upvRefArray_copyRef_pushButton.setObjectName(u"upvRefArray_copyRef_pushButton")

        self.upvRefArray_verticalLayout_1.addWidget(self.upvRefArray_copyRef_pushButton)


        self.upvRefArray_horizontalLayout.addLayout(self.upvRefArray_verticalLayout_1)

        self.upvRefArray_verticalLayout_2 = QVBoxLayout()
        self.upvRefArray_verticalLayout_2.setObjectName(u"upvRefArray_verticalLayout_2")
        self.upvRefArrayAdd_pushButton = QPushButton(self.upvRefArray_groupBox)
        self.upvRefArrayAdd_pushButton.setObjectName(u"upvRefArrayAdd_pushButton")

        self.upvRefArray_verticalLayout_2.addWidget(self.upvRefArrayAdd_pushButton)

        self.upvRefArrayRemove_pushButton = QPushButton(self.upvRefArray_groupBox)
        self.upvRefArrayRemove_pushButton.setObjectName(u"upvRefArrayRemove_pushButton")

        self.upvRefArray_verticalLayout_2.addWidget(self.upvRefArrayRemove_pushButton)

        self.upvRefArray_verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.upvRefArray_verticalLayout_2.addItem(self.upvRefArray_verticalSpacer)


        self.upvRefArray_horizontalLayout.addLayout(self.upvRefArray_verticalLayout_2)


        self.gridLayout_5.addLayout(self.upvRefArray_horizontalLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.upvRefArray_groupBox, 2, 0, 1, 1)

        self.pinRefArray_groupBox = QGroupBox(Form)
        self.pinRefArray_groupBox.setObjectName(u"pinRefArray_groupBox")
        self.gridLayout_4 = QGridLayout(self.pinRefArray_groupBox)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.pinRefArray_horizontalLayout = QHBoxLayout()
        self.pinRefArray_horizontalLayout.setObjectName(u"pinRefArray_horizontalLayout")
        self.pinRefArray_verticalLayout = QVBoxLayout()
        self.pinRefArray_verticalLayout.setObjectName(u"pinRefArray_verticalLayout")
        self.pinRefArray_listWidget = QListWidget(self.pinRefArray_groupBox)
        self.pinRefArray_listWidget.setObjectName(u"pinRefArray_listWidget")
        self.pinRefArray_listWidget.setDragDropOverwriteMode(True)
        self.pinRefArray_listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.pinRefArray_listWidget.setDefaultDropAction(Qt.MoveAction)
        self.pinRefArray_listWidget.setAlternatingRowColors(True)
        self.pinRefArray_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.pinRefArray_listWidget.setSelectionRectVisible(False)

        self.pinRefArray_verticalLayout.addWidget(self.pinRefArray_listWidget)

        self.pinRefArray_copyRef_pushButton = QPushButton(self.pinRefArray_groupBox)
        self.pinRefArray_copyRef_pushButton.setObjectName(u"pinRefArray_copyRef_pushButton")

        self.pinRefArray_verticalLayout.addWidget(self.pinRefArray_copyRef_pushButton)


        self.pinRefArray_horizontalLayout.addLayout(self.pinRefArray_verticalLayout)

        self.pinRefArray_verticalLayout_2 = QVBoxLayout()
        self.pinRefArray_verticalLayout_2.setObjectName(u"pinRefArray_verticalLayout_2")
        self.pinRefArrayAdd_pushButton = QPushButton(self.pinRefArray_groupBox)
        self.pinRefArrayAdd_pushButton.setObjectName(u"pinRefArrayAdd_pushButton")

        self.pinRefArray_verticalLayout_2.addWidget(self.pinRefArrayAdd_pushButton)

        self.pinRefArrayRemove_pushButton = QPushButton(self.pinRefArray_groupBox)
        self.pinRefArrayRemove_pushButton.setObjectName(u"pinRefArrayRemove_pushButton")

        self.pinRefArray_verticalLayout_2.addWidget(self.pinRefArrayRemove_pushButton)

        self.pinRefArray_verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.pinRefArray_verticalLayout_2.addItem(self.pinRefArray_verticalSpacer)


        self.pinRefArray_horizontalLayout.addLayout(self.pinRefArray_verticalLayout_2)


        self.gridLayout_4.addLayout(self.pinRefArray_horizontalLayout, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.pinRefArray_groupBox, 3, 0, 1, 1)


        self.retranslateUi(Form)
        self.ikfk_slider.sliderMoved.connect(self.ikfk_spinBox.setValue)
        self.ikfk_spinBox.valueChanged.connect(self.ikfk_slider.setValue)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle("")
        self.ikfk_label.setText(QCoreApplication.translate("Form", u"FK/IK Blend", None))
        self.maxStretch_label.setText(QCoreApplication.translate("Form", u"Max Stretch", None))
        self.maxStretch_label_2.setText(QCoreApplication.translate("Form", u"Elbow Thickness", None))
        self.divisions_label.setText(QCoreApplication.translate("Form", u"Divisions", None))
        self.ikTR_checkBox.setText(QCoreApplication.translate("Form", u"IK separated Trans and Rot ctl", None))
#if QT_CONFIG(tooltip)
        self.mirrorIK_checkBox.setToolTip(QCoreApplication.translate("Form", u"This option set the axis of the mid CTL (elbow) and the up vector control to move in a mirror behaviour ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.mirrorIK_checkBox.setStatusTip(QCoreApplication.translate("Form", u"This option set the axis of the mid CTL (elbow) and the up vector control to move in a mirror behaviour ", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.mirrorIK_checkBox.setWhatsThis(QCoreApplication.translate("Form", u"This option set the axis of the mid CTL (elbow) and the up vector control to move in a mirror behaviour ", None))
#endif // QT_CONFIG(whatsthis)
        self.mirrorIK_checkBox.setText(QCoreApplication.translate("Form", u"Mirror IK Ctl  axis behaviour", None))
#if QT_CONFIG(tooltip)
        self.mirrorMid_checkBox.setToolTip(QCoreApplication.translate("Form", u"This option set the axis of the mid CTL (elbow) and the up vector control to move in a mirror behaviour ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.mirrorMid_checkBox.setStatusTip(QCoreApplication.translate("Form", u"This option set the axis of the mid CTL (elbow) and the up vector control to move in a mirror behaviour ", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.mirrorMid_checkBox.setWhatsThis(QCoreApplication.translate("Form", u"This option set the axis of the mid CTL (elbow) and the up vector control to move in a mirror behaviour ", None))
#endif // QT_CONFIG(whatsthis)
        self.mirrorMid_checkBox.setText(QCoreApplication.translate("Form", u"MirrorMid Ctl and UPV  axis behaviour", None))
#if QT_CONFIG(tooltip)
        self.extraTweak_checkBox.setToolTip(QCoreApplication.translate("Form", u"This option set the axis of the mid CTL (elbow) and the up vector control to move in a mirror behaviour ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.extraTweak_checkBox.setStatusTip(QCoreApplication.translate("Form", u"This option set the axis of the mid CTL (elbow) and the up vector control to move in a mirror behaviour ", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.extraTweak_checkBox.setWhatsThis(QCoreApplication.translate("Form", u"This option set the axis of the mid CTL (elbow) and the up vector control to move in a mirror behaviour ", None))
#endif // QT_CONFIG(whatsthis)
        self.extraTweak_checkBox.setText(QCoreApplication.translate("Form", u"Add Extra Tweak Ctl", None))
#if QT_CONFIG(tooltip)
        self.supportJoints_checkBox.setToolTip(QCoreApplication.translate("Form", u"This option set the axis of the mid CTL (elbow) and the up vector control to move in a mirror behaviour ", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.supportJoints_checkBox.setStatusTip(QCoreApplication.translate("Form", u"This option set the axis of the mid CTL (elbow) and the up vector control to move in a mirror behaviour ", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.supportJoints_checkBox.setWhatsThis(QCoreApplication.translate("Form", u"This option set the axis of the mid CTL (elbow) and the up vector control to move in a mirror behaviour ", None))
#endif // QT_CONFIG(whatsthis)
        self.supportJoints_checkBox.setText(QCoreApplication.translate("Form", u"Support Elbow Joints", None))
        self.squashStretchProfile_pushButton.setText(QCoreApplication.translate("Form", u"Squash and Stretch Profile", None))
        self.ikRefArray_groupBox.setTitle(QCoreApplication.translate("Form", u"IK Reference Array", None))
        self.ikRefArray_copyRef_pushButton.setText(QCoreApplication.translate("Form", u"Copy from UpV Ref", None))
        self.ikRefArrayAdd_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
        self.ikRefArrayRemove_pushButton.setText(QCoreApplication.translate("Form", u">>", None))
        self.upvRefArray_groupBox.setTitle(QCoreApplication.translate("Form", u"UpV Reference Array", None))
        self.upvRefArray_copyRef_pushButton.setText(QCoreApplication.translate("Form", u"Copy from IK Ref", None))
        self.upvRefArrayAdd_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
        self.upvRefArrayRemove_pushButton.setText(QCoreApplication.translate("Form", u">>", None))
        self.pinRefArray_groupBox.setTitle(QCoreApplication.translate("Form", u"Pin Elbow Reference Array", None))
        self.pinRefArray_copyRef_pushButton.setText(QCoreApplication.translate("Form", u"Copy from IK Ref", None))
        self.pinRefArrayAdd_pushButton.setText(QCoreApplication.translate("Form", u"<<", None))
        self.pinRefArrayRemove_pushButton.setText(QCoreApplication.translate("Form", u">>", None))
    # retranslateUi

