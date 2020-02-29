import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog , QMessageBox

from MainWindow import RegionalGrowthWindow
from Function_mendth import RegionalGrowth

import cv2
import numpy as np



class RegionalGrowthWindow(QMainWindow, RegionalGrowthWindow.Ui_RegionalGrowthWindow):
    def __init__(self, parent=None):
        super(RegionalGrowthWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.open_path = ''
        # 添加打开文件
        self.pushButton.clicked.connect(self.chooseFile)
        # 保存文件
        self.pushButton_2.clicked.connect(self.saveFile)
        # 添加操作
        self.pushButton_3.clicked.connect(lambda: self.div_water(self.open_path))
        self.pushButton_4.clicked.connect(lambda: self.growth_div(self.open_path))

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

    # 区域生长分割
    def growth_div(self, path):
        image = cv2.imread(path)
        seed_points = []
        # 知道图片的路径
        filepath, fullflname = os.path.split(path)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if self.lineEdit_3.text() == '':
            seed_points = [(10, 150), (100, 150), (75, 250), (129, 210), (263, 243)]  # 输入选取的种子像素
        else :
            seed_points = []
            seeds = self.lineEdit_3.text()
            seeds = seeds.replace('(', '')
            seeds = seeds.replace(')', '')
            seeds = seeds.split(' ')
            for each in seeds:
                each = each.split(',')
                a = int(each[0])
                b = int(each[1])
                c = (a, b)
                seed_points.append(c)
        if self.lineEdit_4.text() == '':
            threahold = 15
        else:
            threahold = int(self.lineEdit_4.text())
        self.result = RegionalGrowth.regional_growth(gray, seed_points, threahold)

        path1 = filepath + '/test.jpg'
        # 写入暂存文件，显示在frame上
        cv2.imwrite(path1, self.result)
        self.frame_2.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)

    # 分水岭分割
    def div_water(self, path):
        # 创建动态阈值矩阵
        image = cv2.imread(path)
        self.result = np.copy(image)
        # 知道图片的路径
        filepath, fullflname = os.path.split(path)
        blurred = cv2.pyrMeanShiftFiltering(self.result, 10, 100)  # 去除噪点

        # gray\binary image
        gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # morphology operation
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mb = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
        sure_bg = cv2.dilate(mb, kernel, iterations=3)

        # distance transform
        dist = cv2.distanceTransform(mb, cv2.DIST_L2, 3)
        dist_output = cv2.normalize(dist, 0, 1.0, cv2.NORM_MINMAX)

        ret, surface = cv2.threshold(dist, dist.max() * 0.6, 255, cv2.THRESH_BINARY)

        surface_fg = np.uint8(surface)
        unknown = cv2.subtract(sure_bg, surface_fg)
        ret, markers = cv2.connectedComponents(surface_fg)

        # watershed transfrom
        markers += 1
        markers[unknown == 255] = 0
        markers = cv2.watershed(self.result, markers=markers)
        self.result[markers == -1] = [0, 0, 255]
        path1 = filepath + '/test.jpg'
        # 写入暂存文件，显示在frame上
        cv2.imwrite(path1, self.result)
        self.frame_2.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)
