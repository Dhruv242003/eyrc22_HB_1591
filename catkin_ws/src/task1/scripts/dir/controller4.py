#!/usr/bin/env python3

import rospy
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
from geometry_msgs.msg import PoseArray
global x_goals, y_goals, theta_goals , hola_distance
x_goals = [0,1,-1,0,0]
y_goals = [1,-1,-1,1,-1]
distArr=[0.0,0.0,0.0,0.0,0.0]
Kp = 5.5
Ka = 5.5
theta_goals=[0,0,0,0,0]
global error_x, error_y,vel_x,vel_y, vel_z, distance

global globalGoalDistance0, globalGoalDistance1, globalGoalDistance2, globalGoalDistance3, globalGoalDistance4

globalGoalDistance0=0.0
globalGoalDistance1=0.0
globalGoalDistance2=0.0
globalGoalDistance3=0.0
globalGoalDistance4=0.0

def getRotation (msg):
	globalGoalDistance0= abs(math.sqrt(((x_goals[0])**2) + ((y_goals[0])**2)))
	globalGoalDistance1= abs(math.sqrt(((x_goals[1])**2) + ((y_goals[1])**2)))
	globalGoalDistance2= abs(math.sqrt(((x_goals[2])**2) + ((y_goals[2])**2)))
	globalGoalDistance3= abs(math.sqrt(((x_goals[3])**2) + ((y_goals[3])**2)))
	globalGoalDistance4= abs(math.sqrt(((x_goals[4])**2) + ((y_goals[4])**2)))
	
	distArr=[globalGoalDistance0,globalGoalDistance1,globalGoalDistance2,globalGoalDistance3,globalGoalDistance4]
	#print(globalGoalDistance0
	#print(globalGoalDistance1)
	
	vel = Twist()
	global hola_x, hola_y, coords,yaw, dist
	hola_x = msg.pose.pose.position.x
	hola_y = msg.pose.pose.position.y
	coords = msg.pose.pose.orientation
	orentation_list=[coords.x, coords.y, coords.z, coords.w]
	yaw = euler_from_quaternion(orentation_list)[2]
	
	hola_distance = getGlobalDistance()
	#print(hola_distance<distArr[0]-0.01)
	#print(hola_x < x_goals[0]-0.01)
	#print(hola_x)
	#print(x_goals[0])
	#print((hola_x > x_goals[0]-0.01 or hola_x < x_goals[0]+0.01) and  (hola_y > y_goals[0]-0.01 or hola_y < y_goals[0]+0.01))
	
	# 0
	
	if ((hola_x < x_goals[0]-0.01 or hola_x > x_goals[0]+0.01) and  (hola_y < y_goals[0]-0.01 or hola_y > y_goals[0]+0.01) ):
		dist = coord_calc(hola_x, hola_y,0)
		#print(dist)
		if dist<0.05:
			yaw_calc(yaw,0)
	elif ((hola_x > x_goals[0]-0.01 or hola_x < x_goals[0]+0.01) and  (hola_y > y_goals[0]-0.01 or hola_y < y_goals[0]+0.01)):
		yaw_calc(yaw,6)
		
		
	#1
		
		
	elif ((hola_x < x_goals[1]-0.01 or hola_x > x_goals[1]+0.01) and  (hola_y < y_goals[1]-0.01 or hola_y > y_goals[1]+0.01) ):
		dist = coord_calc(hola_x, hola_y,1)
		#print(dist)
		if dist<0.05:
			yaw_calc(yaw,1)
	elif ((hola_x > x_goals[1]-0.01 or hola_x < x_goals[1]+0.01) and  (hola_y > y_goals[1]-0.01 or hola_y < y_goals[1]+0.01)):
		yaw_calc(yaw,6)
		
		
	#2
		
	elif ((hola_x < x_goals[2]-0.01 or hola_x > x_goals[2]+0.01) and  (hola_y < y_goals[2]-0.01 or hola_y > y_goals[2]+0.01) ):
		dist = coord_calc(hola_x, hola_y,2)
		#print(dist)
		if dist<0.05:
			yaw_calc(yaw,3)
	elif ((hola_x > x_goals[2]-0.01 or hola_x < x_goals[2]+0.01) and  (hola_y > y_goals[2]-0.01 or hola_y < y_goals[2]+0.01)):
		yaw_calc(yaw,6)
		
		
		
	#3
		
		
	
	elif ((hola_x < x_goals[3]-0.01 or hola_x > x_goals[3]+0.01) and  (hola_y < y_goals[3]-0.01 or hola_y > y_goals[3]+0.01) ):
		dist = coord_calc(hola_x, hola_y,3)
		#print(dist)
		if dist<0.05:
			yaw_calc(yaw,3)
	elif ((hola_x > x_goals[3]-0.01 or hola_x < x_goals[3]+0.01) and  (hola_y > y_goals[3]-0.01 or hola_y < y_goals[3]+0.01)):
		yaw_calc(yaw,6)
		
		
		
		
	#4
	
	elif ((hola_x < x_goals[4]-0.01 or hola_x > x_goals[4]+0.01) and  (hola_y < y_goals[4]-0.01 or hola_y > y_goals[4]+0.01) ):
		dist = coord_calc(hola_x, hola_y,4)
		#print(dist)
		if dist<0.05:
			yaw_calc(yaw,4)
	elif ((hola_x > x_goals[4]-0.01 or hola_x < x_goals[4]+0.01) and  (hola_y > y_goals[4]-0.01 or hola_y < y_goals[4]+0.01)):
		yaw_calc(yaw,6)
	else: 
		vel.linear.x=0.0
		vel.linear.y=0.0
		vel.angular.z=0.0
		pub.publish(vel)
			
