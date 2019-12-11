#! /usr/bin/env python
# -*- coding: utf-8 -*-s
from flask import Flask, render_template, jsonify, make_response, request, redirect, url_for
from werkzeug.utils import secure_filename
import datetime
import os
from adapter import getDataFromBag
import dbQueryManager
import json

DB = dbQueryManager.dbQueryManager()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = dbQueryManager.STORAGE_UPLOAD
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
    ans = DB.getMainInfo(defaultCollection)
    return make_response(jsonify(ans), 200)


@app.route('/getFilterData', methods=['GET'])
def getFilterData():
    filterItem = request.args.get('filterItem')
    if (filterItem == "date"):
        direction = request.args.get('dir')
        date = request.args.get('date')
        date = datetime.datetime.strptime(date, "%Y-%m-%d %X")
        ans = ""

        if direction == "exactly":
            ans = DB.getBagsByDateDistance(defaultCollection, date, "exactly")
        if direction == "more":
            ans = DB.getBagsByDateDistance(defaultCollection, date, "more")
        if direction == "less":
            ans = DB.getBagsByDateDistance(defaultCollection, date, "less")
    
    if filterItem == "duration":
        duration = request.args.get('duration')
        print(duration)
        ans = DB.getBagsByDuration(defaultCollection, 0, duration)
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
            status = DB.addFile(defaultCollection, filename)
            if status:
                return make_response(jsonify({"status": "server"}), 200)
            else:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return make_response(jsonify({"status": "error"}), 200)

@app.route("/getTopicsById", methods=['GET'])
def getTopicsById():
    bagId = request.args.get('id')
    print(bagId)
    ans = DB.getTopicsInfoById(defaultCollection, bagId)
    return make_response(jsonify(ans), 200)

@app.route("/getMaxMinDatesByIds", methods=['GET'])
def getMaxMinDatesByIds():
    bagIds = json.loads(request.args.get('ids'))
    print("Requestes ids:", bagIds)
    ans = DB.getMaxMinDatesByIds(defaultCollection, bagIds)
    return make_response(jsonify(ans), 200)

@app.route("/getMaxMinDurationsByIds", methods=['GET'])
def getMaxMinDurationsByIds():
    bagIds = json.loads(request.args.get('ids'))
    print("Requestes ids:", bagIds)
    ans = DB.getMaxMinDurationsByIds(defaultCollection, bagIds)
    return make_response(jsonify(ans), 200)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['bag'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS




if __name__ == '__main__':
    app.run(debug=True)