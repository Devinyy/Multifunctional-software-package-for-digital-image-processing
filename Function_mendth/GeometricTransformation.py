import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import copy as cp
import random
import math
import cv2
import collections

#按比例缩小
def DOWNRESIZE(gray , ratio=0.8) :
    height , width = gray.shape[0] , gray.shape[1]
    resize_width , resize_height = int(width * ratio) , int(height * ratio)
    resize_gray = np.zeros([resize_height,resize_width],np.uint8)   #创建一个和原图像 *缩小比例相同像素的空图
    stepsize = 1.0/ratio    #原图像的采集步长
    for i in range (0,resize_height) :
        for j in range (0,resize_width) :
            if i  == 0 and j == 0 :     #缩小图(0,0)地方的像素用原图(1,1)的地方代替
                resize_gray[i][j] = gray[1][1]
            else :      #缩小图其他地方的像素用此时原图对应的坐标-1的地方代替
                resize_gray[i][j] = gray[int(i*stepsize)-1][int(j*stepsize)-1]


    cv2.imshow("old",gray)
    cv2.imshow("Downresize",resize_gray)
    cv2.waitKey(0)
    return resize_gray




#按比例放大
def UPSIZE(gray , ratio=1.2) :
    height , width = gray.shape[0] , gray.shape[1]
    resize_width , resize_height = int(width * ratio) , int(height * ratio)
    resize_gray = np.zeros([resize_height,resize_width],np.uint8)
    """
    #最邻近插值法
    for i in range (0,resize_height) :
        for j in range (0,resize_width) :
            if i  == 0 and j == 0 :
                resize_gray[i][j] = gray[int(i/ratio)+1][int(j/ratio)+1]
            else :
                resize_gray[i][j] = gray[int(i/ratio)-1][int(j/ratio)-1]
    """
    #双线性插值
    for i in range (0,resize_height) :
        for j in range (0,resize_width) :
            x = i/ratio
            y = j/ratio
            p=(i+0.0)/ratio-x
            q=(j+0.0)/ratio-y
            x=int(x)-1
            y=int(y)-1
            if x+1<i and y+1<j:
                resize_gray[i,j]=int(gray[x,y]*(1-p)*(1-q)+gray[x,y+1]*q*(1-p)+gray[x+1,y]*(1-q)*p+gray[x+1,y+1]*p*q)

    cv2.imshow("old",gray)
    cv2.imshow("Upresize",resize_gray)
    cv2.waitKey(0)
    return resize_gray


#水平内凹
def CONCAVE(gray) :
    RANGE = 200
    height, width = gray.shape[0], gray.shape[1]
    resize_gray = np.zeros([height, width], np.uint8)
    for i in range(height):
        # 得到正弦波的波形，即j对应的起点
        temp = float((width- RANGE) * math.sin(((2 * math.pi * i) / height) / 2))
        for j in range (int(temp+0.5),int(width-temp)) :
            #每行非黑色区域的长度
            distance = int(width-temp) - int(temp+0.5)
            #缩小的倍率
            ratio = distance / width
            #取点的步长
            stepsize = 1.0/ratio
            #将同意行缩小相同倍率
            resize_gray[i][j] = gray[i][int((j-temp)*stepsize)-1]

    cv2.imshow("old", gray)
    cv2.imshow("Concave", resize_gray)
    cv2.waitKey(0)
    return resize_gray


#水平外凸
def CONVEX(gray) :
    RANGE = 150
    height, width = gray.shape[0], gray.shape[1]
    resize_gray = np.zeros([height, width], np.uint8)
    for i in range(height):
        # 得到正弦波的波形，即j对应的起点
        temp = float((width- RANGE) * math.sin(((2 * math.pi * i) / height) / 2))
        temp = 200 - temp
        for j in range (int(temp+0.5),int(width-temp)) :
            #每行非黑色区域的长度
            distance = int(width-temp) - int(temp+0.5)
            #缩小的倍率
            ratio = distance / width
            #取点的步长
            stepsize = 1.0/ratio
            #将同意行缩小相同倍率
            resize_gray[i][j] = gray[i][int((j-temp)*stepsize)]

    cv2.imshow("old", gray)
    cv2.imshow("Convex", resize_gray)
    cv2.waitKey(0)
    return resize_gray


