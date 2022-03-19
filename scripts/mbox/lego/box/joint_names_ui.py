# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'joint_names_ui.ui'
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
        Form.resize(403, 299)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.jointNamesList = QTableWidget(Form)
        if (self.jointNamesList.columnCount() < 1):
            self.jointNamesList.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        self.jointNamesList.setHorizontalHeaderItem(0, __qtablewidgetitem)
        self.jointNamesList.setObjectName(u"jointNamesList")
        self.jointNamesList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.jointNamesList.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.jointNamesList.setAlternatingRowColors(True)
        self.jointNamesList.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.jointNamesList.horizontalHeader().setCascadingSectionResizes(True)
        self.jointNamesList.horizontalHeader().setDefaultSectionSize(100)
        self.jointNamesList.horizontalHeader().setStretchLastSection(True)

        self.horizontalLayout.addWidget(self.jointNamesList)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.add_pushButton = QPushButton(Form)
        self.add_pushButton.setObjectName(u"add_pushButton")

        self.verticalLayout_2.addWidget(self.add_pushButton)

        self.remove_pushButton = QPushButton(Form)
        self.remove_pushButton.setObjectName(u"remove_pushButton")

        self.verticalLayout_2.addWidget(self.remove_pushButton)

        self.removeAll_pushButton = QPushButton(Form)
        self.removeAll_pushButton.setObjectName(u"removeAll_pushButton")

        self.verticalLayout_2.addWidget(self.removeAll_pushButton)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setMinimumSize(QSize(0, 16))
        self.line.setBaseSize(QSize(0, 0))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.moveUp_pushButton = QPushButton(Form)
        self.moveUp_pushButton.setObjectName(u"moveUp_pushButton")

        self.verticalLayout_2.addWidget(self.moveUp_pushButton)

        self.moveDown_pushButton = QPushButton(Form)
        self.moveDown_pushButton.setObjectName(u"moveDown_pushButton")

        self.verticalLayout_2.addWidget(self.moveDown_pushButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Joint Names", None))
        ___qtablewidgetitem = self.jointNamesList.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Name", None));
        self.add_pushButton.setText(QCoreApplication.translate("Form", u"Add", None))
        self.remove_pushButton.setText(QCoreApplication.translate("Form", u"Remove", None))
        self.removeAll_pushButton.setText(QCoreApplication.translate("Form", u"Remove All", None))
        self.moveUp_pushButton.setText(QCoreApplication.translate("Form", u"Move Up", None))
        self.moveDown_pushButton.setText(QCoreApplication.translate("Form", u"Move Down", None))
    # retranslateUi

