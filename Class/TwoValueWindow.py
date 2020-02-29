import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog , QMessageBox

from MainWindow import TwoValueWindow
from Function_mendth import Segmentation

import cv2
import numpy as np



class TwoValueWindow(QMainWindow, TwoValueWindow.Ui_TwoValueWindow):
    def __init__(self, parent=None):
        super(TwoValueWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.open_path = ''
        # 添加打开文件
        self.pushButton.clicked.connect(self.chooseFile)
        # 保存文件
        self.pushButton_2.clicked.connect(self.saveFile)
        # 添加操作
        self.pushButton_3.clicked.connect(lambda:self.all_div(self.open_path))
        self.pushButton_4.clicked.connect(lambda: self.myself_div(self.open_path))

    # 打开文件函数，并将路径写入框内,将原始图片放入frame中
    def chooseFile(self):

        fileName_choose, typefile = QFileDialog.getOpenFileName(self,"选取文件",
                                                     self.cwd,  # 起始路径
                                                     "All Files (*);;Text Files (*.txt)")# 设置文件扩展名过滤,用双分号间隔
        if fileName_choose == "":
            return
        self.lineEdit.setText(fileName_choose)
        self.frame.setStyleSheet("border-image: url("+fileName_choose+");")
        self.open_path = fileName_choose

    # 保存文件函数，并将路径写入框内
    def saveFile(self):
        fileName_choose, filetype = QFileDialog.getSaveFileName(self,"文件保存",
                                                      self.cwd,  # 起始路径
                                                      "All Files (*);;Text Files (*.txt)")# 设置文件扩展名过滤,用双分号间隔
        if fileName_choose == "":
            return
        self.lineEdit_2.setText(fileName_choose)
        # 保存文件
        cv2.imwrite(fileName_choose, self.result)
        QMessageBox.information(self, '温馨提醒', '保存成功!', QMessageBox.Ok)

    # ostu 阈值分割
    def all_div(self, path):
        image = cv2.imread(path)
        # 知道图片的路径
        filepath, fullflname = os.path.split(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.result = Segmentation.myotsu(gray)
        path1 = filepath + '/test.jpg'
        # 写入暂存文件，显示在frame上
        cv2.imwrite(path1, self.result)
        self.frame_2.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)

    # 自定义阈值
    def myself_div(self, path):
        image = cv2.imread(path)
        # 知道图片的路径
        filepath, fullflname = os.path.split(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 处理后最终输出矩阵将齐大小设置为与原图一样
        gray2 = np.array([[0 for i in range(gray.shape[1])] for i in range(gray.shape[0])], dtype='float')
        if self.lineEdit_3.text() != '':
            threshold = int(self.lineEdit_3.text())
        else :
            threshold = 128
        # 用阈值将图片进行二值化
        for i in range(gray.shape[0]):
            for j in range(gray.shape[1]):
                # 对大于阈值的显示为255白色，小于阈值的显示为0黑色
                if gray[i][j] <= threshold:
                    gray2[i][j] = 0
                else:
                    gray2[i][j] = 255
        self.result = gray2
        path1 = filepath + '/test.jpg'
        # 写入暂存文件，显示在frame上
        cv2.imwrite(path1, self.result)
        self.frame_2.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)
