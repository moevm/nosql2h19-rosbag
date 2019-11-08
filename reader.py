import rosbag
import rosmsg
import csv
from operator import itemgetter
import json

def makeTypes(lines):
    types = []
    names = []
    real_names = []

    for line in lines:
        curSpaces = len(line) - len(line.lstrip())
        newLine = line.lstrip()
        type, name = newLine.split()
        types.append([curSpaces, type, True])
        names.append([curSpaces, name, True])
    
    names = mergeLines(names)
    names = [elem[1] for elem in names if elem[2]]

    types = mergeLines(types)
    types = [elem[1] for elem in types if elem[2]]

    return (types, names, real_names)

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

        


def getBagData(bag):
    data = []
    for key, value in bag.get_type_and_topic_info()[1].items():
        storage = {}
        storage["topic_name"] = key
        storage["msgs_num"] = value[1]
        storage["msgs_type"] = value[0]
        storage["msgs_list"] = []
        try:
            lines = rosmsg.get_msg_text(value[0]).splitlines()
            msgTypes, msgNames, real_names = makeTypes(lines)
            for type in msgTypes:
                print type
            for name in msgNames:
                print name
        except rosmsg.ROSMsgException:
            print 'UNKNOWN'
        
        for i in range(len(msgNames)):
            storage["msgs_list"].append({"msg_name" : msgNames[i], "msg_type" : msgTypes[i], "msgs" : []})
        # for topic, msg, t in bag.read_messages(topics=[key]):
        #     print str(msg)
        #     break

        data.append(storage)
    return data

# bag = rosbag.Bag('bags/2011-01-24-06-18-27.bag')
bag = rosbag.Bag('bags/square.bag')
data = getBagData(bag)
print json.dumps(data, indent=2)
bag.close()

# csv_path = "bags/square/_slash_turtle1_slash_cmd_vel.csv"
# with open(csv_path, "r") as f_obj:
#     reader = csv.reader(f_obj)
#     names = reader.next()
#     print names

    
#     for row in reader:
#         content = list(row[i] for i in [1,2])
#         print content
