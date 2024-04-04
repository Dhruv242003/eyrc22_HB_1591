
# Holonomic Art Bot (HolA bot)
 
- A Project made for e-Yantra robotics competition IIT-Bombay 
2022-23

- This Project got **All India Rank 3** among the 372 teams in the HolA Bot theme of this competition.





## Authors
- [@Dhruv242003](https://www.github.com/Dhruv242003)
- [@Prasann-a27](https://www.github.com/Prasann-a27)


## Problem Statement

To make a holonomic drive bot which is able to draw images and complex patterns on the ground without using any sensors on the bot and feedback is with help of a overhead camera and aruco markers.
## Technologies and Tools used
   - Robot Operating System (ROS)
   - Gazebo
   - Embedded Porgramming (Arduino)
   - Python
   - OpenCv
   - WiFi Socket
   - Fusion 360


## Project Timeline

 **Task 0**

Inintially for getting started with the ROS publishers and subscribers we worked on turtle-sim which is a simple simulator in the Robot Operating System (ROS) that allows users to create and interact with a turtle robot in a 2D space. 

The objective was to move the turlte inside the turtlesim window in a vertical D shape of radius 1 unit.

![Task 0 Output](https://i.pinimg.com/originals/46/0e/87/460e8702d22cc369088ab4091a77c4a0.jpg)

**Task 1**

Task 1 started the main theme, we were given a URDF file that had base plate with two omni wheels attached, and we have to attach one more omni wheel at the correct location with appropriate angle, hight and location.

Then we had to deploy that bot in the gazebo enviornment and use teleop operations to control the bot.


![URDF Correction ](https://i.pinimg.com/originals/3c/83/ca/3c83ca07587919bf0b1e774a2fda057e.jpg)


Another subtask, indeed the main task was to design a *closed loop* controller for the bot to go to a defined goal pose.

Here came the main task and also a lot of confusion. Our Challange was to understand the concept of global frame and body frame. Firstly, for the closed loop control we need the feedback of the system. The motors that were used in the bot were not having any kind of encoders, so we could not get the information of the bot's location. So since it was task 1, to keep the difficulty level low, they gave us the liberty to use the [Odom](https://wiki.ros.org/navigation/Tutorials/RobotSetup/Odom) topic. 

Odom topic when subscribed gives us the x,y,theta of bot w.r.t global frame as shown in the figure give below. 

![Odom ](https://blog.hadabot.com/images/hadabot_unicycle_diagram_01.jpg)


And to control the bot we were directly giving the Vx, Vy and Vz to the bot using a custom publisher.

**P-Controller**

To make the bot move towards the goals we cannot tell bot the desired goal position. 

A Proportional-Integral-Derivative (PID) controller is a commonly used feedback control mechanism in robotics to regulate the movement of bots to reach a desired position or setpoint. In the context of your question, We focused on the Proportional (P) controller, which is the simplest form of a PID controller.

In a P controller, the control output is directly proportional to the error between the current position and the desired position

*u(t)=Kp⋅e(t)*

u(t): Actuation  
Kp: Proportional constant  
e(t): Error

Now, for make the bot move in the desierd and shortest path, we have to give the error w.r.t to the body frame.

![Frame Correction](https://i.pinimg.com/originals/c3/19/de/c319de153b1f60926e526496428c7c5d.png)

So to get the error of the bot w.r.t to the body frame, we used the following formula.


![Body Frame Formula ](https://i.pinimg.com/originals/6e/2e/c9/6e2ec94a84e5c91b8f2a05e4551d5304.png )


Hence we succesfully Completed the Task1 by making a P-Controller with all the transfomations required and Tuned the Kp value to get the best results.



**Task2**

In task 2, we have again do the same thing i.e. go-to-goal, but thhis time we were not allowed to use the Odom topic and also we were not having any liberty to directly give the Vx, Vy and Vz to the bot.

For feedback, we have to use a overhead camera that will detect the [Aruco](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html) marker attached on top of the bot. 
It gives us the current pose of the 4 corners of marker and then we calculated the centroid of marker to get the coordinates of the bot w.r.t to the top right corner of the camera frame. Then we shifted the origin to 250,250 to get the origin at center of frame keeping in mind the inverted nature of y axis of camera frame.

![Body Frame Formula ](https://docs.opencv.org/4.x/singlemarkersdetection.jpg)

For controlling the bot, we have to convert the Vx,Vy,Vz to V1,V2,V3 i.e. individual wheel velocity of the bot. We used the following formula to do so.


![Velocity Matrix](https://i.ytimg.com/vi/NcOT9hOsceE/maxresdefault.jpg)


There are two files, feedback.py and controller.py.
feedback.py gets the image from the camera in the gazebo enviornment through a Bridge and the using perspective transfomations and using aruco library we got the coordinates of the bot, and then were published to the /detected_aruco topic

controller.py subscribed the /detected_aruco topic to get the feedback and used the same logic as that of Task1 to go-to-goal, but this time the speeds were converted to the individual wheel velocities and published as a /force topic and were responsible to move the bot.

There were auto-evaluators that judeged the accuracy and speed of the bot to score the teams, and we were qualified for Stage 2 i.e. Hardware stage !!!




