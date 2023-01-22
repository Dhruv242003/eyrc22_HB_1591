#!/usr/bin/env python3

import rospy
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
from geometry_msgs.msg import PoseArray
from threading import Thread
global error_x, error_y,vel_x, vel_z
global x_goals, y_goals, theta_goals
x_goals = [0, 0, 0, 0, 0]
y_goals = [0, 0, 0, 0, 0]
Kp = 2.5
Ka = 1.0
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
theta_goals = [0.0, 0.0, 0.0, 0.0, 0.0]
coords=Odometry()
def getRotation (msg):
	global hola_x, hola_y, coords
	hola_x = msg.pose.pose.position.x
	hola_y = msg.pose.pose.position.y
	coords = msg.pose.pose.orientation
	orentation_list=[coords.x, coords.y, coords.z, coords.w]
	(roll,pitch,yaw) = euler_from_quaternion(orentation_list)
rospy.init_node('controller', anonymous=True)

def task1_goals_Cb(msg):
	global x_goals, y_goals, theta_goals

	x_goals.clear()
	y_goals.clear()
	theta_goals.clear()

	for waypoint_pose in msg.poses:
		x_goals.append(waypoint_pose.position.x)
		y_goals.append(waypoint_pose.position.y)

		orientation_q = waypoint_pose.orientation
		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		theta_goal = euler_from_quaternion (orientation_list)[2]
		theta_goals.append(theta_goal)


sub = rospy.Subscriber('/odom', Odometry, getRotation)
sub2 = rospy.Subscriber('task1_goals', PoseArray, task1_goals_Cb)
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
		error_x = x_goals[i] -hola_x1
		error_y = y_goals[i] -hola_y1
		distance = abs(math.sqrt(((error_x)**2) + ((error_y)**2)))
		if (theta_goals[i]>=0.0 and theta_goals[i]<1.570795) or (theta_goals[i]<=0.0 and theta_goals[i]>-1.570795):
			vel_x = error_x*Kp
			vel_y = error_y*Kp
			vel.linear.x = vel_x
			vel.linear.y= vel_y
			vel.angular.z=0.0
			pub.publish(vel)
			if(distance<0.001 and distance>=0.0009 or distance<-0.0009 and distance>=-0.001):
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
			if(distance<0.001 and distance>=0.0009 or distance<-0.0009 and distance>=-0.001):
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
		error_theta = theta_goals[i] - yaw1
		desired_error=error_theta
		vel_z = abs((error_theta)*Ka)
		vel.angular.z = vel_z
		pub.publish(vel)
			
		if(desired_error<0.001 and desired_error>=0.0009 or desired_error<-0.0009 and desired_error>=-0.001):
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
