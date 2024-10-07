#!/usr/bin/env python

import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from moveit_commander.conversions import pose_to_list

def all_close(goal, actual, tolerance):
    """Helper function to check if the goal and actual poses are close enough"""
    all_equal = True
    for index in range(len(goal)):
        if abs(actual[index] - goal[index]) > tolerance:
            return False
    return True

def move_ur5_to_pose():
    # Initialize moveit_commander and ROS node
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_ur5_to_pose', anonymous=True)

    # Initialize `RobotCommander`, `PlanningSceneInterface`, `MoveGroupCommander`
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()

    group_name = "manipulator"  # Typically, UR5's MoveIt! group name is "manipulator"
    move_group = moveit_commander.MoveGroupCommander(group_name)

    # Get the current state of the robot
    planning_frame = move_group.get_planning_frame()
    print("Planning frame:", planning_frame)

    # Get the current state of the end effector
    eef_link = move_group.get_end_effector_link()
    print("End effector link:", eef_link)

    # Get the current joint states of the robot
    current_joint_values = move_group.get_current_joint_values()
    print("Current Joint Values:", current_joint_values)

    # Get the current pose of the robot
    current_pose = move_group.get_current_pose().pose
    print("Current Pose:", current_pose)

    # Define the target pose
    target_pose = geometry_msgs.msg.Pose()
    target_pose.orientation.w = 1.0
    target_pose.position.x = 0.4
    target_pose.position.y = 0.1
    target_pose.position.z = 0.4

    # Set the robot's target pose
    move_group.set_pose_target(target_pose)

    # Plan and execute the motion
    plan = move_group.go(wait=True)
    move_group.stop()

    # Clear the target
    move_group.clear_pose_targets()

    # Confirm if the movement was successful
    current_pose = move_group.get_current_pose().pose
    success = all_close(pose_to_list(target_pose), pose_to_list(current_pose), 0.01)
    print("Move success:", success)

    # Shutdown and exit moveit_commander
    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        move_ur5_to_pose()
    except rospy.ROSInterruptException:
        pass
