import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog , QMessageBox

from MainWindow import FilterWindow
from Function_mendth import Filter, Canny_Clc
import cv2
import numpy as np



class FilterWindow(QMainWindow, FilterWindow.Ui_FilterWindow):
    def __init__(self, parent=None):
        super(FilterWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.open_path = ''
        # 添加打开文件
        self.pushButton.clicked.connect(self.chooseFile)
        # 保存文件
        self.pushButton_2.clicked.connect(self.saveFile)
        # 添加操作
        self.pushButton_3.clicked.connect(lambda:self.guassian_filter(self.open_path))
        self.pushButton_4.clicked.connect(lambda: self.mean_flite(self.open_path))
        self.pushButton_5.clicked.connect(lambda: self.mid_flite(self.open_path))

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

    # 3*3 中值滤波处理
    def mid_flite(self,path):
        image = cv2.imread(path)
        self.salt_pepper_noise_pic = Filter.salt_pepper_noise(image, prob=0.01)  # 添加椒盐噪声
        # 知道图片的路径
        filepath, fullflname = os.path.split(path)
        # 写入暂存文件，显示在frame上
        path1 = filepath + '/test.jpg'
        cv2.imwrite(path1, self.salt_pepper_noise_pic)
        self.frame.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)
        (sp_b, sp_g, sp_r) = cv2.split(self.salt_pepper_noise_pic)  # 椒盐噪音通道分离
        """##```按3*3模版扩充```##"""
        expandb_result = Filter.expand(sp_b, 3)  # 对每个通道进行填充最近值操作
        expandg_result = Filter.expand(sp_g, 3)  # 对每个通道进行填充最近值操作
        expandr_result = Filter.expand(sp_r, 3)  # 对每个通道进行填充最近值操作
        # 进行3*3卷积计算均值
        # 对椒盐噪声使用均值滤波器分别对三个通道对填充后的灰度级进行卷积
        convert_3b_meanresult = Filter.meanflite(sp_b, expandb_result, 3)
        convert_3g_meanresult = Filter.meanflite(sp_g, expandg_result, 3)
        convert_3r_meanresult = Filter.meanflite(sp_r, expandr_result, 3)
        # 合并通道
        self.result = cv2.merge([convert_3b_meanresult, convert_3g_meanresult, convert_3r_meanresult])
        # 写入暂存文件，显示在frame上
        path1 = filepath + '/test.jpg'
        cv2.imwrite(path1, self.result)
        self.frame_2.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)

    # 3*3均值滤波
    def mean_flite(self,path):
        image = cv2.imread(path)
        self.salt_pepper_noise_pic = Filter.salt_pepper_noise(image, prob=0.01)  # 添加椒盐噪声
        # 知道图片的路径
        filepath, fullflname = os.path.split(path)
        # 写入暂存文件，显示在frame上
        path1 = filepath + '/test.jpg'
        cv2.imwrite(path1, self.salt_pepper_noise_pic)
        self.frame.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)
        (sp_b, sp_g, sp_r) = cv2.split(self.salt_pepper_noise_pic)  # 椒盐噪音通道分离
        """##```按3*3模版扩充```##"""
        expandb_result = Filter.expand(sp_b, 3)  # 对每个通道进行填充最近值操作
        expandg_result = Filter.expand(sp_g, 3)  # 对每个通道进行填充最近值操作
        expandr_result = Filter.expand(sp_r, 3)  # 对每个通道进行填充最近值操作
        # 进行3*3计算中值
        # 使用中值滤波器分别对三个通道对填充后的灰度级进行卷积
        convert_3b_medianresult = Filter.medianfliter(sp_b, expandb_result, 3)
        convert_3g_medianresult = Filter.medianfliter(sp_g, expandg_result, 3)
        convert_3r_medianresult = Filter.medianfliter(sp_r, expandr_result, 3)
        self.result = cv2.merge([convert_3b_medianresult, convert_3g_medianresult, convert_3r_medianresult])
        # 写入暂存文件，显示在frame上
        path1 = filepath + '/test.jpg'
        cv2.imwrite(path1, self.result)
        self.frame_2.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)

    # 5*5高斯滤波器
    def guassian_filter(self,path):
        image = cv2.imread(path)
        # 知道图片的路径
        filepath, fullflname = os.path.split(path)
        # 写入暂存文件，显示在frame上
        path1 = filepath + '/test.jpg'
        cv2.imwrite(path1, image)
        self.frame.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)
        (sp_b, sp_g, sp_r) = cv2.split(image)  # 通道分离
        # 使用高斯滤波器平滑图像
        gaussian_img, gaussian_img1 = Canny_Clc.Smooth(sp_b)
        gaussian_img2, gaussian_img3 = Canny_Clc.Smooth(sp_g)
        gaussian_img4, gaussian_img5 = Canny_Clc.Smooth(sp_r)
        self.result = cv2.merge([gaussian_img1, gaussian_img3, gaussian_img5])
        # 写入暂存文件，显示在frame上
        path1 = filepath + '/test.jpg'
        cv2.imwrite(path1, self.result)
        self.frame_2.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)
