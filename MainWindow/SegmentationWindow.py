# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SegmentationWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Segmentation(object):
    def setupUi(self, Segmentation):
        Segmentation.setObjectName("Segmentation")
        Segmentation.resize(902, 686)
        Segmentation.setStyleSheet("")
        self.pushButton = QtWidgets.QPushButton(Segmentation)
        self.pushButton.setGeometry(QtCore.QRect(780, 90, 93, 31))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Segmentation)
        self.lineEdit.setGeometry(QtCore.QRect(240, 90, 521, 31))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(Segmentation)
        self.label_2.setGeometry(QtCore.QRect(30, 90, 201, 31))
        self.label_2.setStyleSheet("font: 10pt \"Agency FB\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Segmentation)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 221, 51))
        self.label_3.setStyleSheet("font: 10pt \"Agency FB\";")
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(Segmentation)
        self.lineEdit_2.setGeometry(QtCore.QRect(240, 140, 521, 31))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(Segmentation)
        self.pushButton_2.setGeometry(QtCore.QRect(780, 140, 93, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.frame = QtWidgets.QFrame(Segmentation)
        self.frame.setGeometry(QtCore.QRect(10, 260, 431, 401))
        self.frame.setAcceptDrops(False)
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("border-image: url(:/images/images/2.jpg);\n"
"border-image: url(:/images/images/touming.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(Segmentation)
        self.frame_2.setGeometry(QtCore.QRect(460, 260, 431, 401))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label = QtWidgets.QLabel(Segmentation)
        self.label.setGeometry(QtCore.QRect(260, 20, 441, 41))
        self.label.setStyleSheet("font: 75 18pt \"微软雅黑\";")
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(Segmentation)
        self.pushButton_3.setGeometry(QtCore.QRect(680, 200, 131, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_4 = QtWidgets.QLabel(Segmentation)
        self.label_4.setGeometry(QtCore.QRect(30, 190, 171, 61))
        self.label_4.setStyleSheet("font: 10pt \"Agency FB\";")
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(Segmentation)
        self.lineEdit_3.setGeometry(QtCore.QRect(210, 200, 81, 41))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(Segmentation)
        self.lineEdit_4.setGeometry(QtCore.QRect(320, 200, 81, 41))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_5 = QtWidgets.QLabel(Segmentation)
        self.label_5.setGeometry(QtCore.QRect(300, 220, 16, 16))
        self.label_5.setStyleSheet("font: 75 14pt \"Agency FB\";")
        self.label_5.setObjectName("label_5")
        self.pushButton_4 = QtWidgets.QPushButton(Segmentation)
        self.pushButton_4.setGeometry(QtCore.QRect(430, 200, 131, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.frame_3 = QtWidgets.QFrame(Segmentation)
        self.frame_3.setGeometry(QtCore.QRect(0, 0, 901, 681))
        self.frame_3.setStyleSheet("border-image: url(:/images/images/9.jpg);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.raise_()
        self.frame_2.raise_()
        self.pushButton.raise_()
        self.lineEdit.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.lineEdit_2.raise_()
        self.pushButton_2.raise_()
        self.frame.raise_()
        self.label.raise_()
        self.pushButton_3.raise_()
        self.label_4.raise_()
        self.lineEdit_3.raise_()
        self.lineEdit_4.raise_()
        self.label_5.raise_()
        self.pushButton_4.raise_()

        self.retranslateUi(Segmentation)
        QtCore.QMetaObject.connectSlotsByName(Segmentation)

    def retranslateUi(self, Segmentation):
        _translate = QtCore.QCoreApplication.translate
        Segmentation.setWindowTitle(_translate("Segmentation", "Form"))
        self.pushButton.setText(_translate("Segmentation", "选择路径"))
        self.label_2.setText(_translate("Segmentation", "请您选择要处理的图像："))
        self.label_3.setText(_translate("Segmentation", "如需保存，请输入存储位置："))
        self.pushButton_2.setText(_translate("Segmentation", "选择路径"))
        self.label.setText(_translate("Segmentation", "欢迎使用图像全局/动态分割功能"))
        self.pushButton_3.setText(_translate("Segmentation", "全局分割"))
        self.label_4.setText(_translate("Segmentation", "请输入动态分割尺寸："))
        self.label_5.setText(_translate("Segmentation", "*"))
        self.pushButton_4.setText(_translate("Segmentation", "动态分割"))


import images_rc
