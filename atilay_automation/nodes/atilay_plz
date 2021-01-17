#!/usr/bin/env python


import rospy
import math
from sensor_msgs.msg import Range
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def stream(data):
	pub=rospy.Publisher('atilay/cmd_vel', Twist, queue_size=10)
	distance=data.range
	twist = Twist()
	if distance < 1.5:
		twist.linear.z=0.4
	elif distance >= 1.5:
		twist.linear.z=-0.4
	

        rospy.loginfo(twist)
        pub.publish(twist)
        	
		

def streamer():
	rospy.init_node('streamer', anonymous=True)

	rospy.Subscriber("atilay/sonar", Range, stream)

	rate = rospy.Rate(100)

	while not rospy.is_shutdown():
		rate.sleep()	

if __name__ == '__main__':
    try:
        streamer()
    except rospy.ROSInterruptException:
        pass
