import rosbag
import rosmsg
from operator import itemgetter

def makeTypes(lines):
    types = []
    names = []

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
            msgTypes, msgNames = makeTypes(lines)
            print(msgTypes)
            print(msgNames)
        except rosmsg.ROSMsgException as identifier:
            print 'UNKNOWN'
        # for topic, msg, t in bag.read_messages(topics=[key]):

        data.append(storage)
    return data

bag = rosbag.Bag('bags/2011-01-24-06-18-27.bag')
getBagData(bag)
bag.close()