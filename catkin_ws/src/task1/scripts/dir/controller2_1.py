#!/usr/bin/env python3

import rospy
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
from threading import Thread
global error_x, error_y,vel_x, vel_z
x_d = [1, -1, -1, 1, 0]
y_d = [1, 1, -1, -1, 0]
Kp = 3.0
Ka = 0.5
hola_x=0.0
hola_y=0.0
hola_x1=0.0
hola_y1=0.0
vel_x=0.0
vel_y=0.0
vel_z=0.0
error_theta=0.0
error_x=0.0
error_y=0.0
distance=0.0
theta_d = [math.pi/4, 3*(math.pi/4), -3*(math.pi/4), -(math.pi/4), 0]
coords=Odometry()
def getRotation (msg):
	global hola_x, hola_y, coords
	hola_x = msg.pose.pose.position.x
	hola_y = msg.pose.pose.position.y
	coords = msg.pose.pose.orientation
	orentation_list=[coords.x, coords.y, coords.z, coords.w]
	(roll,pitch,yaw) = euler_from_quaternion(orentation_list)
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

def first(i):
	while True:
		hola_x1=hola_x
		hola_y1=hola_y
		error_x = x_d[i] -hola_x1
		error_y = y_d[i] -hola_y1
		distance = abs(math.sqrt(((error_x)**2) + ((error_y)**2)))
		if (theta_d[i]>=0 and theta_d[i]<1.570795) or (theta_d[i]<=0 and theta_d[i]>-1.570795):
			vel_x = error_x*Kp
			vel_y = error_y*Kp
			vel.linear.x = vel_x
			vel.linear.y= vel_y
			vel.angular.z=0.0
			pub.publish(vel)
			print(distance)
			print(vel_x)
			print(vel_y)
			print(str(x_d[i])+" "+str(y_d[i])+" "+str(theta_d[i]))
			if(distance<0.01 and distance>=0.0090 or distance<-0.0090 and distance>=-0.01):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.linear.z=0.0
				pub.publish(vel)
				rospy.sleep(1)	
				break
			r.sleep()
		else:
			vel_x = -(error_x*Kp)
			vel_y = -(error_y*Kp)
			vel.linear.x = vel_x
			vel.linear.y= vel_y
			vel.angular.z=0.0
			pub.publish(vel)
			print(distance)
			print(vel_x)
			print(vel_y)
			print(str(x_d[i])+" "+str(y_d[i])+" "+str(theta_d[i]))
			if(distance<0.01 and distance>=0.0090 or distance<-0.0090 and distance>=-0.01):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.linear.z=0.0
				pub.publish(vel)
				rospy.sleep(1)	
				break
			r.sleep()
			
def second(i):
	while True:
		initial_position = coords
		orentation_list=[coords.x, coords.y, coords.z, coords.w]
		(roll,pitch,yaw) = euler_from_quaternion(orentation_list)
		yaw1=yaw
		error_theta = theta_d[i] - yaw1
		desired_error=error_theta
		vel_z = abs((error_theta)*Kp)
		vel.angular.z = vel_z
		pub.publish(vel)
			
		print(abs(error_theta))
		print(str(x_d[i])+" "+str(y_d[i])+" "+str(theta_d[i]))
			
		if(desired_error<0.01 and desired_error>=0.0090 or desired_error<-0.0090 and desired_error>=-0.01):
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z=0.0
			pub.publish(vel)
			break
		r.sleep()
for i in range (0,5):	
	second(i)	
	first(i)
i=i+1
