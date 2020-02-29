import numpy as np
import copy as cp
import random
import cv2

#向图片中添加椒盐噪声
def salt_pepper_noise(image,prob) :          #prob:盐噪声阈值，由用户自己决定
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob                                    #胡椒噪声阈值
    for i in range(image.shape[0]):               #遍历整个图片的灰度级
        for j in range(image.shape[1]):
            randomnum = random.random()      #生成一个随机0-1之间的随机数
            if randomnum < prob:           #如果随机数大于盐噪声阈值0.1，则将此位置灰度级的值设为0，即添加盐噪声
                output[i][j] = 0                 
            elif randomnum > thres:        #如果随机数大于胡椒噪声阈值1-0.1，则将此位置灰度级的输出设为255，即添加胡椒噪声
                output[i][j] = 255             
            else:                                    #如果随机数处于两者之间，则此位置的灰度级的值等于原图的灰度级值
                output[i][j] = image[i][j]
    return output

#向图片中添加高斯噪声
def gasuss_noise(image, mean=0, var=0.001):         # mean : 均值，var : 方差
    image = np.array(image/255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)     #使用numpy库中的函数生成正态分布矩阵，对应数据分别为概率均值，概率标准差，图像的大小
    output = image + noise         #输出结果为原图灰度级概率与噪声概率相加
    output_handle=np.array([[[0]*3 for i in range(output.shape[1])] for i in range(output.shape[0])], dtype=float)        #处理后最终输出矩阵将齐大小设置为与原图一样
    if output.min() < 0:        #确定一个比较中间值
        low_clip = -1.
    else:
        low_clip = 0.
    for i in range (output.shape[0]):       #遍历整个三位矩阵
        for j in range (output.shape[1]):       
            for k in range (output.shape[2]):
                if output[i][j][k] < low_clip:              #将输出的概率矩阵内的值限定在(-1,1)范围内
                    output_handle[i][j][k] = low_clip   #使其之后*255变为灰度级时不会超出[0-255]的范围
                elif output[i][j][k] > 1.0:
                    output_handle[i][j][k] = 1.0
                else:
                    output_handle[i][j][k] = output[i][j][k]    #在最大值和最小值之间的不变
    output = np.uint8(output_handle*255)   #将处理后的灰度级转化为[0-255]的整数级
    return output

#向图片中添加加性噪声
def addrandom_noise(image,prob=0.1): 
    output = cp.deepcopy(image)           #将原始图像数据拷贝至输出矩阵
    n = random.randint(1,1000) + int(prob*20000)  
    for k in range (n-500) :
        a = random.randint(0,50)
        b = random.randint(0,50)
        c = random.randint(0,50)
        i = random.randint(0,image.shape[0]-1)
        j = random.randint(0,image.shape[1]-1)
        output[i][j][0] = 255-a
        output[i][j][1] = 255-b
        output[i][j][2] = 255-c
    for k in range (n) :
        a = random.randint(0,50)
        b = random.randint(0,50)
        c = random.randint(0,50)
        i = random.randint(0,image.shape[0]-1)
        j = random.randint(0,image.shape[1]-1)
        output[i][j][0] = a
        output[i][j][1] = b
        output[i][j][2] = c
    return output

#滤波处理前填充灰度级矩阵
def expand(image,expandsize=3):  
    imageshape = image.shape
    if expandsize == 3 :        #如果均值根据3*3模版 则sizei为3
        outputshape = (imageshape[0]+2,imageshape[1]+2)
        output = np.zeros(outputshape,np.uint8)
        #直接填充相同的内容
        for i in range (1,output.shape[0]-1):
            for j in range (1,output.shape[1]-1):
                output[i][j] = cp.deepcopy(image[i-1][j-1])
        #填充上下边缘
        for i in (0,outputshape[0]-1) :
            for j in range(1,output.shape[1]-1):
                if i == 0:
                    output[i][j] = cp.deepcopy(image[i][j-1])
                else:
                    output[i][j] = cp.deepcopy(image[i-2][j-1])
        #填充左右边缘
        for j in (0,output.shape[1]-1):
            for i in range (1,output.shape[0]-1):
                if j == 0:
                    output[i][j] = cp.deepcopy(image[i-1][j])
                else:
                    output[i][j] = cp.deepcopy(image[i-1][j-2])
        #填充四个角
        output[0][0] = cp.deepcopy(output[1][1])  #左上
        output[0][outputshape[1]-1] = cp.deepcopy(output[1][outputshape[1]-2])   #右上
        output[outputshape[0]-1][0] = cp.deepcopy(output[outputshape[0]-2][1])   #左下
        output[outputshape[0]-1][outputshape[1]-1] = cp.deepcopy(output[outputshape[0]-2][outputshape[1]-2])     #右下
    if expandsize == 5 :        #如果使用5*5模版则需要扩容两次
        output = expand(image,expandsize=3)
        output = expand(output,expandsize=3)
    return output

