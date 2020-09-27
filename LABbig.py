from tkinter import filedialog
import tkinter as tk
from os import listdir
from os.path import isfile, join
from PIL import Image
import numpy as np
import xlsxwriter
import pandas as pd
from skimage.feature import greycomatrix, greycoprops
from xlwt import Workbook

root = tk.Tk()
root.geometry("1040x320")
list = []
dis_city_list = []
dis_can_list = []

def train_browse():
    global flag
    flag = 0
    filename = filedialog.askdirectory()
    print(filename)
    global train_file
    train_file = filename

def test_browse():
    global flag
    flag = 1
    filename = filedialog.askdirectory()
    print(filename)
    global test_file
    test_file = filename

def ctDDtarin():
    global store
    store = 1
    allFile, path = browse_button(train_file)
    ctAndDD(allFile,path)

def gclmTrain():
    global store
    store = 2
    allFile, path = browse_button(train_file)
    glcm(allFile,path)

def ctDDtest():
    global store
    store = 3
    allFile, path = browse_button(test_file)
    ctAndDD(allFile,path)

def gclmTest():
    global store
    store = 4
    allFile, path = browse_button(test_file)
    glcm(allFile,path)

def browse_button(filename):
    newPath = filename + '/'
    files = [f for f in listdir(newPath) if isfile(join(newPath, f))]
    return files,newPath

def ctAndDD(files,newPath):
    for i in files:
        path = newPath+i
        meanAndOthers = MeanMedianMidrange(path)
        list.append([i, meanAndOthers[0], meanAndOthers[1], meanAndOthers[2], meanAndOthers[3], meanAndOthers[4], meanAndOthers[5]])
    if flag == 0:
        xfile = 'CTDDtrain.xlsx'
    elif flag == 1:
        xfile = 'CTDDtst.xlsx'
    print('writing file')
    xbook = xlsxwriter.Workbook(xfile)
    xsheet = xbook.add_worksheet('data')

    xsheet.write_row(0, 0, ['Image label', 'Mean', 'Median', 'Midrange', 'Range', 'IQR', 'Standard Deviation'])

    for i in range (1,(len(list))):
        xsheet.write_row(i, 0, list[i-1])

    xsheet.write_row(i+1, 0, list[i])

    xbook.close()

def MeanMedianMidrange(path):
    print('calculating value')
    img = Image.open(path)
    img_array = np.array(img.convert('L', colors=8))
    #arry = np.array(img)
    mean = np.mean(img_array)
    median = np.median(img_array)

    midrange = (int(np.amax(img_array))+int(np.amin(img_array)))/2

    max = np.amax(img_array)
    min = np.amin(img_array)
    range = max - min
    q3  = np.percentile(img_array, 75)
    q1  = np.percentile(img_array, 25)
    iqr = q3 - q1
    var = np.mean(abs(img_array - img_array.mean())**2)

    return [mean,median,midrange,range,iqr,(var)**.5]

def glcm(files,newPath):
    for i in files:
        path = newPath+i
        fiveAndOthers = sixthings(path)
        list.append([newPath+i, fiveAndOthers[0], fiveAndOthers[1], fiveAndOthers[2],fiveAndOthers[3],fiveAndOthers[4],
                     fiveAndOthers[5]])
    if flag == 0:
        xfile = 'GLCMtrain.xlsx'
    elif flag == 1:
        xfile = 'GLCMtest.xlsx'
    print('file write')
    xbook = xlsxwriter.Workbook(xfile)
    xsheet = xbook.add_worksheet('data')

    xsheet.write_row(0, 0, ['Image label','Maximum probability','Correlation','Contrast','Uniformity(Energy)','Homogenity','Entropy'])

    for i in range (1,(len(list))):
        xsheet.write_row(i, 0, list[i-1])

    xsheet.write_row(i+1, 0, list[i])

    xbook.close()

def sixthings(path):
    print("value calculation")
    img = Image.open(path)
    img_array = np.array(img.convert('L', colors=8))
    imgmatrix = greycomatrix(img_array,[1], [0], levels=256, symmetric=True, normed=True)
    max_prob = np.amax(imgmatrix)
    correlation = greycoprops(imgmatrix,'correlation')
    contrast = greycoprops(imgmatrix,'contrast')
    energy = greycoprops(imgmatrix, 'energy')
    homogeneity = greycoprops(imgmatrix,'homogeneity')
    entropy = -np.sum(imgmatrix*np.log2(imgmatrix + (imgmatrix==0)))
    return [max_prob,correlation,contrast,energy,homogeneity,entropy]

