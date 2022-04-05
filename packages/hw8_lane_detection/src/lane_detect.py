#!/usr/bin/env python3

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from math import sin, cos, pi
import numpy as np

class pubsubber:
	def __init__(self):
		rospy.Subscriber("/image_white", Image, self.callback_white) #register subscriber with ROS
		rospy.Subscriber("/image_yellow", Image, self.callback_yellow)
		rospy.Subscriber("/image_cropped", Image, self.callback)
		self.pub_edges = rospy.Publisher('/image_edges', Image, queue_size=10)	#register publisher with ROS
		self.pub_white = rospy.Publisher('/image_lines_white', Image, queue_size=10)
		self.pub_yellow = rospy.Publisher('/image_lines_yellow', Image, queue_size=10)

		self.bridge = CvBridge() #instantiate the converter class once by using class member


	def callback_white(self, msg):
		self.cv_white = self.bridge.imgmsg_to_cv2(msg, "bgr8")

	def callback_yellow(self, msg):
		self.cv_yellow = self.bridge.imgmsg_to_cv2(msg, "bgr8")

	def callback(self, msg):
		#rospy.loginfo(rospy.get_caller_id() + " published {}".format(msg))
		#rospy.loginfo(msg)
		cv_cropped = self.bridge.imgmsg_to_cv2(msg, "bgr8") #convert to cv image using bridge
		image_canny = cv2.Canny(cv_cropped,200 ,400)
		canny_output = self.bridge.cv2_to_imgmsg(image_canny, "mono8")
		
		self.pub_edges.publish(canny_output)

		edges_white = cv2.bitwise_and(image_canny, self.cv_white, mask=None) #combining canny edge detection and filtered image
		edges_yellow = cv2.bitwise_and(image_canny, self.cv_yellow, mask=None)
		lines_white = cv2.HoughLinesP(edges_white, rho=1, theta=pi/180, threshold=10, lines=50, minLineLength=10, maxLineLength=22)
		lines_yellow = cv2.HoughLinesP(edges_yellow, rho=1, theta=pi/180, threshold=10, lines=50, minLineLength=10, maxLineLength=22)

		#draws set of lines on hough image
		hough_white = np.copy(lines_white)
		if lines_white is not None:
			for i in range(len(lines_white)):
				l = lines_white[i][0]
				cv2.line(hough_white, (l[0],l[1]), (l[2],l[3]), (255,0,0), 2, cv2.LINE_AA)
				cv2.circle(hough_white, (l[0],l[1]), 2, (0,255,0))
				cv2.circle(hough_white, (l[2],l[3]), 2, (0,0,255))

		hough_yellow = np.copy(lines_yellow)
		if lines_yellow is not None:
			for i in range(len(lines_yellow)):
				l = lines_yellow[i][0]
				cv2.line(hough_yellow, (l[0],l[1]), (l[2],l[3]), (255,0,0), 2, cv2.LINE_AA)
				cv2.circle(hough_yellow, (l[0],l[1]), 2, (0,255,0))
				cv2.circle(hough_yellow, (l[2],l[3]), 2, (0,0,255))

		#image_line_white = output_lines(self, edges_white, lines_white)
		#image_line_yellow = output_lines(self, edges_yellow, lines_yellow)
		white_output = self.bridge.cv2_to_imgmsg(hough_white, "mono8")
		yellow_output = self.bridge.cv2_to_imgmsg(hough_yellow, "mono8")
		
		self.pub_white.publish(white_output)
		self.pub_yellow.publish(yellow_output)


if __name__ == '__main__':
	rospy.init_node('image_edit', anonymous=True)
	pubsubber()
	rospy.spin() # spin() simply keeps python from exiting until this node is stopped
	