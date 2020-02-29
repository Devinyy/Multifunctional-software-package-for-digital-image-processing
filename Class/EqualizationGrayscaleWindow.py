import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog , QMessageBox

from MainWindow import EqualizationGrayscaleWindow
from Function_mendth import Equalization_Grayscal

import numpy as np
import cv2



# 创建灰度化和均衡化窗口
class EqualizationGrayscaleWindow(QMainWindow, EqualizationGrayscaleWindow.Ui_EqualizationWindow):
    def __init__(self, parent=None):
        super(EqualizationGrayscaleWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.open_path = ''
        # 对均衡化按钮添加打开文件
        self.pushButton.clicked.connect(self.chooseFile)
        # 对均衡化按钮添加保存文件
        self.pushButton_2.clicked.connect(self.saveFile)
        # 对均衡化按钮添加操作
        self.pushButton_3.clicked.connect(lambda:self.equalization(self.open_path))
        # 对灰度化按钮添加操作
        self.pushButton_4.clicked.connect(lambda: self.grayscale(self.open_path))

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

    # 对图像进行均衡化
    def equalization(self,path):
        image = cv2.imread(path)
        # 知道图片的路径
        filepath, fullflname = os.path.split(path)
        # 创建空的查找表
        lut = np.zeros(256, dtype=image.dtype)

        b = Equalization_Grayscal.get_blue(image)
        g = Equalization_Grayscal.get_green(image)
        r = Equalization_Grayscal.get_red(image)

        hist_new_b = Equalization_Grayscal.clczhifangtu(b)
        hist_new_g = Equalization_Grayscal.clczhifangtu(g)
        hist_new_r = Equalization_Grayscal.clczhifangtu(r)

        result_b = Equalization_Grayscal.clcresult(hist_new_b, lut, b)
        result_g = Equalization_Grayscal.clcresult(hist_new_g, lut, g)
        result_r = Equalization_Grayscal.clcresult(hist_new_r, lut, r)
        # 合并通道
        self.result = cv2.merge((result_b, result_g, result_r))
        path1 = filepath + '/test.jpg'
        # 写入暂存文件，显示在frame上
        cv2.imwrite(path1, self.result)
        self.frame_2.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)

    # 对图像进行均衡化
    def grayscale(self,path):
        image = cv2.imread(path)
        # 知道图片的路径
        filepath, fullflname = os.path.split(path)
        self.result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        path1 = filepath + '/test.jpg'
        # 写入暂存文件，显示在frame上
        cv2.imwrite(path1, self.result)
        self.frame_2.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)