# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'rootnameui.ui'
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
        Form.resize(356, 456)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox_8 = QGroupBox(Form)
        self.groupBox_8.setObjectName(u"groupBox_8")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_8.sizePolicy().hasHeightForWidth())
        self.groupBox_8.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.groupBox_8)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.controls_name_convention_lineEdit = QLineEdit(self.groupBox_8)
        self.controls_name_convention_lineEdit.setObjectName(u"controls_name_convention_lineEdit")

        self.horizontalLayout.addWidget(self.controls_name_convention_lineEdit)

        self.reset_controls_convention_pushButton = QPushButton(self.groupBox_8)
        self.reset_controls_convention_pushButton.setObjectName(u"reset_controls_convention_pushButton")
        self.reset_controls_convention_pushButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout.addWidget(self.reset_controls_convention_pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.groupBox_8)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.label)

        self.controls_letter_case_comboBox = QComboBox(self.groupBox_8)
        self.controls_letter_case_comboBox.addItem("")
        self.controls_letter_case_comboBox.addItem("")
        self.controls_letter_case_comboBox.addItem("")
        self.controls_letter_case_comboBox.addItem("")
        self.controls_letter_case_comboBox.setObjectName(u"controls_letter_case_comboBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.controls_letter_case_comboBox.sizePolicy().hasHeightForWidth())
        self.controls_letter_case_comboBox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.controls_letter_case_comboBox)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_3.addWidget(self.groupBox_8)

        self.groupBox_9 = QGroupBox(Form)
        self.groupBox_9.setObjectName(u"groupBox_9")
        sizePolicy.setHeightForWidth(self.groupBox_9.sizePolicy().hasHeightForWidth())
        self.groupBox_9.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.joint_name_convention_lineEdit = QLineEdit(self.groupBox_9)
        self.joint_name_convention_lineEdit.setObjectName(u"joint_name_convention_lineEdit")

        self.horizontalLayout_2.addWidget(self.joint_name_convention_lineEdit)

        self.reset_joint_convention_pushButton = QPushButton(self.groupBox_9)
        self.reset_joint_convention_pushButton.setObjectName(u"reset_joint_convention_pushButton")
        self.reset_joint_convention_pushButton.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_2.addWidget(self.reset_joint_convention_pushButton)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.groupBox_9)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.label_3)

        self.joint_letter_case_comboBox = QComboBox(self.groupBox_9)
        self.joint_letter_case_comboBox.addItem("")
        self.joint_letter_case_comboBox.addItem("")
        self.joint_letter_case_comboBox.addItem("")
        self.joint_letter_case_comboBox.addItem("")
        self.joint_letter_case_comboBox.setObjectName(u"joint_letter_case_comboBox")
        sizePolicy2.setHeightForWidth(self.joint_letter_case_comboBox.sizePolicy().hasHeightForWidth())
        self.joint_letter_case_comboBox.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.joint_letter_case_comboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout_3.addWidget(self.groupBox_9)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox_10 = QGroupBox(Form)
        self.groupBox_10.setObjectName(u"groupBox_10")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.groupBox_10.sizePolicy().hasHeightForWidth())
        self.groupBox_10.setSizePolicy(sizePolicy3)
        self.formLayout_2 = QFormLayout(self.groupBox_10)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_4 = QLabel(self.groupBox_10)
        self.label_4.setObjectName(u"label_4")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_4)

        self.controls_direction_left_lineEdit = QLineEdit(self.groupBox_10)
        self.controls_direction_left_lineEdit.setObjectName(u"controls_direction_left_lineEdit")
        sizePolicy4 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.controls_direction_left_lineEdit.sizePolicy().hasHeightForWidth())
        self.controls_direction_left_lineEdit.setSizePolicy(sizePolicy4)
        self.controls_direction_left_lineEdit.setMinimumSize(QSize(50, 0))
        self.controls_direction_left_lineEdit.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.controls_direction_left_lineEdit)

        self.label_5 = QLabel(self.groupBox_10)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_5)

        self.controls_direction_right_lineEdit = QLineEdit(self.groupBox_10)
        self.controls_direction_right_lineEdit.setObjectName(u"controls_direction_right_lineEdit")
        sizePolicy4.setHeightForWidth(self.controls_direction_right_lineEdit.sizePolicy().hasHeightForWidth())
        self.controls_direction_right_lineEdit.setSizePolicy(sizePolicy4)
        self.controls_direction_right_lineEdit.setMinimumSize(QSize(50, 0))
        self.controls_direction_right_lineEdit.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.controls_direction_right_lineEdit)

        self.label_6 = QLabel(self.groupBox_10)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_6)

        self.controls_direction_center_lineEdit = QLineEdit(self.groupBox_10)
        self.controls_direction_center_lineEdit.setObjectName(u"controls_direction_center_lineEdit")
        sizePolicy4.setHeightForWidth(self.controls_direction_center_lineEdit.sizePolicy().hasHeightForWidth())
        self.controls_direction_center_lineEdit.setSizePolicy(sizePolicy4)
        self.controls_direction_center_lineEdit.setMinimumSize(QSize(50, 0))
        self.controls_direction_center_lineEdit.setAlignment(Qt.AlignCenter)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.controls_direction_center_lineEdit)

        self.reset_controls_direction_pushButton = QPushButton(self.groupBox_10)
        self.reset_controls_direction_pushButton.setObjectName(u"reset_controls_direction_pushButton")
        sizePolicy4.setHeightForWidth(self.reset_controls_direction_pushButton.sizePolicy().hasHeightForWidth())
        self.reset_controls_direction_pushButton.setSizePolicy(sizePolicy4)
        self.reset_controls_direction_pushButton.setMaximumSize(QSize(16777215, 16777215))

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.reset_controls_direction_pushButton)


        self.gridLayout.addWidget(self.groupBox_10, 0, 0, 1, 1)

        self.groupBox_12 = QGroupBox(Form)
        self.groupBox_12.setObjectName(u"groupBox_12")
        sizePolicy3.setHeightForWidth(self.groupBox_12.sizePolicy().hasHeightForWidth())
        self.groupBox_12.setSizePolicy(sizePolicy3)
        self.formLayout_4 = QFormLayout(self.groupBox_12)
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_9 = QLabel(self.groupBox_12)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_4.setWidget(0, QFormLayout.LabelRole, self.label_9)

        self.joint_direction_left_lineEdit = QLineEdit(self.groupBox_12)
        self.joint_direction_left_lineEdit.setObjectName(u"joint_direction_left_lineEdit")
        sizePolicy4.setHeightForWidth(self.joint_direction_left_lineEdit.sizePolicy().hasHeightForWidth())
        self.joint_direction_left_lineEdit.setSizePolicy(sizePolicy4)
        self.joint_direction_left_lineEdit.setMinimumSize(QSize(50, 0))
        self.joint_direction_left_lineEdit.setAlignment(Qt.AlignCenter)

        self.formLayout_4.setWidget(0, QFormLayout.FieldRole, self.joint_direction_left_lineEdit)

        self.label_10 = QLabel(self.groupBox_12)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_4.setWidget(1, QFormLayout.LabelRole, self.label_10)

        self.joint_direction_right_lineEdit = QLineEdit(self.groupBox_12)
        self.joint_direction_right_lineEdit.setObjectName(u"joint_direction_right_lineEdit")
        sizePolicy4.setHeightForWidth(self.joint_direction_right_lineEdit.sizePolicy().hasHeightForWidth())
        self.joint_direction_right_lineEdit.setSizePolicy(sizePolicy4)
        self.joint_direction_right_lineEdit.setMinimumSize(QSize(50, 0))
        self.joint_direction_right_lineEdit.setAlignment(Qt.AlignCenter)

        self.formLayout_4.setWidget(1, QFormLayout.FieldRole, self.joint_direction_right_lineEdit)

        self.label_11 = QLabel(self.groupBox_12)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_4.setWidget(2, QFormLayout.LabelRole, self.label_11)

        self.joint_direction_center_lineEdit = QLineEdit(self.groupBox_12)
        self.joint_direction_center_lineEdit.setObjectName(u"joint_direction_center_lineEdit")
        sizePolicy4.setHeightForWidth(self.joint_direction_center_lineEdit.sizePolicy().hasHeightForWidth())
        self.joint_direction_center_lineEdit.setSizePolicy(sizePolicy4)
        self.joint_direction_center_lineEdit.setMinimumSize(QSize(50, 0))
        self.joint_direction_center_lineEdit.setAlignment(Qt.AlignCenter)

        self.formLayout_4.setWidget(2, QFormLayout.FieldRole, self.joint_direction_center_lineEdit)

        self.reset_joint_direction_pushButton = QPushButton(self.groupBox_12)
        self.reset_joint_direction_pushButton.setObjectName(u"reset_joint_direction_pushButton")
        sizePolicy4.setHeightForWidth(self.reset_joint_direction_pushButton.sizePolicy().hasHeightForWidth())
        self.reset_joint_direction_pushButton.setSizePolicy(sizePolicy4)
        self.reset_joint_direction_pushButton.setMaximumSize(QSize(16777215, 16777215))

        self.formLayout_4.setWidget(3, QFormLayout.FieldRole, self.reset_joint_direction_pushButton)


        self.gridLayout.addWidget(self.groupBox_12, 0, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.formLayout = QFormLayout(self.groupBox)
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.controls_padding_spinBox = QSpinBox(self.groupBox)
        self.controls_padding_spinBox.setObjectName(u"controls_padding_spinBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.controls_padding_spinBox)

        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_12)

        self.joint_padding_spinBox = QSpinBox(self.groupBox)
        self.joint_padding_spinBox.setObjectName(u"joint_padding_spinBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.joint_padding_spinBox)


        self.horizontalLayout_4.addWidget(self.groupBox)

        self.groupBox_11 = QGroupBox(Form)
        self.groupBox_11.setObjectName(u"groupBox_11")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.groupBox_11.sizePolicy().hasHeightForWidth())
        self.groupBox_11.setSizePolicy(sizePolicy5)
        self.formLayout_3 = QFormLayout(self.groupBox_11)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_7 = QLabel(self.groupBox_11)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_7)

        self.controls_name_ext_lineEdit = QLineEdit(self.groupBox_11)
        self.controls_name_ext_lineEdit.setObjectName(u"controls_name_ext_lineEdit")
        sizePolicy4.setHeightForWidth(self.controls_name_ext_lineEdit.sizePolicy().hasHeightForWidth())
        self.controls_name_ext_lineEdit.setSizePolicy(sizePolicy4)
        self.controls_name_ext_lineEdit.setMinimumSize(QSize(50, 0))
        self.controls_name_ext_lineEdit.setAlignment(Qt.AlignCenter)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.controls_name_ext_lineEdit)

        self.label_8 = QLabel(self.groupBox_11)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_8)

        self.joint_name_ext_lineEdit = QLineEdit(self.groupBox_11)
        self.joint_name_ext_lineEdit.setObjectName(u"joint_name_ext_lineEdit")
        sizePolicy4.setHeightForWidth(self.joint_name_ext_lineEdit.sizePolicy().hasHeightForWidth())
        self.joint_name_ext_lineEdit.setSizePolicy(sizePolicy4)
        self.joint_name_ext_lineEdit.setMinimumSize(QSize(50, 0))
        self.joint_name_ext_lineEdit.setAlignment(Qt.AlignCenter)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.joint_name_ext_lineEdit)

        self.reset_name_ext_pushButton = QPushButton(self.groupBox_11)
        self.reset_name_ext_pushButton.setObjectName(u"reset_name_ext_pushButton")
        sizePolicy4.setHeightForWidth(self.reset_name_ext_pushButton.sizePolicy().hasHeightForWidth())
        self.reset_name_ext_pushButton.setSizePolicy(sizePolicy4)
        self.reset_name_ext_pushButton.setMaximumSize(QSize(16777215, 16777215))

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.reset_name_ext_pushButton)


        self.horizontalLayout_4.addWidget(self.groupBox_11)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.verticalSpacer = QSpacerItem(20, 10000, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("Form", u"Controls Name Convention", None))
