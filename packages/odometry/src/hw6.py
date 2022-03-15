#!/usr/bin/env python3

import rospy
from odometry_hw_msgs.msg import (DistWheel, Pose2D)
from math import sin, cos

class pubsubber:
	theta = 0
	x = 0
	y = 0
	def __init__(self):
		rospy.Subscriber("/dist_wheel", DistWheel, self.callback)	#register subscriber with ROS
		self.pub = rospy.Publisher('/pose', Pose2D, queue_size=10)	#register publisher with ROS
		
	def callback(self, msg):
		rospy.loginfo(rospy.get_caller_id() + " published {}".format(msg))
		rospy.loginfo(msg)

		L=.05
		dist_left = msg.dist_wheel_left
		dist_right = msg.dist_wheel_right
		dist_mid = (dist_left+dist_right)/2
		delta_theta = (dist_r-dist_l)/(2*L)
		delta_x = delta__mid*cos(theta+delta_theta/2)
		delta_y = delta__mid*sin(theta+delta_theta/2)

		theta+=delta_theta
		x+= delta_x
		y+= delta_y

		new_coords = [x, y, theta]
		self.pub.publish(new_coords)	#publish message

		
if __name__ == '__main__':
	rospy.init_node('hw3_pubsub', anonymous=True)
	pubsubber()
	rospy.spin() # spin() simply keeps python from exiting until this node is stopped
	
	

