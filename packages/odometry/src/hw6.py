#!/usr/bin/env python3

import rospy
from odometry_hw.msg import (DistWheel, Pose2D)
from math import sin, cos

class pubsubber:
	def __init__(self):
		rospy.Subscriber("/dist_wheel", DistWheel, self.callback)	#register subscriber with ROS
		self.pub = rospy.Publisher('/pose', Pose2D, queue_size=10)	#register publisher with ROS
		
		self.pose = Pose2D()
		self.theta = 0
		self.x = 0
		self.y= 0

	def callback(self, msg):
		rospy.loginfo(rospy.get_caller_id() + " published {}".format(msg))
		rospy.loginfo(msg)

		L=.05
		dist_left = msg.dist_wheel_left
		dist_right = msg.dist_wheel_right
		dist_mid = (dist_left+dist_right)/2
		delta_theta = (dist_right-dist_left)/(2*L)
		delta_x = dist_mid*cos(self.theta+delta_theta/2)
		delta_y = dist_mid*sin(self.theta+delta_theta/2)

		
		self.theta += delta_theta
		self.x += delta_x
		self.y += delta_y
		#last_theta = 

		self.pose.x = self.x
		self.pose.y = self.y
		self.pose.theta = self.theta
		self.pub.publish(self.pose)	#publish message

		
if __name__ == '__main__':
	rospy.init_node('pos_tracker', anonymous=True)
	pubsubber()
	rospy.spin() # spin() simply keeps python from exiting until this node is stopped
	
	