#if QT_CONFIG(tooltip)
        self.controls_name_convention_lineEdit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">Custom Naming rule:</span></p><p>To configure custom names, please use the following tokes with &quot;<span style=\" font-weight:600;\">{}</span>&quot;</p><p><br/></p><p><span style=\" font-weight:600;\">{name}</span> = The name of the component</p><p><span style=\" font-weight:600;\">{direction}</span> = The side of the component</p><p><span style=\" font-weight:600;\">{index</span>} = Index of the component. This is important when more than one component have the same name</p><p><span style=\" font-weight:600;\">{description}</span> = The name of the object inside the component</p><p><span style=\" font-weight:600;\">{extension}</span> = The extension of the object. For example &quot;ctl&quot; for controls or &quot;jnt&quot; for joints</p><p><br/></p><p><span style=\" font-weight:600;\">NOTE:</span> the only valid separator is &quot;_&quot;. This is a Maya limitation.</p><p><br/></p><p><br/></p><p><span style=\" font-weight:600;\">This is the default co"
                        "nfiguration:</span></p><p>{name}_{direction}{index}_{description}_{extension}</p><p><br/></p><p><br/></p><p><span style=\" font-weight:600;\">Other examples of configurations:</span></p><p>{name}{direction}{index}{description}{extension}</p><p>{name}{index}_{description}_{extension}_{direction}</p><p>{name}{index}_some_random_text_{description}_{extension}_{direction}</p><p><br/></p><p><span style=\" font-weight:600;\">It is recommended to use all the tokens to ensure that there is no name clashing</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.controls_name_convention_lineEdit.setText(QCoreApplication.translate("Form", u"{name}_{direction}{index}_{description}_{extension}", None))
        self.reset_controls_convention_pushButton.setText(QCoreApplication.translate("Form", u"Reset", None))
        self.label.setText(QCoreApplication.translate("Form", u"{descrition} Letter Case", None))
        self.controls_letter_case_comboBox.setItemText(0, QCoreApplication.translate("Form", u"Default", None))
        self.controls_letter_case_comboBox.setItemText(1, QCoreApplication.translate("Form", u"Upper Case", None))
        self.controls_letter_case_comboBox.setItemText(2, QCoreApplication.translate("Form", u"Lower Case", None))
        self.controls_letter_case_comboBox.setItemText(3, QCoreApplication.translate("Form", u"Capitalization", None))

        self.groupBox_9.setTitle(QCoreApplication.translate("Form", u"Joint Name Convention", None))
