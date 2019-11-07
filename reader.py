import rosbag
import rosmsg
from operator import itemgetter

bag = rosbag.Bag('bags/2011-01-24-06-18-27.bag')

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

    print("\nNames:")
    for line in names:
        print line
    print("\nTypes:")
    for line in types:
        print line

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
            lines = rosmsg.get_msg_text(value[0])
            # print lines
            # for elem in makeTypes(lines):
                # print(elem)

            # print(type)
        except rosmsg.ROSMsgException as identifier:
            print 'UNKNOWN'
        # for topic, msg, t in bag.read_messages(topics=[key]):

        data.append(storage)
    return data


# for topic, msg, t in bag.read_messages(topics=['/chatter']):
#     print msg
# getBagData(bag)

# tmp = bag.get_type_and_topic_info()[1]
# types = []
# for i in range(0,len(bag.get_type_and_topic_info()[1].values())):
#     types.append(bag.get_type_and_topic_info()[1].values()[i][0])

# print(tmp)
# print(types)
bag.close()


test = '''std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
geometry_msgs/PoseWithCovariance pose
  geometry_msgs/Pose pose
    geometry_msgs/Point position
      float64 x
      float64 y
      float64 z
    geometry_msgs/Quaternion orientation
      float64 x
      float64 y
      float64 z
      float64 w
  float64[36] covariance'''.splitlines()
makeTypes(test)