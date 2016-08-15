import csv
import os
import ntpath
import sys
import collections
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdates
# import datetime
# import numpy as np
import json

def getUiP(inputCSVFile):
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

    #Close file
    fileObject.close()

    return json.dumps({"ip":unique_ip})