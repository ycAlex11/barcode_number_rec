import sys
#sys.path.insert(1,'/usr/local/opencv/opencv-2.4.11/lib/python2.7/site-packages')
import cv2
import numpy as np

# this file is method for image pre-processing


#dilation image based on X and with close, erode and dia try to remove 
# most of pixel and leave some blobs
def dilationX(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    blur = cv2.blur(gray,(3,3))
    edges = cv2.Canny(blur,100,150)
    kernelD = np.ones((1, 30), np.uint8)
    diaFirst = cv2.dilate(edges,kernelD,iterations=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    ret, th = cv2.threshold(diaFirst, 15, 255, cv2.THRESH_BINARY)
    closed = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
    erode = cv2.erode(closed, None, iterations=40)
    dia = cv2.dilate(erode, None, iterations=50)
    return dia


#dilation image based on X(0 degree) but kernel size reduce 50%
def dilationX_half(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    blur = cv2.blur(gray,(3,3))
    edges = cv2.Canny(blur,100,150)
    kernelD = np.ones((1, 15), np.uint8)
    diaFirst = cv2.dilate(edges,kernelD,iterations=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    ret, th = cv2.threshold(diaFirst, 150, 255, cv2.THRESH_BINARY)
    closed = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
    erode = cv2.erode(closed, None, iterations=40)
    dia = cv2.dilate(erode, None, iterations=50)
    return dia

#dilation image based on Y(90 degree)
def dilationY(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    blur = cv2.blur(gray,(3,3))
    edges = cv2.Canny(blur,100,150)
    kernelD = np.ones((30, 1), np.uint8)
    diaFirst = cv2.dilate(edges,kernelD,iterations=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    ret, th = cv2.threshold(diaFirst, 150, 255, cv2.THRESH_BINARY)
    closed = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
    erode = cv2.erode(closed, None, iterations=40)
    dia = cv2.dilate(erode, None, iterations=50)

    return dia


#dilation image based on Y(90 degree) but kernel size reduce 50%
def dilationY_half(img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    blur = cv2.blur(gray,(3,3))
    edges = cv2.Canny(blur,100,150)
    kernelD = np.ones((15, 1), np.uint8)
    diaFirst = cv2.dilate(edges,kernelD,iterations=2)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    ret, th = cv2.threshold(diaFirst, 150, 255, cv2.THRESH_BINARY)
    closed = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
    erode = cv2.erode(closed, None, iterations=40)
    dia = cv2.dilate(erode, None, iterations=50)
    return dia

