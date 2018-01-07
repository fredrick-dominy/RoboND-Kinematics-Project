#!/usr/bin/env python

# Copyright (C) 2017 Udacity Inc.
#
# This file is part of Robotic Arm: Pick and Place project for Udacity
# Robotics nano-degree program
#
# All Rights Reserved.

# Author: Harsh Pandya

# import modules
import random

import rospy
import tf
from kuka_arm.srv import *
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from geometry_msgs.msg import Pose
from mpmath import *
from sympy import *


from sympy import init_printing
init_printing()

# Conversion Factors
# rtd = 180. / np.pi  # radians to degrees
# dtr = np.pi / 180.  # degrees to radians

# Define Modified DH Transformation matrix
def construct_matrix(a, alpha, d, q):
    temp = Matrix([[cos(q), -sin(q), 0, a],
                   [sin(q) * cos(alpha), cos(q1) * cos(alpha), -sin(alpha), -sin(alpha) * d],
                   [sin(q) * sin(alpha), cos(q1) * sin(alpha), cos(alpha), cos(alpha) * d],
                   [0, 0, 0, 1]])

    return temp.subs(dh_params)

# Define DH param symbols
q1, q2, q3, q4, q5, q6, q7 = symbols('q1:8')
d1, d2, d3, d4, d5, d6, d7 = symbols('d1:8')
a0, a1, a2, a3, a4, a5, a6 = symbols('a0:7')
alpha0, alpha1, alpha2, alpha3, alpha4, alpha5, alpha6 = symbols('alpha0:7')

# Step 1: is to complete the DH parameter table for the manipulator.
# Modified DH params
# alpha = twist angle
# a = link length
# d = link offset
# q = joint vars
dh_params = {
    alpha0:     0,      a0: 0,      d1: 0.75,
    alpha1:     -pi/2,  a1: 0.35,   d2: 0,      q2: q2-pi/2,
    alpha2:     0,      a2: 1.25,   d3: 0,
    alpha3:     -pi/2,  a3: -0.054, d4: 1.50,
    alpha4:     pi/2,   a4: 0,      d5: 0,
    alpha5:     -pi/2,  a5: 0,      d6: 0,
    alpha6:     0,      a6: 0,      d7: 0.303,      q7:0
}


# Create individual transformation matrices
T0_1 = construct_matrix(a0, alpha0, d1, q1)
T1_2 = construct_matrix(a1,alpha1,d2,d2)
T2_3 = construct_matrix(a2,alpha2,d3,d3)
T3_4 = construct_matrix(a3,alpha3,d4,d4)
T4_5 = construct_matrix(a4,alpha4,d5,d5)
T5_6 = construct_matrix(a5,alpha5,d6,d6)
T6_7 = construct_matrix(a6,alpha6,d7,d7)

T0_6 = simplify( T0_1 * T1_2 * T2_3 * T3_4 * T4_5 * T5_6 )




def handle_calculate_IK(req):
    rospy.loginfo("Received %s eef-poses from the plan" % len(req.poses))
    if len(req.poses) < 1:
        print "No valid poses received"
        return -1
    else:

        ### Your FK code here
        # Create symbols
	#
	#
	# Create Modified DH parameters
	#
	#
	# Define Modified DH Transformation matrix
	#
	#
	# Create individual transformation matrices
	#
	#
	# Extract rotation matrices from the transformation matrices
	#
	#
        ###

        # Initialize service response
        joint_trajectory_list = []
        for x in xrange(0, len(req.poses)):
            # IK code starts here
            joint_trajectory_point = JointTrajectoryPoint()

	    # Extract end-effector position and orientation from request
	    # px,py,pz = end-effector position
	    # roll, pitch, yaw = end-effector orientation

            # Extract end-effector position and orientation from request
            # px,py,pz = end-effector position
            # roll, pitch, yaw = end-effector orientation
            px = req.poses[x].position.x
            py = req.poses[x].position.y
            pz = req.poses[x].position.z

            (roll, pitch, yaw) = tf.transformations.euler_from_quaternion(
                [req.poses[x].orientation.x, req.poses[x].orientation.y,
                    req.poses[x].orientation.z, req.poses[x].orientation.w])

            ### Your IK code here
	    # Compensate for rotation discrepancy between DH parameters and Gazebo
	    #
	    #
	    # Calculate joint angles using Geometric IK method
	    #
	    #
            ###

            # Calculate wrist center - Step 2: is to find the location of the WC relative to the base frame.




            # Calculate joint angles using Geometric IK method

            # if px < 0.001 :
            #     if py < 0.001:
            #         print('px and py are negative at ', px, ' ', py, ' thus Q3')
            #         theta1 = atan(py / px)+pi
            #     else:
            #         print('px is neg and py is pos at ', px, ' ', py, ' thus Q2')
            #         theta1 = atan(py / px) + pi/2
            # else:
            #     if py < 0.001:
            #         print('px is pos and py is neg at ', px, ' ', py, ' thus Q4')
            #         theta1 = atan(py / px) - pi/2
            #     else:
            print('px and py are ', px, ' ', px)
            #         theta1 = atan(py / px)

            # Populate response for the IK request
            theta1 = atan2(py, px)
            print('theta1 is ', theta1)
            theta2 = 0.3
            theta3 = pi/6
            theta4 = 0
            theta5 = 0
            theta6 = 0

            # In the next line replace theta1,theta2...,theta6 by your joint angle variables
            joint_trajectory_point.positions = [theta1, theta2, theta3, theta4, theta5, theta6]
            joint_trajectory_list.append(joint_trajectory_point)

        rospy.loginfo("length of Joint Trajectory List: %s" % len(joint_trajectory_list))
        return CalculateIKResponse(joint_trajectory_list)


def IK_server():
    # initialize node and declare calculate_ik service
    rospy.init_node('IK_server')
    s = rospy.Service('calculate_ik', CalculateIK, handle_calculate_IK)
    print "Ready to receive an IK request"
    rospy.spin()

if __name__ == "__main__":
    IK_server()
