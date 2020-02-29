import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog , QMessageBox

from MainWindow import SegmentationWindow
from Function_mendth import Segmentation

import cv2
import numpy as np



class SegmentationWindow(QMainWindow, SegmentationWindow.Ui_Segmentation):
    def __init__(self, parent=None):
        super(SegmentationWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.open_path = ''
        # 添加打开文件
        self.pushButton.clicked.connect(self.chooseFile)
        # 保存文件
        self.pushButton_2.clicked.connect(self.saveFile)
        # 添加操作
        self.pushButton_3.clicked.connect(lambda:self.all_div(self.open_path))
        self.pushButton_4.clicked.connect(lambda: self.active_div(self.open_path))

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

    # 全局阈值分割
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

    # 动态阈值分割
    def active_div(self, path):
        # 创建动态阈值矩阵
        image = cv2.imread(path)
        # 知道图片的路径
        filepath, fullflname = os.path.split(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape[0], gray.shape[1]
        Dynamic_threshold_image = np.array([[0 for i in range(gray.shape[1])] for i in range(gray.shape[0])],
                                           dtype=np.uint8)
        # 调用自己写的otsu算法，进行阈值化分割图像处理
        if ((self.lineEdit_3.text() == '') or (self.lineEdit_4.text() == '')) :
            self.m = 4
            self.n = 4
        else :
            self.m = int (self.lineEdit_3.text())
            self.n = int (self.lineEdit_4.text())

        each_width = int(width / (self.m))
        each_height = int(height / (self.n))
        divide_list = Segmentation.divide(gray, self.m + 1, self.n + 1)  # 分割成为4*4的块
        # 用ostu算法计算每一小块图片的最佳阈值，进行动态阈值处理
        num = 0  # 记录这是第几块图形，第一块为0
        for each in divide_list:
            # 根据第几幅图算出他在原图中所在的行号和列号
            r = int(num / self.m)  # 行
            c = num % self.n  # 列
            ostu_image = Segmentation.myotsu(each)
            for i in range(ostu_image.shape[0]):
                for j in range(ostu_image.shape[1]):
                    Dynamic_threshold_image[i + r * each_height][j + c * each_width] = ostu_image[i][j]
            num += 1
        self.result = Dynamic_threshold_image
        path1 = filepath + '/test.jpg'
        # 写入暂存文件，显示在frame上
        cv2.imwrite(path1, self.result)
        self.frame_2.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)
