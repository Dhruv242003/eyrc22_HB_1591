#!/usr/bin/env python3

import rospy
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
from threading import Thread
from geometry_msgs.msg import PoseArray
global error_x, error_y,vel_x, vel_z
global hola_x, hola_y, coords, yaw
x_d = [0,1,-1,0,0]
y_d = [1,-1,-1,1,-1]
Kp = 2.755      #2.75
Ka = 5.515      #4.51
hola_x=0.0
hola_y=0.0
hola_x1=0.0
hola_y1=0.0
vel_x=0.0
vel_y=0.0
vel_z=0.0
error_theta=0.0
coords=[0.0,0.0,0.0,0.0]
error_x=0.0
error_y=0.0
distance=0.0
yaw=0.0
orientation_list=[0.0,0.0,0.0,0.0]
theta_d = [0, 0, 0, 0, 0]


def getRotation (msg):
	global hola_x, hola_y, coords, yaw
	
	hola_x = msg.pose.pose.position.x
	hola_y = msg.pose.pose.position.y
	coords = msg.pose.pose.orientation
	orentation_list=[coords.x, coords.y, coords.z, coords.w]
	yaw = euler_from_quaternion (orientation_list)[2]
	
rospy.init_node('controller2', anonymous=True)


sub = rospy.Subscriber('/odom', Odometry, getRotation)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.sleep(1)
vel = Twist()
vel.linear.x = 0.0
vel.linear.y = 0.0
vel.angular.z = 0.0
	
r = rospy.Rate(50)
i=0



def main(i):
	while True:
		hola_x1=hola_x
		hola_y1=hola_y
		error_x = x_d[i] -hola_x1
		error_y = y_d[i] -hola_y1
		distance = abs(math.sqrt(((error_x)**2) + ((error_y)**2)))
		print("Distance: "+ str(distance))
		orentation_list=[coords.x, coords.y, coords.z, coords.w]
		(roll,pitch,yaw) = euler_from_quaternion(orentation_list)
		yaw1=yaw
		error_theta = theta_d[i] - yaw1
		desired_error=error_theta
		print("desrierd_error: "+ str(desired_error))
		
		if ((theta_d[i]>=0 and theta_d[i]<1.570795) or (theta_d[i]<=0 and theta_d[i]>-1.570795)):
			vel_x = error_x*Kp
			vel_y = error_y*Kp
			vel_z = abs(error_theta*Ka)
			vel.linear.x = vel_x
			vel.linear.y= vel_y
			vel.angular.z=vel_z
			pub.publish(vel)
			#print(distance)
			#print(vel_x)
			#print(vel_y)
			#print(vel_z)
			#print(str(x_d[i])+" "+str(y_d[i])+" "+str(theta_d[i]))
			
			if(distance>0.0 and distance<0.009):
				vel.linear.x=0.0
				vel.linear.y=0.0
				pub.publish(vel)
				if((desired_error>=0.0 and desired_error<0.009) or (desired_error<0.0 and desired_error>=-0.009)):
					vel.angular.z=0.0
					pub.publish(vel)
					rospy.sleep(10)
					break
			r.sleep()
		else:
			vel_x = -(error_x*Kp)
			vel_y = -(error_y*Kp)
			vel_z = abs(error_theta*Ka)
			vel.linear.x = vel_x
			vel.linear.y= vel_y
			vel.angular.z=vel_z
			pub.publish(vel)
			#print(distance)
			#print(vel_x)
			#print(vel_y)
			#print(vel_z)
			#print(str(x_d[i])+" "+str(y_d[i])+" "+str(theta_d[i]))
			
			if(distance>0.0 and distance<0.009):
				vel.linear.x=0.0
				vel.linear.y=0.0
				pub.publish(vel)
				if((desired_error>=0.0 and desired_error<0.009) or (desired_error<0.0 and desired_error>=-0.009)):
					vel.angular.z=0.0
					pub.publish(vel)
					rospy.sleep(10)
					break
			r.sleep()

for i in range (0,len(x_d)):		
	main(i)