def load_all_data():
    global store
    print('loading Done')
    root.sourceFile = filedialog.askopenfilename(parent=root, initialdir= "/", title='Select a file')
    dir = pd.read_excel(root.sourceFile)
    if (store == 1):
        global name_train1,mean_train,median_train,mode_train,midrange_train,range_train, iqr_train,sd_train
        name_train1 = []
        mean_train = []
        median_train = []
        mode_train = []
        midrange_train = []
        range_train = []
        iqr_train = []
        sd_train = []

        name_train1 = dir.iloc[:, 0]
        mean_train = dir.iloc[:, 1]
        median_train = dir.iloc[:, 2]
        #mode_train = dir.iloc[:, 3]
        midrange_train = dir.iloc[:, 3]
        range_train = dir.iloc[:, 4]
        iqr_train = dir.iloc[:, 5]
        sd_train = dir.iloc[:,6]
        print ("done1")
    if store == 3:
        global name_test3,mean_test,median_test,mode_test,midrange_test,midrange_test,range_test, iqr_test,sd_test
        name_test3 = []
        mean_test = []
        median_test = []
        mode_test = []
        midrange_test = []
        range_test = []
        iqr_test = []
        sd_test = []

        name_test3 = dir.iloc[:, 0]
        mean_test = dir.iloc[:, 1]
        median_test = dir.iloc[:, 2]
        #mode_test = dir.iloc[:, 3]
        midrange_test = dir.iloc[:, 3]
        range_test = dir.iloc[:, 4]
        iqr_test = dir.iloc[:, 5]
        sd_test = dir.iloc[:,6]
        print ("done3")
    if store == 2:
        global name_train2,max_prob_ary2,correlation_ary2,contrast_ary2,energy_ary2,homogeneity_ary2,entropy_ary2
        name_train2 = []
        max_prob_ary2= []
        correlation_ary2 = []
        contrast_ary2 = []
        energy_ary2 = []
        homogeneity_ary2 = []
        entropy_ary2 = []

        name_train2 = dir.iloc[:, 0]
        max_prob_ary2 = dir.iloc[:, 1]
        correlation_ary2 = dir.iloc[:, 2]
        contrast_ary2 = dir.iloc[:, 3]
        energy_ary2 = dir.iloc[:, 4]
        homogeneity_ary2 = dir.iloc[:, 5]
        entropy_ary2 = dir.iloc[:, 6]
        print("done2")
    if store == 4:
        global name_test4,max_prob_ary4,correlation_ary4,contrast_ary4,energy_ary4,homogeneity_ary4,entropy_ary4
        name_test4 = []
        max_prob_ary4 = []
        correlation_ary4 = []
        contrast_ary4 = []
        energy_ary4 = []
        homogeneity_ary4 = []
        entropy_ary4 = []

        name_test4 = dir.iloc[:, 0]
        max_prob_ary4 = dir.iloc[:, 1]
        correlation_ary4 = dir.iloc[:, 2]
        contrast_ary4 = dir.iloc[:, 3]
        energy_ary4 = dir.iloc[:, 4]
        homogeneity_ary4 = dir.iloc[:, 5]
        entropy_ary4 = dir.iloc[:, 6]

        print("done4")


def cityBlock():
    global store
    print("city block")
    file_train = train_file + '/'
    traing_file = [f for f in listdir(file_train) if isfile(join(file_train, f))]

    file_test = test_file + '/'
    testing_file = [f for f in listdir(file_test) if isfile(join(file_test, f))]

    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')

    row = 1

    for i in range(0,len(testing_file)):
        print("new one")
        j = 0
        dis_city_list.clear()
        for k in traing_file:
            if store == 3:
                dis_city_list.append([file_train+k,float(abs(mean_train[j]-mean_test[i])+abs(median_train[j]-median_test[i])
                                                         +abs(midrange_train[j]-midrange_test[i])+abs(range_train[j]-range_test[i])+abs(iqr_train[j]-iqr_test[i])+abs(sd_train[j]-sd_test[i]))])


            if store == 4:
                dis_city_list.append([file_train+k,float(abs(max_prob_ary2[j]-max_prob_ary4[i])+abs(correlation_ary2[j]-correlation_ary4[i])
                                                         +abs(contrast_ary2[j]-contrast_ary4[i])+abs(energy_ary2[j]-energy_ary4[i])+
                                                 abs(homogeneity_ary2[j]-homogeneity_ary4[i])+abs(entropy_ary2[j]-entropy_ary4[i]))])
            j = j+1


        if store == 3:
            dis_city_list.sort(key=lambda x: x[1])
            sheet1.write(row,0,dis_city_list[1][0])
            print(dis_city_list[1])
            row = row+1
            wb.save('CTDDcity.xls')
        if store == 4:
            dis_city_list.sort(key=lambda x: x[1])
            sheet1.write(row,0,dis_city_list[1][0])
            print(dis_city_list[1])
            row = row+1
            wb.save('GLCMcity.xls')



