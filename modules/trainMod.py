import csv
import os
import ntpath
import collections
import datetime
import numpy
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.layers import Dense
import json

outputDir = os.getcwd() + "/parsedOutput/"
modelDir = os.getcwd() + "/builtModels/"

def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return numpy.array(dataX), numpy.array(dataY)

def createFile(filename,req_ip):

	outputDir = os.getcwd() + "/parsedOutput/"
	fileObject = open(outputDir+os.path.splitext(ntpath.basename(filename))[0]+".csv","r") 
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
	#final_dict = {}
	#tr = [] # list containing request hits at particular ip
	#t_list = [] #list containg formatted timestamp

 	# initialization of request hit to 0 corresponding timestamp
	for j in range(len(timestamp)):
		temp_dict[timestamp[j]] = 0

	# incrementing the count for each ip
	for j in range(len(timestamp)):
		if ip[j] == str(req_ip):
			temp_dict[timestamp[j]]+=1

	# sorting dictionary by keys
	od = collections.OrderedDict(sorted(temp_dict.items()))
	#print od

	#Creating new parsed o/p file
	outputFileName = outputDir + "Parsed_"+str(req_ip)+"_"+os.path.splitext(ntpath.basename(filename))[0] + ".csv"

	# Opening output file
	outputFile = open(outputFileName,"w+")

	fieldnames = ['Timestamp','RequestHits']

	#Defining the attributes for the csv file
	writer = csv.DictWriter(outputFile,fieldnames=fieldnames)

	writer.writeheader()

	try:

		for key,val in od.iteritems():
			
			#Creating a dictionary to store the current row values
			d1 = {}

			#Adding lineCount value to field 'f0'
			d1['Timestamp'] = key
			d1['RequestHits'] = val

			writer.writerow(d1)

			#Clear the dictionary
			d1.clear()

	except Exception as e:

		print e

	#Closing file objects
	fileObject.close()
	outputFile.close()

	return

def modelTrain(filename, no_ep, req_ip):

	# fix random seed for reproducibility
	numpy.random.seed(7)
	
	no_ep = int(no_ep)

	inpFileName = outputDir + "Parsed_"+str(req_ip)+"_"+os.path.splitext(ntpath.basename(filename))[0] + ".csv"	
	
	# load the dataset
	dataframe = pd.read_csv( inpFileName ,usecols=[1], engine='python', skipfooter=0)
	
	dataset = dataframe.values
	dataset = dataset.astype('float32')

	# split into train and test sets
	train_size = int(len(dataset))
	
	#test_size = len(dataset) - train_size
	train= dataset[0:train_size,:]
	print(len(train))
	
	# reshape into X=t and Y=t+1
	look_back = 1
	trainX, trainY = create_dataset(train, look_back)
	
	# create and fit Multilayer Perceptron model
	model = Sequential()
	model.add(Dense(8, input_dim=look_back, activation='relu'))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='rmsprop')
	
	model.fit(trainX, trainY, nb_epoch=no_ep, batch_size=2, verbose=2)
	
	# Estimate model performance
	trainScore = model.evaluate(trainX, trainY, verbose=0)
	print('Train Score: %.2f MSE (%.2f RMSE)' % (trainScore, math.sqrt(trainScore)))

	#Files for the given IP's
	model_file_name = modelDir + str(req_ip) + "model.json"
	model_weights_name = modelDir + str(req_ip) + "model.h5"

	#save model to json format
	model_json = model.to_json()
	with open(model_file_name, 'w') as json_file:
		json_file.write(model_json)
	model.save_weights(model_weights_name)
	print "saved"

	# generate predictions for training
	trainPredict = model.predict(trainX)

	# shift train predictions for plotting
	trainPredictPlot = numpy.empty_like(dataset)
	trainPredictPlot[:, :] = numpy.nan
	trainPredictPlot[look_back:len(trainPredict)+look_back, :] = trainPredict



	print len(trainPredictPlot)
	# plot baseline and predictions
	plt.plot(dataset)
	plt.plot(trainPredictPlot)
	plt.show()

	return json.dumps({"msg" : "Model Trained" })

filename = raw_input("file: ")
ip = raw_input("ip: ")
createFile(filename,ip)
ep = raw_input("ep")
k = modelTrain(filename, ep, ip)
print k
