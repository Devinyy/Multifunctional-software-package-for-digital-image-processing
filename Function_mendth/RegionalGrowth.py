import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import copy as cp
import random
import math
import cv2
import collections

#使用otsu算法思维求出阈值并对图像进行二值化处理
def myotsu(gray):
    countdown = 0
    countup = 0
    hist_new = []
    num = []
    hist_countresult = []
    hist_key = []
    hist_proresult = []
    #处理后最终输出矩阵将齐大小设置为与原图一样
    gray2=np.array([[0 for i in range(gray.shape[1])] for i in range(gray.shape[0])], dtype='float') 
    #gray1 用于统计每哥灰度级所有的个数 ，因为是列表不是矩阵，
    #所以要先将gray的灰度级矩阵变成一维列表
    gray1 = list(gray.ravel())
    #以字典的形式保存，统计出来的灰度级及其个数
    obj = dict(collections.Counter(gray1))
    obj = sorted(obj.items(),key=lambda item:item[0])
    #将统计出来的灰度级的值与他的个数分开用列表保存
    for each in obj :
        key = list(each)[0]
        num =list(each)[1]
        hist_key.append(key)
        hist_new.append(num)
    #检查从0-255每个灰度级是否都有个数，没有的话添加并将值设为0
    for i in range (0,256) :
        if i in hist_key :
            num = hist_key.index(i)
            hist_countresult.append(hist_new[num])
        else :
            hist_countresult.append(0)
    if len(hist_countresult) < 256 :
        for i in range (0,256-len(hist_countresult)) :
            hist_new.append(0)
    #计算整幅图的像素数目
    hist_sum = gray.shape[0] * gray.shape[1]
    #计算每个灰度级的像素数目占整个数目的比重
    for each in hist_countresult :
        result = float(each / hist_sum)
        hist_proresult.append(result)
    #遍历灰度级[0,255],寻找合适的threshold
    w0 = w1 = u0tmp = u1tmp = u0 = u1 = deltaTmp = deltaMax = float(0)
    for i in range (256) :
        w0 = w1 = u0tmp = u1tmp = u0 = u1 = deltaTmp = float(0)
        for j in range (256) :
            if j <= i : #背景部分
                w0 = float(w0 + hist_proresult[j])
                u0tmp += j * hist_proresult[j]
            else :  #前景部分
                w1 += float(hist_proresult[j])
                u1tmp += j * hist_proresult[j]
        if w0 == 0.0 or w1 == 0.0:
            pass
        else :
            u0 = float(u0tmp / w0)
            u1 = float(u1tmp / w1)
            deltaTmp = (float)(w0 *w1* pow((u0 - u1), 2)) 
            if deltaTmp > deltaMax : 
                deltaMax = deltaTmp
                threshold = i
    #用ostu大津算法得出最适当的阈值后，将图片进行二值化
    for i in range(gray.shape[0]) :
        for j in range(gray.shape[1]) :
             #对大于阈值的显示为255白色，小于阈值的显示为0黑色
            if gray[i][j] <= threshold :
                gray2[i][j] = 0
                countdown += 1
            else :
                gray2[i][j] = 255
                countup += 1
    return gray2

#分割成为多块区域
def divide(gray,m,n) :
    height,width = gray.shape[0],gray.shape[1]
    each_width = int(width / (m-1))
    each_height = int(height / (n-1))
    #生成存放16块图像灰度值的列表
    divide_list = []
    for i in range (m-1) :
        for j in range (n-1):
            #生成存放每块小图片灰度级的矩阵
            divide_image = np.array([[0 for i in range(each_width)] for i in range(each_height)], dtype=np.uint8) 
            for divide_i in range (each_height):
                for divide_j in range (each_width) :
                    divide_image[divide_i][divide_j] = gray[ i*each_height + divide_i ][ j*each_width + divide_j]
            divide_list.append(divide_image)
    return divide_list

#求两个点的差值
def getGrayDiff(image,currentPoint,tmpPoint):
    return abs(int(image[currentPoint[0],currentPoint[1]]) - int(image[tmpPoint[0],tmpPoint[1]]))

#区域生长算法
def regional_growth (gray,seeds,threshold=15) :
    #每次区域生长的时候的种子像素之间的八个邻接点
    connects = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), \
                        (0, 1), (-1, 1), (-1, 0)]    
    threshold = threshold #种子生长时候的相似性阈值，默认即灰度级不相差超过15以内的都算为相同
    height, weight = gray.shape
    seedMark = np.zeros(gray.shape)
    seedList = []
    for seed in seeds:
        seedList.append(seed)   #将种子添加到种子的列表中
    label = 255	#标记点的flag
    while(len(seedList)>0):     #如果种子列表里还存在种子点
        currentPoint = seedList.pop(0)  #将最前面的那个种子抛出
        seedMark[currentPoint[0],currentPoint[1]] = label   #将对应位置的点标志为1
        for i in range(8):  #对这个种子点周围的8个点一次进行相似性判断
            tmpX = currentPoint[0] + connects[i][0]
            tmpY = currentPoint[1] + connects[i][1]
            if tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= weight:    #如果超出限定的阈值范围
                continue    #跳过并继续
            grayDiff = getGrayDiff(gray,currentPoint,(tmpX,tmpY))   #计算此点与种子像素点的灰度级之差
            if grayDiff < threshold and seedMark[tmpX,tmpY] == 0:
                seedMark[tmpX,tmpY] = label
                seedList.append((tmpX,tmpY))
    return seedMark