def canberra():
    print("canberra")
    file_train = train_file + '/'
    traing_file = [f for f in listdir(file_train) if isfile(join(file_train, f))]

    file_test = test_file + '/'
    testing_file = [f for f in listdir(file_test) if isfile(join(file_test, f))]

    wb = Workbook()
    sheet1 = wb.add_sheet('Sheet 1')

    row = 1
    for i in range(0,len(testing_file)):
        j=0
        dis_can_list.clear()
        print("new one")
        for k in traing_file:
            if store == 3:
                canberra_distance = (abs(mean_train[j]-mean_test[i])/(abs(mean_train[j])+abs(mean_test[i])))\
                                    +(abs(midrange_train[j]-midrange_test[i])/(abs(midrange_train[j])+abs(midrange_test[i])))\
                                    +(abs(range_train[j]-range_test[i])/(abs(range_train[j])+abs(range_test[i])))+(abs(iqr_train[j]-iqr_test[i])
                                                                                                                   /(abs(iqr_train[j])+abs(iqr_test[i])))+\
                                    (abs(median_train[j]-median_test[i])/(abs(median_train[j])+abs(median_test[i])))\
                                    +(abs(sd_train[j]-sd_test[i])/(abs(sd_train[j])+abs(sd_test[i])))
                dis_can_list.append([file_train+k,canberra_distance])


            if store == 4:
                canberra_distance = (abs(max_prob_ary2[j]-max_prob_ary4[i])/(abs(max_prob_ary2[j])+abs(max_prob_ary4[i])))\
                                    +(abs(correlation_ary2[j]-correlation_ary4[i])/(abs(correlation_ary2[j])+abs(correlation_ary4[i])))\
                                    +(abs(contrast_ary2[j]-contrast_ary4[i])/(abs(contrast_ary2[j])+abs(contrast_ary4[i])))+(abs(energy_ary2[j]-energy_ary4[i])
                                                                                                                   /(abs(energy_ary2[j])+abs(energy_ary4[i])))+\
                                    (abs(homogeneity_ary2[j]-homogeneity_ary4[i])/(abs(homogeneity_ary2[j])+abs(homogeneity_ary2[i])))\
                                    +(abs(entropy_ary2[j]-entropy_ary4[i])/(abs(entropy_ary2[j])+abs(entropy_ary4[i])))
                dis_can_list.append([file_train+k,canberra_distance])
            j = j+1


        if store == 3:
            dis_can_list.sort(key=lambda x: x[1])
            sheet1.write(row,0,dis_can_list[1][0])
            print(dis_can_list[1])
            row = row+1
            wb.save('CTDDcan.xls')
        if store == 4:
            dis_can_list.sort(key=lambda x: x[1])
            sheet1.write(row,0,dis_can_list[1][0])
            print(dis_can_list[1])
            row = row+1
            wb.save('GLCMcan.xls')

button1 = tk.Button(root,
                   text="Load Training images",
                   fg="blue",
                   command=train_browse)

button1.pack(side='top')
button2 = tk.Button(root,
                   text="Extract CT+DD Feature and store in database",
                   fg="green",
                   command=ctDDtarin)

button2.pack(side='top')
button3 = tk.Button(root,
                   text="Extract GLCM Feature and store in database",
                   fg="red",
                   command=gclmTrain)

button3.pack(side='top')
button4 = tk.Button(root,
                   text="Extract SIFT Feature and store in database",
                   fg="orange",
                   command=quit)

button4.pack(side='top')
button5 = tk.Button(root,
                   text="Extract SURF Feature and store in database",
                   fg="black",
                   command=quit)

button5.pack(side='top')

button6 = tk.Button(root,
                   text="Load Training Feature Data",
                   fg="red",
                   command=load_all_data)

button6.pack(side='left')
button7 = tk.Button(root,
                   text="Load Test images",
                   fg="red",
                   command=test_browse)

button7.pack(side='left')

button12 = tk.Button(root,
                   text="Load Test Feature Data",
                   fg="blue",
                   command=load_all_data)

button12.pack(side='bottom')
button11 = tk.Button(root,
                   text="Extract SURF Feature for query images and store in database",
                   fg="green",
                   command=quit)

button11.pack(side='bottom')
button10 = tk.Button(root,
                   text="Extract SIFT Feature for query images and store in database",
                   fg="red",
                   command=quit)

button10.pack(side='bottom')
button9 = tk.Button(root,
                   text="Extract GLCM Feature for query images and store in database",
                   fg="orange",
                   command=gclmTest)

button9.pack(side='bottom')
button8 = tk.Button(root,
                   text="Extract CT+DD Feature for query images and store in database",
                   fg="black",
                   command=ctDDtest)

button8.pack(side='bottom')

button13 = tk.Button(root,
                   text="Show similar images using City block distance",
                   fg="green",
                   command=cityBlock)

button13.pack(side='right')
button13 = tk.Button(root,
                   text="Show similar images using Canberra distance",
                   fg="green",
                   command=canberra)

button13.pack(side='right')
button14 = tk.Button(root,
                   text="Show similar images using Random Forest distance",
                   fg="green",
                   command=quit)

button14.pack(side='right')

root.mainloop()
