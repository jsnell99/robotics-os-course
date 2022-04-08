#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from math import sin, cos

class pubsubber:
	def __init__(self):
		rospy.Subscriber("/image_pub/image", Image, self.callback)	#register subscriber with ROS
		self.pub_cropped = rospy.Publisher('/image_cropped', Image, queue_size=10)	#register publisher with ROS
		self.pub_yellow = rospy.Publisher('/image_yellow', Image, queue_size=10)
		self.pub_white = rospy.Publisher('/image_white', Image, queue_size=10)
		self.bridge = CvBridge() #instantiate the converter class once by using class member

	def callback(self, msg):
		#rospy.loginfo(rospy.get_caller_id() + " published {}".format(msg))
		#rospy.loginfo(msg)

		cv_img = self.bridge.imgmsg_to_cv2(msg, "bgr8") #convert to cv image using bridge
		cv_cropped = cv_img[220:1000, 0:900]
		ros_cropped = self.bridge.cv2_to_imgmsg(cv_cropped, "bgr8") #convert back to ROS image

		hsv_image = cv2.cvtColor(cv_cropped, cv2.COLOR_BGR2HSV)
		yellow_filtered = cv2.inRange(hsv_image, (20,75,210), (100,250, 250))
		white_filtered = cv2.inRange(hsv_image, (0,0,150), (130,30, 255))
		yellow_output = self.bridge.cv2_to_imgmsg(yellow_filtered, "mono8") 
		white_output = self.bridge.cv2_to_imgmsg(white_filtered, "mono8")

		self.pub_white.publish(white_output)
		self.pub_yellow.publish(yellow_output)
		self.pub_cropped.publish(ros_cropped)	#publish message

if __name__ == '__main__':
	rospy.init_node('image_edit', anonymous=True)
	pubsubber()
	rospy.spin() # spin() simply keeps python from exiting until this node is stopped
	
	

