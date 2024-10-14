#!/usr/bin/env python3

import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import shape_msgs.msg
import yaml
import rospkg

def load_obstacles_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        obstacles_data = yaml.safe_load(file)
    return obstacles_data

def add_obstacles_from_yaml(scene, obstacles_data):
    for obstacle_data in obstacles_data['obstacles']:
        # Create obstacles
        obstacle = moveit_msgs.msg.CollisionObject()
        obstacle.id = obstacle_data['id']
        obstacle.header.frame_id = obstacle_data['frame_id']  # 参考坐标系

        # Define the shapes and sizes of obstacles
        solid_primitive = shape_msgs.msg.SolidPrimitive()
        solid_primitive.type = shape_msgs.msg.SolidPrimitive.BOX
        solid_primitive.dimensions = obstacle_data['dimensions']

        # Define the poses of obstacles
        pose = geometry_msgs.msg.Pose()
        pose.position.x = obstacle_data['pose']['position']['x']
        pose.position.y = obstacle_data['pose']['position']['y']
        pose.position.z = obstacle_data['pose']['position']['z']
        pose.orientation.x = obstacle_data['pose']['orientation']['x']
        pose.orientation.y = obstacle_data['pose']['orientation']['y']
        pose.orientation.z = obstacle_data['pose']['orientation']['z']
        pose.orientation.w = obstacle_data['pose']['orientation']['w']

        # Add shapes and poses to obstacles lists
        obstacle.primitives.append(solid_primitive)
        obstacle.primitive_poses.append(pose)
        obstacle.operation = obstacle.ADD

        # Add obstacles to scenes
        scene.add_object(obstacle)

if __name__ == "__main__":
    rospy.init_node("add_obstacles_node", anonymous=True)
    scene = moveit_commander.PlanningSceneInterface()

    # Wait for initialization of scene
    rospy.sleep(2)

    # Load obstacles infomation from yaml
    rospack = rospkg.RosPack()
    package_path = rospack.get_path('ur5_move')
    yaml_file = package_path + "/config/environments/obstacles.yaml"
    obstacles_data = load_obstacles_from_yaml(yaml_file)

    # Add obstacles
    add_obstacles_from_yaml(scene, obstacles_data)
    print("Current objects in the scene:", scene.get_known_object_names())

    # Wait for Rviz update of displaying obstacles
    rospy.sleep(2)

    rospy.spin()