#if QT_CONFIG(tooltip)
        self.joint_name_convention_lineEdit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p><span style=\" font-weight:600;\">Custom Naming rule:</span></p><p>To configure custom names, please use the following tokes with &quot;<span style=\" font-weight:600;\">{}</span>&quot;</p><p><br/></p><p><span style=\" font-weight:600;\">{name}</span> = The name of the component</p><p><span style=\" font-weight:600;\">{direction}</span> = The side of the component</p><p><span style=\" font-weight:600;\">{index</span>} = Index of the component. This is important when more than one component have the same name</p><p><span style=\" font-weight:600;\">{description}</span> = The name of the object inside the component</p><p><span style=\" font-weight:600;\">{extension}</span> = The extension of the object. For example &quot;ctl&quot; for controls or &quot;jnt&quot; for joints</p><p><br/></p><p><span style=\" font-weight:600;\">NOTE:</span> the only valid separator is &quot;_&quot;. This is a Maya limitation.</p><p><br/></p><p><br/></p><p><span style=\" font-weight:600;\">This is the default co"
                        "nfiguration:</span></p><p>{name}_{direction}{index}_{description}_{extension}</p><p><br/></p><p><br/></p><p><span style=\" font-weight:600;\">Other examples of configurations:</span></p><p>{name}{direction}{index}{description}{extension}</p><p>{name}{index}_{description}_{extension}_{direction}</p><p>{name}{index}_some_random_text_{description}_{extension}_{direction}</p><p><br/></p><p><span style=\" font-weight:600;\">It is recommended to use all the tokens to ensure that there is no name clashing</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.joint_name_convention_lineEdit.setText(QCoreApplication.translate("Form", u"{name}_{direction}{index}_{description}_{extension}", None))
        self.reset_joint_convention_pushButton.setText(QCoreApplication.translate("Form", u"Reset", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"{descrition} Letter Case", None))
        self.joint_letter_case_comboBox.setItemText(0, QCoreApplication.translate("Form", u"Default", None))
        self.joint_letter_case_comboBox.setItemText(1, QCoreApplication.translate("Form", u"Upper Case", None))
        self.joint_letter_case_comboBox.setItemText(2, QCoreApplication.translate("Form", u"Lower Case", None))
        self.joint_letter_case_comboBox.setItemText(3, QCoreApplication.translate("Form", u"Capitalization", None))

        self.groupBox_10.setTitle(QCoreApplication.translate("Form", u"Controls Direction", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Left", None))
#if QT_CONFIG(tooltip)
        self.controls_direction_left_lineEdit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>set the text that will be used for the side:</p><p><br/></p><p><span style=\" font-weight:600;\">for example:</span></p><p>L</p><p>left</p><p>Left</p><p>l</p><p><br/></p><p>r</p><p>right</p><p>Right</p><p>Derecha</p><p>R</p><p><br/></p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.controls_direction_left_lineEdit.setText(QCoreApplication.translate("Form", u"L", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Right", None))
