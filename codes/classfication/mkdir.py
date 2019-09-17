import os

#create folder for each's barcode' number
def mkdir(path,i):

    string = str(i)
    name = 'barcode'+string
    newPath = path+ name
    isExists = os.path.exists(newPath)

    if not isExists:
        os.makedirs(newPath)
        newPath=newPath+'/'
        return newPath

    else:
        newPath = newPath + '/'
        return newPath


