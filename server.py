import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import json
import modules.parse_current as parser
UPLOAD_FOLDER = '/home/shreyansh/Documents/code/logParserWeb/uploadedLogs'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'csv', 'log'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cur_filename = ""
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOWED_EXTENSIONS

#Basic route at '/'
@app.route('/')
def hello():
	return json.dumps({"message":"hello"})

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
            parser.parser(UPLOAD_FOLDER + '/' + filename)
            return json.dumps({"message":"success!!"})

    return render_template('sample_upload.html')

if __name__ == "__main__":
	app.run(debug = True)