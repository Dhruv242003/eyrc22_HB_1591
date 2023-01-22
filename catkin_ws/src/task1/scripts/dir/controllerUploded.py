#!/usr/bin/env python3

import rospy
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
from geometry_msgs.msg import PoseArray
global x_goals, y_goals, theta_goals
x_goals = [0,0,0,0,0]
y_goals = [0,0,0,0,0]
Kp = 6.5
Ka = 6.5
theta_goals=[0,0,0,0,0]
j=-1
global error_x, error_y,vel_x,vel_y, vel_z,distance

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


def getRotation (msg):
	vel = Twist()
	global hola_x, hola_y, coords,yaw, dist, j
	hola_x = msg.pose.pose.position.x
	hola_y = msg.pose.pose.position.y
	coords = msg.pose.pose.orientation
	orentation_list=[coords.x, coords.y, coords.z, coords.w]
	yaw = euler_from_quaternion(orentation_list)[2]
	if j==-1:
		dist = coord_calc(hola_x, hola_y,0)
		
		if dist<0.04:
			j = yaw_calc(yaw,0,j)
	elif j==0:
		dist = coord_calc(hola_x, hola_y,0)
		
		if dist<0.04:
			j = yaw_calc(yaw,0,j)
	elif j==1:
		j = yaw_calc(yaw,6,j)
	elif j==2:
		dist = coord_calc(hola_x, hola_y,1)
		
		if dist<0.04:
			j = yaw_calc(yaw,1,j)
	elif j==3:
		j = yaw_calc(yaw,6,j)
	elif j==4:
		dist = coord_calc(hola_x, hola_y,2)
		
		if dist<0.04:
			j = yaw_calc(yaw,2,j)
	elif j==5:
		j = yaw_calc(yaw,6,j)
	elif j==6:
		dist = coord_calc(hola_x, hola_y,3)
		
		if dist<0.04:
			j = yaw_calc(yaw,3,j)
	elif j==7:
		j = yaw_calc(yaw,6,j)
	elif j==8:
		dist = coord_calc(hola_x, hola_y,4)
		
		if dist<0.04:
			j = yaw_calc(yaw,4,j)
	else: 
		vel.linear.x=0.0
		vel.linear.y=0.0
		vel.angular.z=0.0
		pub.publish(vel)
			
def yaw_calc(yaw,i,j):
	vel = Twist()
	theta_d=theta_goals.copy()
	if i>=0 and i<5:
		print(str(theta_d[i])+" "+str(yaw))
		if theta_d[i]>=0 and yaw>=0.00:
			error_theta = theta_d[i] - yaw
			
			vel_z = (error_theta)*Ka
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z = vel_z
			pub.publish(vel)
			if((error_theta<0.009 and error_theta>=0.008) or (error_theta<-0.008 and error_theta>=-0.009)):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
				rospy.sleep(1.25)
				j=j+1
		elif theta_d[i]<0 and yaw<0 :
			theta_d[i]=6.283+theta_d[i]
			yaw=6.283+yaw
			error_theta = theta_d[i] - yaw
				
			vel_z = (error_theta)*Ka
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z = vel_z
			pub.publish(vel)
			if((error_theta<0.009 and error_theta>=0.008) or (error_theta<-0.008 and error_theta>=-0.009)):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
				rospy.sleep(1.25)
				j=j+1
		elif theta_d[i]<0 and yaw>=0:
			theta_d[i] =6.283+theta_d[i]
			error_theta = theta_d[i] - yaw
			
			vel_z = (error_theta)*Ka
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z = vel_z
			pub.publish(vel)
			if((error_theta<0.009 and error_theta>=0.008) or (error_theta<-0.008 and error_theta>=-0.009)):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
				rospy.sleep(1.25)
				j=j+1
		elif theta_d[i]>=0 and yaw<0:
			yaw = 6.283+yaw
			error_theta = theta_d[i] - yaw
		
			vel_z = (error_theta)*Ka
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z = vel_z
			pub.publish(vel)
			if((error_theta<0.009 and error_theta>=0.008) or (error_theta<-0.008 and error_theta>=-0.009)):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
				rospy.sleep(1.25)
				j=j+1
	else:
		theta=0.0
		if theta>=0 and yaw>=0.00:
			error_theta = theta - yaw
			
			vel_z = (error_theta)*Ka
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z = vel_z
			pub.publish(vel)
			if((error_theta<0.009 and error_theta>=0.008) or (error_theta<-0.008 and error_theta>=-0.009)):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
				rospy.sleep(1.25)
				j=j+1
		elif theta>=0 and yaw<0:
			yaw = 6.283+yaw
			error_theta = theta - yaw
		
			vel_z = (error_theta)*Ka
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z = vel_z
			pub.publish(vel)
			if((error_theta<0.009 and error_theta>=0.008) or (error_theta<-0.008 and error_theta>=-0.009)):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
				rospy.sleep(1.25)
				j=j+1
	return j	
	
def coord_calc(hola_x, hola_y,i):
	x_d=x_goals.copy()
	y_d=y_goals.copy()
	theta_d=theta_goals.copy()
	vel = Twist()
	error_x = x_d[i]-hola_x
	error_y = y_d[i]-hola_y
	
	distance = abs(math.sqrt(((error_x)**2) + ((error_y)**2)))
	#print(distance)
	
	vel_x=error_x*Kp
	vel_y = error_y*Kp

		
				
	vel.linear.x = vel_x
	vel.linear.y= vel_y
	vel.angular.z = 0.0
	pub.publish(vel)
	return distance

		
		
		
	
		
def main():
    	global pub
    	rospy.init_node('controller', anonymous=True)
    
    	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	
    	sub = rospy.Subscriber('/odom', Odometry, getRotation)
    	sub2 = rospy.Subscriber('task1_goals', PoseArray, task1_goals_Cb)
    	rospy.spin()

if __name__ == '__main__':
    main()
