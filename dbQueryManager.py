#! /usr/bin/env python
# -*- coding: utf-8 -*-s
from pymongo import MongoClient
from bson.objectid import ObjectId  
import datetime
from pprint import pprint
from adapter import getDataFromBag
from collections import namedtuple

ReturnedTuple = namedtuple('ReturnedTuple', ["data", "status"])

STORAGE_UPLOAD = "bags/"

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

    def addFile(self, collection_name, fileName):
        try:
            bagname = STORAGE_UPLOAD + fileName
            newDocument = getDataFromBag(bagname)
            collection = self.db[collection_name]
            collection.insert_one(newDocument)
        except:
            return False
        return True

    def getNumberOfDocuments(self, collection_name):
        try:
            collection = self.db[collection_name]
            result = collection.count({})
        except:
            return ReturnedTuple(data=0, status=False)
        return ReturnedTuple(data=result, status=True)

    def getBagInfo(self, collection_name):
        try:
            collection = self.db[collection_name]
            resultCursor = collection.aggregate([{
                    "$project": {
                        "filename": 1,
                        "date_creation": 1,
                        "duration": 1,
                    }
                }
            ])
        except:
            return ReturnedTuple(data=[], status=False)
        return ReturnedTuple(data=self.__newGetList(resultCursor), status=True)

    def getBagsByTopics(self, collection_name, bagIds, topics):
        try:
            bagIds = map(ObjectId, bagIds)
            collection = self.db[collection_name]
            resultCursor = collection.aggregate([
                {
                    "$match": {
                        "_id": { "$in": bagIds },
                        "topics_list.topic_name": {
                            "$in": topics
                        }
                    }
                }
            ])
        except:
            return ReturnedTuple(data=[], status=False)            
        return ReturnedTuple(data=self.__newGetList(resultCursor), status=True)

    def getBagsByDateDistance(self, collection_name, bagIds, date, direction):
        if direction == "more":
            cmper = "$gte"
        if direction == "less":
            cmper = "$lte"
        if direction == "exactly":
            cmper = "$eq"
        try:
            bagIds = map(ObjectId, bagIds)
            collection = self.db[collection_name]
            resultCursor = collection.aggregate([{
                    "$match": {
                        "_id": {
                            "$in": bagIds
                        },
                        "date_creation": {
                            cmper: date
                        }
                    }
            }])
        except:
            return ReturnedTuple(data=[], status=False)
        return ReturnedTuple(data=self.__newGetList(resultCursor), status=True)

    def getBagsByDuration(self, collection_name, bagIds, duration, direction):
        if direction == "more":
            cmper = "$gte"
        if direction == "less":
            cmper = "$lte"
        if direction == "exactly":
            cmper = "$eq" # todo особый случай. если 24, то между 24 и 25
        try:
            bagIds = map(ObjectId, bagIds)
            collection = self.db[collection_name]
            resultCursor = collection.aggregate([{
                    "$match": {
                        "_id": {
                            "$in": bagIds
                        },
                        "duration": {
                            cmper: float(duration)
                        }
                    }
            }])
        except:
            return ReturnedTuple(data=[], status=False)
        return ReturnedTuple(data=self.__newGetList(resultCursor), status=True)


    def __newGetList(self, cursor):
        returnedList = []
        for doc in cursor:
            docId = str(doc.pop("_id"))
            doc["id"] = docId
            returnedList.append(doc)
        return returnedList
    
    def getTopicsInfoById(self, collection_name, bagId):
        try:
            collection = self.db[collection_name]
            resultCursor = collection.aggregate([{
                    "$match": {
                        "_id": ObjectId(bagId)
                    }
                }, {
                    "$project": {
                        "msgs_num": "$topics_list.msgs_num",
                        "msgs_type": "$topics_list.msgs_type",
                        "topic_name":"$topics_list.topic_name",
                    }
                }
            ])
        except:
            return ReturnedTuple(data=[], status=False)
        
        returnedList = self.__newGetList(resultCursor)
        return ReturnedTuple(data=returnedList, status=True)

    def getTopicNamesForIds(self, collection_name, bagIds):
        try:
            bagIds = map(ObjectId, bagIds)
            collection = self.db[collection_name]    
            resultCursor = collection.aggregate([{
                    "$match": {
                        "_id": { "$in": bagIds }
                    }
                }, {
                    "$project": {
                        "topic_names": "$topics_list.topic_name",
                    }
                },
                {
                    "$unwind": "$topic_names"
                },
                {
                    "$group": { "_id": "$topic_names" }
                }
            ])
        except:
            return ReturnedTuple(data=[], status=False)
        
        ans = [x['_id'] for x in list(resultCursor)]
        return ReturnedTuple(data=ans, status=True)

    def getMaxMinDatesByIds(self, collection_name, bagIds):
        bagIds = map(ObjectId, bagIds)
        collection = self.db[collection_name]
        ans = collection.aggregate([{
                "$match": {
                    "_id": {
                        "$in": bagIds
                    }
                }
            }, {
                "$group": {
                    "_id": "null",
                    "max": { "$max": "$date_creation" },
                    "min": { "$min": "$date_creation" }
                }
            }, {
                "$project": {
                    "_id": 0
                }
            }
        ])
        ans = list(ans)[0]
        return ans

    def getMaxMinDurationsByIds(self, collection_name, bagIds):
        bagIds = map(ObjectId, bagIds)
        collection = self.db[collection_name]
        ans = collection.aggregate([{
                "$match": {
                    "_id": {
                        "$in": bagIds
                    }
                }
            }, {
                "$group": {
                    "_id": "null",
                    "max": { "$max": "$duration" },
                    "min": { "$min": "$duration" }
                }
            }, {
                "$project": {
                    "_id": 0
                }
            }
        ])
        ans = list(ans)[0]
        return ans

    def getMsgsInfoByIdAndTopicName(self, collection_name, bagId, topic_name):
        try:
            collection = self.db[collection_name]
            bagId = ObjectId(bagId)
            queryText = self.__getQueryToGetMsgsByIdAndTopicName(bagId, topic_name)
            resultCursor = collection.aggregate(queryText)
        except:
            return ReturnedTuple(data=[], status=False)
        
        returnedList = self.__newGetList(resultCursor)
        # Костыль! нужно поправить запрос
        for document in returnedList:
            document['msgs_list'] = document['msgs_list']['msgs_list']
        # /Костыль!
        return ReturnedTuple(data=returnedList, status=True)

    def getMsgsByIdAndTopicNameAndMsgsName(self, collection_name, bagId, topic_name, msg_name):
        collection = self.db[collection_name]
        bagId = ObjectId(bagId)
        queryText = self.__getQueryToGetMsgsByIdAndTopicNameAndMsgsName(bagId, topic_name, msg_name)
        queryText += [{
                "$project": {
                    "_id": 0,
                    "type": "$ans.msg_type",
                    "msgs": "$ans.msgs"
                }
            }
        ]
        ans = collection.aggregate(queryText)
        ans = list(ans)[0]
        ans["isNumeric"] = self.__isNumuricMsgType(ans['type'])
        del ans['type']
        return ans

    def getSummOfMsgs(self, collection_name, bagId, topic_name, msg_name):
        collection = self.db[collection_name]
        bagId = ObjectId(bagId)
        queryText = self.__getQueryToGetMsgsByIdAndTopicNameAndMsgsName(bagId, topic_name, msg_name)
        queryText += [{
                "$project": {
                    "_id": 0,
                    "type": "$ans.msg_type",
                    "summary": { "$sum": "$ans.msgs"}
                }
            },
        ]
        ans = collection.aggregate(queryText)
        return list(ans)[0]

    def getAvgOfMsgs(self, collection_name, bagId, topic_name, msg_name):
        collection = self.db[collection_name]
        bagId = ObjectId(bagId)
        queryText = self.__getQueryToGetMsgsByIdAndTopicNameAndMsgsName(bagId, topic_name, msg_name)
        queryText += [{
                "$project": {
                    "_id": 0,
                    "type": "$ans.msg_type",
                    "average": { "$avg": "$ans.msgs"}
                }
            },
        ]
        ans = collection.aggregate(queryText)
        return list(ans)[0]

    def __getQueryToGetMsgsByIdAndTopicName(self, bagObjId, topic_name):
        return [{
                "$match": {
                    "_id": bagObjId,
                    "topics_list.topic_name": topic_name
                }
            }, {
                "$project": {
                    "msgs_list": {
                        "$filter": {
                            "input": "$topics_list",
                            "as": "item",
                            "cond": { "$eq": ["$$item.topic_name", topic_name] }
                        }
                    }
                }
            }, {
                "$unwind": "$msgs_list"
            },
        ]
    
    def __getQueryToGetMsgsByIdAndTopicNameAndMsgsName(self, bagObjId, topic_name, msg_name):
        queryText = self.__getQueryToGetMsgsByIdAndTopicName(bagObjId, topic_name)
        queryText += [{
                "$project": {
                    "ans": {
                        "$filter": {
                            "input": "$msgs_list.msgs_list",
                            "as": "item",
                            "cond": { "$eq": ["$$item.msg_name", msg_name] }
                        }
                    }
                }
            }, {
                "$unwind": "$ans"
            },
        ]
        return queryText

    @staticmethod
    def __isNumuricMsgType(msg_type):
        return msg_type in ["float32", "float64", "int8", "int16", "int32", "int64"]

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
    print("Test for query manager!")
    
    # lel = manager.getMainInfo(collection)
    # lel = manager.getBagsByTopics(collection, ["quaternionTopic", "poseTopic"])
    # lel = manager.getBagsByTopics(collection, ["/chatter"])
    # lel = manager.getBagsByMsgsNumber(collection, 9, 1000)
    # date = datetime.datetime(2019, 11, 10, 0,0,0,0)
    # lel = manager.getBagsByDateDistance(collection, date, "more")


    

