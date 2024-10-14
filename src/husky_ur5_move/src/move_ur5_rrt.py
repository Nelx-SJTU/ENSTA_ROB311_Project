#!/usr/bin/env python

import sys
import rospy
import moveit_commander
import geometry_msgs.msg
from math import pi
from moveit_commander.conversions import pose_to_list
import tf.transformations
import yaml
import rospkg

def euler_to_quaternion(roll, pitch, yaw):
    # Use tf.transformations to convert Euler angles to quaternion
    quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
    return quaternion

def move_ur5_to_pose(target_pose):
    # Publish the current end effector pose to RViz
    current_pose_pub = rospy.Publisher('/ur5_current_pose', geometry_msgs.msg.PoseStamped, queue_size=10)
    target_pose_pub = rospy.Publisher('/ur5_target_pose', geometry_msgs.msg.PoseStamped, queue_size=10)

    # Get the current state of the end effector
    current_pose = move_group.get_current_pose().pose
    print("Current Pose:", current_pose)

    current_pose_stamped = geometry_msgs.msg.PoseStamped()
    current_pose_stamped.header.stamp = rospy.Time.now()
    current_pose_stamped.header.frame_id = move_group.get_planning_frame()
    current_pose_stamped.pose = current_pose
    current_pose_pub.publish(current_pose_stamped)

    # Publish the target end effector pose to RViz
    target_pose_stamped = geometry_msgs.msg.PoseStamped()
    target_pose_stamped.header.stamp = rospy.Time.now()
    target_pose_stamped.header.frame_id = move_group.get_planning_frame()
    target_pose_stamped.pose = target_pose
    target_pose_pub.publish(target_pose_stamped)

    # Set the target pose
    move_group.set_pose_target(target_pose)

    # Set the planner algorithm to RRT*
    move_group.set_planner_id("RRTstar")

    # Plan the motion path and execute
    plan = move_group.go(wait=True)
    move_group.stop()

    # Clear the target
    move_group.clear_pose_targets()

def read_poses_from_yaml(file_path):
    # Read YAML file and parse target poses
    with open(file_path, 'r') as file:
        poses_data = yaml.safe_load(file)
    
    target_poses = []
    for pose_data in poses_data['poses']:
        target_pose = geometry_msgs.msg.Pose()

        # Read position (x, y, z)
        target_pose.position.x = pose_data['x']
        target_pose.position.y = pose_data['y']
        target_pose.position.z = pose_data['z']

        # Read Euler angles (roll, pitch, yaw) and convert to quaternion
        roll = pose_data['roll']
        pitch = pose_data['pitch']
        yaw = pose_data['yaw']
        quaternion = euler_to_quaternion(roll, pitch, yaw)

        # Set the quaternion for the target pose
        target_pose.orientation.x = quaternion[0]
        target_pose.orientation.y = quaternion[1]
        target_pose.orientation.z = quaternion[2]
        target_pose.orientation.w = quaternion[3]

        target_poses.append(target_pose)

    return target_poses

if __name__ == '__main__':
    # Initialize RobotCommander, PlanningSceneInterface, MoveGroupCommander
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_ur5_rrt_star', anonymous=True)
    
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group_name = "manipulator"
    move_group = moveit_commander.MoveGroupCommander(group_name)

    # Wait for the scene to finish updating
    rospy.sleep(2)  # Wait long enough to ensure obstacles are loaded
    known_objects = scene.get_known_object_names()
    print("Known objects in the scene:", known_objects)

    # Read target poses
    rospack = rospkg.RosPack()
    package_path = rospack.get_path('husky_ur5_move')  # Replace 'your_package_name' with your package name
    yaml_file = package_path + "/config/poses/grab_poses.yaml"  # Assuming YAML file is located in the config directory of the ROS package
    target_poses = read_poses_from_yaml(yaml_file)

    try:
        # Iterate through each target pose and execute the motion
        for i, target_pose in enumerate(target_poses):
            rospy.loginfo(f"Moving to pose {i+1}/{len(target_poses)}...")
            move_ur5_to_pose(target_pose)
            rospy.sleep(1)  # Pause for 1 second after each move
    except rospy.ROSInterruptException:
        pass
    finally:
        # Shutdown MoveIt!
        moveit_commander.roscpp_shutdown()
