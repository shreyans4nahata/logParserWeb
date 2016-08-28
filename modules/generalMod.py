import csv
import os
import ntpath
import sys
import collections
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import json

def getUiP(inputCSVFile):
    outputDir = os.getcwd() + "/parsedOutput/"
    fileObject = open(outputDir+inputCSVFile,"r")
    reader = csv.DictReader(fileObject)

    timestamp = [] # list to store all timestamps includes duplicates
    ip = [] # list to store all remote ip's
    unique_ip = []

    # storing timestamp and ip's in a list
    for row in reader:
        timestamp.append(row['f1'])
        ip.append(row['f2'])

    unique_ip = list(set(ip)) # contains unique ip's

    unique_ip_len = len(unique_ip)

    #Close file
    fileObject.close()

    return json.dumps({"ip":unique_ip})

def completeListIQR(inputCSVFile,alpha,req_ip):

    alpha = abs(float(alpha))

    inliers_final = []
    outliers_final = []

    outputDir = os.getcwd() + "/parsedOutput/"
    fileObject = open(outputDir+inputCSVFile,"r")
    reader = csv.DictReader(fileObject)
    #print "DEBUgs"

    timestamp = [] # list to store all timestamps includes duplicates
    ip = [] # list to store all remote ip's

    # storing timestamp and ip's in a list
    for row in reader:
        timestamp.append(row['f1'])
        ip.append(row['f2'])

    unique_ip = list(set(ip)) # contains unique ip's

    unique_ip_len = len(unique_ip)

    temp_dict = {} # temporary dictinary
    final_dict = {}
    tr = [] # list containing request hits at particular ip
    t_list = [] #list containg formatted timestamp

    # initialization of request hit to 0 corresponding timestamp
    for j in range(len(timestamp)):
        temp_dict[timestamp[j]] = 0

    # incrementing the count for each ip
    for j in range(len(timestamp)):
        if ip[j] == str(req_ip):
            temp_dict[timestamp[j]]+=1

    # sorting dictionary by keys
    od = collections.OrderedDict(sorted(temp_dict.items()))


    for t,i in od.iteritems():
        #sp_dict = {}
        t_list.append(t)
        tr.append(i)
        #inliers_final.append({"x":time_val,"y":i})

    # diff_tim = []
    # diff_tim.append(0)
    # for x in range(1,len(t_list)):
    #     diff_tim.append(t_list[x] - t_list[0])

    len_tr = len(tr)

    q75, q25 = np.percentile(tr, [75 ,25])
    iqr = q75 - q25
    ul = q75 + alpha*iqr
    ll = q25 - alpha*iqr

    print q75,q25
    outlier = []
    outlier_x = []
    index = 0
    for h in range(len_tr):
        new_dict = {}
        if tr[h] < ll or tr[h] > ul:
            #When u uncomment below lines don't forget to do debug = false in server.py
            outlier.append(tr[h])
            outlier_x.append(t_list[h])
            new_dict["x"] =  index
            new_dict["y"] =  tr[h]
            new_dict["time"] = t_list[h]
            outliers_final.append(new_dict)
            index+=1
        else:
            new_dict["x"] =  index
            new_dict["y"] =  tr[h]
            new_dict["time"] = t_list[h]
            inliers_final.append(new_dict)
            index+=1

    # When u uncomment below lines don't forget to do debug = false in server.py
    #plt.plot(t_list,tr)
    #plt.plot(outlier_x,outlier,linestyle = '-',marker = 'o',color = 'r')
    #plt.show()

    return json.dumps({ "inliers" : inliers_final, "outliers" : outliers_final })


def completeListMed(inputCSVFile,req_ip,alpha,window):

    window = int(abs(window))
    alpha = float(abs(alpha))

    inliers_final = []
    outliers_final = []

    outputDir = os.getcwd() + "/parsedOutput/"
    fileObject = open(outputDir+inputCSVFile,"r")
    reader = csv.DictReader(fileObject)

    timestamp = [] # list to store all timestamps includes duplicates
    ip = [] # list to store all remote ip's

    # storing timestamp and ip's in a list
    for row in reader:
        timestamp.append(row['f1'])
        ip.append(row['f2'])

    unique_ip = list(set(ip)) # contains unique ip's

    unique_ip_len = len(unique_ip)

    temp_dict = {} # temporary dictinary
    final_dict = {}
    tr = [] # list containing request hits at particular ip
    t_list = [] #list containg formatted timestamp

    # initialization of request hit to 0 corresponding timestamp
    for j in range(len(timestamp)):
        temp_dict[timestamp[j]] = 0

    # incrementing the count for each ip
    for j in range(len(timestamp)):
        if ip[j] == str(req_ip):
            temp_dict[timestamp[j]]+=1

    od = collections.OrderedDict(sorted(temp_dict.items()))

    for t,i in od.iteritems():
        t_list.append(t)
        tr.append(i)

    #For median absolute deviation
    tuned_param = alpha
    # window = 10

    median_tr = np.median(tr[0:window])
    r_outlier = []
    r_outlier_x = []

    len_tr = len(tr)
    tot_dev = 0
    whole_median = np.median(tr)
    for i in range(1,(len_tr-window)):
        ch_tr = np.abs(tr[(window+i)]-median_tr)
        tot_dev+=ch_tr
        median_tr = np.median(tr[i:window+i])

    mad_val = abs(tot_dev/(len_tr-window))
    ul = tuned_param*mad_val + whole_median
    ll = whole_median - tuned_param*mad_val

    index = 0

    for h in range(len_tr):
        new_dict = {}
        if tr[h] < ll or tr[h] > ul:
            # When u uncomment below lines don't forget to do debug = false in server.py
            r_outlier.append(tr[h])
            r_outlier_x.append(t_list[h])
            new_dict["x"] =  index
            new_dict["y"] =  tr[h]
            new_dict["time"] = t_list[h]
            outliers_final.append(new_dict)
            index+=1
        else:
            new_dict["x"] =  index
            new_dict["y"] =  tr[h]
            new_dict["time"] = t_list[h]
            inliers_final.append(new_dict)
            index+=1

    # When u uncomment below lines don't forget to do debug = false in server.py
    #plt.plot(t_list,tr)
    #plt.plot(r_outlier_x,r_outlier,linestyle = '-',marker = 'o',color = 'r')
    #plt.show()


    #Close file
    fileObject.close()

    return json.dumps({ "inliers" : inliers_final, "outliers" : outliers_final })
