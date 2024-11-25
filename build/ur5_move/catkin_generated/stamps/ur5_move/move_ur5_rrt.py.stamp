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
from std_msgs.msg import String

class NLPTopicListener:
    def __init__(self, topic_name, message_type):
        self.received_message = None
        self.topic_name = topic_name
        self.message_type = message_type

    def callback(self, data):
        """
        A callback function that handles the messages subscribed to and is stored in the class properties.
        """
        rospy.loginfo("Message received: %s", data.data)
        self.received_message = data

    def task_to_pose(self):
        if self.received_message:
            # if self.received_message.data == "1_to_2":
            #     return "1_to_2"
            # elif self.received_message.data == "1_to_3":
            #     return "1_to_3"
            # elif self.received_message.data == "1_to_4":
            #     return "1_to_4"
            # elif self.received_message.data == "2_to_1":
            #     return "2_to_1"
            if self.received_message.data == "2_to_3":
                print("YESYESYESYES")
                return "2_to_3"
            elif self.received_message.data == "2_to_4":
                return "2_to_4"
            # elif self.received_message.data == "3_to_1":
            #     return "3_to_1"
            elif self.received_message.data == "3_to_2":
                return "3_to_2"
            elif self.received_message.data == "3_to_4":
                return "3_to_4"
            # elif self.received_message.data == "4_to_1":
            #     return "4_to_1"
            elif self.received_message.data == "4_to_2":
                return "4_to_2"
            elif self.received_message.data == "4_to_3":
                return "4_to_3"
        else:
            rospy.loginfo("Cannot read pose file as message is not correctly received and saved.")
            rospy.loginfo("The robot will perform the default task.")
            print("FUCK !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return "grab_poses"

    def wait_for_message(self):
        """
        Wait until the message is received.
        """
        rospy.Subscriber(self.topic_name, self.message_type, self.callback)

        # Loop waiting for messages
        while not rospy.is_shutdown():
            if self.received_message:
                rospy.loginfo("Exiting after receiving the message.")
                break  # Exit the loop after receiving a message
            rospy.sleep(0.5)  # Slightly hibernate to avoid excessive CPU usage
        return self.received_message

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
    package_path = rospack.get_path('ur5_move')

    try:
        # Initialise the class and specify the topic name and message type
        topic_listener = NLPTopicListener("task_name", String)
        message = topic_listener.wait_for_message()  # Wait for messages
        rospy.loginfo("Final received message: {}".format(message.data))

        poses_file_name = topic_listener.task_to_pose()
        yaml_file = package_path + "/config/poses/" + str(poses_file_name) + ".yaml"
    except rospy.ROSInterruptException:
        rospy.loginfo("Node terminated.")


    target_poses = read_poses_from_yaml(yaml_file)

    # target_poses = read_poses_from_yaml(package_path + "/config/poses/4_to_3.yaml")

    try:
        # Iterate through each target pose and execute the motion
        for i, target_pose in enumerate(target_poses):
            #rospy.loginfo(f"Moving to pose {i+1}/{len(target_poses)}")
            move_ur5_to_pose(target_pose)
            rospy.sleep(0.5)  # Pause for 1 second after each move
    except rospy.ROSInterruptException:
        pass
    finally:
        # Shutdown MoveIt!
        moveit_commander.roscpp_shutdown()