#! /usr/bin/env python
# -*- coding: utf-8 -*-s
from pymongo import MongoClient
from bson.objectid import ObjectId  
import datetime
from pprint import pprint
from adapter import getDataFromBag

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



    def addAll(self, collection_name):
        for bagname in ['bags/Double.bag', 'bags/hello.bag', 'bags/square.bag']:
            newDocument = getDataFromBag(bagname)
            collection = self.db[collection_name]
            post_id = collection.insert_one(newDocument).inserted_id
        resultCursor = collection.find({}, {"topics_list.msgs_list.msgs" : {"$slice": 10}})
        return self.tmpGetDict(resultCursor)



    def addFile(self, collection_name, fileName):
        try:
            bagname = STORAGE_UPLOAD + fileName
            newDocument = getDataFromBag(bagname)
            collection = self.db[collection_name]
            collection.insert_one(newDocument)
        except Exception:
            return False
        return True



    def getNumberOfDocuments(self, collection_name):
        collection = self.db[collection_name]
        result = collection.count({})
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

    def getBagsByTopics(self, collection_name, bagIds, topics):
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
        return self.tmpGetDict(resultCursor)
        # return dbQueryManager.__cursorToMap(resultCursor)

    def getBagsByDateDistance(self, collection_name, bagIds, date, direction):
        bagIds = map(ObjectId, bagIds)
        if direction == "more":
            cmper = "$gte"
        if direction == "less":
            cmper = "$lte"
        if direction == "exactly":
            cmper = "$eq"
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
        # return dbQueryManager.__cursorToMap(resultCursor)
        return self.tmpGetDict(resultCursor)

    def getBagsByDuration(self, collection_name, bagIds, duration, direction):
        bagIds = map(ObjectId, bagIds)
        if direction == "more":
            cmper = "$gte"
        if direction == "less":
            cmper = "$lte"
        if direction == "exactly":
            cmper = "$eq" # todo особый случай. если 24, то между 24 и 25
        collection = self.db[collection_name]
        
        print("Duration:", float(duration))
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


    def getStats(self, collection_name):
        collection = self.db[collection_name]
        topic = "quaternionTopic"
        msgName = "x"
        summary = collection.aggregate([
            { "$match": { 
            "$and": [
                    { "filename": "Double.bag" },
                    { "topics_list.topic_name": topic },
                    { "topics_list.msgs_list.msg_name": msgName }
            ]
            } }, # Match documents to shrink their quantity
            { "$project": {
            #  "list": "$topics_list.msgs_list.msgs",
                "filteredByTopic": {
                    "$filter": {
                    "input": "$topics_list",
                    "cond": { "$and": [
                        { "$eq": [ '$$this.topic_name', topic ] },
                        ] }
                    }
                }
            } }, # Filter topics_list by topic name
            { "$project": {
                "filteredByTopic": {"$arrayElemAt": ["$filteredByTopic", 0] },
            } }, # Take first elem in result
            { "$project": {
                "filteredByTopic": "$filteredByTopic.msgs_list",
            } }, # Take msges in that topic
            { "$project": {
                "filteredByMsgName": {
                    "$filter": {
                        "input": "$filteredByTopic",
                        "cond": {
                            "$eq": [ "$$this.msg_name", msgName]
                        }
                    }
                }
            } }, # Filter msges by msg name
            { "$project": {
                "filteredByMsgName": {"$arrayElemAt": ["$filteredByMsgName", 0] },
            } }, # Take first elem in result
        { "$project": {
            "sum": { "$sum": "$filteredByMsgName.msgs" },
        } }, # Sum all elements in msgs
        ]) # .next()
        return self.tmpGetDict(sum)

    def getNumberOfMsgs(self, collection_name):
        pass

    def tmpGetDict(self, iterableOfMaps):
        returned = {}
        for obj in iterableOfMaps:
            objID = str(obj.pop("_id"))
            # print dir(objID)
            # print int(getattr(objID, '_ObjectId__id'), 0)
            returned[objID] = obj
        return returned
    
    def getTopicsInfoById(self, collection_name, bagId):
        collection = self.db[collection_name]
        ans = collection.aggregate([{
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
        return self.tmpGetDict(ans)

    def getTopicsByIds(self, collection_name, bagIds):
        bagIds = map(ObjectId, bagIds)
        collection = self.db[collection_name]    
        ans = collection.aggregate([{
                "$match": {
                    "_id": {
                        "$in": bagIds
                    }
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
                "$group": {
                    "_id": "$topic_names",
                }
            }
        ])
        ans = [x['_id'] for x in list(ans)]
        return ans  

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
                    "max": {
                        "$max": "$date_creation"
                    },
                    "min": {
                        "$min": "$date_creation"
                    }
                }
        }])
        ans = list(ans)[0]
        del ans["_id"]
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
                    "max": {
                        "$max": "$duration"
                    },
                    "min": {
                        "$min": "$duration"
                    }
                }
        }])
        ans = list(ans)[0]
        del ans["_id"]
        return ans

    def getMsgsInfoByIdAndTopicName(self, collection_name, bagId, topic_name):
        collection = self.db[collection_name]
        ans = collection.aggregate([{
                "$match": {
                    "_id": ObjectId(bagId),
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
            }
        ])
        return self.tmpGetDict(ans)

    def getMsgsByIdAndTopicNameAndMsgsName(self, collection_name, bagId, topic_name, msg_name):
        collection = self.db[collection_name]
        ans = collection.aggregate([{
                "$match": {
                    "_id": ObjectId(bagId),
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
            {
                "$project": {
                    "msgs": '$msgs_list.msgs_list'
                }
            },
            {
                "$project": {
                    "ans": {
                        "$filter": {
                            "input": "$msgs",
                            "as": "item",
                            "cond": { "$eq": ["$$item.msg_name", msg_name] }
                        }
                    }
                }
            }, {
                "$unwind": "$ans"
            },{
                "$project": {
                    "_id": 0,
                    "type": "$ans.msg_type",
                    "msgs": "$ans.msgs"
                }
            }
            
        ])
        ans = list(ans)[0]
        ans["isNumeric"] = self.__isNumuricMsgType(ans['type'])
        del ans['type']
        return ans

    def getSummOfMsgs(self, collection_name, bagId, topic_name, msg_name):
        collection = self.db[collection_name]
        ans = collection.aggregate([{
                "$match": {
                    "_id": ObjectId(bagId),
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
            {
                "$project": {
                    "msgs": '$msgs_list.msgs_list'
                }
            },
            {
                "$project": {
                    "ans": {
                        "$filter": {
                            "input": "$msgs",
                            "as": "item",
                            "cond": { "$eq": ["$$item.msg_name", msg_name] }
                        }
                    }
                }
            }, {
                "$unwind": "$ans"
            },
            {
                "$project": {
                    "_id": 0,
                    "type": "$ans.msg_type",
                    "summary": { "$sum": "$ans.msgs"}
                }
            },
        ])
        return list(ans)[0]

    def getAvgOfMsgs(self, collection_name, bagId, topic_name, msg_name):
        collection = self.db[collection_name]
        ans = collection.aggregate([{
                "$match": {
                    "_id": ObjectId(bagId),
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
            {
                "$project": {
                    "msgs": '$msgs_list.msgs_list'
                }
            },
            {
                "$project": {
                    "ans": {
                        "$filter": {
                            "input": "$msgs",
                            "as": "item",
                            "cond": { "$eq": ["$$item.msg_name", msg_name] }
                        }
                    }
                }
            }, {
                "$unwind": "$ans"
            },
            {
                "$project": {
                    "_id": 0,
                    "type": "$ans.msg_type",
                    "average": { "$avg": "$ans.msgs"}
                }
            },
        ])
        return list(ans)[0]

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
    
    manager.getNumberOfDocuments(collection)
    manager.getDocumentNames(collection)
    
    lel = manager.getMainInfo(collection)
    # lel = manager.getBagsByTopics(collection, ["quaternionTopic", "poseTopic"])
    # lel = manager.getBagsByTopics(collection, ["/chatter"])
    # lel = manager.getBagsByMsgsNumber(collection, 9, 1000)
    date = datetime.datetime(2019, 11, 10, 0,0,0,0)
    # lel = manager.getBagsByDateDistance(collection, date, "more")

    
    # print(manager.getNumberOfMsgs(collection))
    # kek = manager.getSortedBy(collection, "date_creation")
    # kek = [elem["_id"] for elem in kek]
    # print(kek)

    # for bag in lel.values():
    #     print(bag["filename"])
    

