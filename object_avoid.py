#!/usr/bin/env python
import rospy
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist
import time
import sys
import os

rospy.init_node('zumo_object_avoid', anonymous=True)
pub = rospy.Publisher('/zumo/3/cmd_vel', Twist, queue_size=10)
#these are the topics that we will use for the if statements
current_topic = 0
new_topic = 1

#this function is responsible for making the zumo robot move right
def right():
 vel_msg = Twist()
 vel_msg.linear.x = 0
 vel_msg.linear.y = 1
 vel_msg.linear.z = 0
 vel_msg.angular.x = 0
 vel_msg.angular.y = 0
 vel_msg.angular.z = 0
 vel_msg.linear.x = 0
 pub.publish(vel_msg)
#this function is responsible for making the zumo robot move left
def left():
 vel_msg = Twist()
 vel_msg.linear.x = 0
 vel_msg.linear.y = -1
 vel_msg.linear.z = 0
 vel_msg.angular.x = 0
 vel_msg.angular.y = 0
 vel_msg.angular.z = 0
 vel_msg.linear.x = 0
 pub.publish(vel_msg)


def handle_zumo_sensor(wall_msg):
 global current_topic
 if(wall_msg.data < 20):
     new_topic = 2
     
     right()
 else:
     new_topic = 1

def handle_zumo_leftsensor(wall_msg):
 global current_topic
 if(wall_msg.data < 20):
     new_topic = 2
     right()
 else:
     new_topic = 1

def handle_zumo_rightsensor(wall_msg):
 global current_topic
 if(wall_msg.data < 20):
     new_topic = 2
     left()
 else:
     new_topic = 1

#so over here are the conditions of mux tool that will determine which file need to run based of the condition
 if(current_topic ==1 and new_topic == 2):
  os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/3/cmd_vel")
  current_topic = 2

 if(current_topic ==2 and new_topic == 1):
  os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel")
  current_topic = 1
 


rospy.Subscriber('/zumo/front', UInt16, handle_zumo_sensor)
rospy.Subscriber('/zumo/left', UInt16, handle_zumo_leftsensor)
rospy.Subscriber('/zumo/right', UInt16, handle_zumo_rightsensor)
#take over
os.system("rosrun topic_tools mux_select mux_cmdvel /zumo/1/cmd_vel")
current_topic = 1
rospy.spin()
