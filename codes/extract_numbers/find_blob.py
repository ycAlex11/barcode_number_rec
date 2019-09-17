import sys
#sys.path.insert(1,'/usr/local/opencv/opencv-2.4.11/lib/python2.7/site-packages')
import cv2
import numpy as np
from crop_image import Blob



#after image preprocessing,get a few of blobs
#checked the size of blob to get potential blob 
def pen_blob(dia,img):
    (cnts, _) = cv2.findContours(dia.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)

    height,width= img.shape[:2]

    low_width=width/8
    high_width = (4*width)/8
    low_height=height/8
    high_height=(4*height)/8
    small_blobs = []
    for x in c :
        rect = cv2.minAreaRect(x)

        if (rect[1][1]>low_height and rect[1][1]<high_height and rect[1][0]>low_width and rect[1][0]<high_width):
            small_blobs.append(x)
    return small_blobs

#crop each potential blob for ready check do they contains parallel lines
def store_blob(small_blobs,img):
    height,width = img.shape[:2]
    templist = []
    rectList=[]
    img_rots=[]
    for cnt in small_blobs:
        rect = cv2.minAreaRect(cnt)
        box = np.int0(cv2.cv.BoxPoints(rect))
        angle = rect[2]
        M = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)

        img_rot = cv2.warpAffine(img, M, (width, height))

        pts = np.int0(cv2.transform(np.array([box]), M))[0]
        img_crop = img_rot[pts[1][1]:pts[0][1],
                   pts[1][0]:pts[2][0]]
        points = []
        points.append(pts[1][0])
        points.append(pts[2][0])
        points.append(pts[1][1])
        points.append(pts[0][1])
        cropped = Blob(points,angle,img_crop,None)
        templist.append(cropped)
        rectList.append(rect)
        img_rots.append(img_rot)
    return templist,rectList,img_rots










