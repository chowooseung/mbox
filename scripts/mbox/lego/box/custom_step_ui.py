# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'custom_step_ui.ui'
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
        Form.resize(312, 655)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.preCustomStep_checkBox = QCheckBox(self.groupBox)
        self.preCustomStep_checkBox.setObjectName(u"preCustomStep_checkBox")

        self.verticalLayout.addWidget(self.preCustomStep_checkBox)

        self.preSearch_lineEdit = QLineEdit(self.groupBox)
        self.preSearch_lineEdit.setObjectName(u"preSearch_lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.preSearch_lineEdit.sizePolicy().hasHeightForWidth())
        self.preSearch_lineEdit.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.preSearch_lineEdit)

        self.preCustomStep_horizontalLayout = QHBoxLayout()
        self.preCustomStep_horizontalLayout.setObjectName(u"preCustomStep_horizontalLayout")
        self.preCustomStep_verticalLayout_1 = QVBoxLayout()
        self.preCustomStep_verticalLayout_1.setObjectName(u"preCustomStep_verticalLayout_1")
        self.preCustomStep_listWidget = QListWidget(self.groupBox)
        self.preCustomStep_listWidget.setObjectName(u"preCustomStep_listWidget")
        self.preCustomStep_listWidget.setDragDropOverwriteMode(True)
        self.preCustomStep_listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.preCustomStep_listWidget.setDefaultDropAction(Qt.MoveAction)
        self.preCustomStep_listWidget.setAlternatingRowColors(True)
        self.preCustomStep_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.preCustomStep_listWidget.setProperty("isWrapping", False)
        self.preCustomStep_listWidget.setViewMode(QListView.ListMode)

        self.preCustomStep_verticalLayout_1.addWidget(self.preCustomStep_listWidget)


        self.preCustomStep_horizontalLayout.addLayout(self.preCustomStep_verticalLayout_1)

        self.preCustomStep_verticalLayout_2 = QVBoxLayout()
        self.preCustomStep_verticalLayout_2.setObjectName(u"preCustomStep_verticalLayout_2")
        self.preCustomStepAdd_pushButton = QPushButton(self.groupBox)
        self.preCustomStepAdd_pushButton.setObjectName(u"preCustomStepAdd_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.preCustomStepAdd_pushButton)

        self.preCustomStepNew_pushButton = QPushButton(self.groupBox)
        self.preCustomStepNew_pushButton.setObjectName(u"preCustomStepNew_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.preCustomStepNew_pushButton)

        self.preCustomStepDuplicate_pushButton = QPushButton(self.groupBox)
        self.preCustomStepDuplicate_pushButton.setObjectName(u"preCustomStepDuplicate_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.preCustomStepDuplicate_pushButton)

        self.preCustomStepRemove_pushButton = QPushButton(self.groupBox)
        self.preCustomStepRemove_pushButton.setObjectName(u"preCustomStepRemove_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.preCustomStepRemove_pushButton)

        self.preCustomStepRun_pushButton = QPushButton(self.groupBox)
        self.preCustomStepRun_pushButton.setObjectName(u"preCustomStepRun_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.preCustomStepRun_pushButton)

        self.preCustomStepEdit_pushButton = QPushButton(self.groupBox)
        self.preCustomStepEdit_pushButton.setObjectName(u"preCustomStepEdit_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.preCustomStepEdit_pushButton)

        self.preCustomStepExport_pushButton = QPushButton(self.groupBox)
        self.preCustomStepExport_pushButton.setObjectName(u"preCustomStepExport_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.preCustomStepExport_pushButton)

        self.preCustomStepImport_pushButton = QPushButton(self.groupBox)
        self.preCustomStepImport_pushButton.setObjectName(u"preCustomStepImport_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.preCustomStepImport_pushButton)

        self.preCustomStep_verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.preCustomStep_verticalLayout_2.addItem(self.preCustomStep_verticalSpacer)


        self.preCustomStep_horizontalLayout.addLayout(self.preCustomStep_verticalLayout_2)


        self.verticalLayout.addLayout(self.preCustomStep_horizontalLayout)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName(u"line")
        self.line.setLineWidth(3)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.postCustomStep_checkBox = QCheckBox(self.groupBox)
        self.postCustomStep_checkBox.setObjectName(u"postCustomStep_checkBox")

        self.verticalLayout_2.addWidget(self.postCustomStep_checkBox)

        self.postSearch_lineEdit = QLineEdit(self.groupBox)
        self.postSearch_lineEdit.setObjectName(u"postSearch_lineEdit")
        sizePolicy.setHeightForWidth(self.postSearch_lineEdit.sizePolicy().hasHeightForWidth())
        self.postSearch_lineEdit.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.postSearch_lineEdit)

        self.preCustomStep_horizontalLayout_2 = QHBoxLayout()
        self.preCustomStep_horizontalLayout_2.setObjectName(u"preCustomStep_horizontalLayout_2")
        self.preCustomStep_verticalLayout_3 = QVBoxLayout()
        self.preCustomStep_verticalLayout_3.setObjectName(u"preCustomStep_verticalLayout_3")
        self.postCustomStep_listWidget = QListWidget(self.groupBox)
        self.postCustomStep_listWidget.setObjectName(u"postCustomStep_listWidget")
        self.postCustomStep_listWidget.setDragDropOverwriteMode(True)
        self.postCustomStep_listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.postCustomStep_listWidget.setDefaultDropAction(Qt.MoveAction)
        self.postCustomStep_listWidget.setAlternatingRowColors(True)
        self.postCustomStep_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.postCustomStep_listWidget.setViewMode(QListView.ListMode)
        self.postCustomStep_listWidget.setWordWrap(False)
        self.postCustomStep_listWidget.setSelectionRectVisible(False)

        self.preCustomStep_verticalLayout_3.addWidget(self.postCustomStep_listWidget)


        self.preCustomStep_horizontalLayout_2.addLayout(self.preCustomStep_verticalLayout_3)

        self.preCustomStep_verticalLayout_4 = QVBoxLayout()
        self.preCustomStep_verticalLayout_4.setObjectName(u"preCustomStep_verticalLayout_4")
        self.postCustomStepAdd_pushButton = QPushButton(self.groupBox)
        self.postCustomStepAdd_pushButton.setObjectName(u"postCustomStepAdd_pushButton")

        self.preCustomStep_verticalLayout_4.addWidget(self.postCustomStepAdd_pushButton)

        self.postCustomStepNew_pushButton = QPushButton(self.groupBox)
        self.postCustomStepNew_pushButton.setObjectName(u"postCustomStepNew_pushButton")

        self.preCustomStep_verticalLayout_4.addWidget(self.postCustomStepNew_pushButton)

        self.postCustomStepDuplicate_pushButton = QPushButton(self.groupBox)
        self.postCustomStepDuplicate_pushButton.setObjectName(u"postCustomStepDuplicate_pushButton")

        self.preCustomStep_verticalLayout_4.addWidget(self.postCustomStepDuplicate_pushButton)

        self.postCustomStepRemove_pushButton = QPushButton(self.groupBox)
        self.postCustomStepRemove_pushButton.setObjectName(u"postCustomStepRemove_pushButton")

        self.preCustomStep_verticalLayout_4.addWidget(self.postCustomStepRemove_pushButton)

        self.postCustomStepRun_pushButton = QPushButton(self.groupBox)
        self.postCustomStepRun_pushButton.setObjectName(u"postCustomStepRun_pushButton")

        self.preCustomStep_verticalLayout_4.addWidget(self.postCustomStepRun_pushButton)

        self.postCustomStepEdit_pushButton = QPushButton(self.groupBox)
        self.postCustomStepEdit_pushButton.setObjectName(u"postCustomStepEdit_pushButton")

        self.preCustomStep_verticalLayout_4.addWidget(self.postCustomStepEdit_pushButton)

        self.postCustomStepExport_pushButton = QPushButton(self.groupBox)
        self.postCustomStepExport_pushButton.setObjectName(u"postCustomStepExport_pushButton")

        self.preCustomStep_verticalLayout_4.addWidget(self.postCustomStepExport_pushButton)

        self.postCustomStepImport_pushButton = QPushButton(self.groupBox)
        self.postCustomStepImport_pushButton.setObjectName(u"postCustomStepImport_pushButton")

        self.preCustomStep_verticalLayout_4.addWidget(self.postCustomStepImport_pushButton)

        self.preCustomStep_verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.preCustomStep_verticalLayout_4.addItem(self.preCustomStep_verticalSpacer_2)


        self.preCustomStep_horizontalLayout_2.addLayout(self.preCustomStep_verticalLayout_4)


        self.verticalLayout_2.addLayout(self.preCustomStep_horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Custom Steps", None))
        self.preCustomStep_checkBox.setText(QCoreApplication.translate("Form", u"Pre Custom Step", None))
        self.preCustomStepAdd_pushButton.setText(QCoreApplication.translate("Form", u"Add", None))
        self.preCustomStepNew_pushButton.setText(QCoreApplication.translate("Form", u"New", None))
        self.preCustomStepDuplicate_pushButton.setText(QCoreApplication.translate("Form", u"Duplicate", None))
        self.preCustomStepRemove_pushButton.setText(QCoreApplication.translate("Form", u"Remove", None))
        self.preCustomStepRun_pushButton.setText(QCoreApplication.translate("Form", u"Run Sel.", None))
        self.preCustomStepEdit_pushButton.setText(QCoreApplication.translate("Form", u"Edit", None))
        self.preCustomStepExport_pushButton.setText(QCoreApplication.translate("Form", u"Export", None))
        self.preCustomStepImport_pushButton.setText(QCoreApplication.translate("Form", u"Import", None))
        self.postCustomStep_checkBox.setText(QCoreApplication.translate("Form", u"Post  Custom Step", None))
        self.postCustomStepAdd_pushButton.setText(QCoreApplication.translate("Form", u"Add", None))
        self.postCustomStepNew_pushButton.setText(QCoreApplication.translate("Form", u"New", None))
        self.postCustomStepDuplicate_pushButton.setText(QCoreApplication.translate("Form", u"Duplicate", None))
        self.postCustomStepRemove_pushButton.setText(QCoreApplication.translate("Form", u"Remove", None))
        self.postCustomStepRun_pushButton.setText(QCoreApplication.translate("Form", u"Run Sel.", None))
        self.postCustomStepEdit_pushButton.setText(QCoreApplication.translate("Form", u"Edit", None))
        self.postCustomStepExport_pushButton.setText(QCoreApplication.translate("Form", u"Export", None))
        self.postCustomStepImport_pushButton.setText(QCoreApplication.translate("Form", u"Import", None))
    # retranslateUi