#中值滤波 a为要处理的图像  windowsize为采用的模版大小
def medianfliter(a,output,windowsize):
    if windowsize == 3 :
        output1 = np.zeros(a.shape,np.uint8)
        for i in range (1,output.shape[0]-1):       #求齐周围9个方格与模版进行冒泡排序
            for j in range (1,output.shape[1]-1):
                value1 = [output[i-1][j-1],output[i-1][j],output[i-1][j+1],output[i][j-1],output[i][j],output[i][j+1],output[i+1][j-1],output[i+1][j],+output[i+1][j+1]]
                value1.sort()   #对这九个数进行排序
                value = value1[4]    #中值为排序后中间这个数的正中间
                output1[i-1][j-1] = value
    elif windowsize == 5:
        output1 = np.zeros(a.shape,np.uint8)
        for i in range (2,output.shape[0]-2):       #求齐周围25个方格与模版进行卷积
            for j in range (2,output.shape[1]-2):
                value1 = [output[i-2][j-2],output[i-2][j-1],output[i-2][j],output[i-2][j+1],output[i-2][j+2],output[i-1][j-2],output[i-1][j-1],output[i-1][j],output[i-1][j+1],\
                            output[i-1][j+2],output[i][j-2],output[i][j-1],output[i][j],output[i][j+1],output[i][j+2],output[i+1][j-2],output[i+1][j-1],output[i+1][j],output[i+1][j+1],\
                            output[i+1][j+2],output[i+2][j-2],output[i+2][j-1],output[i+2][j],output[i+2][j+1],output[i+2][j+2]]
                value1.sort()   #对这九个数进行排序
                value = value1[12]    #中值为排序后中间这个数的正中间
                output1[i-2][j-2] = value   #将计算结果填入原本位置
    else :  
        print('模版大小输入错误，请输入3或5，分别代表3*3或5*5模版！')
    return output1

#均值滤波 a为要处理的图像  windowsize为采用的模版大小
def meanflite(a,output,windowsize):
    if windowsize == 3 :
        window = np.ones((3, 3)) / 3 ** 2  #生成3*3模版
        output1 = np.zeros(a.shape,np.uint8)
        for i in range (1,output.shape[0]-1):       #求齐周围9个方格与模版进行卷积
            for j in range (1,output.shape[1]-1):
                value = (output[i-1][j-1]*window[0][0]+output[i-1][j]*window[0][1]+output[i-1][j+1]*window[0][2]+\
                            output[i][j-1]*window[1][0]+output[i][j]*window[1][1]+output[i][j+1]*window[1][2]+\
                            output[i+1][j-1]*window[2][0]+output[i+1][j]*window[2][1]+output[i+1][j+1]*window[2][2])
                output1[i-1][j-1] = value   #将计算结果填入原本位置
    elif windowsize == 5:
        window = np.ones((5, 5)) / 5 ** 2  #生成5*5模版
        output1 = np.zeros(a.shape,np.uint8)
        for i in range (2,output.shape[0]-2):       #求齐周围25个方格与模版进行卷积
            for j in range (2,output.shape[1]-2):
                value = (output[i-2][j-2]*window[0][0]+output[i-2][j-1]*window[0][1]+output[i-2][j]*window[0][2]+output[i-2][j+1]*window[0][3]+output[i-2][j+2]*window[0][4]+\
                            output[i-1][j-2]*window[1][0]+output[i-1][j-1]*window[1][1]+output[i-1][j]*window[1][2]+output[i-1][j+1]*window[1][3]+output[i-1][j+2]*window[1][4]+\
                            output[i][j-2]*window[2][0]+output[i][j-1]*window[2][1]+output[i][j]*window[2][2]+output[i][j+1]*window[2][3]+output[i][j+2]*window[2][4]+\
                            output[i+1][j-2]*window[3][0]+output[i+1][j-1]*window[3][1]+output[i+1][j]*window[3][2]+output[i+1][j+1]*window[3][3]+output[i+1][j+2]*window[3][4]+\
                            output[i+2][j-2]*window[4][0]+output[i+2][j-1]*window[4][1]+output[i+2][j]*window[4][2]+output[i+2][j+1]*window[4][3]+output[i+2][j+2]*window[4][4])
                output1[i-2][j-2] = value   #将计算结果填入原本位置
    else :  
        print('模版大小输入错误，请输入3或5，分别代表3*3或5*5模版！')
    
    return output1

