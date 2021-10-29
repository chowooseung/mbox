# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rootcustomstepui.ui'
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
        Form.resize(336, 336)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.customStep_checkBox = QCheckBox(self.groupBox)
        self.customStep_checkBox.setObjectName(u"customStep_checkBox")

        self.verticalLayout.addWidget(self.customStep_checkBox)

        self.search_lineEdit = QLineEdit(self.groupBox)
        self.search_lineEdit.setObjectName(u"search_lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_lineEdit.sizePolicy().hasHeightForWidth())
        self.search_lineEdit.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.search_lineEdit)

        self.preCustomStep_horizontalLayout = QHBoxLayout()
        self.preCustomStep_horizontalLayout.setObjectName(u"preCustomStep_horizontalLayout")
        self.customStep_verticalLayout_1 = QVBoxLayout()
        self.customStep_verticalLayout_1.setObjectName(u"customStep_verticalLayout_1")
        self.customStep_listWidget = QListWidget(self.groupBox)
        self.customStep_listWidget.setObjectName(u"customStep_listWidget")
        self.customStep_listWidget.setDragDropOverwriteMode(True)
        self.customStep_listWidget.setDragDropMode(QAbstractItemView.InternalMove)
        self.customStep_listWidget.setDefaultDropAction(Qt.MoveAction)
        self.customStep_listWidget.setAlternatingRowColors(True)
        self.customStep_listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.customStep_listWidget.setProperty("isWrapping", False)
        self.customStep_listWidget.setViewMode(QListView.ListMode)

        self.customStep_verticalLayout_1.addWidget(self.customStep_listWidget)


        self.preCustomStep_horizontalLayout.addLayout(self.customStep_verticalLayout_1)

        self.preCustomStep_verticalLayout_2 = QVBoxLayout()
        self.preCustomStep_verticalLayout_2.setObjectName(u"preCustomStep_verticalLayout_2")
        self.customStepAdd_pushButton = QPushButton(self.groupBox)
        self.customStepAdd_pushButton.setObjectName(u"customStepAdd_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.customStepAdd_pushButton)

        self.customStepNew_pushButton = QPushButton(self.groupBox)
        self.customStepNew_pushButton.setObjectName(u"customStepNew_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.customStepNew_pushButton)

        self.customStepDuplicate_pushButton = QPushButton(self.groupBox)
        self.customStepDuplicate_pushButton.setObjectName(u"customStepDuplicate_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.customStepDuplicate_pushButton)

        self.customStepRemove_pushButton = QPushButton(self.groupBox)
        self.customStepRemove_pushButton.setObjectName(u"customStepRemove_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.customStepRemove_pushButton)

        self.customStepRun_pushButton = QPushButton(self.groupBox)
        self.customStepRun_pushButton.setObjectName(u"customStepRun_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.customStepRun_pushButton)

        self.customStepEdit_pushButton = QPushButton(self.groupBox)
        self.customStepEdit_pushButton.setObjectName(u"customStepEdit_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.customStepEdit_pushButton)

        self.customStepExport_pushButton = QPushButton(self.groupBox)
        self.customStepExport_pushButton.setObjectName(u"customStepExport_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.customStepExport_pushButton)

        self.customStepImport_pushButton = QPushButton(self.groupBox)
        self.customStepImport_pushButton.setObjectName(u"customStepImport_pushButton")

        self.preCustomStep_verticalLayout_2.addWidget(self.customStepImport_pushButton)

        self.customStep_verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.preCustomStep_verticalLayout_2.addItem(self.customStep_verticalSpacer)


        self.preCustomStep_horizontalLayout.addLayout(self.preCustomStep_verticalLayout_2)


        self.verticalLayout.addLayout(self.preCustomStep_horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_3.addWidget(self.groupBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Custom Steps", None))
        self.customStep_checkBox.setText(QCoreApplication.translate("Form", u"Custom Step", None))
        self.customStepAdd_pushButton.setText(QCoreApplication.translate("Form", u"Add", None))
        self.customStepNew_pushButton.setText(QCoreApplication.translate("Form", u"New", None))
        self.customStepDuplicate_pushButton.setText(QCoreApplication.translate("Form", u"Duplicate", None))
        self.customStepRemove_pushButton.setText(QCoreApplication.translate("Form", u"Remove", None))
        self.customStepRun_pushButton.setText(QCoreApplication.translate("Form", u"Run Sel.", None))
        self.customStepEdit_pushButton.setText(QCoreApplication.translate("Form", u"Edit", None))
        self.customStepExport_pushButton.setText(QCoreApplication.translate("Form", u"Export", None))
        self.customStepImport_pushButton.setText(QCoreApplication.translate("Form", u"Import", None))
    # retranslateUi

