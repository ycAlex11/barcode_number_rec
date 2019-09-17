import sys
#sys.path.insert(1,'/usr/local/opencv/opencv-2.4.11/lib/python2.7/site-packages')
import cv2
import numpy as np
from operator import itemgetter

#this file is for check on one image, which blob contains most of parallel
#line, if the number of parallel lines are more than 70 I treat it is a blob 
#include barcode 

#get slope
def get_slope(point1, point2):
    if point1[0] == point2[0]:
        return float('inf')
    else:
        return (float(point1[1]) - float(point2[1])) / (float(point1[0]) - float(point2[0]))

#if lines are parallel,number +1
def check_parallel(slope, votes):
    flag = False
    for x in votes:
        if x[0] == slope:
            x[1] += 1
            flag = True
            break
    if not flag:
        votes.append([slope, 1])


#for an image ,find which blob has most parallel lines,if it has more than 70 parallel, treat this blob include barcode
def rec_barcode(list1,rectList,img_crops):
    values = []
	#check each blob, the idea is pretty much same as hough line's accumulator
	#do a voting on based on the slope
    for cropped in list1:
        votes = []
        gray = cv2.cvtColor(cropped.getCropped(),cv2.COLOR_BGR2GRAY)
        edgs = cv2.Canny(gray,50,150,apertureSize=3)
        if edgs is not None:
            minLineLength = 300
            maxLineGap = 3
            lines = cv2.HoughLinesP(edgs, 1, np.pi / 180, 5, minLineLength, maxLineGap)
            if lines is not None:
                for x1, y1, x2, y2 in lines[0]:
                    cv2.line(edgs, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    pt1 =[]
                    pt1.append(x1)
                    pt1.append(y1)
                    pt2=[]
                    pt2.append(x2)
                    pt2.append(y2)
                    slope= get_slope(pt1,pt2)
                    check_parallel(slope,votes)
        values.append(votes)
	#First find maximum slope and its number for each blob from values list
	#insert them to a list
    tempList = []
    for i in range(len(values)):
        if len(values[i])==0:
            tempList.append([float('inf'),-1])
        else:
            tempList.append(max(values[i],key=itemgetter(1)))
    flag = False
    barcode_blob = None
    max_slope=None
    #find which blob has maximum parallel lines
    if(len(tempList)!=0):
        max_slope = max(tempList,key=itemgetter(1))
        indx = tempList.index(max_slope)
        barcode_blob = list1[indx]
     #if has more than parallel line treat it as a blob with barcode   
    if max_slope is not None:
        if(max_slope[1]>70):
            barcode_blob.setSlope(max_slope[0])
            flag=True
	#if find blob return True and that blob 
    if flag==True:
        indx = tempList.index(max_slope)
        rect = rectList[indx]
        img_rot = img_crops[indx]
        return True,barcode_blob,rect,img_rot
    else:
        return False,None,None,None
