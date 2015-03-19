#!/usr/local/bin/python

import threading
import time
import sys
import os
import logging
import string
import random


from flask import Flask, request
from sqlalchemy import create_engine
from werkzeug import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['log']);

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024



def rstring():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
        
def allowed_file(filename):
        return '.' in filename and \
                filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
# Flask routing.

@app.route('/')
def root():
        return 'This is the root of the varnish report gatherer.'

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                       rstring() + "-" + filename))
                return("OK");
        else:
                return("ERROR");
    else:
        return("Please submit a test result. 'make report' in the source tree.")

if __name__ == '__main__':
    app.run(debug=True)
