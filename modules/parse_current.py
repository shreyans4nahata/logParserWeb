# A simple parser for log files.
import sys
import os
import ntpath
import re
import csv
import collections
import datetime
import numpy as np
import json

def parser(inputFileName):

	# Opening the file
	inputFile = open(inputFileName,"r")

	# Creating output file
	outputDir = os.getcwd() + "/parsedOutput/"
	outputFileName = outputDir + os.path.splitext(ntpath.basename(inputFileName))[0] + ".csv"

	# Opening output file
	outputFile = open(outputFileName,"w+")

	#Row name fields (Currently settitng sample names)
	fieldnames = ['f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12','f13','f14','f15']

	#Defining the attributes for the csv file
	writer = csv.DictWriter(outputFile,fieldnames=fieldnames)

	writer.writeheader()

	# The Initial regex
	logRegex = "\[(.*?)\] ([(\d\.)]+) ([(\d\.)]+) - - (\d*) (\S+) (\S*)(\s*)(\S*)(\s*)(\S*)(\s*)(\d*) (\w*)(\W*) (\w+)"

	#To keep the count of line no.
	lineCount = 0

	try:

		for eachLine in inputFile:

			lineCount+=1
			extTuple = list(re.match(logRegex,eachLine).groups())

			#Creating a dictionary to store the current row values
			d1 = {}

			#Adding lineCount value to field 'f0'
			d1['f0'] = lineCount

			if 'HTTP' not in extTuple[7]:
				#Solution to the get request parameters shifting to http version field in the output
				del extTuple[6]
				del extTuple[7]

			extTupleLen = len(extTuple)

			for i in range(extTupleLen):
				#i+1 done as need to access fields from 'f1'
				d1[fieldnames[i+1]] = extTuple[i]

			writer.writerow(d1)

			#Clear the dictionary
			d1.clear()

	except Exception as e:

		print e
		print "Occured at line: " + str(lineCount)

	inputFile.close()
	outputFile.close()
	#Return output file name
	return outputFileName

# Modified parser which removes outliers too
def modParser(inputFileName,req_ip):

	alpha = 1.5
	inliers_final = []
	outliers_final = []

	outputDir = os.getcwd() + "/parsedOutput/"
	fileObject = open(outputDir+os.path.splitext(ntpath.basename(inputFileName))[0]+".csv","r")
	reader = csv.DictReader(fileObject)
    
	timestamp = [] # list to store all timestamps includes duplicates
	ip = [] # list to store all remote ip's

	# storing timestamp and ip's in a list
	for row in reader:
		timestamp.append(datetime.datetime.strptime(row['f1'].split(" ")[0], "%d/%b/%Y:%H:%M:%S"))
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

	len_tr = len(tr)

	q75, q25 = np.percentile(tr, [75 ,25])
	iqr = q75 - q25
	ul = q75 + alpha*iqr
	ll = q25 - alpha*iqr
	print q75,q25,iqr
	outlier = []
	outlier_x = []
	index = 0
	for h in range(len_tr):
		new_dict = {}
		if tr[h] < ll or tr[h] > ul:
			tr[h] = (ll + ul)/2
		new_dict["x"] =  index
		new_dict["y"] =  tr[h]
		new_dict["time"] = t_list[h]
		inliers_final.append(new_dict)
		index+=1

	outputFileName = outputDir + "ModParsed_" + str(req_ip) + "_" + os.path.splitext(ntpath.basename(inputFileName))[0] + ".csv"

	# Opening output file
	outputFile = open(outputFileName,"w+")

	fieldnames = ['Timestamp','RequestHits']

	#Defining the attributes for the csv file
	writer = csv.DictWriter(outputFile,fieldnames=fieldnames)

	writer.writeheader()

	try:

		for i in range(len_tr):

			#Creating a dictionary to store the current row values
			d1 = {}

			#Adding lineCount value to field 'f0'
			d1['Timestamp'] = t_list[i]
			d1['RequestHits'] = tr[i]

			writer.writerow(d1)

			#Clear the dictionary
			d1.clear()

	except Exception as e:

		print e

	#Closing file objects
	fileObject.close()
	outputFile.close()


	return json.dumps({ "Mod FIle" : outputFileName })