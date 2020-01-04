#! /usr/bin/env python
# -*- coding: utf-8 -*-s
from flask import Flask, render_template, jsonify, make_response, request, send_file
import datetime
import json
import pprint

import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


from adapter import getDataFromBag

app = Flask(__name__)
from up_down_loading import loading_api
app.register_blueprint(loading_api)

import dbQueryManager
DB = dbQueryManager.dbQueryManager()

app.config['UPLOAD_FOLDER'] = dbQueryManager.STORAGE_UPLOAD
app.config["defaultCollection"] = "bagfiles_test"
defaultCollection = app.config["defaultCollection"]



@app.route("/")
def hello(name=None):
    return render_template('index.html', name=name)

@app.route("/getFilesNumber")
def getFilesNumber():
    result = DB.getNumberOfDocuments(defaultCollection)

    ans = {'status': True, 'result': result}
    print(jsonify(ans))
    return make_response(jsonify(ans), 200)

@app.route('/getBagInfo', methods=['GET'])
def getBagInfo():
    answerFromDB = DB.getBagInfo(defaultCollection)
    if answerFromDB.status:
        return make_response(jsonify(answerFromDB.data), 200)
    else:
        return make_response(jsonify({}), 500)


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


@app.route("/getTopicsInfoById", methods=['GET'])
def getTopicsInfoById():
    bagId = request.args.get('id')
    answer = DB.getTopicsInfoById(defaultCollection, bagId)
    if answer.status:
        assert len(answer.data) == 1, "Must find only one document!"
        return make_response(jsonify(answer.data[0]), 200)
    else:
        return make_response(jsonify({}), 500)


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
    answer = DB.getMsgsInfoByIdAndTopicName(defaultCollection, bagId, topic_name)

    if answer.status:
        assert len(answer.data) == 1, "Must find only one document!"
        return make_response(jsonify(answer.data[0]), 200)
    else:
        return make_response(jsonify({}), 500)


@app.route("/getMsgsByIdAndTopicNameAndMsgsName", methods=['GET'])
def getMsgsByIdAndTopicNameAndMsgsName():
    bagId = request.args.get('id')
    topic_name = request.args.get('topic_name')
    msg_name = request.args.get('msg_name')
    ans = DB.getMsgsByIdAndTopicNameAndMsgsName(defaultCollection, bagId, topic_name, msg_name)
    del ans['isNumeric']
    return make_response(jsonify(ans), 200)


@app.route("/getSummOfMsgs", methods=['GET'])
def getSummOfMsgs():
    bagId = request.args.get('id')
    topic_name = request.args.get('topic_name')
    msg_name = request.args.get('msg_name')
    ans = DB.getSummOfMsgs(defaultCollection, bagId, topic_name, msg_name)

    ans["isValid"] = True
    if not ans['type'] in ["float32", "float64", "int8", "int16", "int32", "int64"]:
        ans["isValid"] = False
    del ans['type']
    return make_response(jsonify(ans), 200)


@app.route("/getAvgOfMsgs", methods=['GET'])
def getAvgOfMsgs():
    bagId = request.args.get('id')
    topic_name = request.args.get('topic_name')
    msg_name = request.args.get('msg_name')
    ans = DB.getAvgOfMsgs(defaultCollection, bagId, topic_name, msg_name)
    
    ans["isValid"] = True
    if not ans['type'] in ["float32", "float64", "int8", "int16", "int32", "int64"]:
        ans["isValid"] = False
    del ans['type']
    return make_response(jsonify(ans), 200)


@app.route("/getGraph", methods=['GET'])
def getGraph():
    bagId = request.args.get('id')
    topic_name = request.args.get('topic_name')
    msg_name = request.args.get('msg_name')
    ans = DB.getMsgsByIdAndTopicNameAndMsgsName(defaultCollection, bagId, topic_name, msg_name)

    output = io.BytesIO()
    if ans['isNumeric']:
        fig = Figure(figsize=(9, 6), dpi=80)
        axis = fig.add_subplot(1, 1, 1)
        xs = range(len(ans['msgs']))
        ys = ans['msgs']
        axis.plot(xs, ys)
        FigureCanvas(fig).print_png(output)
    
    r = Response(output.getvalue(), mimetype='image/png')
    r.headers['isNumeric'] = ans['isNumeric']
    return r



if __name__ == '__main__':
    app.run(debug=True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    