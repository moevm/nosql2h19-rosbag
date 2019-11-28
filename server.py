#! /usr/bin/env python
# -*- coding: utf-8 -*-s
from flask import Flask, render_template, jsonify, make_response, request
import datetime
from pymongo import MongoClient
from adapter import getDataFromBag
import dbQueryManager
from pprint import pprint

DB = dbQueryManager.dbQueryManager()
app = Flask(__name__)
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


@app.route('/addData', methods=['GET'])
def addData():
    print "add data resp"
    ans = DB.addAll(defaultCollection)
    print(jsonify(ans))
    return make_response(jsonify(ans), 200)

@app.route('/getFaceData', methods=['GET'])
def getFaceData():
    print("Server respones get")
    ans = DB.getMainInfo(defaultCollection)
    # ans = collection.count({})
    print(ans)
    # print(DB.db)
    return make_response(jsonify(ans), 200)


@app.route('/getFilterData', methods=['GET'])
def getFilterData():
    print("Server respones", request.args.get('dir'))
    dir = request.args.get('dir')
    date = datetime.datetime(2019, 11, 7, 0,0,0,0)
    if dir == "more":
        ans = DB.getBagsByDateDistance(defaultCollection, date, "more")
    else:
        ans = DB.getBagsByDateDistance(defaultCollection, date, "less")
    # ans = collection.count({})
    print(len(ans))
    # print(DB.db)
    return make_response(jsonify(ans), 200)
if __name__ == '__main__':
    app.run(debug=True)