def yaw_calc(yaw,i):
	vel = Twist()
	theta_d=theta_goals.copy()
	if (i>=0 and i<5):
		#print(str(theta_d[i])+" "+str(yaw))
		if theta_d[i]>=0 and yaw>=0.00:
			error_theta = theta_d[i] - yaw
			
			vel_z = (error_theta)*Ka
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z = vel_z
			pub.publish(vel)
			if((error_theta<0.01 and error_theta>=0.009) or (error_theta<-0.009 and error_theta>=-0.01)):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
		elif theta_d[i]<0 and yaw<0 :
			theta_d[i]=6.283+theta_d[i]
			yaw=6.283+yaw
			error_theta = theta_d[i] - yaw
				
			vel_z = (error_theta)*Ka
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z = vel_z
			pub.publish(vel)
			if((error_theta<0.01 and error_theta>=0.009) or (error_theta<-0.009 and error_theta>=-0.01)):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
		elif theta_d[i]<0 and yaw>=0:
			theta_d[i] =6.283+theta_d[i]
			error_theta = theta_d[i] - yaw
			
			vel_z = (error_theta)*Ka
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z = vel_z
			pub.publish(vel)
			if((error_theta<0.01 and error_theta>=0.009) or (error_theta<-0.009 and error_theta>=-0.01)):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
		elif theta_d[i]>=0 and yaw<0:
			yaw = 6.283+yaw
			error_theta = theta_d[i] - yaw
		
			vel_z = (error_theta)*Ka
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z = vel_z
			pub.publish(vel)
			if((error_theta<0.01 and error_theta>=0.009) or (error_theta<-0.009 and error_theta>=-0.01)):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
	else:
		theta=0.0
		if theta>=0 and yaw>=0.00:
			error_theta = theta - yaw
			
			vel_z = (error_theta)*Ka
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z = vel_z
			pub.publish(vel)
			if((error_theta<0.01 and error_theta>=0.009) or (error_theta<-0.009 and error_theta>=-0.01)):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
		elif theta>=0 and yaw<0:
			yaw = 6.283+yaw
			error_theta = theta - yaw
		
			vel_z = (error_theta)*Ka
			vel.linear.x=0.0
			vel.linear.y=0.0
			vel.angular.z = vel_z
			pub.publish(vel)
			if((error_theta<0.01 and error_theta>=0.009) or (error_theta<-0.009 and error_theta>=-0.01)):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
	
def getGlobalDistance():
	global_distance = 0.0
	hola_x_1= 0.0
	hola_y_1= 0.0
	hola_x_1 = hola_x
	hola_y_1 = hola_y
	
	global_distance = abs(math.sqrt(((hola_x)**2) + ((hola_y)**2)))
	
	return global_distance
	

	
	
def coord_calc(hola_x, hola_y,i):
	x_d=x_goals.copy()
	y_d=y_goals.copy()
	theta_d=theta_goals.copy()
	vel = Twist()
	error_x = x_d[i]-hola_x
	error_y = y_d[i]-hola_y
	
	distance = abs(math.sqrt(((error_x)**2) + ((error_y)**2)))
	#print(distance)

	vel_x = error_x*Kp
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
    	#sub2 = rospy.Subscriber('task1_goals', PoseArray, task1_goals_Cb)
    	rospy.spin()

if __name__ == '__main__':
    main()
