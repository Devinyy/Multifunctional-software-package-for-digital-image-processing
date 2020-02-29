# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CannyWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CannyWindow(object):
    def setupUi(self, CannyWindow):
        CannyWindow.setObjectName("CannyWindow")
        CannyWindow.resize(902, 686)
        CannyWindow.setStyleSheet("")
        self.pushButton = QtWidgets.QPushButton(CannyWindow)
        self.pushButton.setGeometry(QtCore.QRect(780, 90, 93, 31))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(CannyWindow)
        self.label.setGeometry(QtCore.QRect(260, 20, 371, 41))
        self.label.setStyleSheet("font: 75 18pt \"微软雅黑\";")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(CannyWindow)
        self.lineEdit.setGeometry(QtCore.QRect(240, 90, 521, 31))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(CannyWindow)
        self.label_2.setGeometry(QtCore.QRect(30, 90, 201, 31))
        self.label_2.setStyleSheet("font: 10pt \"Agency FB\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(CannyWindow)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 221, 51))
        self.label_3.setStyleSheet("font: 10pt \"Agency FB\";")
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(CannyWindow)
        self.lineEdit_2.setGeometry(QtCore.QRect(240, 140, 521, 31))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(CannyWindow)
        self.pushButton_2.setGeometry(QtCore.QRect(780, 140, 93, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.frame = QtWidgets.QFrame(CannyWindow)
        self.frame.setGeometry(QtCore.QRect(10, 260, 431, 401))
        self.frame.setAcceptDrops(False)
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("border-image: url(:/images/images/2.jpg);\n"
                                "border-image: url(:/images/images/touming.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(CannyWindow)
        self.frame_2.setGeometry(QtCore.QRect(460, 260, 431, 401))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.pushButton_3 = QtWidgets.QPushButton(CannyWindow)
        self.pushButton_3.setGeometry(QtCore.QRect(405, 200, 131, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.frame_3 = QtWidgets.QFrame(CannyWindow)
        self.frame_3.setGeometry(QtCore.QRect(0, 0, 901, 691))
        self.frame_3.setStyleSheet("border-image: url(:/images/images/7.jpg);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.raise_()
        self.frame_2.raise_()
        self.pushButton.raise_()
        self.label.raise_()
        self.lineEdit.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.lineEdit_2.raise_()
        self.pushButton_2.raise_()
        self.frame.raise_()
        self.pushButton_3.raise_()

        self.retranslateUi(CannyWindow)
        QtCore.QMetaObject.connectSlotsByName(CannyWindow)

    def retranslateUi(self, CannyWindow):
        _translate = QtCore.QCoreApplication.translate
        CannyWindow.setWindowTitle(_translate("CannyWindow", "Form"))
        self.pushButton.setText(_translate("CannyWindow", "选择路径"))
        self.label.setText(_translate("CannyWindow", "欢迎使用图像边缘检测功能"))
        self.label_2.setText(_translate("CannyWindow", "请您选择要处理的图像："))
        self.label_3.setText(_translate("CannyWindow", "如需保存，请输入存储位置："))
        self.pushButton_2.setText(_translate("CannyWindow", "选择路径"))
        self.pushButton_3.setText(_translate("CannyWindow", "canny边缘检测"))


import images_rc
