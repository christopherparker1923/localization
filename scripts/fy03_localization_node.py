#!/usr/bin/env python

import rospy
# from ros_dwm1001.msg import UWBTag, UWBAnchor
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry

from matplotlib.pyplot import *
from random import *
from math import *
import scipy as scipy
#import scipy.stats
#from numpy import *

class LocalizationNode:
    def __init__(self):
        #
        # Instantiate Localization object.
        # self.localization = Localization()
        #

        # self.tag_msg_ = Tag()
        # self.anchor_msg_ = Anchor()
        self.imu_msg_ = Imu()
        self.fused_pose_msg_ = Odometry()
        
        # self.uwb_tag_sub_ = rospy.Subscriber("/uwb_tag", Tag, self.tagCallback)
        # self.uwb_anchor_sub_ = rospy.Subscriber("/uwb_anchor", Anchor, self.anchorCallback)
        self.imu_sub_ = rospy.Subscriber("/imu", Imu, self.imuCallback)
        self.fused_pose_pub_ = rospy.Publisher('/fused_pose', Odometry, queue_size = 1)

	# Particle Filter.	
	self.num_particles = 10
    	self.x_range = (0,10)
    	self.y_range = (0,10)
    	self.x_vals = []
    	self.y_vals = []
    	self.weights = []
    	self.current_estimate = ()
    	self.normalized_weights = []
    	self.UWB_covariance = 0.3

    	# Create initial particles.
    	self.initialize_particles()
    	
	# Plot initial particles with default weights.
    	self.plot_particles()

    def run(self):
        rospy.spin()
    
    def tagCallback(self, tag_msg):
        #self.publishFusedPose(fused_pose)
	pass

    def anchorCallback(self, anchor_msg):
        #self.publishFusedPose(fused_pose)
	pass

    def imuCallback(self, imu_msg):
    	#message_time = imu_msg.header.stamp.to_sec()
    	#rospy.loginfo("Message sequence: %f, Message time: %f", imu_msg.header.seq, message_time)

    	linear_acceleration_x = imu_msg.linear_acceleration.x
    	linear_acceleration_y = imu_msg.linear_acceleration.y
    	#linear_acceleration_z = imu_msg.linear_acceleration.z
	u = [linear_acceleration_x, linear_acceleration_y]	
	
	#predict(u)

    def publishFusedPose(self, fused_pose):
        # self.fused_pose_pub_.publish(self.fused_pose_msg_)
        pass

    # Initial generation of particle based on uniform distribution.
    def initialize_particles(self):
	for i in range(self.num_particles):
            self.x_vals.append(uniform(self.x_range[0], self.x_range[1]))
            self.y_vals.append(uniform(self.y_range[0], self.y_range[1]))

    # Plot particles on scatter plot.
    # Weights set to 1 by default, unless specified through argument/parameter.
    def plot_particles(self, weights = 1):
    	scatter(self.x_vals, self.y_vals, weights)
    	show()

    # Prediction step.
    # Get motion data (control inputs) from IMU and move particles.
    def predict(self, u, dt = 1.): #std: float):
        #dist = (u[1] * dt) + (np.random.randn(N) * std[1])
        #particles[:, 0] += np.cos(u[0]) * dist
        #particles[:, 1] += np.sin(u[0]) * dist

	linear_acceleration_x = u[0]
	linear_acceleration_y = u[1]
	
	linear_velocity_x = linear_acceleration_x * dt
	linear_velocity_y = linear_acceleration_y * dt

	linear_displacement_x = linear_velocity_x * dt
	linear_displacement_y = linear_velocity_y * dt

        for i in range(self.num_particles):
            self.x_vals[i] += linear_displacement_x
            self.y_vals[i] += linear_displacement_y

	self.plot_particles()

if __name__ == '__main__':
    rospy.init_node("fy03_localization_node")
    localization_node = LocalizationNode()
    
    try:
        localization_node.run()
    except rospy.ROSInterruptException:
        pass

