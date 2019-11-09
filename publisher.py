#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Quaternion

def talker():
    pub = rospy.Publisher('poseTopic', Pose, queue_size=10)
    pub2 = rospy.Publisher('quaternionTopic', Quaternion, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(5) # 10hz
    for i in range(5):
        msg = Pose()
        msg.position.x = 1.1
        msg.position.y = 2.2
        msg.position.z = 3.3
        msg.orientation.x = 10.1 + i
        msg.orientation.y = 12.1 + i
        msg.orientation.z = 23.1 + i
        rospy.loginfo(str(msg))
        pub.publish(msg)

        msg = Quaternion()
        msg.x = 10
        msg.y = float(100) / (i+1) 
        msg.z = 10 + i
        msg.w = 22.2
        pub2.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass