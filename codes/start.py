import sys
sys.path.append('/extract_numbers/')
sys.path.append('/img_segmentation/')
sys.path.append('/classfication/')
sys.path.insert(1,'/usr/local/opencv/opencv-2.4.11/lib/python2.7/site-packages')
from extract_numbers import img_pre as ip
from extract_numbers import find_blob as fb
from extract_numbers import parall_line as pl
from extract_numbers import blob_preprocessing as bp
from extract_numbers import number_extraction as ne
from img_segmentation import seg_img as si
#from img_segmentation import writeToDir
from classfication import knn_train as kt
from classfication import training_data as td
from classfication import mkdir as md
import numpy as np
from os import listdir
from os.path import isfile,join
import cv2

#this is like main file,The idea is barcode they are close, so dilation 
#on X axis first, see if can find potential area, if not, maybe beause kernel
# is too big, reduce kernel half and dilation on X amis again, if still can 
#not find repeat same on Y axis 
#

#compare tash1.sh, this one doing the same thing to find the potential blob
#with barcode and numbers, the different is it does not write that blob to 
#disk. it would pass number segmentation to segmentate the number


img_path = '../test/task4/'

write_path= '/output/'
training_path = '../training/'

knn = td.training(training_path)

afiles = [f for f in listdir(img_path) if isfile(join(img_path,f))]
j = 1
for f in range(1,6):
	
    findNumber = False
    fileName = 'img'+str(f)+'.jpg'
    img =cv2.imread(img_path+fileName)
    gray = cv2.imread(img_path+fileName,0)
    mask = np.zeros(gray.shape,np.uint8)
    s=[]
    dia = ip.dilationX(img)

    numbers= None
    s= fb.pen_blob(dia,img)
    #
    if len(s)!=0:
        blobs,rectList ,img_rots= fb.store_blob(s,img)
        flag,blob,rect,img_rot = pl.rec_barcode(blobs,rectList,img_rots)


        if flag ==True:
           angle = bp.rotate_angle(blob)
           area = None
           if abs(angle)!=0:
                blob,img_rot = bp.rotation_image(img,angle,rect)
                blob = bp.checkSlope(blob)
           height, width = img.shape[:2]
           size1 = img.size
           size2 = blob.getCropped().size
           radio = (float(size2)) / size1
           size = 0
           if (radio < 0.8):
               size = 0.03

           elif radio > 0.8 and radio < 1.3:
               size = 0.006
           else:
               size = 0
           newCro ,slope= ne.expand_blob(blob,size,img_rot)



           if len(newCro)!=0:
               if slope!=float('inf'):
                   newCro=ne.rotationBN(newCro,slope)

               numbers,findNumber = ne.extract_number(newCro)



    if findNumber==False:
        dia = ip.dilationX_half(img)
        s = fb.pen_blob(dia, img)
        if len(s) != 0:
            blobs, rectList, img_rots = fb.store_blob(s, img)
            flag, blob, rect, img_rot = pl.rec_barcode(blobs, rectList, img_rots)

            if flag == True:
                angle = bp.rotate_angle(blob)
                area = None
                if abs(angle) != 0:
                    blob, img_rot = bp.rotation_image(img, angle, rect)
                    blob = bp.checkSlope(blob)
                height, width = img.shape[:2]
                size1 = img.size
                size2 = blob.getCropped().size
                radio = (float(size2)) / size1
                size = 0
                if (radio < 0.8):
					#change here from 0.08 to 0.1
                    size = 0.1

                elif radio > 0.8 and radio < 1.3:
                    size = 0.008
                else:
                    size = 0
                newCro, slope = ne.expand_blob(blob, size, img_rot)


                if len(newCro) != 0:
                    if slope != float('inf'):
                        newCro = ne.rotationBN(newCro, slope)

                    numbers, findNumber = ne.extract_number(newCro)




    if findNumber==False:
        dia = ip.dilationY(img)

        s = fb.pen_blob(dia, img)
        if len(s) != 0:
            blobs, rectList, img_rots = fb.store_blob(s, img)
            flag, blob, rect, img_rot = pl.rec_barcode(blobs, rectList, img_rots)

            if flag == True:
                angle = bp.rotate_angle(blob)
                area = None
                if abs(angle) != 0:
                    blob, img_rot = bp.rotation_image(img, angle, rect)
                    blob = bp.checkSlope(blob)
                height, width = img.shape[:2]
                size1 = img.size
                size2 = blob.getCropped().size
                radio = (float(size2)) / size1
                size = 0
                if (radio < 0.8):
                    size = 0.05

                elif radio > 0.8 and radio < 1.3:
                    size = 0.006
                else:
                    size = 0
                newCro, slope = ne.expand_blob(blob, size, img_rot)

                if len(newCro) != 0:
                    if slope != float('inf'):
                        newCro = ne.rotationBN(newCro, slope)

                    numbers, findNumber = ne.extract_number(newCro)


    if findNumber==False:
        dia = ip.dilationY_half(img)

        s= fb.pen_blob(dia, img)
        if len(s) != 0:
            blobs, rectList, img_rots = fb.store_blob(s, img)
            flag, blob, rect, img_rot = pl.rec_barcode(blobs, rectList, img_rots)

            if flag == True:
                angle = bp.rotate_angle(blob)
                area = None
                if abs(angle) != 0:
                    blob, img_rot = bp.rotation_image(img, angle, rect)
                    blob = bp.checkSlope(blob)
                height, width = img.shape[:2]
                size1 = img.size
                size2 = blob.getCropped().size
                radio = (float(size2)) / size1
                size = 0
                if (radio < 0.8):
                    size = 0.05

                elif radio > 0.8 and radio < 1.3:
                    size = 0.006
                else:
                    size = 0
                newCro, slope = ne.expand_blob(blob, size, img_rot)
                if len(newCro) != 0:
                    if slope != float('inf'):
                        newCro = ne.rotationBN(newCro, slope)

                    numbers, findNumber = ne.extract_number(newCro)
     

	#pass it to image segmentation
    if findNumber==True:
        print('find the blob contains image start image segmentation and classfication')
        seg_nums = si.seg_number(numbers)
        if len(seg_nums)!=0:
            k=1
            path = md.mkdir(write_path,j)
            #after segmentate number pass to number classfication
            for seg_num in seg_nums:
                result = kt.find_digits(knn,seg_num)
                #get the result then write the final result to disk
                if k < 10:
                    f1 = open(path + 'd0'  + str(k) + '.txt', 'w')
                    f1.write(str(result))
                    f1.close()

                else:
                    f1 = open(path + 'd' + str(k) + '.txt', 'w')
                    f1.write(str(result))
                    f1.close()
                k=k+1
    else:
        print('this does not have numbers with barcode')
    j=j+1
