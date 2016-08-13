# A simple parser for log files.
import sys
import os
import ntpath
import re
import csv

def parser(inputFileName):

	# Opening the file
	inputFile = open(inputFileName,"r")

	# Creating output file
	outputDir = os.getcwd() + "/parsedOutput/"
	outputFileName = outputDir + "Parsed_" + os.path.splitext(ntpath.basename(inputFileName))[0] + ".csv"

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
