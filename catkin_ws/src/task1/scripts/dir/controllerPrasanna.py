#!/usr/bin/env python3

import rospy
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import math
from geometry_msgs.msg import PoseArray
from threading import Thread
global error_x, error_y,vel_x,vel_y, vel_z, error_xb, error_yb, vel_x2, vel_y2
global x_goals, y_goals, theta_goals, x_goalsb, y_goalsb
x_goals = [1,-1,-1,1,0]
y_goals = [1,1,-1,-1,0]

Kp = 1.5
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
theta_goals = [0.785,1.57,-0.785,1.57,0]
coords=[0.0,0.0,0.0,0.0]
def getRotation (msg):
	global hola_x, hola_y, coords
	hola_x = msg.pose.pose.position.x
	hola_y = msg.pose.pose.position.y
	coords = msg.pose.pose.orientation
	orentation_list=[coords.x, coords.y, coords.z, coords.w]
	(roll,pitch,yaw) = euler_from_quaternion(orentation_list)
rospy.init_node('controller', anonymous=True)





sub = rospy.Subscriber('/odom', Odometry, getRotation)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rospy.sleep(1)
vel = Twist()
vel.linear.x = 0.0
vel.linear.y = 0.0
vel.angular.z = 0.0


rospy.Rate(10)


def main():
	global i
	i=0
	while(i<5):
		
		hola_x1=hola_x
		hola_y1=hola_y
		error_x = x_goals[i]-hola_x1
		error_y = y_goals[i]-hola_y1
			
				
		initial_position = coords
		orentation_list=[coords.x, coords.y, coords.z, coords.w]
		(roll,pitch,yaw) = euler_from_quaternion(orentation_list)
		yaw1=yaw
		x_goalsb = ((x_goals[i])*(math.cos(yaw)))+((y_goals[i])*(math.cos(yaw)))
		y_goalsb = ((y_goals[i])*(math.cos(yaw)))-((x_goals[i])*(math.sin(yaw)))
		hola_x2 = ((hola_x)*(math.cos(yaw)))+((hola_y)*(math.cos(yaw)))
		hola_y2 = ((hola_y)*(math.cos(yaw)))-((hola_x)*(math.sin(yaw)))
		error_xb= x_goalsb-hola_x2
		error_yb= y_goalsb-hola_y2
		
		error_theta = abs(theta_goals[i] - yaw1)
		error_theta1 = (theta_goals[i]-yaw1)
		
		desired_error=error_theta
		distance = abs(math.sqrt(((error_x)**2) + ((error_y)**2)))
		distanceb= abs(math.sqrt(((error_xb)**2) + ((error_yb)**2)))
		print(distanceb)
		#print(distanceb)
		vel_z = (error_theta1)*Ka
		vel_x = (error_x*Kp)
		vel_y = (error_y*Kp)
		vel_x2 = (error_xb*Kp)
		vel_y2 = (error_yb*Kp)
		
			
		if (yaw > -0.001 and yaw < 0.001):
			if(distance>0.0098 and error_theta>0.01):
				vel.linear.x = vel_x
				vel.linear.y= vel_y
				vel.angular.z= vel_z
				pub.publish(vel)
			elif(distance<0.0098 and error_theta>0.01):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=vel_z
				pub.publish(vel)
			elif(distance >0.0098 and error_theta<0.01):
				vel.linear.x=vel_x
				vel.linear.y=vel_y
				vel.angular.z=0.0
				pub.publish(vel)
			elif(distance<0.0098 and error_theta<0.01):
				vel.linear.x=0.0
				vel.linear.y=0.0
				vel.angular.z=0.0
				pub.publish(vel)
				rospy.sleep(2)
				i=i+1
				
						
		else:
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
				rospy.sleep(2)
				i=i+1
			
		
	
if __name__ == "__main__":
	while not rospy.is_shutdown():

		try:
			main()
		except rospy.ROSInterruptException:
			pass		
