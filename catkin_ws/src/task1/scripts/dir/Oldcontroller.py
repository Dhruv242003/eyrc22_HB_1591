#!/usr/bin/env python3

import rospy
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
from geometry_msgs.msg import PoseArray
global x_goals, y_goals, theta_goals
x_goals = [0,1,-1,0,0]
y_goals = [1,-1,-1,1,-1]
Kp = 5.5
Ka = 5.5
theta_goals=[0,0,0,0,0]
global error_x, error_y,vel_x,vel_y, vel_z,distance,a

a=0
def getRotation (msg):
	vel = Twist()
	global hola_x, hola_y, coords,yaw, dist
	hola_x = msg.pose.pose.position.x
	hola_y = msg.pose.pose.position.y
	coords = msg.pose.pose.orientation
	orentation_list=[coords.x, coords.y, coords.z, coords.w]
	yaw = euler_from_quaternion(orentation_list)[2]	
	#print((hola_x < x_goals[0]-0.01 or hola_x > x_goals[0]+0.01) and  (hola_y < y_goals[0]-0.01 or hola_y > y_goals[0]+0.01) )
	#print((hola_x > x_goals[0]-0.01 or hola_x < x_goals[0]+0.01) and  (hola_y > y_goals[0]-0.01 or hola_y < y_goals[0]+0.01))
	#print((hola_x < x_goals[1]-0.01 or hola_x > x_goals[1]+0.01) and  (hola_y < y_goals[1]-0.01 or hola_y > y_goals[1]+0.01) )
	print(hola_x > x_goals[0]+0.01)
	
	if ((hola_x < x_goals[0]-0.01 or hola_x > x_goals[0]+0.01) and  (hola_y < y_goals[0]-0.01 or hola_y > y_goals[0]+0.01) ):
		
		a=1
		print(a)
		switch(a)
		
	elif ((hola_x > x_goals[0]-0.01 or hola_x < x_goals[0]+0.01) and  (hola_y > y_goals[0]-0.01 or hola_y < y_goals[0]+0.01)):
		a=0
		switch(a)
		
		
	elif ((hola_x < x_goals[1]-0.01 or hola_x > x_goals[1]+0.01) and  (hola_y < y_goals[1]-0.01 or hola_y > y_goals[1]+0.01) ):
		a=2
		switch(a)
	elif ((hola_x > x_goals[1]-0.01 or hola_x < x_goals[1]+0.01) and  (hola_y > y_goals[1]-0.01 or hola_y < y_goals[1]+0.01)):
		a=0
		switch(a)
		
		
		
	elif ((hola_x < x_goals[2]-0.01 or hola_x > x_goals[2]+0.01) and  (hola_y < y_goals[2]-0.01 or hola_y > y_goals[2]+0.01) ):
		a=3
		switch(a)
	elif ((hola_x > x_goals[2]-0.01 or hola_x < x_goals[2]+0.01) and  (hola_y > y_goals[2]-0.01 or hola_y < y_goals[2]+0.01)):
		a=0
		switch(a)
		
		
		
	elif ((hola_x < x_goals[3]-0.01 or hola_x > x_goals[3]+0.01) and  (hola_y < y_goals[3]-0.01 or hola_y > y_goals[3]+0.01) ):
		a=4
		switch(a)
	elif ((hola_x > x_goals[3]-0.01 or hola_x < x_goals[3]+0.01) and  (hola_y > y_goals[3]-0.01 or hola_y < y_goals[3]+0.01)):
		a=0
		switch(a)
		
	elif ((hola_x < x_goals[4]-0.01 or hola_x > x_goals[4]+0.01) and  (hola_y < y_goals[4]-0.01 or hola_y > y_goals[4]+0.01) ):
		a=5
		switch(a)
	elif ((hola_x > x_goals[4]-0.01 or hola_x < x_goals[4]+0.01) and  (hola_y > y_goals[4]-0.01 or hola_y < y_goals[4]+0.01)):
		a=0
		switch(a)
		
	else: 
		vel.linear.x=0.0
		vel.linear.y=0.0
		vel.angular.z=0.0
		pub.publish(vel)
		
		
		
def switch(a):
	
	if a == 0:
		yaw_calc(yaw,6)
		rospy.sleep(1)
		return
	elif a == 1:
		dist = coord_calc(hola_x, hola_y,0)
		
		if dist<0.05:
			yaw_calc(yaw,0)
			return
			
	elif a==2:
		dist = coord_calc(hola_x, hola_y,1)
		
		if dist<0.05:
			yaw_calc(yaw,1)
			return
			
	elif a == 3:
		dist = coord_calc(hola_x, hola_y,2)
		
		if dist<0.05:
			yaw_calc(yaw,2)
			return
	elif a == 4:
		dist = coord_calc(hola_x, hola_y,3)
		
		if dist<0.05:
			yaw_calc(yaw,3)
			return
	elif a == 5:
		dist = coord_calc(hola_x, hola_y,4)
		
		if dist<0.05:
			yaw_calc(yaw,4)
			return	
			
def yaw_calc(yaw,i):
	vel = Twist()
	theta_d=theta_goals.copy()
	if i>=0 and i<5:
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
				return
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
				return
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
				return
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
				return
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
				return
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
				return
	
	
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
