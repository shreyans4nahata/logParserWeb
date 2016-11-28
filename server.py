import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import json
import modules.parse_current as parser
import modules.generalMod as gen
import modules.trainMod as pred
UPLOAD_FOLDER = './uploadedLogs'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'csv', 'log'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cur_filename = ""
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS

#Basic route at '/'
@app.route('/')
def hello():
	return render_template('app.html')

#Route for handling file uploads
@app.route('/upload',methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            saved_file = parser.parser(UPLOAD_FOLDER + '/' + filename)
            return json.dumps({"parsed":saved_file})

    #return render_template('app.html')

#Route for unique Ip's
@app.route('/listOfIp/<filename>',methods = ['POST'] )
def getIpList(filename):
    if filename == "" or filename == None:
        flash('Specify the filename')
        return redirect(request.url)
    if filename :
        return gen.getUiP(filename)

@app.route('/interq',methods = ['POST'])
def IQR():
    param = json.loads(request.data)
    filename = param['filename']
    ip = param['ip']
    alpha = float(param['alpha'])

    if filename == "" or alpha == "" or ip == "":
        flash('Irregular')
        return redirect(request.url)
    return gen.completeListIQR(filename,alpha,ip)

@app.route('/movmedian', methods = ['POST'])
def median():
    param = json.loads(request.data)
    filename = param['filename']
    ip = param['ip']
    alpha = float(param['alpha'])
    window = int(param['window_size'])

    return gen.completeListMed(filename,ip,alpha,window)

@app.route('/movaverage', methods = ['POST'])
def moavg():
    param = json.loads(request.data)
    filename = param['filename']
    ip = param['ip']
    window = int(param['window_size'])

    return gen.completeListMov(filename,ip,window)

@app.route('/createModel', methods = ['POST'])
def createModel():
    param = json.loads(request.data)
    filename = param['filename']
    no_ep = param['no_of_epochs']
    ip = param['ip']

    pred.createFile(filename,ip)
    return pred.modelTrain(filename, no_ep, ip) #Returns model trained msg on success

@app.route('/predict', methods = ['POST'])
def predict():
    param = json.loads(request.data)
    filename = param['filename']
    rang_t = param['range_of_time_stamps']
    ip = param['ip']

    pred.createPredict(filename, ip, rang_t)
    return pred.prediction(filename, ip, rang_t) #Returns prediction result

if __name__ == "__main__":
	app.run(debug = True)
