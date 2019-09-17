import numpy as np
#this is main application for CCL
'''
first_pass is based on 8 neighbours does first labeling
here for easy to programming, i went through all 8 neighbours 
 rather then only 5
''' 
def first_pass(i,j,label,labels,equ_lable,height,width):
    #list1 is a list for store lable value of neighbours 
    list1 = []
    temp = []
    #check 8 neighbours and store their value in a list
    for k in range(i-1,i+2):
        for l in range(j-1,j+2):
            if k<0 or l<0 or (k==i and l==j) or k ==height or l == width:
                continue
            else:
                list1.append(labels[k][l])
                
    #insert all non-zero value to a temp-list from previous list 
    for x in list1:
        if x != 0 :
            temp.append(x)
    '''if the temp length is 0 which means this pixel is 
         the first pixel of this blob
		if not, i sort the temp and delete repeat value, the label for this
		pixel will be the first element in the temp list
    '''        
    if len(temp) == 0:
        labels[i][j] = label
        label = label + 1
    else:
        temp = list(set(temp))
        temp.sort()
        labels[i][j] = temp[0]
	
	'''
		Then check if temp is in the equivalent labels or not
		if not insert into equivalent labels
	''' 
    if (len(temp)!=0) and (temp not in equ_lable):
        equ_lable.append(temp)

    return label
    
'''
this method is for merge equivlent lables, the idea is after sorting of 
equivalent labels,i pick the first set in equivalent labels to another list
then start check 2nd element in equivalent labels, if they have at least one
element same, merge them, if not, insert 2nd element to another list.
Then loop two list until all list in equivalent labels insert to another list 
Another list will be a list of list, the length of list is number of blobs 
'''
def check_labels(list1):
    list1.sort()
    temp = []
    temp.append(list1[0])
    for i in range(1, len(list1)):
        flag = False
        for k in range(len(list1[i])):
            for l in range(len(temp)):
                for m in range(len(temp[l])):
                    if list1[i][k] == temp[l][m]:
                        flag = True
                        temp[l] = list(set(temp[l] + list1[i]))
                        break
                if flag == True:
                    break
            if flag == True:
                break

        if flag == False:
            temp.append(list1[i])
    return temp


'''
 change the lable,the idea is using function non-zeros from numpy only check
the non-zeros labels also the equivalent labels is sorted
for each one check is it the first of each list in list if they are the first one,
do nothing, break loop go next one, if it is not , then check in which list and change 
it to the first elememnt in its list
'''
def second_pass(labels,res,ys,xs):
    for i in range(len(ys)):
        x=xs[i]
        y=ys[i]
        flag = False
        for j in range(len(res)):
            if labels[y][x] == res[j][0]:
                flag =True
                break
        if flag==False:
            #flag2 = False
            for j in range(len(res)):
                for k in range(1,len(res[j])):
                    if labels[y][x] == res[j][k]:
                        labels[y][x] = res[j][0]
                        flag =True
                        break
                if flag ==True:
                    break


'''
get the top-left and bottom-right
this one is based on nonzeros function from numpy
nonzeros return 2 array, one is for row and one is for column
the Yone is the on the first row and Ytwo is on the last row
Xone is most left one,X2 is most right one
'''
def get_Points(res,labels,ys,xs):
    points = []
    #based on how many blobs know how many points need
    for k in range(len(res)):
        one_point = []
        tempList = []
        yTwo = 1000
        # this is for get Xone,Xtwo,Yone,Ytwo
        for i in range(len(ys)):
            x = xs[i]
            y = ys[i]
            if labels[y][x] == res[k]:
                yOne = y
                one_point.append(yOne)
                break
        for i in range(len(ys)):
            x = xs[i]
            y = ys[i]
            if labels[y][x] == res[k]:
                yTwo = y
            if labels[y][x] == res[k]:
                if x not in tempList:
                    tempList.append(x)

        one_point.append(yTwo)
        one_point.append(min(tempList))
        one_point.append(max(tempList))
        points.append(one_point)
    return points
