import sys
#sys.path.insert(1,'/usr/local/opencv/opencv-2.4.11/lib/python2.7/site-packages')
import cv2
import numpy as np
import knn_train as kt
from os import listdir
from os.path import isfile,join

#read all training data and invoking the inikNN to set up training data

def training(training_path):
    datas = []
    for j in range(0,10):
        training_paths = training_path+str(j)+'/'
        afiles = [f for f in listdir(training_paths) if isfile(join(training_paths, f))]
        for f in afiles:
            img = cv2.imread(training_paths + f)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            th = cv2.resize(th, (20, 20))
            datas.append(th)

    knn = kt.initKNN(datas)
    return knn
