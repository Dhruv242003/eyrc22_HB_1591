
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





