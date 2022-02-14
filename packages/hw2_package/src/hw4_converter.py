#!/usr/bin/env python3

import random
import rospy
from mystery_package.msg import UnitsLabelled

import rospy

class pubsubber:
	def __init__(self):
		rospy.Subscriber("/mystery/output2", UnitsLabelled, self.callback)			#register subscriber with ROS
		self.pub = rospy.Publisher('hw3_unit_converted', UnitsLabelled, queue_size=10)	#register publisher with ROS
		
	def callback(self, msg):
		rospy.loginfo(rospy.get_caller_id() + " initially published {}".format(msg))
			
		if rospy.has_param("unit"):
			self.foo=rospy.get_param("unit")
			if self.foo == 'meters':
				rospy.loginfo(msg)
				self.pub.publish(msg)	#publish message
			if self.foo == 'feet':
				msg.value = msg.value*3.28084
				msg.units = self.foo
				rospy.loginfo(msg)
				self.pub.publish(msg)	
			if self.foo == 'smoots':
				msg.value = msg.value/1.7018
				msg.units = self.foo
				rospy.loginfo(msg)
				self.pub.publish(msg)
		else:
			self.foo="default"
			self.pub.publish(msg)
		
if __name__ == '__main__':
	rospy.init_node('hw3_pubsub', anonymous=True)
	pubsubber()
	rospy.spin() # spin() simply keeps python from exiting until this node is stopped
	

