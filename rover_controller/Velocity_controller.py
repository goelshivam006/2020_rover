#!/usr/bin/env python
import rospy
from std_msgs.msg import String 
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

global vx
global vz

def callback():
    rospy.Subscriber('/rover/cmd_vel',Twist,Velocity_controller)
    rospy.spin()
    
def Velocity_controller(data):
    
    vx=data.linear.x
    vz=data.angular.z
    ang=0.3*vz/2
    
    publm=rospy.Publisher('/rover/bogie_left_wheel_lm_controller/command',Float64,queue_size=50)
    publf=rospy.Publisher('/rover/corner_lf_wheel_lf_controller/command',Float64,queue_size=50)
    pubrm=rospy.Publisher('/rover/bogie_right_wheel_rm_controller/command',Float64,queue_size=50)
    pubrf=rospy.Publisher('/rover/corner_rf_wheel_rf_controller/command',Float64,queue_size=50)
    publb=rospy.Publisher('/rover/corner_lb_wheel_lb_controller/command',Float64,queue_size=50)
    pubrb=rospy.Publisher('/rover/corner_rb_wheel_rb_controller/command',Float64,queue_size=50)
    publm.publish(vx+ang)
    pubrf.publish(-1*vx+ang)
    publf.publish(vx+ang)
    pubrm.publish(-1*vx+ang)
    pubrb.publish(-1*vx+ang)
    publb.publish(vx+ang)
    rospy.loginfo(vx+ang)

if __name__=='__main__':
    try:
        rospy.init_node('Velocity_controller',anonymous=True)
        callback()
    except rospy.ROSInterruptException:
        pass
