import cv2
import matplotlib.pyplot as plt
import copy
import numpy as np

from src import model
from src import util
from src.body import Body
from src.hand import Hand

#一共18个关键点，18个点的颜色
colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0], [0, 255, 0], \
          [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255], \
          [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]

body_estimation = Body('model/body_pose_model.pth')

# test_image = 'images/demo.jpg'
#test_image = 'images/test3.jpg'
test_image = 'images/sit3.jpg'



oriImg = cv2.imread(test_image)  # B,G,R order
candidate, subset = body_estimation(oriImg)
canvas = copy.deepcopy(oriImg)
#canvas = util.draw_bodypose(canvas, candidate, subset)

# subset 的 shape 为 (n, 20)，其中 n 为检测到了 n 个人体， 
# 20 为 20个不同的部位点
# subset[n][i] 表示 第 n 个人的编号为 i 的关键点在 candidate 中的索引，
# 如果 -1 则表示这个人的这个点不在图中


# 0 鼻子 1脖子  2右肩 5左肩 3右肘 6左肘 4右腕 7左腕 8左髋kuan  11右髋 9,12左右膝 
# 主要用这几个点 2右肩  5左肩 14右眼 15左眼 16右耳 17左耳


#point_index_list = [2, 5, 14, 15]   #点的索引列表
point_index_list = [2, 5, 14, 15, 8, 11]

import math
# 计算两点间距离公式
def distance_liangdian(x1, y1, x2, y2):
    d = math.sqrt( (x1-x2)**2 + (y1-y2)**2  )
    # print(d)
    return(d)


# 这里选择要画哪些人
""" 原始的
for n in range(len(subset)):
    print("第 %d 个人" % n)
    # 这里选择要画哪些关键点
    for i in point_index_list:
        index = int(subset[n][i])
        if index == -1:     #点不存在时
            continue
        x, y = candidate[index][0:2]
        cv2.circle(canvas, (int(x), int(y)), 4, colors[i], thickness=-1)
        print(x, y) 
"""
for n in range(len(subset)):
    print("第 %d 个人" % (n+1))
    # 这里选择要画哪些关键点
    for i in point_index_list:
        index = int(subset[n][i])
        if index == -1:
            continue
        
        x, y = candidate[index][0:2]
        cv2.circle(canvas, (int(x), int(y)), 4, colors[i], thickness=-1)
        #cv2.circle(image, center_coordinates, radius, color, thickness)
        #image:它是要在其上绘制圆的图像。
        # (int(x), int(y))它是圆的中心坐标。坐标表示为两个值的元组，
        # 即(X坐标值，Y坐标值)。
        # 4 是圆的半径。
        # colors[i] 是要绘制的圆的边界线的颜色。对于BGR，
        # 我们通过一个元组。例如：(255，0，0)为蓝色。
        # thickness:它是圆边界线的粗细像素。厚度-1像素将以指定的颜色填充矩形形状。
        
        # print(x, y)
        # 2右肩  5左肩 14右眼 15左眼 
        if i==2:
            x_zuojian = x
            y_zuojian = y
            print("左肩：%d, %d" %(x_zuojian,y_zuojian) )
        if i==5:
            x_youjian = x
            y_youjian = y
            print("右肩：%d, %d" %(x_youjian,y_youjian) )
        if i==14:
            x_zuoyan = x
            y_zuoyan = y
            print("左眼：%d, %d" %(x_zuoyan,y_zuoyan) )
        if i==15:
            x_youyan = x
            y_youyan = y
            print("右眼：%d, %d" %(x_youyan,y_youyan) )

    if (y_zuojian - y_youjian) >3:
        print("身体左倾")
    elif (y_youjian - y_zuojian) >3:
        print("身体右倾")
    elif (y_zuoyan - y_youyan) >3:
        print("头部右倾")
    elif (y_youyan - y_zuoyan) >3:
        print("头部左倾")
    else:
        print("坐姿标准！")

    print("左右肩的距离: ",int(distance_liangdian(x_youjian,y_youjian, 
                        x_zuojian, y_zuojian)))        
    print("左右眼的距离: ",int(distance_liangdian(x_youyan,y_youyan, 
                        x_zuoyan, y_zuoyan)))

    if index == -1:
            continue





cv2.imshow("image", canvas)
cv2.waitKey(0)
