import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from MainWindow import MainWindow
from Class import EqualizationGrayscaleWindow, CannyWindow, SegmentationWindow, RegionalGrowthwindow, GeometricTransformationWindow
from Class import TwoValueWindow, FilterWindow

# 创建窗口主界面
class MyMainWindow(QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 主界面实例化，显示主界面
    mymainwindow = MyMainWindow()
    mymainwindow.show()
    # 均衡化、灰度化处理界面实例化
    equalizationWindow = EqualizationGrayscaleWindow.EqualizationGrayscaleWindow()
    # 图像的滤波器处理界面实例化
    filterwindow = FilterWindow.FilterWindow()
    # 图像的二值化处理界面实例化
    twovaluewindow = TwoValueWindow.TwoValueWindow()
    # 图像的几何处理界面实例化
    geometrictransformationWindow = GeometricTransformationWindow.GeometricTransformationWindow()
    # 全局、动态分割实例化
    segmentationwindow = SegmentationWindow.SegmentationWindow()
    # 区域生长、分水岭实例化
    regionalgrowthwindow = RegionalGrowthwindow.RegionalGrowthWindow()
    # canny边缘检测界面实例化
    cannywindow = CannyWindow.CannyWindow()

    '''***对菜单栏首页添加对应的跳转事件***'''
    main_btn = mymainwindow.menu
    main_btn.addAction(mymainwindow.show())

    '''***对菜单栏图像灰度化添加对应的跳转事件***'''
    main_graybtn = mymainwindow.action_3
    main_graybtn.triggered.connect(lambda:equalizationWindow.show())

    '''***对菜单栏图像均衡化添加对应的跳转事件***'''
    main_equalbtn = mymainwindow.action_4
    main_equalbtn.triggered.connect(lambda:equalizationWindow.show())

    '''***对菜单栏图像滤波器处理加对应的跳转事件***'''
    main_filterbtn = mymainwindow.menu_13
    main_filterbtn.triggered.connect(lambda: filterwindow.show())

    '''***对菜单栏图像二值化处理加对应的跳转事件***'''
    main_twovaluebtn = mymainwindow.menu_3
    main_twovaluebtn.triggered.connect(lambda: twovaluewindow.show())

    '''***对菜单栏图像几何处理加对应的跳转事件***'''
    main_Geometricbtn = mymainwindow.menu_4
    main_Geometricbtn.triggered.connect(lambda: geometrictransformationWindow.show())

    '''***对菜单栏图像分割(全局分割、动态分割)添加对应的跳转事件***'''
    main_all_div_btn = mymainwindow.action_8
    main_all_div_btn.triggered.connect(lambda: segmentationwindow.show())
    main_active_div_btn = mymainwindow.action_9
    main_active_div_btn.triggered.connect(lambda: segmentationwindow.show())
    '''***对菜单栏图像分割(区域生长、分水岭分割)添加对应的跳转事件***'''
    main_regionalgrowth_btn = mymainwindow.action_11
    main_regionalgrowth_btn.triggered.connect(lambda: regionalgrowthwindow.show())
    main_div_water_btn = mymainwindow.action_13
    main_div_water_btn.triggered.connect(lambda: regionalgrowthwindow.show())

    '''***对菜单栏图像边缘检测添加对应的跳转事件***'''
    main_cannybtn = mymainwindow.actioncanny
    main_cannybtn.triggered.connect(lambda: cannywindow.show())




    sys.exit(app.exec_())