#if QT_CONFIG(tooltip)
        self.controls_direction_right_lineEdit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>set the text that will be used for the side:</p><p><br/></p><p><span style=\" font-weight:600;\">for example:</span></p><p>L</p><p>left</p><p>Left</p><p>l</p><p><br/></p><p>r</p><p>right</p><p>Right</p><p>Derecha</p><p>R</p><p><br/></p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.controls_direction_right_lineEdit.setText(QCoreApplication.translate("Form", u"R", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Center", None))
#if QT_CONFIG(tooltip)
        self.controls_direction_center_lineEdit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>set the text that will be used for the side:</p><p><br/></p><p><span style=\" font-weight:600;\">for example:</span></p><p>L</p><p>left</p><p>Left</p><p>l</p><p><br/></p><p>r</p><p>right</p><p>Right</p><p>Derecha</p><p>R</p><p><br/></p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.controls_direction_center_lineEdit.setText(QCoreApplication.translate("Form", u"C", None))
        self.reset_controls_direction_pushButton.setText(QCoreApplication.translate("Form", u"Reset", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("Form", u"Joint Direction", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"Left", None))
#if QT_CONFIG(tooltip)
        self.joint_direction_left_lineEdit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>set the text that will be used for the side:</p><p><br/></p><p><span style=\" font-weight:600;\">for example:</span></p><p>L</p><p>left</p><p>Left</p><p>l</p><p><br/></p><p>r</p><p>right</p><p>Right</p><p>Derecha</p><p>R</p><p><br/></p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.joint_direction_left_lineEdit.setText(QCoreApplication.translate("Form", u"L", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"Right", None))
#if QT_CONFIG(tooltip)
        self.joint_direction_right_lineEdit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>set the text that will be used for the side:</p><p><br/></p><p><span style=\" font-weight:600;\">for example:</span></p><p>L</p><p>left</p><p>Left</p><p>l</p><p><br/></p><p>r</p><p>right</p><p>Right</p><p>Derecha</p><p>R</p><p><br/></p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.joint_direction_right_lineEdit.setText(QCoreApplication.translate("Form", u"R", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Center", None))