#梯形形变
def TRAPEZOID(gray,k=0.3,transform='y') :
    height, width = gray.shape[0], gray.shape[1]
    resize_gray = np.zeros([height, width], np.uint8)
    if transform == 'x' :
        value = k*height
        for i in range (height) :
            temp = int( value - k * i ) 
            for j in range (temp,width-temp) :
                #每行非黑色区域的长度
                distance = int(width-temp) - int(temp+0.5)
                #缩小的倍率
                ratio = distance / width
                #取点的步长
                stepsize = 1.0/ratio
                #将同意行缩小相同倍率
                resize_gray[i][j] = gray[i][int((j-temp)*stepsize)]
    else :
        value = k*width
        for i in range (width) :
            temp = int( value - k * i ) 
            for j in range (temp,height-temp) :
                #每行非黑色区域的长度
                distance = int(height-temp) - int(temp+0.5)
                #缩小的倍率
                ratio = distance / height
                #取点的步长
                stepsize = 1.0/ratio
                #将同意列缩小相同倍率
                resize_gray[j][i] = gray[int((j-temp)*stepsize)][i]

    cv2.imshow("old", gray)
    cv2.imshow("Trapezoid", resize_gray)
    cv2.waitKey(0)
    return resize_gray


#直角三角形形变
def TRIANGLE(gray,k=0.5,transform='y') :
    height, width = gray.shape[0], gray.shape[1]
    resize_gray = np.zeros([height, width], np.uint8)
    if transform == 'x' :
        for i in range (height) :
            temp = int( k * i ) 
            for j in range (temp) :
                #每行非黑色区域的长度
                distance = temp
                #缩小的倍率
                ratio = distance / width
                #取点的步长
                stepsize = 1.0/ratio
                #将同意行缩小相同倍率
                resize_gray[i][j] = gray[i][int((j-temp)*stepsize)]
    else :
        k = height /(2*width) 
        value = k*width
        for i in range (width) :
            temp = int( value - k * i ) 
            for j in range (temp,height-temp) :
                #每行非黑色区域的长度
                distance = int(height-temp) - int(temp+0.5)
                #缩小的倍率
                ratio = distance / height
                #取点的步长
                stepsize = 1.0/ratio
                #将同意列缩小相同倍率
                resize_gray[j][i] = gray[int((j-temp)*stepsize)][i]

    cv2.imshow("old", gray)
    cv2.imshow("Triangle", resize_gray)
    cv2.waitKey(0)
    return resize_gray



#S形变
def SSHAPE(gray,RANGE=450) :
    height, width = gray.shape[0], gray.shape[1]
    resize_gray = np.zeros([height, width], np.uint8)
    for i in range(height):
        # 得到正弦波的波形，即j对应的起点
        temp = float((width - RANGE) / 2 + (width- RANGE) * math.sin((2 * math.pi * i) / height + math.pi) / 2)
        for j in range (int(temp+0.5),int(RANGE+temp)) :
            #映射关系
            m = int(((j-temp) * width / RANGE))
            if m >= width :
                m=width-1
            if m < 0 :
                m=0
            resize_gray[i,j]=gray[i,m]

    cv2.imshow("old", gray)
    cv2.imshow("Sshape", resize_gray)
    cv2.waitKey(0)
    return resize_gray



#图片旋转
def ROTATE(gray, ANGLE = 45,center=None, scale=1.0) :
    #将角度转化为弧度
    (height, width) = gray.shape[:2]
    (cX, cY) = (width // 2, height // 2)
 
    M = cv2.getRotationMatrix2D((cX, cY), -ANGLE, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    nW = int((height * sin) + (width * cos))
    nH = int((height * cos) + (width * sin))
 
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
 
    shuchu=cv2.warpAffine(gray, M, (nW, nH))

    cv2.imshow("old", gray)
    cv2.imshow("Rotate", shuchu)
    cv2.waitKey(0)
    return shuchu



#图片平移
def HORIZONTALMOVE(gray,move_x=10,move_y=10) :
    height, width = gray.shape[0], gray.shape[1]
    resize_gray = np.zeros([height, width], np.uint8)
    for i in range (height) :
        for j in range (width) :
            if i + move_x < height and j + move_y < width :
                resize_gray[i][j] = gray[i+move_x][j+move_y]
            else :
                resize_gray [i][j] = 0

    cv2.imshow("old", gray)
    cv2.imshow("Horizeontalmove", resize_gray)
    cv2.waitKey(0)
    return resize_gray

#图片翻转
def FLIP(gray, transformmethod):
    height, width = gray.shape[0], gray.shape[1]
    resize_gray = np.zeros([height, width], np.uint8)
    # 如果按 x 翻转
    if transformmethod == 'x':
        for i in range (height) :
            for j in range (width) :
                resize_gray[i][j] = gray[i][319-j]

        cv2.imshow("old", gray)
        cv2.imshow("FLIP-x", resize_gray)
        cv2.waitKey(0)
        return resize_gray

    # 如果按 y 翻转
    else :
        for i in range (height) :
            for j in range (width) :
                resize_gray[i][j] = gray[279-i][j]

        cv2.imshow("old", gray)
        cv2.imshow("FLIP-y", resize_gray)
        cv2.waitKey(0)
        return resize_gray


