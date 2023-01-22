#!/usr/bin/env python3

import rospy
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
from geometry_msgs.msg import PoseArray
from threading import Thread
import numpy as np
global error_x, error_y,vel_x,vel_y, vel_z, error_xb, error_yb, vel_x2, vel_y2
global x_goals, y_goals, theta_goals
x_goals = []
y_goals = []
theta_goals = []

x_goalsb=0
y_goalsb=0
Kp = 2
Ka = 2.5
hola_x=0.0
hola_y=0.0
hola_x1=0.0
hola_y1=0.0
vel_x=0.0
vel_y=0.0
vel_x2=0.0
vel_y2=0.0
vel_z=0.0
error_theta=0.0
error_x=0.0
error_y=0.0
error_xb=0.0
error_yb=0.0
distance=0.0
vel = Twist()
coords=[0,0,0,0,0]

def getRotation (msg):
	global hola_x, hola_y, coords
	hola_x = msg.pose.pose.position.x
	hola_y = msg.pose.pose.position.y
	coords = msg.pose.pose.orientation
	orentation_list=[coords.x, coords.y, coords.z, coords.w]
	(roll,pitch,yaw) = euler_from_quaternion(orentation_list)


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






def main(i):
	
	global hola_x,hola_y,hola_theta,vel_x1,vel_y1,vel_z1,vel_x2,vel_y2,vel_z2
	global x_goals,y_goals,theta_goals
	rospy.init_node('controller', anonymous=True)
	sub2 = rospy.Subscriber('task1_goals', PoseArray, task1_goals_Cb)
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	sub = rospy.Subscriber('/odom', Odometry, getRotation)
	
	rospy.sleep(0.1)
	
	vel.linear.x=0.0
	vel.linear.y=0.0
	vel.angular.z=0.0

	rate = rospy.Rate(50)
	
	while(i<5):
	
	
		hola_x1=hola_x
		hola_y1=hola_y
		#if(x_goals[0]==0.0 and y_goals[0]==0.0 and theta_goals[0]==0.0):
			#rospy.sleep(0.0001)
		if(i>=len(x_goals)):
			continue
		error_x = x_goals[i]-hola_x1
		error_y = y_goals[i]-hola_y1
				
				
		initial_position = coords
		orentation_list=[coords.x, coords.y, coords.z, coords.w]
		(roll,pitch,yaw) = euler_from_quaternion(orentation_list)
		yaw1=yaw
			
			
			
			
		body_coords = [0 , 0 , 0]
		global_coords = [x_goals[i], y_goals[i] , 1]
		multiplier_matrix = [[math.cos(yaw),math.sin(yaw),(-(hola_x*math.cos(yaw))-(hola_y*math.sin(yaw)))], [-(math.sin(yaw)),math.cos(yaw),((hola_x*math.sin(yaw))-(hola_y*math.cos(yaw)))],[0,0,1]]
		body_coords = np.dot(multiplier_matrix,global_coords)
		x_goalsb = body_coords[0]	
		y_goalsb = body_coords[1]
		
		hola_body = [0,0,0]
		global_hola= [hola_x,hola_y,1]
		hola_body = np.dot(multiplier_matrix,global_hola)
			
		hola_x2 = hola_body[0]
		hola_y2 =hola_body[1]
			
			
		error_xb= x_goalsb-hola_x2
		error_yb= y_goalsb-hola_y2
		if(i>=len(theta_goals)):
			continue	
		error_theta = abs(theta_goals[i] - yaw1)
		error_theta1 = (theta_goals[i]-yaw1)
			
		desired_error=error_theta
		distance = abs(math.sqrt(((error_x)**2) + ((error_y)**2)))
		distanceb= abs(math.sqrt(((error_xb)**2) + ((error_yb)**2)))
		#print(distanceb)
		#print(distanceb)
		vel_z = (error_theta1)*Ka
		
		vel_x2 = (error_xb*Kp)
		vel_y2 = (error_yb*Kp)
			
	
	
		if(distanceb>0.0098 and error_theta>0.01):
			vel.linear.x = vel_x2
			vel.linear.y= vel_y2
			vel.angular.z= vel_z
			pub.publish(vel)
		elif(distanceb<0.0098 and error_theta>0.01):
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z=vel_z
			pub.publish(vel)
		elif(distanceb >0.0098 and error_theta<0.01):
			vel.linear.x=vel_x2
			vel.linear.y=vel_y2
			vel.angular.z=0.0
			pub.publish(vel)
		elif(distanceb <0.0098 and error_theta<0.01):
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z=0.0
			pub.publish(vel)
			rospy.sleep(1)
			i=i+1
			if(i==5):
				while(True):
					vel.linear.x=0.0
					vel.linear.y=0.0
					vel.angular.z=0.0
					pub.publish(vel)
						
	
				
	
	
				
		
	
if __name__ == "__main__":

	while not rospy.is_shutdown():
		try:
			main(0)
			
		except rospy.ROSInterruptException:
			pass		
