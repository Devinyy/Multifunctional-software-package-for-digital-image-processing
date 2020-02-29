import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog , QMessageBox

from MainWindow import CannyWindow
from Function_mendth import Canny_Clc
import cv2



# 创建图像分割检测窗口
class CannyWindow(QMainWindow, CannyWindow.Ui_CannyWindow):
    def __init__(self, parent=None):
        super(CannyWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.open_path = ''
        # 对图像边缘检测添加打开文件
        self.pushButton.clicked.connect(self.chooseFile)
        # 对图像边缘检测保存文件
        self.pushButton_2.clicked.connect(self.saveFile)
        # 对图像边缘检测添加操作
        self.pushButton_3.clicked.connect(lambda:self.clc_canny(self.open_path))

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

    # canny 边缘检测
    def clc_canny(self, path):
        image = cv2.imread(path)
        # 知道图片的路径
        filepath, fullflname = os.path.split(path)
        # 图片灰度化
        gray_pic = Canny_Clc.Gray_pic(image)
        # 使用高斯滤波器平滑图像
        gaussian_img, gaussian_img1 = Canny_Clc.Smooth(gray_pic)
        # 计算梯度的幅值和方向
        (dx, dy, M, theta) = Canny_Clc.Gradients(gaussian_img)
        # 非极大值抑制（NMS），细化边缘
        nms = Canny_Clc.NMS(M, dx, dy)
        # 双阈值选取，确定最终的边缘
        self.result = Canny_Clc.Double_threshold(nms)
        path1 = filepath + '/test.jpg'
        # 写入暂存文件，显示在frame_2上
        cv2.imwrite(path1, self.result)
        self.frame_2.setStyleSheet("border-image: url(" + path1 + ");")
        # 删除文件
        if os.path.exists(path1):
            os.remove(path1)