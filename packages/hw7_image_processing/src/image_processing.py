#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from math import sin, cos

class pubsubber:
	def __init__(self):
		rospy.Subscriber("/image", Image, self.callback)	#register subscriber with ROS
		self.pub = rospy.Publisher('/image_cropped', Image, queue_size=10)	#register publisher with ROS
		self.bridge = CvBridge() #instantiate the converter class once by using class member

	def callback(self, msg):
		#rospy.loginfo(rospy.get_caller_id() + " published {}".format(msg))
		#rospy.loginfo(msg)

		cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8") #convert to cv image using bridge
		#cv_cropped = cv_image[0:500, 0:500]
		ros_cropped = self.bridge.cv2_to_imgmsg(cv_cropped) #convert back to ROS image
	
		self.pub.publish(ros_cropped)	#publish message

		
if __name__ == '__main__':
	rospy.init_node('image_edit', anonymous=True)
	pubsubber()
	rospy.spin() # spin() simply keeps python from exiting until this node is stopped
	
	
