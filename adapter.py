import rosbag
import rosmsg
import csv
from operator import itemgetter
import json

__all__ = ["getDataFromBag"]

def getDataFromBag(bag_path):
    bag = rosbag.Bag(bag_path)
    bag.close()
    
    data = []
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

        data.append(storage)
    return data

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

        


if __name__ == "__main__":
    # bagName = 'bags/2011-01-24-06-18-27.bag')
    bagName = 'bags/Double.bag'
    data = getDataFromBag(bagName)
    print json.dumps(data, indent=2)

# csv_path = "bags/square/_slash_turtle1_slash_cmd_vel.csv"
# with open(csv_path, "r") as f_obj:
#     reader = csv.reader(f_obj)
#     names = reader.next()
#     print names

    
#     for row in reader:
#         content = list(row[i] for i in [1,2])
#         print content
