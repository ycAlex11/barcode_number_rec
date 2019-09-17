import sys
#sys.path.insert(1,'/usr/local/opencv/opencv-2.4.11/lib/python2.7/site-packages')
import cv2
import numpy as np
from collections import Counter
#this file is for extraction numbers


# expand the cropped blob 
def expand_blob(blob,size,img):
    height,width = img.shape[:2]

    y1 = blob.getPoints()[2]-int(height*size)
    y2= blob.getPoints()[3] + int(height * size)
    x1 = blob.getPoints()[0] - int(width * size)
    x2 = blob.getPoints()[1] + int(width * size)
    if y1<0:
        y1 =0
    if x1<0:
        x1= 0
    if y2>height:
        y2 = height
    if x2>width:
        x2=width
    newCro= img[y1:y2,x1:x2]

    return newCro,blob.getSlope()
    
    
#rotation by 90 degree
def rotationBN(newCro,slope):
    raida = np.arctan(slope)
    angle = np.rad2deg(raida)+90
    height,width = newCro.shape[:2]
    (cx,cy) = (width//2,height//2)

    M = cv2.getRotationMatrix2D((cx,cy),angle,1.0)
    cos = np.abs(M[0,0])
    sin = np.abs(M[0,1])
    nW= int((height*sin)+(width*cos))
    nH= int((height*cos)+(width*sin))
    M[0,2]+=(nW/2)-cx
    M[1,2]+=(nH/2)-cy
    newCro=cv2.warpAffine(newCro,M,(nW,nH))

    return  newCro

#this method is for extract the numbers, the idea is find the potential area
#because the height of each number are pretty same, so for each blob, convert
#their top-left Y value to integer, and insert to a list, the most common one
#would be a number, then find other blob's top-left Y vaule around that.Then 
#based on the Y value it could be known the image is up-side down or now
#check the top-left X value, if it is up-side down, start with the biggest one,otherwise
#smallest one, then based on the biggest and smallest can get the area of numbers
def extract_number(newCro):
    result = None
    height,width = newCro.shape[:2]
    flag1 = False
    gray = cv2.cvtColor(newCro,cv2.COLOR_BGR2GRAY)
    th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 2)

    (cnts, _) = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)
    pen_numbers=[]
    for cnt in c:
        rect = cv2.minAreaRect(cnt)
        #change here 0.035 to 0.025
        if rect[1][0]<width*0.3 and rect[1][1]<height*0.3 and rect[1][0]>width*0.025 and rect[1][1]>height*0.025 and float(rect[1][0])/rect[1][1]>0.5 and float(rect[1][0])/rect[1][1]<2:


            pen_numbers.append(rect)


    numbers =[]
    for sth in pen_numbers:
        numbers.append(int(sth[0][1]))
   
    if len(numbers)>2:
        temp_height = Counter(numbers).most_common(1)[0][0]
        #print(temp_height)
        nums = []
        for num in pen_numbers:
			#change here from 7 to 8
            if  temp_height-8<num[0][1]<temp_height+8:
                nums.append(num)

        if temp_height>height*0.5:
            minX,widthX,heightX,topY=findMin(nums)
            x1 = minX-int(widthX*0.75)
            #y1 = topY-int(heightX*0.88)
            y1 = topY - int(heightX * 0.9)
            maxX,widthX,heightX,topY = findMax(nums)
            x2 = maxX+int(widthX*0.5)
            #y2 = topY+int(heightX*0.88)
            y2 = topY + int(heightX * 0.9)
            x2 = x2+int((x2-x1)*0.135)
            if y1 < 0:
                y1 = 0
            if x1 < 0:
                x1 = 0
            if y2 > height:
                y2 = height
            if x2 > width:
                x2 = width

            result= newCro[y1:y2,x1:x2]


            if x2 - x1 > width * 0.6 :
                flag1 = True
	
		# if upside-down extract number first then rotation	
        else:
            minX, widthX, heightX, topY = findMin(nums)
            x1 = minX - int(widthX * 0.75)
            #y1 = topY - int(heightX * 0.88)
            y1 = topY - int(heightX * 0.9)
            maxX, widthX, heightX, topY = findMax(nums)
            x2 = maxX + int(widthX * 0.5)
            #y2 = topY + int(heightX * 0.88)
            y2 = topY + int(heightX * 0.9)
            x1 = x1 - int((x2 - x1) * 0.14)
            if y1 < 0:
                y1 = 0
            if x1 < 0:
                x1 = 0
            if y2 > height:
                y2 = height
            if x2 > width:
                x2 = width
            result = newCro[y1:y2, x1:x2]

            if x2-x1>width*0.6:
                flag1=True
            if flag1==True:
                result= rotationBOne(result)

    return result,flag1

# rotation by 180 degree
def rotationBOne(newCro):
    angle = 180
    height,width = newCro.shape[:2]
    (cx,cy) = (width//2,height//2)

    M = cv2.getRotationMatrix2D((cx,cy),angle,1.0)
    cos = np.abs(M[0,0])
    sin = np.abs(M[0,1])
    nW= int((height*sin)+(width*cos))
    nH= int((height*cos)+(width*sin))
    M[0,2]+=(nW/2)-cx
    M[1,2]+=(nH/2)-cy
    newCro=cv2.warpAffine(newCro,M,(nW,nH))

    return newCro
#find the minimum X values and its width and height
def findMin(nums):
    minX = nums[0][0][0]
    widthX = nums[0][1][0]
    heightX= nums[0][1][1]
    topY= nums[0][0][1]

    for i in range(1,len(nums)):
        if nums[i][0][0]<minX:
            minX = nums[i][0][0]
            widthX = nums[i][1][0]
            heightX = nums[i][1][1]
            topY = nums[i][0][1]
    return int(minX),int(widthX),int(heightX),int(topY)
#find the maximum of X values and its width and height
def findMax(nums):
    maxX = nums[0][0][0]
    widthX= nums[0][1][0]
    heightX = nums[0][1][1]
    topY = nums[0][0][1]
    for i in range(1, len(nums)):
        if nums[i][0][0] > maxX:
            maxX = nums[i][0][0]
            widthX = nums[i][1][0]
            heightX = nums[i][1][1]
            topY = nums[i][0][1]
    return int(maxX),int(widthX),int(heightX),int(topY)






