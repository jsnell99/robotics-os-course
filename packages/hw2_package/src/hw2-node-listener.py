#!/usr/bin/env python3
# adapted from http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29

import rospy

from std_msgs.msg import Float32

class Listener:
	def __init__(self):
		rospy.Subscriber("/mystery/output1", Float32, self.callback)
	def callback(self, msg):
		rospy.loginfo(rospy.get_caller_id() + "published %s", msg.data)


if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    Listener()

    # spin() simply keeps python from exiting until this node is stopped

    rospy.spin()


