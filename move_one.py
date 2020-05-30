#!/usr/bin/env python
import rospy
from std_msgs.msg import String 
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

global vx
global vz

def callback():
    rospy.Subscriber('/rover/cmd_vel',Twist,divert)
    rospy.spin()
    
def divert(data):
    
    vx=data.linear.x
    vz=data.angular.z
    turn(vz)
    move_forward(vx)
    
def move_forward(vx):

    publm=rospy.Publisher('/rover/bogie_left_wheel_lm_controller/command',Float64,queue_size=50)
    publf=rospy.Publisher('/rover/corner_lf_wheel_lf_controller/command',Float64,queue_size=50)
    pubrm=rospy.Publisher('/rover/bogie_right_wheel_rm_controller/command',Float64,queue_size=50)
    pubrf=rospy.Publisher('/rover/corner_rf_wheel_rf_controller/command',Float64,queue_size=50)
    publb=rospy.Publisher('/rover/corner_lb_wheel_lb_controller/command',Float64,queue_size=50)
    pubrb=rospy.Publisher('/rover/corner_rb_wheel_rb_controller/command',Float64,queue_size=50)
    publm.publish(vx)
    pubrf.publish(-1*vx)
    publf.publish(vx)
    pubrm.publish(-1*vx)
    pubrb.publish(-1*vx)
    publb.publish(vx)

def turn(vz):
    ang=vz*0.1
    pubrb=rospy.Publisher('/rover/rocker_right_corner_rb_controller/command',Float64,queue_size=50)
    publb=rospy.Publisher('/rover/rocker_left_corner_lb_controller/command',Float64,queue_size=50)
    publf=rospy.Publisher('/rover/bogie_left_corner_lf_controller/command',Float64,queue_size=50)
    pubrf=rospy.Publisher('/rover/bogie_right_corner_rf_controller/command',Float64,queue_size=50)
    publf.publish(ang)
    pubrb.publish(ang)
    publb.publish(ang)
    pubrf.publish(ang)

if __name__=='__main__':
    try:
        rospy.init_node('move_one',anonymous=True)
        callback()
    except rospy.ROSInterruptException:
        pass
