import sys
#sys.path.insert(1,'/usr/local/opencv/opencv-2.4.11/lib/python2.7/site-packages')
import cv2
import numpy as np
from crop_image import Blob
import parall_line as db
from operator import itemgetter
#these functions do rotation on whole image and crop the potential 
#blob for extract the numbers

#a function to check if need rotation and return rotation angle
def rotate_angle(blob):
    angle=0
    if blob.getSlope() != float('inf'):
        radian = np.arctan(blob.getSlope())

        angle = np.rad2deg(radian)
    return angle


#rotation image twice and crop the blob include barcode
def rotation_image(img,angle2,rect):
	
	#first rotation based on the angle of blob
    box = np.int0(cv2.cv.BoxPoints(rect))
    angle = rect[2]
    height, width = img.shape[:2]
    M = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)

    img_rot = cv2.warpAffine(img, M, (width, height))
    pts = np.int0(cv2.transform(np.array([box]), M))
    #the angle of blob may not the angle of barcode
    #so based on the angle of barcode 2nd rotation
    M2 = cv2.getRotationMatrix2D((width / 2, height / 2), angle2, 1)
    img_rot = cv2.warpAffine(img_rot,M2,(width,height))
	
    pts3 = np.int0(cv2.transform(pts,M2))[0]
    
    #cropped the barcode blob and get points
    img_crop = img_rot[pts3[1][1]:pts3[0][1],
               pts3[1][0]:pts3[2][0]]
    points = []
    points.append(pts3[1][0])
    points.append(pts3[2][0])
    points.append(pts3[1][1])
    points.append(pts3[0][1])
    
    #store points, rotation angele and the cropped blob into object for 
    #for next step 
    cropped = Blob(points, angle, img_crop, None)
    checkSlope(cropped)
	# return object and whole image after rotation
    return cropped,img_rot


#based on the line's slope check the blob include barcode is 
#vertical or horizontal 
def checkSlope(cropped):
    values = []
    votes = []
    gray = cv2.cvtColor(cropped.getCropped(), cv2.COLOR_BGR2GRAY)
    edgs = cv2.Canny(gray, 50, 125, apertureSize=3)
    if edgs is not None:
        minLineLength = 200
        maxLineGap = 3
        lines = cv2.HoughLinesP(edgs, 1, np.pi / 180, 5, minLineLength, maxLineGap)
        if lines is not None:
            for x1, y1, x2, y2 in lines[0]:
                pt1 = []
                pt1.append(x1)
                pt1.append(y1)
                pt2 = []
                pt2.append(x2)
                pt2.append(y2)
                slope = db.get_slope(pt1, pt2)
                db.check_parallel(slope, votes)
    values.append(votes)

    max_slope=[]
    if len(values)!=0:
        for j in range(len(values)):
            max_slope.append(max(values[j], key=itemgetter(1)))

    if len(max_slope)!=0:
        max_slope=max(max_slope,key=itemgetter(1))
        cropped.setSlope(max_slope[0])
    return cropped
