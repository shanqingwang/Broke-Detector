import os
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from .brokedetector import process_img

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

error = False

def error():
    return error
            
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            error = True
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            error = True
        if file and allowed_file(file.filename):
            error = False
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#process_img(os.path.join(app.config['UPLOAD_FOLDER'], filename))



    return '''
    <!doctype html>
    <title>Broke Detector</title>
    <h1>Broken?</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    <head>
      {% if error %}
      <div>Bad file</div>
      {% else &}
      <img src="{{ os.path.join(app.config['UPLOAD_FOLDER'], filename }}"
      width="200" height="85">
      {% endif %}
    </head>
    '''

       

