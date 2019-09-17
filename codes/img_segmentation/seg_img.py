import sys
#sys.path.insert(1,'/usr/local/opencv/opencv-2.4.11/lib/python2.7/site-packages')
import cv2
import numpy as np
import ccl
from cropped_img import Cropped_image
'''a function import a image and invoking KNN to start image segmatation 
'''

#this pretty much same as task2.py from task
#the different is remove the write method and 
#the criterion of find the numbers
def seg_number(img):
    segNums =[]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    height, width = th.shape
    labels = np.zeros((height, width), dtype=int)

    equ_lables = []

    label = 1

    for i in range(height):
        for j in range(width):
            if th[i][j] == 0:
                label = ccl.first_pass(i, j, label, labels, equ_lables, height, width)

    result_labels = ccl.check_labels(equ_lables)

    for i in range(len(result_labels)):
        result_labels[i].sort()

    ys, xs = np.nonzero(labels)

    ccl.second_pass(labels, result_labels, ys, xs)
    sec_labels = []
    for j in result_labels:
        sec_labels.append(j[0])

    points = ccl.get_Points(sec_labels, labels, ys, xs)

    obj_list = []
    for z in range(len(points)):
        height1 = points[z][1] - points[z][0]
        cropped_image = Cropped_image(points[z], height1)
        obj_list.append(cropped_image)

    obj_list.sort(cmp=None, key=lambda x: x.height, reverse=True)
    num_temp=[]
    num_list = []
	#the cropped image may have big barcode line on the top,so any blob
	#height =0 does not treat 
    for i in range(0, len(obj_list)):
        if obj_list[i].get_points()[0]!=0 and obj_list[i].get_points()[2]!=0:
                num_temp.append(obj_list[i])
    num_temp.sort(cmp=None, key=lambda x: x.points[2])
    length=0
    #if there is no more than 13 blob, just pick up all blobs
    if len(num_temp)>13:
        length = 13
    else:
        length = len(num_temp)

	
    for l in range(0,length):
        num_list.append(num_temp[l])
	#crop each numbers and insert to a list 
    num = 1
    for obj in num_list:
        # print(obj.get_points()[0])
        y1 = obj.get_points()[0] - 2
        y2 =obj.get_points()[1] + 2
        x1 =obj.get_points()[2] - 2
        x2 = obj.get_points()[3] + 2
        if y1<0:
            y1= 0
        if y2>height:
            y2 = height
        if x1 <0:
            x1= 0
        if x2>width:
            x2=width
        crop = img[y1 :y2 ,x1:x2]
        segNums.append(crop)

    return segNums

