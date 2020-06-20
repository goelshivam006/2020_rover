#!/usr/bin/env python
import rospy

from geometry_msgs.msg import Pose,Point,Twist
from tf.transformations import euler_from_quaternion
from nav_msgs.msg import Odometry
from math import atan2,pi

goal_x=0.0
goal_y=0.0
x=0.0
y=0.0
theta=0.0

def command(msg):

    global x,y,theta
    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    
    rot_q=msg.pose.pose.orientation
    (roll,pitch,theta)=euler_from_quaternion([rot_q.x,rot_q.y,rot_q.z,rot_q.w])
#    rospy.loginfo("x :%f    y:%f",x,y)

def assign(msg):
    global goal_x,goal_y
    goal_x=msg.position.x 
    goal_y=msg.position.y 

    speed=Twist()
    pub=rospy.Publisher('/rover/cmd_vel',Twist,queue_size=50)
    rate=rospy.Rate(10)
    inc_x=goal_x-x
    inc_y=goal_y-y
    turn=atan2(inc_y,inc_x)
    if(turn<0):
        turn+=pi
    elif(turn>0):
	turn-=pi
    if(pi-abs(turn)<0.1):
	   if(theta<0):
		  turn=-pi
	   else:
		  turn =pi
    rospy.loginfo("x :%f   y :%f  theta :%f  turn: %f",x,y,theta,turn)
    if (((inc_x*inc_x)+(inc_y*inc_y))<=0.01):
        speed.angular.z=0.0
        speed.linear.x=0.0
    elif(abs(turn-theta)>0.1):
        speed.angular.z=100.0*(-turn+theta)
        speed.linear.x=10.0
    else:
        speed.angular.z=0.0
        speed.linear.x=100.0

    pub.publish(speed)
    rate.sleep()
    
    

if __name__=='__main__':
    rospy.init_node('controller',anonymous=True)
    rospy.Subscriber('/rover/odom',Odometry,command)
    rospy.Subscriber('/rover/cmd_pose',Pose,assign)
    rospy.spin()
