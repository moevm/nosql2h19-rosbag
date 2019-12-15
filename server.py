#! /usr/bin/env python
# -*- coding: utf-8 -*-s
from flask import Flask, render_template, jsonify, make_response, request, redirect, url_for, send_file, send_from_directory
from werkzeug.utils import secure_filename
import datetime
import os
from adapter import getDataFromBag
import dbQueryManager
import json
import io
import zipfile
import time
from up_down_loading import loading_api

app = Flask(__name__)
app.register_blueprint(loading_api)

DB = dbQueryManager.dbQueryManager()
app.config['UPLOAD_FOLDER'] = dbQueryManager.STORAGE_UPLOAD
defaultCollection = "bagfiles_test"

@app.route("/")
def hello(name=None):
    return render_template('index.html', name=name)

@app.route("/getFilesNumber")
def getFilesNumber():
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
    # TODO error "exactly" not working correctly
    filterItem = request.args.get('filterItem')
    bagIds = json.loads(request.args.get('ids'))
    ans = ""

    if not bagIds:
        return make_response(jsonify("No ids to filter"), 200)    
    
    if filterItem == "date":
        date = datetime.datetime.strptime(request.args.get('date'), "%Y-%m-%d %X")
        direction = request.args.get('dir')
        if direction in ["exactly", "more", "less"]:
            ans = DB.getBagsByDateDistance(defaultCollection, bagIds, date, direction)
    
    if filterItem == "duration":
        duration = request.args.get('duration')
        direction = request.args.get('dir')
        if direction in ["exactly", "more", "less"]:
            ans = DB.getBagsByDuration(defaultCollection, bagIds, duration, direction)
    
    if filterItem == "topics":
        topics = json.loads(request.args.get('topics'))
        ans = DB.getBagsByTopics(defaultCollection, bagIds, topics)
    
    return make_response(jsonify(ans), 200)




@app.route('/getStats', methods=['GET'])
def getStats():
    ans = DB.getStats(defaultCollection)
    return make_response(jsonify(ans), 200)


@app.route("/getTopicsInfoById", methods=['GET'])
def getTopicsInfoById():
    bagId = request.args.get('id')
    print(bagId)
    ans = DB.getTopicsInfoById(defaultCollection, bagId)
    return make_response(jsonify(ans), 200)

@app.route("/getTopicsByIds", methods=['GET'])
def getTopicsByIds():
    bagIds = json.loads(request.args.get('ids'))
    ans = DB.getTopicsByIds(defaultCollection, bagIds)
    ans = {"topics": ans}
    return make_response(jsonify(ans), 200)

@app.route("/getMaxMinDatesByIds", methods=['GET'])
def getMaxMinDatesByIds():
    bagIds = json.loads(request.args.get('ids'))
    ans = DB.getMaxMinDatesByIds(defaultCollection, bagIds)
    return make_response(jsonify(ans), 200)

@app.route("/getMaxMinDurationsByIds", methods=['GET'])
def getMaxMinDurationsByIds():
    bagIds = json.loads(request.args.get('ids'))
    ans = DB.getMaxMinDurationsByIds(defaultCollection, bagIds)
    return make_response(jsonify(ans), 200)

@app.route("/getMsgsInfoByIdAndTopicName", methods=['GET'])
def getMsgsInfoByIdAndTopicName():
    bagId = request.args.get('id')
    topic_name = request.args.get('topic_name')
    ans = DB.getMsgsInfoByIdAndTopicName(defaultCollection, bagId, topic_name)
    return make_response(jsonify(ans), 200)


if __name__ == '__main__':
    app.run(debug=True)
    