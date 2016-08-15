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

    # storing timestamp and ip's in a list
    for row in reader:
        timestamp.append(row['f1'])
        ip.append(row['f2'])

    unique_ip = list(set(ip)) # contains unique ip's

    unique_ip_len = len(unique_ip)

    #Close file
    fileObject.close()

    return json.dumps({"ip":unique_ip})

def completeListIQR(inputCSVFile,alpha,ip):

    alpha = abs(alpha)
    
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
        if ip[j] == ip:
            temp_dict[timestamp[j]]+=1

    # sorting dictionary by keys
    od = collections.OrderedDict(sorted(temp_dict.items()))

    for t,i in od.iteritems():
        #sp_dict = {}
        time,dis =t.split(' ')
        time_stamp = datetime.datetime.strptime(time,'%d/%b/%Y:%H:%M:%S')
        time_val = mdates.date2num(time_stamp)
        t_list.append(time_val)
        tr.append(i)
        #inliers_final.append({"x":time_val,"y":i})
    
    diff_tim = []
    diff_tim.append(0)
    for x in range(1,len(t_list)):
        diff_tim.append(t_list[x] - t_list[0])
    
    print tr
    q75, q25 = np.percentile(tr, [75 ,25])
    iqr = q75 - q25
    ul = q75 + alpha*iqr
    ll = q25 - alpha*iqr

    print q75,q25
    outlier = []
    outlier_x = []
    for h in range(len(tr)):
        if tr[h] < ll or tr[h] > ul:
            
            outliers_final.append({"x": t_list[h],"y":tr[h]})
        else:
            inliers_final.append({"x": t_list[h],"y":tr[h]})

    return json.dumps({ "inliers" : inliers_final, "outliers" : outliers_final })