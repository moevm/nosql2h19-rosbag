from flask import Flask, render_template, jsonify, make_response
from pymongo import MongoClient
from adapter import getDataFromBag
from dbQueryManager import dbQueryManager
# from pprint import pprint
# client = MongoClient()
queryManager = dbQueryManager("bagfiles_test")
app = Flask(__name__)

# print(getDataFromBag('bags/Double.bag'))

@app.route("/")
def hello(name=None):
    return render_template('index.html', name=name)

@app.route("/getDocunentsNumber")
def getDocsData():
    result = queryManager.getNumberOfDocuments()

    ans = {'status': True, 'result': result}
    print(jsonify(ans))
    return make_response(jsonify(ans), 200)


@app.route('/addData', methods=['POST'])
def addData():
    # db = client.test_database
    # topic = "quaternionTopic"
    # msgName = "x"
    # summary = db.bagfiles_test.aggregate([
    #  { "$match": { 
    #     "$and": [
    #          { "filename": "bags/Double.bag" },
    #          { "topics_list.topic_name": topic },
    #          { "topics_list.msgs_list.msg_name": msgName }
    #     ]
    #  } }, # Match documents to shrink their quantity
    #  { "$project": {
    #     #  "list": "$topics_list.msgs_list.msgs",
    #      "filteredByTopic": {
    #          "$filter": {
    #             "input": "$topics_list",
    #             "cond": { "$and": [
    #                 { "$eq": [ '$$this.topic_name', topic ] },
    #              ] }
    #          }
    #      }
    #  } }, # Filter topics_list by topic name
    #  { "$project": {
    #      "filteredByTopic": {"$arrayElemAt": ["$filteredByTopic", 0] },
    #  } }, # Take first elem in result
    #  { "$project": {
    #      "filteredByTopic": "$filteredByTopic.msgs_list",
    #  } }, # Take msges in that topic
    #  { "$project": {
    #      "filteredByMsgName": {
    #          "$filter": {
    #              "input": "$filteredByTopic",
    #              "cond": {
    #                  "$eq": [ "$$this.msg_name", msgName]
    #              }
    #          }
    #      }
    #  } }, # Filter msges by msg name
    #  { "$project": {
    #      "filteredByMsgName": {"$arrayElemAt": ["$filteredByMsgName", 0] },
    #  } }, # Take first elem in result
    # #  { "$project": {
    # #      "sum": { "$sum": "$filteredByMsgName.msgs" },
    # #  } }, # Sum all elements in msgs
    # ]) # .next()
    # # pprint(list(summary));
    # numbersList = list(summary)[0]['filteredByMsgName']['msgs']
    # firstEl = numbersList[0]
    # print("List elem type:", type(firstEl))
    # print("Array:")
    # print(numbersList)
    # numbersList = map(float, numbersList)
    # print("Sum:", sum(numbersList))
    db = client.test_database
    newDocument = getDataFromBag('bags/square.bag')
    bags = db.bagfiles_test
    post_id = bags.insert_one(newDocument).inserted_id
    print(post_id)

    ans = {'status': True}
    print(jsonify(ans))
    return make_response(jsonify(ans), 200)


if __name__ == '__main__':
    app.run(debug=True)