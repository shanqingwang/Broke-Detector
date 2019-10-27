import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from .brokedetector import process_img

UPLOAD_FOLDER = 'app/static' 
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    filename = ""
    second = False
    error = False
    res = ("", False)
    if request.method == 'POST':
        second = "true"
        # check if the post request has the file part
        if 'file' not in request.files:
            error = "true"
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            error = "true"
        if file and allowed_file(file.filename):
            error = ""
            filename = secure_filename(file.filename)
            full_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(full_file)
            res = process_img(full_file)
        else:
            error = "true"
#process_img(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("index.html", filename=filename,
            out=res[0], res=res[1], error=error,
        second=second)
       

