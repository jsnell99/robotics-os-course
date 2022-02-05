#!/usr/bin/env python3

import random
import rospy
from mystery_package.msg import UnitsLabelled #maybe correct?

import rospy

class Listener:
	def __init__(self):
		rospy.Subscriber("/mystery/output2", UnitsLabelled, self.callback)
	def callback(self, msg):
		rospy.loginfo(rospy.get_caller_id() + "published {}".format(msg.data))


if __name__ == '__main__':
    rospy.init_node('listener', anonymous=True)
    Listener()

    # spin() simply keeps python from exiting until this node is stopped

    rospy.spin()
    
    #######################################################################

class Talker:
	def __init__(self):
		self.pub = rospy.Publisher('/hw3_unit_converted', UnitsLabelled, queue_size=10) 
		
	def talk(self):
		conversion = Listener.msg.data*3.28084
		converted = "{} feet".format(converted)
		rospy.loginfo(converted)
		self.pub.publish(converted)
		
if __name__ == '__main__':
	try:
		rospy.init_node('talker', anonymous=True)
		t = Talker()
		rate = rospy.Rate(1)	#1 hz
		while not rospy.is_shutdown():
			t.talk()
			rate.sleep()
	except rospy.ROSInterruptException:
