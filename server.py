#! /usr/bin/env python
# -*- coding: utf-8 -*-s
from flask import Flask, render_template, jsonify, make_response
from pymongo import MongoClient
from adapter import getDataFromBag
import dbQueryManager
from pprint import pprint

# from pymongo import MongoClient
# client = MongoClient()
# db = client["test_database"]
# collection = db["bagfiles_test"]

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


@app.route('/addData', methods=['POST'])
def addData():
    # newDocument = getDataFromBag('bags/square.bag')
    # bags = db.bagfiles_test
    # post_id = bags.insert_one(newDocument).inserted_id
    # print(post_id)

    ans = {'status': True}
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

if __name__ == '__main__':
    app.run(debug=True)