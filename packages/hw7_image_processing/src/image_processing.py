#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class image_cropper:
	def __init__(self):
		rospy.Subscriber("image", Image, self.callback)	#register subscriber with ROS
		self.pub = rospy.Publisher('image_cropped', Image, queue_size=10)	#register publisher with ROS
		self.bridge = CvBridge() #instantiate the converter class once by using class member

	def callback(self, msg):
		cv_img = self.bridge.imgmsg_to_cv2(msg, "8UC3") #convert to cv image using bridge
		cv_cropped = cv_img[0:240, 0:640]
		ros_cropped = self.bridge.cv2_to_imgmsg(cv_cropped, "8UC3") #convert back to ROS image
	
		self.pub.publish(ros_cropped)	#publish message

		
if __name__ == '__main__':
	rospy.init_node('image_edit', anonymous=True)
	image_cropper()
	rospy.spin() # keeps python from exiting until this node is stopped
	
	
