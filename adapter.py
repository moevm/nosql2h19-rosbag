#! /usr/bin/env python
# -*- coding: utf-8 -*-
import rosbag
import rosmsg
from operator import itemgetter
import string
from datetime import datetime
import os
from pprint import pprint

__all__ = ["getDataFromBag"]

def getDataFromBag(bag_path):
    bag = rosbag.Bag(bag_path)
    structure = getBagStructureWithoutMsgs(bag)
    msgsWithTopics = getMsgsWithTopic(bag)
    bag.close()

    mergeStructureAndMsgs(structure, msgsWithTopics)
    return structure


def getBagStructureWithoutMsgs(bag):
    bagfile = {}
    _, tail = os.path.split(bag.filename)
    bagfile["filename"] = tail
    bagfile["date_creation"] = datetime.fromtimestamp(bag.get_start_time())
    bagfile["duration"] = bag.get_end_time() - bag.get_start_time()
    bagfile["topics_list"] = []
    for key, value in bag.get_type_and_topic_info()[1].items():    
        storage = {}
        storage["topic_name"] = key
        storage["msgs_num"] = value[1]
        storage["msgs_type"] = value[0]
        storage["msgs_list"] = []
        try:
            lines = rosmsg.get_msg_text(value[0]).splitlines()
            msgTypes, msgNames = makeTypes(lines)
        except rosmsg.ROSMsgException:
            print 'UNKNOWN TYPE OS MSG'
        
        for i in range(len(msgNames)):
            storage["msgs_list"].append({"msg_name" : msgNames[i], "msg_type" : msgTypes[i], "msgs" : []})
        bagfile["topics_list"].append(storage)
    return bagfile

def makeTypes(lines):
    types = []
    names = []

    for line in lines:
        newLine = line.lstrip()
        curSpaces = len(line) - len(newLine)
        type, name = newLine.split()
        types.append([curSpaces, type, True])
        names.append([curSpaces, name, True])
    
    names = mergeLines(names)
    names = [elem[1] for elem in names if elem[2]]

    types = mergeLines(types)
    types = [elem[1] for elem in types if elem[2]]

    return (types, names)

def mergeLines(lines):
    minIndent = min(lines, key=itemgetter(0))[0]
    maxIndent = max(lines, key=itemgetter(0))[0]
    
    while minIndent != maxIndent:
        lastMinValue = ""
        lastMinValueIndex = -1
        index = 0

        for line in lines:
            if line[0] == minIndent:
                lastMinValue = line[1]
                lastMinValueIndex = index
            if line[0] > minIndent:
                if line[0] - 2 == minIndent:
                    line[1] = lastMinValue + "/" + line[1]
                    lines[lastMinValueIndex][2] = False
                line[0] -= 2
            if line[0] < minIndent:
                print "error"
            index += 1
        minIndent = min(lines, key=itemgetter(0))[0]
        maxIndent = max(lines, key=itemgetter(0))[0]

    return lines

def getMsgsWithTopic(bag):
    bagContents = bag.read_messages()

    #get list of topics from the bag
    listOfTopics = []
    msgaOfTopics = {}
    for topic, msg, t in bagContents:
        if topic not in listOfTopics:
            listOfTopics.append(topic)

    for topicName in listOfTopics:
        msgaOfTopics[topicName] = []
        firstIteration = True	#allows header row
        for _, msg, t in bag.read_messages(topicName):	# for each instant in time that has data for topicName
            #parse data from this instant, which is of the form of multiple lines of "Name: value\n"
            #	- put it in the form of a list of 2-element lists\
            msgString = str(msg)
            msgList = string.split(msgString, '\n')
            instantaneousListOfData = []
            for nameValuePair in msgList:
                splitPair = string.split(nameValuePair, ':')
                for i in range(len(splitPair)):	#should be 0 to 1
                    splitPair[i] = string.strip(splitPair[i])
                instantaneousListOfData.append(splitPair)
            #write the first row from the first element of each pair
            if firstIteration:	# header
                headers = ["rosbagTimestamp"]	#first column header
                for pair in instantaneousListOfData:
                    headers.append(pair[0])
                msgaOfTopics[topicName].append(headers)
                firstIteration = False
            # write the value from each pair to the file
            values = [str(t)]	#first column will have rosbag timestamp
            for pair in instantaneousListOfData:
                if len(pair) > 1:
                    values.append(pair[1])
            msgaOfTopics[topicName].append(values)
    return msgaOfTopics

def mergeStructureAndMsgs(bagfile, msgsWithTopics):
    for topicName, msgsList in msgsWithTopics.items():
        names = msgsList[0]
        names = names[1:] # убираем TimeStomp

        msgsInColumns = []
        for row in msgsList[1:]: # убираем TimeStomp
            content = list(row[i] for i in range(1, len(names)+1))
            msgsInColumns.append(content)

        prev = 0
        fullMsgsList = []
        stack = []
        columnNumbersOfMsg = []
        index = 0

        for name in names:
            if msgsInColumns[0][index] == '':
                if prev == 0: # если предыдуший тоже пустой
                    stack.append(name)
                if prev == 1: # если пред не пустой
                    stack.pop()
                    stack.append(name)
                prev = 0
            else: # если столбец не пустой
                res = '/'.join(stack + [name])
                fullMsgsList.append(res)
                prev = 1
                columnNumbersOfMsg.append(index)
            index += 1
        
        for topic_record in bagfile["topics_list"]:
            if topic_record["topic_name"] == topicName:
                for msgDict in topic_record["msgs_list"]:
                    msgNumber = 0
                    for msgName in fullMsgsList:
                        if msgName == msgDict["msg_name"]:
                            for row in msgsInColumns:
                                msg = row[columnNumbersOfMsg[msgNumber]]
                                msgtype = msgDict["msg_type"]
                                rightMsg = getMsgWithRightType(msg, msgtype)
                                msgDict["msgs"].append(rightMsg)
                            break
                        msgNumber += 1

def getMsgWithRightType(msg, msgType):
    type = msgType.split('/')[-1]
    if type in ["float32", "float64"]:
        return float(msg)
    if type in ["int8", "int16", "int32", "int64"]:
        return int(msg)
    return msg

if __name__ == "__main__":
    # bagName = 'bags/2011-01-24-06-18-27.bag')
    from pymongo import MongoClient
    client = MongoClient()
    db = client["test_database"]

    for bagname in ['bags/Double.bag', 'bags/hello.bag', 'bags/square.bag']:
        newDocument = getDataFromBag(bagname)
        print(newDocument)
        # bags = db.bagfiles_test
        # post_id = bags.insert_one(newDocument).inserted_id
        # print(post_id)