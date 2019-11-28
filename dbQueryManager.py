#! /usr/bin/env python
# -*- coding: utf-8 -*-s
from pymongo import MongoClient
import datetime
from pprint import pprint
from adapter import getDataFromBag


class dbQueryManager(object):
    def __new__(self, db_name="test_database"):
        if not hasattr(self, 'instance'):
            self.instance = super(dbQueryManager, self).__new__(self)
        return self.instance
    '''
    В конструктор передаётся название коллекции и базы данных (опционально).
    '''
    def __init__(self, db_name="test_database"):
        self.client = MongoClient()
        self.db = self.client[db_name]

    def addAll(self, collection_name):
        for bagname in ['bags/Double.bag', 'bags/hello.bag', 'bags/square.bag']:
            newDocument = getDataFromBag(bagname)
            collection = self.db[collection_name]
            post_id = collection.insert_one(newDocument).inserted_id
            print("Id добавленного:", post_id)
        resultCursor = collection.find({}, {"topics_list.msgs_list.msgs" : {"$slice": 10}})
        return self.tmpGetDict(resultCursor)


    def getNumberOfDocuments(self, collection_name):
        collection = self.db[collection_name]
        result = collection.count({})
        # result = 3
        return result

    def getDocumentNames(self, collection_name):
        result = ["Name1", "Name2", "Name3"]
        return result

    def getMainInfo(self, collection_name):
        collection = self.db[collection_name]
        resultCursor = collection.find({}, {"topics_list.msgs_list.msgs" : {"$slice": 10}})
        return self.tmpGetDict(resultCursor)
        # return dbQueryManager.__cursorToMap(resultCursor)

    def getSortedBy(self, collection_name, sortedKey):
        collection = self.db[collection_name]
        resultCursor = collection.find().sort(
            [(sortedKey, 1)]
        )
        return dbQueryManager.__cursorToMap(resultCursor)

    def getBagsByTopics(self, collection_name, topics):
        collection = self.db[collection_name]
        resultCursor = collection.aggregate([
            {
                "$match": {
                    "topics_list.topic_name": {
                        "$in": topics
                    }
                }
            }
        ])
        return dbQueryManager.__cursorToMap(resultCursor)

    def getBagsByDateDistance(self, collection_name, date, direction):
        if direction == "more":
            cmper = "$gte"
        else:
            cmper = "$lte"
        collection = self.db[collection_name]
        resultCursor = collection.find({
            "date_creation": {
                cmper: date
            }
        })
        # return dbQueryManager.__cursorToMap(resultCursor)
        return self.tmpGetDict(resultCursor)

    def getBagsByMsgsNumber(self, collection_name, min_num, max_num):
        collection = self.db[collection_name]
        resultCursor = collection.aggregate([
            {
                "$match": {
                    "topics_list.msgs_num": {
                        "$gte": min_num,
                        "$lte": max_num
                    }
                }
            }
        ])
        return dbQueryManager.__cursorToMap(resultCursor)

        collection = self.db[collection_name]
        all = collection.aggregate([
            {
                "$group": {
                    "_id": "None",
                    "msgsInTopics": {
                        "$push": {
                            "objId": "$_id",
                            "msgsInTopic": "$topics_list.msgs_num"
                        }
                    }
                }
            }
        ])
        res = dbQueryManager.__cursorToMap(all)["None"]["msgsInTopics"]
        res = [x["objId"] for x in res if sum(x['msgsInTopic']) > min_num and  sum(x['msgsInTopic']) < max_num]

        ans = collection.find({
            "_id": {"$in": res}
        })

        # for kek in ans:
        #     pprint(kek["filename"])
        return dbQueryManager.__cursorToMap(ans)

    # def getNumberOfMsgs(self, collection_name):
    #     # pass
    #     resultCursor = collection.aggregate([
    #         {
    #             "$project": {
    #                 "msgs": {
    #                     "$map": {
    #                         "input": "topics_list",
    #                         "as": "topicMsgs",
    #                         "in": {
    #                             "$add": 
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #     ]
            
    #     )
    #     return dbQueryManager.__cursorToMap(resultCursor)
    #     # return list(resultCursor)

    def tmpGetDict(self, iterableOfMaps):
        returned = {}
        for obj in iterableOfMaps:
            objID = str(obj.pop("_id"))
            # print dir(objID)
            # print int(getattr(objID, '_ObjectId__id'), 0)
            returned[objID] = obj
        return returned

    @staticmethod
    def __cursorToMap(iterableOfMaps):
        returned = {}
        for obj in iterableOfMaps:
            objID = obj.pop("_id")
            returned[objID] = obj
        return returned



if __name__ == "__main__":
    manager = dbQueryManager()
    collection = "bagfiles_test"
    
    manager.getNumberOfDocuments(collection)
    manager.getDocumentNames(collection)
    
    lel = manager.getMainInfo(collection)
    # lel = manager.getBagsByTopics(collection, ["quaternionTopic", "poseTopic"])
    # lel = manager.getBagsByTopics(collection, ["/chatter"])
    # lel = manager.getBagsByMsgsNumber(collection, 9, 1000)
    date = datetime.datetime(2019, 11, 10, 0,0,0,0)
    lel = manager.getBagsByDateDistance(collection, date, "more")

    
    # print(manager.getNumberOfMsgs(collection))
    # kek = manager.getSortedBy(collection, "date_creation")
    # kek = [elem["_id"] for elem in kek]
    # print(kek)

    for bag in lel.values():
        print(bag["filename"])
    

