#!/usr/bin/env python3

import rospy
from std_msgs.msg import String, Float32
import numpy as np

class control:
	def __init__(self):
		rospy.Subscriber("velocity", Float32, self.v_cb)		#register subscriber with ROS	#register publisher with ROS
		rospy.Subscriber("error", Float32, self.callback)
		self.pub = rospy.Publisher('control_input', Float32, queue_size=10)
		self.int_last = None
	def v_cb(self, msg):
		self.v = msg.data

	def callback(self, msg):
		#rospy.loginfo(rospy.get_caller_id() + " received {}".format(msg))
		error = msg.data
		time_step = np.float32(0.1)
		derv = self.v
		if self.int_last == None:
			int = error*time_step
			#rospy.logwarn("haven't gotten last int yet")
		else:
			int = error*time_step+self.int_last
			#rospy.logwarn("accumulating last int")
		k_p = 0.4
		k_i = 0.022
		k_d = 0.8
		total_control = k_p*error + k_i*int - k_d*derv
		self.int_last = int
		#rospy.logwarn(str(total_control))
		self.pub.publish(total_control) #publish world coord

if __name__ == '__main__':
	rospy.init_node('transform', anonymous=True)
	control()
	rospy.spin() # spin() simply keeps python from exiting until this node is stopped
