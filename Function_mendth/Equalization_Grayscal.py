import numpy as np
import collections

def clczhifangtu(gray):
    # 计算彩色图单通道的直方图
    hist_new = []
    num = []
    hist_result = []
    hist_key = []
    gray1 = list(gray.ravel())
    obj = dict(collections.Counter(gray1))
    obj = sorted(obj.items(),key=lambda item:item[0])

    for each in obj :
        hist1 = []
        key = list(each)[0]
        each =list(each)[1]
        hist_key.append(key)
        hist1.append(each)
        hist_new.append(hist1)
    for i in range (0,256) :
        if i in hist_key :
            num = hist_key.index(i)
            hist_result.append(hist_new[num])
        else :
            hist_result.append([0])
    if len(hist_result) < 256 :
        for i in range (0,256-len(hist_result)) :
            hist_new.append([0])
    hist_result = np.array(hist_result)
    return hist_result

#单通道均衡化
def clcresult(hist_new, lut, gray):
    sum = 0
    Value_sum = []
    hist1 = []
    binValue = []

    for hist1 in hist_new:
        for j in hist1:
            binValue.append(j)
            sum += j
            Value_sum.append(sum)

    min_n = min(Value_sum)
    max_num = max(Value_sum)

    # 生成查找表
    for i, v in enumerate(lut):
        lut[i] = int(254.0 * Value_sum[i] / max_num + 0.5)

    # 计算
    result = lut[gray]
    return result

#获取红色通道：

def get_red(img):
    redImg = img[:, :, 2]
    return redImg

#获取绿色通道：

def get_green(img):
    greenImg = img[:, :, 1]
    return greenImg

#获取蓝色通道

def get_blue(img):
    blueImg = img[:, :, 0]
    return blueImg





