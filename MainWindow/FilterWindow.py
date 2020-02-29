# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FilterWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FilterWindow(object):
    def setupUi(self, FilterWindow):
        FilterWindow.setObjectName("FilterWindow")
        FilterWindow.resize(904, 681)
        FilterWindow.setStyleSheet("")
        self.pushButton = QtWidgets.QPushButton(FilterWindow)
        self.pushButton.setGeometry(QtCore.QRect(780, 90, 93, 31))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(FilterWindow)
        self.lineEdit.setGeometry(QtCore.QRect(240, 90, 521, 31))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(FilterWindow)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 221, 51))
        self.label_3.setStyleSheet("font: 10pt \"Agency FB\";")
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(FilterWindow)
        self.lineEdit_2.setGeometry(QtCore.QRect(240, 140, 521, 31))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(FilterWindow)
        self.pushButton_2.setGeometry(QtCore.QRect(780, 140, 93, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.frame = QtWidgets.QFrame(FilterWindow)
        self.frame.setGeometry(QtCore.QRect(10, 260, 431, 401))
        self.frame.setAcceptDrops(False)
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet("border-image: url(:/images/images/2.jpg);\n"
"border-image: url(:/images/images/touming.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(FilterWindow)
        self.frame_2.setGeometry(QtCore.QRect(460, 260, 431, 401))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label = QtWidgets.QLabel(FilterWindow)
        self.label.setGeometry(QtCore.QRect(260, 20, 441, 41))
        self.label.setStyleSheet("font: 75 18pt \"微软雅黑\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(FilterWindow)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 201, 31))
        self.label_2.setStyleSheet("font: 10pt \"Agency FB\";")
        self.label_2.setObjectName("label_2")
        self.pushButton_3 = QtWidgets.QPushButton(FilterWindow)
        self.pushButton_3.setGeometry(QtCore.QRect(600, 200, 275, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_5 = QtWidgets.QPushButton(FilterWindow)
        self.pushButton_5.setGeometry(QtCore.QRect(10, 200, 275, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_4 = QtWidgets.QPushButton(FilterWindow)
        self.pushButton_4.setGeometry(QtCore.QRect(300, 200, 280, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.frame_3 = QtWidgets.QFrame(FilterWindow)
        self.frame_3.setGeometry(QtCore.QRect(0, 0, 911, 681))
        self.frame_3.setStyleSheet("border-image: url(:/images/images/16.jpg);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.raise_()
        self.frame_2.raise_()
        self.pushButton.raise_()
        self.lineEdit.raise_()
        self.label_3.raise_()
        self.lineEdit_2.raise_()
        self.pushButton_2.raise_()
        self.frame.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_5.raise_()
        self.pushButton_4.raise_()

        self.retranslateUi(FilterWindow)
        QtCore.QMetaObject.connectSlotsByName(FilterWindow)

    def retranslateUi(self, FilterWindow):
        _translate = QtCore.QCoreApplication.translate
        FilterWindow.setWindowTitle(_translate("FilterWindow", "Form"))
        self.pushButton.setText(_translate("FilterWindow", "选择路径"))
        self.label_3.setText(_translate("FilterWindow", "如需保存，请输入存储位置："))
        self.pushButton_2.setText(_translate("FilterWindow", "选择路径"))
        self.label.setText(_translate("FilterWindow", "欢迎使用图像滤波器功能"))
        self.label_2.setText(_translate("FilterWindow", "请您选择要处理的图像："))
        self.pushButton_3.setText(_translate("FilterWindow", "5*5 高斯滤波"))
        self.pushButton_5.setText(_translate("FilterWindow", "3*3 中值滤波"))
        self.pushButton_4.setText(_translate("FilterWindow", "3*3 均值滤波"))


import images_rc
