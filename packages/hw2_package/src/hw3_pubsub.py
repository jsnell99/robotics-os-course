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
		rospy.loginfo(rospy.get_caller_id() + " published {}".format(msg))
		#if rospy.has_param("meters"):
		#	self.foo=rospy.get_param("meters")
		#	self.publish(msg)
		#if rospy.has_param("feet"):
			#self.foo=rospy.get_param("feet")
		msg.value = msg.value*3.28084
		msg.units='feet'
		rospy.loginfo(msg)
		self.pub.publish(msg)	#publish message
		#if rospy.has_param("smoots"):
		#	self.foo=rospy.get_param("smoots")
		#	msg.value = msg.value/1.7018
		#	msg.units = 'smoots'
		#	rospy.loginfo(msg)
		#	self.pub.publish(msg)
		#else:
		#	self.foo="default"
		
if __name__ == '__main__':
	rospy.init_node('hw3_pubsub', anonymous=True)
	pubsubber()
	rospy.spin() # spin() simply keeps python from exiting until this node is stopped
	
	

