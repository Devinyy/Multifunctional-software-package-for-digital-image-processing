import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog , QMessageBox

from MainWindow import GeometricTransformationWindow
from Function_mendth import GeometricTransformation

import cv2



# 创建灰度化和均衡化窗口
class GeometricTransformationWindow(QMainWindow, GeometricTransformationWindow.Ui_GeometricTransformationWindow):
    def __init__(self, parent=None):
        super(GeometricTransformationWindow, self).__init__(parent)
        self.setupUi(self)
        self.cwd = os.getcwd()  # 获取当前程序文件位置
        self.open_path = ''
        # 对均衡化按钮添加打开文件
        self.pushButton.clicked.connect(self.chooseFile)
        # 对均衡化按钮添加保存文件
        self.pushButton_2.clicked.connect(self.saveFile)
        # 对执行按钮添加操作
        self.pushButton_3.clicked.connect(lambda:self.clc_transform(self.open_path))

    # 打开文件函数，并将路径写入框内
    def chooseFile(self):

        fileName_choose, typefile = QFileDialog.getOpenFileName(self,"选取文件",
                                                     self.cwd,  # 起始路径
                                                     "All Files (*);;Text Files (*.txt)")# 设置文件扩展名过滤,用双分号间隔
        if fileName_choose == "":
            return
        self.lineEdit.setText(fileName_choose)
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

    # 根据所选功能进行调用相应函数进行运算
    def clc_transform(self,path):
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        select = self.lineEdit_11.text()
        if select == '' :
            QMessageBox.information(self, '温馨提醒', '尚未选择功能!', QMessageBox.Ok)
        elif select == '1' :
            if self.lineEdit_4.text()== '':
                ratio = 0.8
            else:
                ratio = float (self.lineEdit_4.text())
            self.result = GeometricTransformation.DOWNRESIZE(gray, ratio)

        elif select == '2' :
            if self.lineEdit_3.text()== '':
                ratio = 1.2
            else:
                ratio = float (self.lineEdit_3.text())
            self.result = GeometricTransformation.UPSIZE(gray, ratio)

        elif select == '3' :
            self.result = GeometricTransformation.CONCAVE(gray)

        elif select == '4':
            self.result = GeometricTransformation.CONVEX(gray)

        elif select == '5':
            if self.lineEdit_5.text()== '':
                k = 0.2
            else:
                k = float (self.lineEdit_5.text())
            if self.lineEdit_6.text()== '':
                transform = 'y'
            else:
                transform = str(self.lineEdit_6.text())
            self.result = GeometricTransformation.TRAPEZOID(gray, k, transform)
        elif select == '6':
            if self.lineEdit_12.text()== '':
                k = 0.2
            else:
                k = float (self.lineEdit_12.text())
            if self.lineEdit_13.text()== '':
                transform = 'y'
            else:
                transform = str(self.lineEdit_13.text())
            self.result = GeometricTransformation.TRIANGLE(gray, k, transform)
        elif select == '7':
            if self.lineEdit_14.text()== '':
                RANGE = 250
            else:
                RANGE = float(self.lineEdit_14.text())
            self.result = GeometricTransformation.SSHAPE(gray,RANGE)
        elif select == '8':
            if self.lineEdit_7.text()== '':
                RANGE = 45
            else:
                RANGE = float(self.lineEdit_7.text())
            self.result = GeometricTransformation.ROTATE(gray,RANGE)
        elif select == "9" :
            if self.lineEdit_8.text() != '':
                move_x = int(self.lineEdit_8.text())
            else :
                move_x = 10
            if self.lineEdit_9.text() != '':
                move_y = int(self.lineEdit_9.text())
            else :
                move_y = 10
            self.result = GeometricTransformation.HORIZONTALMOVE(gray,move_x,move_y)
        elif select == "10" :
            if self.lineEdit_10.text() != '':
                transformmethod = str(self.lineEdit_10.text())
            else :
                transformmethod = 'y'
            self.result = GeometricTransformation.FLIP(gray,transformmethod)