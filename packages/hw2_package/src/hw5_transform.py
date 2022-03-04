#!/usr/bin/env python3

import rospy
import numpy as np
from math import radians, pi, sin, cos
from duckietown_msgs.msg import Vector2D
from std_msgs.msg import String

class transform:
	def __init__(self):
		rospy.Subscriber("/sensor_coord", Vector2D, self.callback)			#register subscriber with ROS
		self.pub1 = rospy.Publisher('/robot_coord', Vector2D, queue_size=10)	#register publisher with ROS
		self.pub2 = rospy.Publisher('/world_coord', Vector2D, queue_size=10)

	def callback(self, msg):
		rospy.loginfo(rospy.get_caller_id() + " published {}".format(msg))

		print(msg)
		point = np.matrix([[msg.x],[msg.y],[1]])
		theta_rw = 135/180*pi
		theta_sr = pi

		T_sr = np.matrix([[cos(theta_sr), -sin(theta_sr), -1], [sin(theta_sr), cos(theta_sr), 0], [0,0,1]])
		T_rw = np.matrix([[cos(theta_rw), -sin(theta_rw), 3], [sin(theta_rw), cos(theta_rw), 2], [0,0,1]])
		
		P_pr = T_sr*point
		P_pw = T_rw*P_pr

		msg.x = P_pr[0]
		msg.y = P_pr[1]
		self.pub1.publish(msg)	#publish robot coord

		msg.x = P_pw[0]
		msg.y = P_pw[1]
		self.pub2.publish(msg) #publish world coord

if __name__ == '__main__':
	rospy.init_node('transform', anonymous=True)
	transform()
	rospy.spin() # spin() simply keeps python from exiting until this node is stopped