def main():
    image = cv2.imread(r'D:/Code/Python/2.jpg')
    cv2.imshow('old_pic',image)    #原图
    salt_pepper_noise_pic = salt_pepper_noise(image,prob=0.01)  #添加椒盐噪声
    cv2.imshow('salt_pepper_noise_pic',salt_pepper_noise_pic)

    gasuss_noise_pic = gasuss_noise(image,mean=0,var=0.01)  #添加高斯噪声
    cv2.imshow('gasuss_noise',gasuss_noise_pic)

    addrandom_noise_pic = addrandom_noise(image,prob=0.05)  #添加加性随机噪声
    cv2.imshow('add_noise',addrandom_noise_pic)

    """*******************************"""
    """```##```椒盐噪声处理```##```"""
    """*******************************"""
    
    (sp_b,sp_g,sp_r) = cv2.split(salt_pepper_noise_pic)  # 椒盐噪音通道分离
    """##```按3*3模版扩充```##"""
    expandb_result = expand(sp_b,3)    #对每个通道进行填充最近值操作
    expandg_result = expand(sp_g,3)    #对每个通道进行填充最近值操作
    expandr_result = expand(sp_r,3)    #对每个通道进行填充最近值操作
    """均值滤波器处理"""
    #进行3*3卷积计算均值
    #对椒盐噪声使用均值滤波器分别对三个通道对填充后的灰度级进行卷积
    convert_3b_meanresult = meanflite(sp_b,expandb_result,3)
    convert_3g_meanresult = meanflite(sp_g,expandg_result,3)
    convert_3r_meanresult = meanflite(sp_r,expandr_result,3)
    #合并通道
    convert_3_meanresult = cv2.merge([convert_3b_meanresult,convert_3g_meanresult,convert_3r_meanresult])
    cv2.imshow('sp_noise_mean_3*3_pic',convert_3_meanresult)       
    """中值滤波器处理""" 
    #进行3*3计算中值
    #使用中值滤波器分别对三个通道对填充后的灰度级进行卷积
    convert_3b_medianresult = medianfliter(sp_b,expandb_result,3)
    convert_3g_medianresult = medianfliter(sp_g,expandg_result,3)
    convert_3r_medianresult = medianfliter(sp_r,expandr_result,3)
    convert_3_medianresult = cv2.merge([convert_3b_medianresult,convert_3g_medianresult,convert_3r_medianresult])
    cv2.imshow('sp_noise_median_3*3_pic',convert_3_medianresult)       
    """##```按5*5模版扩充```##"""
    expandb_result = expand(sp_b,5)    #对每个通道进行两次填充最近值操作
    expandg_result = expand(sp_g,5)    #对每个通道进行两次填充最近值操作
    expandr_result = expand(sp_r,5)    #对每个通道进行两次填充最近值操作
    """均值滤波器处理"""
    #进行5*5卷积计算均值
    #使用均值滤波器分别对三个通道对填充后的灰度级进行卷积
    convert_5b_meanresult = meanflite(sp_b,expandb_result,5)
    convert_5g_meanresult = meanflite(sp_g,expandg_result,5)
    convert_5r_meanresult = meanflite(sp_r,expandr_result,5)
    #合并通道
    convert_5_meanresult = cv2.merge([convert_5b_meanresult,convert_5g_meanresult,convert_5r_meanresult])
    cv2.imshow('sp_noise_mean_5*5_pic',convert_5_meanresult)          
    """中值滤波器处理"""
    #进行5*5计算中值
    #使用中值滤波器分别对三个通道对填充后的灰度级进行卷积
    convert_5b_medianresult = medianfliter(sp_b,expandb_result,5)
    convert_5g_medianresult = medianfliter(sp_g,expandg_result,5)
    convert_5r_medianresult = medianfliter(sp_r,expandr_result,5)
    convert_5_medianresult = cv2.merge([convert_5b_medianresult,convert_5g_medianresult,convert_5r_medianresult])
    cv2.imshow('sp_noise_median_5*5_pic',convert_5_medianresult)       

    """*******************************"""
    """```##```高斯噪声处理```##```"""
    """*******************************"""

    (gs_b,gs_g,gs_r) = cv2.split(gasuss_noise_pic)  # 高斯噪声通道分离
    """##```按3*3模版扩充```##"""
    expand_gs_b_result = expand(gs_b,3)    #对每个通道进行填充最近值操作
    expand_gs_g_result = expand(gs_g,3)    #对每个通道进行填充最近值操作
    expand_gs_r_result = expand(gs_r,3)    #对每个通道进行填充最近值操作
    """均值滤波器处理"""
    #进行3*3卷积计算均值
    #对高斯噪声使用均值滤波器分别对三个通道对填充后的灰度级进行卷积
    convert_gs_3b_meanresult = meanflite(gs_b,expand_gs_b_result,3)
    convert_gs_3g_meanresult = meanflite(gs_g,expand_gs_g_result,3)
    convert_gs_3r_meanresult = meanflite(gs_r,expand_gs_r_result,3)
    #合并通道
    convert_gs_3_meanresult = cv2.merge([convert_gs_3b_meanresult,convert_gs_3g_meanresult,convert_gs_3r_meanresult])
    cv2.imshow('gs_noise_mean_3*3_pic',convert_gs_3_meanresult)       
    """中值滤波器处理""" 
    #进行3*3计算中值
    #使用中值滤波器分别对三个通道对填充后的灰度级进行卷积
    convert_gs_3b_medianresult = medianfliter(gs_b,expand_gs_b_result,3)
    convert_gs_3g_medianresult = medianfliter(gs_g,expand_gs_g_result,3)
    convert_gs_3r_medianresult = medianfliter(gs_r,expand_gs_r_result,3)
    convert_gs_3_medianresult = cv2.merge([convert_gs_3b_medianresult,convert_gs_3g_medianresult,convert_gs_3r_medianresult])
    cv2.imshow('gs_noise_median_3*3_pic',convert_gs_3_medianresult)      
    """##```按5*5模版扩充```##"""
    expand_gs_b_result = expand(gs_b,5)    #对每个通道进行两次填充最近值操作
    expand_gs_g_result = expand(gs_g,5)    #对每个通道进行两次填充最近值操作
    expand_gs_r_result = expand(gs_r,5)    #对每个通道进行两次填充最近值操作
    """均值滤波器处理"""
    #进行5*5卷积计算均值
    #使用均值滤波器分别对三个通道对填充后的灰度级进行卷积
    convert_gs_5b_meanresult = meanflite(gs_b,expand_gs_b_result,5)
    convert_gs_5g_meanresult = meanflite(gs_g,expand_gs_g_result,5)
    convert_gs_5r_meanresult = meanflite(gs_r,expand_gs_r_result,5)
    #合并通道
    convert_gs_5_meanresult = cv2.merge([convert_gs_5b_meanresult,convert_gs_5g_meanresult,convert_gs_5r_meanresult])
    cv2.imshow('gs_noise_mean_5*5_pic',convert_gs_5_meanresult)          
    """中值滤波器处理"""
    #进行5*5计算中值
    #使用中值滤波器分别对三个通道对填充后的灰度级进行卷积
    convert_gs_5b_medianresult = medianfliter(gs_b,expandb_result,5)
    convert_gs_5g_medianresult = medianfliter(gs_g,expandg_result,5)
    convert_gs_5r_medianresult = medianfliter(gs_r,expandr_result,5)
    convert_gs_5_medianresult = cv2.merge([convert_gs_5b_medianresult,convert_gs_5g_medianresult,convert_gs_5r_medianresult])
    cv2.imshow('gs_noise_median_5*5_pic',convert_gs_5_medianresult)       

    cv2.waitKey(0)

if __name__ == "__main__":
    main()