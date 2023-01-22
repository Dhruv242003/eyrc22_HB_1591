#!/usr/bin/env python3

import rospy
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
from geometry_msgs.msg import PoseArray
global x_goals, y_goals, theta_goals
x_goals = [1,2,1,-1,-2]
y_goals = [1,-1,2,1,2]
x_goals_2=[0,0,0,0,0]
y_goals_2=[0,0,0,0,0]
Kp = 1.5
Ka = 1.5
theta_goals=0.785

global error_x, error_y,vel_x,vel_y, vel_z,distance,distance2

global theta_goals_2,i
i=0

for j in range(0,5):
	x_goals_2[j]=x_goals[j]*(math.cos(theta_goals))
	y_goals_2[j]=y_goals[j]*(math.sin(theta_goals))
def getRotation (msg):
	vel = Twist()
	global hola_x, hola_y, coords,yaw, dist
	hola_x = msg.pose.pose.position.x
	hola_y = msg.pose.pose.position.y
	coords = msg.pose.pose.orientation
	orentation_list=[coords.x, coords.y, coords.z, coords.w]
	yaw = euler_from_quaternion(orentation_list)[2]
	


	

	'''x_d=x_goals
	y_d=y_goals
	theta_d=theta_goals
	vel = Twist()
	error_body_x=x_d-hola_x
	error_body_y=y_d-hola_y
	x_2=((hola_x)*(math.cos(yaw))) +((hola_y)*(math.sin(yaw)))
	y_2=((hola_y)*(math.cos(yaw)))- ((hola_x)*(math.sin(yaw)))
	print(hola_x)
	print(hola_y)
	print(x_2)
	print(y_2)
	error_global_x = (x_d-x_2)
	error_global_y = (y_d-y_2)
	error_theta = theta_d - yaw
	distance = abs(math.sqrt(((error_global_x)**2) + ((error_global_y)**2)))	
		
	vel_x = (error_global_x*Kp)
	vel_y = (error_global_y*Kp)
	vel_z = error_theta*Ka
	
	vel.linear.x= vel_x
	vel.linear.y= vel_y
	vel.angular.z = vel_z
	pub.publish(vel)
	
	
		
	if(((error_theta<0.009 and error_theta>=0.008) or (error_theta<-0.008 and error_theta>=-0.009))and distance<0.01):
			
		vel.linear.x=0.0
		vel.linear.y=0.0
		vel.angular.z=0.0
		pub.publish(vel)
		rospy.sleep(25)'''
		
		
def main(i):
	
	global pub
    	
	rospy.init_node('controller', anonymous=True)
    
	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	rospy.Rate(1000)
	sub = rospy.Subscriber('/odom', Odometry, getRotation) 
	rospy.spin()
	while(i<5):
			error_x=x_goals[i]-hola_x
			error_y=y_goals[i]-hola_y
			hola_x_2=hola_x*(math.cos(yaw))
			hola_y_2=hola_y*(math.sin(yaw))
			
			error_x_2=x_goals_2[i]-hola_x_2
			error_y_2=y_goals_2[i]-hola_y_2
			
			error_theta=theta_goals-yaw
			vel_x=error_x_2*Kp
			vel_y=error_y_2*Kp
			vel_z=error_theta*Ka
			
			distance = abs(math.sqrt(((error_x)**2) + ((error_y)**2)))
			distance2 = abs(math.sqrt(((error_x_2)**2) + ((error_y_2)**2)))
			
			vel.linear.x= vel_x
			vel.linear.y= vel_y
			vel.angular.z = vel_z
			pub.publish(vel)
			print(str(distance2)+ " " + str(error_theta))
			if(distance2<0.0045  ):
				vel.linear.x= 0.0
				vel.linear.y= 0.0
				pub.publish(vel)
				if(error_theta<0.001):
					vel.angular.z = 0.0
					pub.publish(vel)
					i=i+1
		

if __name__ == "__main__":
	try:
		main(i)
	except rospy.ROSInterruptException:
		pass



		
