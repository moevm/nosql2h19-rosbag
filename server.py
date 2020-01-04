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
# is not used
def getFilesNumber():
    answerFromDB = DB.getNumberOfDocuments(defaultCollection)
    if answerFromDB.status:
        return make_response(jsonify(answerFromDB.data), 200)
    else:
        return make_response(jsonify({}), 500)

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

    if not bagIds:
        return make_response(jsonify("No ids to filter"), 200)    
    
    if filterItem == "date":
        date = datetime.datetime.strptime(request.args.get('date'), "%Y-%m-%d %X")
        direction = request.args.get('dir')
        if direction in ["exactly", "more", "less"]:
            answerFromDB = DB.getBagsByDateDistance(defaultCollection, bagIds, date, direction)
    
    if filterItem == "duration":
        duration = request.args.get('duration')
        direction = request.args.get('dir')
        if direction in ["exactly", "more", "less"]:
            answerFromDB = DB.getBagsByDuration(defaultCollection, bagIds, duration, direction)
    
    if filterItem == "topics":
        topics = json.loads(request.args.get('topics'))
        answerFromDB = DB.getBagsByTopics(defaultCollection, bagIds, topics)
    
    if answerFromDB.status:
        return make_response(jsonify(answerFromDB.data), 200)
    else:
        return make_response(jsonify({}), 500)


@app.route("/getTopicsInfoById", methods=['GET'])
def getTopicsInfoById():
    bagId = request.args.get('id')
    answerFromDB = DB.getTopicsInfoById(defaultCollection, bagId)

    if answerFromDB.status:
        assert len(answerFromDB.data) == 1, "Must find only one document!"
        return make_response(jsonify(answerFromDB.data[0]), 200)
    else:
        return make_response(jsonify({}), 500)


@app.route("/getTopicNamesForIds", methods=['GET'])
def getTopicNamesForIds():
    bagIds = json.loads(request.args.get('ids'))
    answerFromDB = DB.getTopicNamesForIds(defaultCollection, bagIds)

    if answerFromDB.status:
        return make_response(jsonify(answerFromDB.data), 200)
    else:
        return make_response(jsonify({}), 500)

@app.route("/getMaxMinDatesByIds", methods=['GET'])
def getMaxMinDatesByIds():
    bagIds = json.loads(request.args.get('ids'))
    answerFromDB = DB.getMaxMinDatesByIds(defaultCollection, bagIds)

    if answerFromDB.status:
        return make_response(jsonify(answerFromDB.data), 200)
    else:
        return make_response(jsonify({}), 500)

@app.route("/getMaxMinDurationsByIds", methods=['GET'])
def getMaxMinDurationsByIds():
    bagIds = json.loads(request.args.get('ids'))
    answerFromDB = DB.getMaxMinDurationsByIds(defaultCollection, bagIds)
    
    if answerFromDB.status:
        return make_response(jsonify(answerFromDB.data), 200)
    else:
        return make_response(jsonify({}), 500)

@app.route("/getMsgsInfoByIdAndTopicName", methods=['GET'])
def getMsgsInfoByIdAndTopicName():
    bagId = request.args.get('id')
    topic_name = request.args.get('topic_name')
    answerFromDB = DB.getMsgsInfoByIdAndTopicName(defaultCollection, bagId, topic_name)

    if answerFromDB.status:
        assert len(answerFromDB.data) == 1, "Must find only one document!"
        return make_response(jsonify(answerFromDB.data[0]), 200)
    else:
        return make_response(jsonify({}), 500)


@app.route("/getMsgsByIdAndTopicNameAndMsgsName", methods=['GET'])
def getMsgsByIdAndTopicNameAndMsgsName():
    bagId = request.args.get('id')
    topic_name = request.args.get('topic_name')
    msg_name = request.args.get('msg_name')

    answerFromDB = DB.getMsgsByIdAndTopicNameAndMsgsName(defaultCollection, bagId, topic_name, msg_name)

    if answerFromDB.status:
        del answerFromDB.data['isNumeric']
        return make_response(jsonify(answerFromDB.data), 200)
    else:
        return make_response(jsonify({}), 500)


@app.route("/getSummOfMsgs", methods=['GET'])
def getSummOfMsgs():
    bagId = request.args.get('id')
    topic_name = request.args.get('topic_name')
    msg_name = request.args.get('msg_name')
    answerFromDB = DB.getSummOfMsgs(defaultCollection, bagId, topic_name, msg_name)

    if answerFromDB.status:
        answerFromDB.data["isValid"] = True
        if not answerFromDB.data['type'] in ["float32", "float64", "int8", "int16", "int32", "int64"]:
            answerFromDB.data["isValid"] = False
        del answerFromDB.data['type']
        return make_response(jsonify(answerFromDB.data), 200)
    else:
        return make_response(jsonify({}), 500)


@app.route("/getAvgOfMsgs", methods=['GET'])
def getAvgOfMsgs():
    bagId = request.args.get('id')
    topic_name = request.args.get('topic_name')
    msg_name = request.args.get('msg_name')
    answerFromDB = DB.getAvgOfMsgs(defaultCollection, bagId, topic_name, msg_name)
    
    if answerFromDB.status:
        answerFromDB.data["isValid"] = True
        if not answerFromDB.data['type'] in ["float32", "float64", "int8", "int16", "int32", "int64"]:
            answerFromDB.data["isValid"] = False
        del answerFromDB.data['type']
        return make_response(jsonify(answerFromDB.data), 200)
    else:
        return make_response(jsonify({}), 500)


@app.route("/getGraph", methods=['GET'])
def getGraph():
    bagId = request.args.get('id')
    topic_name = request.args.get('topic_name')
    msg_name = request.args.get('msg_name')
    answerFromDB = DB.getMsgsByIdAndTopicNameAndMsgsName(defaultCollection, bagId, topic_name, msg_name)

    if answerFromDB.status:
        output = io.BytesIO()
        if answerFromDB.data['isNumeric']:
            fig = Figure(figsize=(9, 6), dpi=80)
            axis = fig.add_subplot(1, 1, 1)
            xs = range(len(answerFromDB.data['msgs']))
            ys = answerFromDB.data['msgs']
            axis.plot(xs, ys)
            FigureCanvas(fig).print_png(output)
        
        r = Response(output.getvalue(), mimetype='image/png')
        r.headers['isNumeric'] = answerFromDB.data['isNumeric']
        return r
    else:
        return make_response(jsonify({}), 500)



if __name__ == '__main__':
    app.run(debug=True)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    