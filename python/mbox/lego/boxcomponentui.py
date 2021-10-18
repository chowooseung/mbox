# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'boxcomponentui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from mgear.vendor.Qt.QtCore import *
from mgear.vendor.Qt.QtGui import *
from mgear.vendor.Qt.QtWidgets import *

from mgear.core.widgets import DragQListView


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(344, 635)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tools_groupBox = QGroupBox(Form)
        self.tools_groupBox.setObjectName(u"tools_groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.tools_groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.settings_pushButton = QPushButton(self.tools_groupBox)
        self.settings_pushButton.setObjectName(u"settings_pushButton")

        self.verticalLayout_2.addWidget(self.settings_pushButton)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.duplicate_pushButton = QPushButton(self.tools_groupBox)
        self.duplicate_pushButton.setObjectName(u"duplicate_pushButton")

        self.horizontalLayout.addWidget(self.duplicate_pushButton)

        self.dupSym_pushButton = QPushButton(self.tools_groupBox)
        self.dupSym_pushButton.setObjectName(u"dupSym_pushButton")

        self.horizontalLayout.addWidget(self.dupSym_pushButton)

        self.extrCtl_pushButton = QPushButton(self.tools_groupBox)
        self.extrCtl_pushButton.setObjectName(u"extrCtl_pushButton")

        self.horizontalLayout.addWidget(self.extrCtl_pushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.build_pushButton = QPushButton(self.tools_groupBox)
        self.build_pushButton.setObjectName(u"build_pushButton")

        self.verticalLayout_2.addWidget(self.build_pushButton)


        self.verticalLayout_3.addWidget(self.tools_groupBox)

        self.list_groupBox = QGroupBox(Form)
        self.list_groupBox.setObjectName(u"list_groupBox")
        self.verticalLayout = QVBoxLayout(self.list_groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.search_lineEdit = QLineEdit(self.list_groupBox)
        self.search_lineEdit.setObjectName(u"search_lineEdit")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search_lineEdit.sizePolicy().hasHeightForWidth())
        self.search_lineEdit.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.search_lineEdit)

        self.splitter = QSplitter(self.list_groupBox)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.component_listView = DragQListView(self.splitter)
        self.component_listView.setObjectName(u"component_listView")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.component_listView.sizePolicy().hasHeightForWidth())
        self.component_listView.setSizePolicy(sizePolicy1)
        self.component_listView.setMinimumSize(QSize(0, 0))
        self.component_listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.component_listView.setProperty("showDropIndicator", False)
        self.component_listView.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.component_listView.setDefaultDropAction(Qt.CopyAction)
        self.component_listView.setAlternatingRowColors(True)
        self.component_listView.setSelectionMode(QAbstractItemView.SingleSelection)
        self.splitter.addWidget(self.component_listView)
        self.info_plainTextEdit = QPlainTextEdit(self.splitter)
        self.info_plainTextEdit.setObjectName(u"info_plainTextEdit")
        self.info_plainTextEdit.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.info_plainTextEdit.sizePolicy().hasHeightForWidth())
        self.info_plainTextEdit.setSizePolicy(sizePolicy2)
        self.info_plainTextEdit.setMinimumSize(QSize(0, 50))
        self.info_plainTextEdit.setMaximumSize(QSize(16777215, 100))
        self.info_plainTextEdit.setBaseSize(QSize(0, 50))
        self.info_plainTextEdit.setUndoRedoEnabled(False)
        self.info_plainTextEdit.setReadOnly(True)
        self.splitter.addWidget(self.info_plainTextEdit)

        self.verticalLayout.addWidget(self.splitter)

        self.draw_pushButton = QPushButton(self.list_groupBox)
        self.draw_pushButton.setObjectName(u"draw_pushButton")

        self.verticalLayout.addWidget(self.draw_pushButton)

        self.showUI_checkBox = QCheckBox(self.list_groupBox)
        self.showUI_checkBox.setObjectName(u"showUI_checkBox")
        self.showUI_checkBox.setChecked(True)

        self.verticalLayout.addWidget(self.showUI_checkBox)


        self.verticalLayout_3.addWidget(self.list_groupBox)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.tools_groupBox.setTitle(QCoreApplication.translate("Form", u"Box Tools", None))
#if QT_CONFIG(whatsthis)
        self.settings_pushButton.setWhatsThis(QCoreApplication.translate("Form", u"<html><head/><body><p>Open Component/Guide root settings window.</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.settings_pushButton.setText(QCoreApplication.translate("Form", u"Settings", None))
#if QT_CONFIG(tooltip)
        self.duplicate_pushButton.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Duplicate selected component.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.duplicate_pushButton.setText(QCoreApplication.translate("Form", u"Duplicate", None))
#if QT_CONFIG(tooltip)
        self.dupSym_pushButton.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Duplicate symmetrical selected component.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.dupSym_pushButton.setText(QCoreApplication.translate("Form", u"Dupl. Sym.", None))
#if QT_CONFIG(tooltip)
        self.extrCtl_pushButton.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Extract Selected Controls and store as control Buffer.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.extrCtl_pushButton.setText(QCoreApplication.translate("Form", u"Extr. Ctl.", None))
#if QT_CONFIG(tooltip)
        self.build_pushButton.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Build rig from selection</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.build_pushButton.setWhatsThis(QCoreApplication.translate("Form", u"<html><head/><body><p>Open Component/Guide root settings window.</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.build_pushButton.setText(QCoreApplication.translate("Form", u"Build From Selection", None))
        self.list_groupBox.setTitle(QCoreApplication.translate("Form", u"Blocks List", None))
        self.info_plainTextEdit.setPlainText("")
#if QT_CONFIG(tooltip)
        self.draw_pushButton.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Draw selected component.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.draw_pushButton.setText(QCoreApplication.translate("Form", u"Draw Component", None))
        self.showUI_checkBox.setText(QCoreApplication.translate("Form", u"Show Setting After Create New Component.", None))
    # retranslateUi

