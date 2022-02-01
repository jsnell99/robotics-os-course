#!/usr/bin/env python3

import random
import rospy
from std_msgs.msg import Float32 #maybe correct?

class Talker:
	def __init__(self):
		self.pub = rospy.Publisher('/mystery/input', Float32, queue_size=10) #may need /mystery/input
		
	def talk(self):
		rng = random.randint(0,10)
		rospy.loginfo(rng)
		self.pub.publish(rng)
		
if __name__ == '__main__':
	try:
		rospy.init_node('talker', anonymous=True)
		t = Talker()
		rate = rospy.Rate(1)	#1 hz
		while not rospy.is_shutdown():
			t.talk()
			rate.sleep()
	except rospy.ROSInterruptException:
		pass
