# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chain_guide_initializer_ui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(200, 133)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sections_label = QLabel(Dialog)
        self.sections_label.setObjectName(u"sections_label")

        self.horizontalLayout.addWidget(self.sections_label)

        self.sections_spinBox = QSpinBox(Dialog)
        self.sections_spinBox.setObjectName(u"sections_spinBox")
        self.sections_spinBox.setMinimum(1)
        self.sections_spinBox.setMaximum(999)
        self.sections_spinBox.setValue(3)

        self.horizontalLayout.addWidget(self.sections_spinBox)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.direction_label = QLabel(Dialog)
        self.direction_label.setObjectName(u"direction_label")

        self.horizontalLayout_2.addWidget(self.direction_label)

        self.direction_comboBox = QComboBox(Dialog)
        self.direction_comboBox.addItem("")
        self.direction_comboBox.addItem("")
        self.direction_comboBox.addItem("")
        self.direction_comboBox.addItem("")
        self.direction_comboBox.addItem("")
        self.direction_comboBox.addItem("")
        self.direction_comboBox.setObjectName(u"direction_comboBox")

        self.horizontalLayout_2.addWidget(self.direction_comboBox)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.spacing_label = QLabel(Dialog)
        self.spacing_label.setObjectName(u"spacing_label")

        self.horizontalLayout_3.addWidget(self.spacing_label)

        self.spacing_doubleSpinBox = QDoubleSpinBox(Dialog)
        self.spacing_doubleSpinBox.setObjectName(u"spacing_doubleSpinBox")
        self.spacing_doubleSpinBox.setDecimals(4)
        self.spacing_doubleSpinBox.setMaximum(999.990000000000009)
        self.spacing_doubleSpinBox.setValue(1.000000000000000)

        self.horizontalLayout_3.addWidget(self.spacing_doubleSpinBox)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.sections_label.setText(QCoreApplication.translate("Dialog", u"Sections Number", None))
        self.direction_label.setText(QCoreApplication.translate("Dialog", u"Direction", None))
        self.direction_comboBox.setItemText(0, QCoreApplication.translate("Dialog", u"X", None))
        self.direction_comboBox.setItemText(1, QCoreApplication.translate("Dialog", u"Y", None))
        self.direction_comboBox.setItemText(2, QCoreApplication.translate("Dialog", u"Z", None))
        self.direction_comboBox.setItemText(3, QCoreApplication.translate("Dialog", u"-X", None))
        self.direction_comboBox.setItemText(4, QCoreApplication.translate("Dialog", u"-Y", None))
        self.direction_comboBox.setItemText(5, QCoreApplication.translate("Dialog", u"-Z", None))

        self.spacing_label.setText(QCoreApplication.translate("Dialog", u"Spacing", None))
    # retranslateUi

