import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import copy as cp
import random
import math
import cv2
import collections

# 图片灰度化函数
def Gray_pic(image):
    # BGR 转换成 RGB 格式
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # 灰度化，根据人眼观察的效果
    gray_pic = np.dot(image_rgb[...,:3], [0.299, 0.587, 0.114])
    #将灰度级数组转化为unit8形式,否则opencv无法显示
    gray_pic=np.array(gray_pic,dtype='uint8') 
    return gray_pic

# 去除噪音 - 使用 5x5 的高斯滤波器
def Smooth(gray_pic):
    # 生成一个高斯滤波器
    sigma1 = sigma2 = 1
    gau_sum = 0
    gaussian = np.zeros([5, 5])
    for i in range(5):
        for j in range(5):
            gaussian[i, j] = math.exp((-1/(2*sigma1*sigma2))*(np.square(i-3) 
                                + np.square(j-3)))/(2*math.pi*sigma1*sigma2)
            gau_sum =  gau_sum + gaussian[i, j]
    # 归一化处理
    gaussian = gaussian / gau_sum
    # 高斯滤波
    W, H = gray_pic.shape
    gaussian_img = np.zeros([W-5, H-5])
    for i in range(W-5):
        for j in range(H-5):
            gaussian_img[i, j] = np.sum(gray_pic[i:i+5, j:j+5] * gaussian)  # 与高斯矩阵卷积实现滤波
    # 将灰度级数组转化为unit8形式,否则opencv无法显示
    gaussian_img1 = np.array(gaussian_img, dtype='uint8')
    return gaussian_img, gaussian_img1

# 计算梯度的幅值和方向
def Gradients(gaussian_img):
    W, H = gaussian_img.shape
    dx = np.zeros([W-1, H-1])   # x方向的渐变
    dy = np.zeros([W-1, H-1])   # y方向的渐变
    M = np.zeros([W-1, H-1])    # 梯度幅值
    theta = np.zeros([W-1, H-1])    # 梯度方向
    for i in range(W-1):
        for j in range(H-1):
            dx[i, j] = gaussian_img[i+1, j] - gaussian_img[i, j]
            dy[i, j] = gaussian_img[i, j+1] - gaussian_img[i, j]
             # 图像梯度幅值作为图像强度值
            M[i, j] = np.sqrt(np.square(dx[i, j]) + np.square(dy[i, j]))
            # 计算梯度方向  θ - artan(dx/dy)
            theta[i, j] = math.atan(dx[i, j] / (dy[i, j] + 0.000000001)) 
    return dx, dy, M, theta

#非极大值抑制（NMS）
def NMS(M, dx, dy):
    d = np.copy(M)
    W, H = M.shape
    NMS = np.copy(d)
    NMS[0, :] = NMS[W-1, :] = NMS[:, 0] = NMS[:, H-1] = 0
    for i in range(1, W-1):
        for j in range(1, H-1):
            # 如果当前梯度为0，该点就不是边缘点
            if M[i, j] == 0:
                NMS[i, j] = 0
            else:
                gradX = dx[i, j] # 当前点 x 方向导数
                gradY = dy[i, j] # 当前点 y 方向导数
                gradTemp = d[i, j] # 当前梯度点
                # 如果 y 方向梯度值比较大，说明导数方向趋向于 y 分量
                if np.abs(gradY) > np.abs(gradX):
                    weight = np.abs(gradX) / np.abs(gradY) # 权重
                    grad2 = d[i-1, j]
                    grad4 = d[i+1, j]
                    # 如果 x, y 方向导数符号一致
                    # 像素点位置关系
                    # g1 g2
                    #     c
                    #     g4 g3
                    if gradX * gradY > 0:
                        grad1 = d[i-1, j-1]
                        grad3 = d[i+1, j+1]
                    # 如果 x，y 方向导数符号相反
                    # 像素点位置关系
                    #      g2 g1
                    #      c
                    # g3 g4
                    else:
                        grad1 = d[i-1, j+1]
                        grad3 = d[i+1, j-1]
                # 如果 x 方向梯度值比较大
                else:
                    weight = np.abs(gradY) / np.abs(gradX)
                    grad2 = d[i, j-1]
                    grad4 = d[i, j+1]
                    # 如果 x, y 方向导数符号一致
                    # 像素点位置关系
                    #        g3
                    # g2 c g4
                    # g1
                    if gradX * gradY > 0:

                        grad1 = d[i+1, j-1]
                        grad3 = d[i-1, j+1]  
                    # 如果 x，y 方向导数符号相反
                    # 像素点位置关系
                    # g1
                    # g2 c g4
                    #         g3
                    else:
                        grad1 = d[i-1, j-1]
                        grad3 = d[i+1, j+1]
                # 利用 grad1-grad4 对梯度进行插值
                gradTemp1 = weight * grad1 + (1 - weight) * grad2
                gradTemp2 = weight * grad3 + (1 - weight) * grad4
                # 当前像素的梯度是局部的最大值，可能是边缘点
                if gradTemp >= gradTemp1 and gradTemp >= gradTemp2:
                    NMS[i, j] = gradTemp            
                else:
                    # 不可能是边缘点
                    NMS[i, j] = 0
    return NMS

# 双阈值选取
def Double_threshold(nms):
    W, H = nms.shape
    result_img = np.zeros([W, H])
    # 定义高低阈值
    TL = 0.2 * np.max(nms)
    TH = 0.3 * np.max(nms)
    for i in range(1, W-1):
        for j in range(1, H-1):
           # 双阈值选取
            if (nms[i, j] < TL):    # 小于低阈值的一定不是边缘
                result_img[i, j] = 0       
            elif (nms[i, j] > TH):  # 大于高阈值的一定是边缘
                result_img[i, j] = 255
           # 两个阈值之间的边缘，如果它们连接到真边缘像素，则它们就是边缘的一部分
            elif (nms[i-1, j-1:j+1] < TH).any() or (nms[i+1, j-1:j+1].any()
                    or (nms[i, [j-1, j+1]] < TH).any()):
                result_img[i, j] = 255
    return result_img 
