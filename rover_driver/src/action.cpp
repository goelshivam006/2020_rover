#include <ros/ros.h>
#include <tf/tf.h>
#include <geometry_msgs/Twist.h>
#include <geometry_msgs/Point.h>
#include <geometry_msgs/Pose.h>
#include <nav_msgs/Odometry.h>
#include <stdlib.h> 
#include <math.h>
#include <iostream>
#include <geometry_msgs/Pose2D.h>
#include "sensor_msgs/LaserScan.h"
#include "geometry_msgs/Twist.h"

float min_range,min_range_angle;
float range[360];
void callBackAvoid(const sensor_msgs::LaserScan::ConstPtr& msga){
    min_range = msga->ranges[0];
	min_range_angle = 0;
    
    for(int j=0;j<360;j++){
        range[j] = msga->ranges[j];
    }
}


geometry_msgs::Pose2D pose2d;
void callBack(const nav_msgs::Odometry::ConstPtr msg){
    pose2d.x = msg->pose.pose.position.x;
    pose2d.y = msg->pose.pose.position.y;
    
    tf::Quaternion q(
        msg->pose.pose.orientation.x,
        msg->pose.pose.orientation.y,
        msg->pose.pose.orientation.z,
        msg->pose.pose.orientation.w);
    tf::Matrix3x3 m(q);
    double roll, pitch, yaw;
    m.getRPY(roll, pitch, yaw);
    
    pose2d.theta = yaw;
}
geometry_msgs::Point goal;
void callBackTarget(const geometry_msgs::Point::ConstPtr msg){
    goal.x = msg->x;
    goal.y = msg->y;
}

int main(int argc, char **argv) {
      ros::init(argc, argv, "speed_controller");
      ros::NodeHandle nh;

      ros::Subscriber sub2 = nh.subscribe("/rover/scan", 100, callBackAvoid);
      ros::Subscriber sub = nh.subscribe("/rover/odom", 100, callBack);
      ros::Subscriber sub1 = nh.subscribe("/rover/target", 100, callBackTarget);
      ros::Publisher pub =nh.advertise<geometry_msgs::Twist>("cmd_vel", 100);
      
      srand(time(0));
      ros::Rate rate(100);

        while(ros::ok()) {
            ros::spinOnce();
            geometry_msgs::Twist speed;
            
            double inc_x = goal.x -pose2d.x;
            double inc_y = goal.y -pose2d.y;

            double distance = sqrt(inc_x*inc_x + inc_y*inc_y);
            double theta_one = std::atan(inc_y/inc_x);
            double final_theta =  pose2d.theta - theta_one ;

//obstacle_avoidance
            for(int j=0;j<360;j++) //increment by one degree
	        {
	  	        if(range[j]<min_range)
		        {
			        min_range=range[j];
			        min_range_angle=j/2;
		        }
	        }
            if(min_range<=1.5)
	        {
			    speed.angular.z=100.0;
			    speed.linear.x=0;
	        }
	        else
	        {
		        if (final_theta > 0.1){
                    speed.linear.x = 0.0;
                    speed.angular.z = 100;
                }
                else{
                    speed.linear.x = 20;
                    speed.angular.z = 0.0;
                }

                if(distance <0.01){
                    speed.linear.x = 0;
                }
	        }
            pub.publish(speed);
            rate.sleep();
        }
}