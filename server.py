#! /usr/bin/env python
# -*- coding: utf-8 -*-s
from flask import Flask, render_template, jsonify, make_response, request, redirect, url_for
from werkzeug.utils import secure_filename
import datetime
import os
from adapter import getDataFromBag
import dbQueryManager

UPLOAD_FOLDER = '/path/to/the/uploads'

DB = dbQueryManager.dbQueryManager()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "bags/" 
defaultCollection = "bagfiles_test"

@app.route("/")
def hello(name=None):
    return render_template('index.html', name=name)

@app.route("/getDocumentsNumber")
def getDocsData():
    result = DB.getNumberOfDocuments(defaultCollection)

    ans = {'status': True, 'result': result}
    print(jsonify(ans))
    return make_response(jsonify(ans), 200)

@app.route('/getFaceData', methods=['GET'])
def getFaceData():
    print("Server respones get")
    ans = DB.getMainInfo(defaultCollection)
    return make_response(jsonify(ans), 200)


@app.route('/getFilterData', methods=['GET'])
def getFilterData():
    dir = request.args.get('dir')
    date = datetime.datetime(2019, 11, 7, 0,0,0,0)
    if dir == "more":
        ans = DB.getBagsByDateDistance(defaultCollection, date, "more")
    else:
        ans = DB.getBagsByDateDistance(defaultCollection, date, "less")
    return make_response(jsonify(ans), 200)

@app.route('/getStats', methods=['GET'])
def getStats():
    ans = DB.getStats(defaultCollection)
    return make_response(jsonify(ans), 200)

@app.route("/uploadBags", methods=['GET', 'POST'])
def uploadBags():
    if request.method == 'POST':
        file = request.files['upload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return make_response(jsonify({"ans": "1"}), 200)
    return make_response(jsonify({"status": "error"}), 200)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['bag'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)