#if QT_CONFIG(tooltip)
        self.joint_direction_center_lineEdit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>set the text that will be used for the side:</p><p><br/></p><p><span style=\" font-weight:600;\">for example:</span></p><p>L</p><p>left</p><p>Left</p><p>l</p><p><br/></p><p>r</p><p>right</p><p>Right</p><p>Derecha</p><p>R</p><p><br/></p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.joint_direction_center_lineEdit.setText(QCoreApplication.translate("Form", u"C", None))
        self.reset_joint_direction_pushButton.setText(QCoreApplication.translate("Form", u"Reset", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Index Padding", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Controls", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Joint", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("Form", u"Extensions Naming", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Controls", None))
#if QT_CONFIG(tooltip)
        self.controls_name_ext_lineEdit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Set the extension name for controls</p><p><br/></p><p><span style=\" font-weight:600;\">For example:</span></p><p>ctl</p><p>control</p><p>mover</p><p>ct</p><p>etc..</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.controls_name_ext_lineEdit.setText(QCoreApplication.translate("Form", u"ctl", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Joints", None))
#if QT_CONFIG(tooltip)
        self.joint_name_ext_lineEdit.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Set the extension name for joints</p><p><br/></p><p><span style=\" font-weight:600;\">For example:</span></p><p>jnt</p><p>joint</p><p>bone</p><p>j</p><p>etc..</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.joint_name_ext_lineEdit.setText(QCoreApplication.translate("Form", u"jnt", None))
        self.reset_name_ext_pushButton.setText(QCoreApplication.translate("Form", u"Reset", None))
    # retranslateUi

