#!/usr/bin/env python3

import rospy
import numpy as np
from math import radians, sin, cos
from duckietown_msgs.msg import Vector2D
from std_msgs.msg import String

class transform:
	def __init__(self):
		rospy.Subscriber("/sensor_coord", Vector2D, self.callback)			#register subscriber with ROS
		self.pub1 = rospy.Publisher('/robot_coord', Vector2D, queue_size=10)	#register publisher with ROS
		self.pub2 = rospy.Publisher('/world_coord', Vector2D, queue_size=10)

	def callback(self, msg):
		rospy.loginfo(rospy.get_caller_id() + " published {}".format(msg))

		#print(msg.value)
		theta_rw = 135/180*pi
		theta_sr = pi
		P_a = np.matrix[[18], [8], [1]]
		P_b = np.matrix[[1], [-9], [1]]
		P_c = np.matrix[[-11], [12], [1]]
		P_d = np.matrix[[-20], [-18], [1]]

		T_sr = np.matrix[[cos(theta_rw), -sin(theta_rw), -1], [sin(theta_rw), cos(theta_rw), 0], [0,0,1]]
		T_rw = np.matrix[[cos(theta_sr), -sin(theta_sr), 3], [sin(theta_sr), cos(theta_sr), 2], [0,0,1]]
		
		P_ar = T_sr*P_a
		P_br = T_sr*P_b
		P_cr = T_sr*P_c
		P_dr = T_sr*P_d

		P_aw = T_rw*P_ar
		P_bw = T_rw*P_br
		P_cw = T_rw*P_cr
		P_dw = T_rw*P_dr
		#T_rw = np.matrix[[-1/math.sqrt(2), -1/math.sqrt(2), 3], [1/math.sqrt(2), -1/math.sqrt(2), 2], [0,0,1]]
	
		self.pub1.publish(P_ar, P_br, P_cr, P_dr)	#publish message
		self.pub2.publish(P_aw)
		#, P_bw, P_cw, P_dw)
		#self.pub1.publish("hi")
if __name__ == '__main__':
	rospy.init_node('transform', anonymous=True)
	transform()
	rospy.spin() # spin() simply keeps python from exiting until this node is stopped
