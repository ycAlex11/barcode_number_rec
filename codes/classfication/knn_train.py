import sys
#sys.path.insert(1,'/usr/local/opencv/opencv-2.4.11/lib/python2.7/site-packages')
import cv2
import numpy as np

#set up knn at here I used each training data size 20*20
#read all training data and inser into a list 
def initKNN(datas):
    k = np.arange(10)
    samples= np.empty((0,400)).astype(np.float32)
    for sample in datas:
        sample = sample.reshape((1,400)).astype(np.float32)
        samples =np.append(samples,sample,0)
     # set up labels ,at here for each number i made 50
    train_labels = np.repeat(k,50)
    knn = cv2.KNearest()
    knn.train(samples,train_labels)
    return knn

#use Knn to detect each image's number
def find_digits(knn,img):
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    th = cv2.resize(th, (20, 20))
    out = th.reshape(-1, 400).astype(np.float32)
    ret, result, neighbours, dis = knn.find_nearest(out, k=3)
    return int(result[0][0])

