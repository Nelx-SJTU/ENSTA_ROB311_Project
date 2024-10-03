#!/usr/bin/env python3

import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import shape_msgs.msg

def add_obstacle(scene):
    # 创建障碍物
    obstacle = moveit_msgs.msg.CollisionObject()
    obstacle.id = "box1"
    obstacle.header.frame_id = "world"

    # 定义障碍物的形状和尺寸
    box = shape_msgs.msg.SolidPrimitive()
    box.type = shape_msgs.msg.SolidPrimitive.BOX
    box.dimensions = [0.5, 0.5, 0.5]  # 立方体的尺寸

    # 定义障碍物的位置
    box_pose = geometry_msgs.msg.Pose()
    box_pose.position.x = 0.6
    box_pose.position.y = 0.0
    box_pose.position.z = 0.25
    box_pose.orientation.w = 1.0

    # 将形状和位姿添加到障碍物
    obstacle.primitives.append(box)
    obstacle.primitive_poses.append(box_pose)
    obstacle.operation = obstacle.ADD

    # 将障碍物添加到规划场景中
    scene.add_object(obstacle)

if __name__ == "__main__":
    rospy.init_node("add_obstacles_node", anonymous=True)
    scene = moveit_commander.PlanningSceneInterface()

    # 等待场景完全初始化
    rospy.sleep(2)

    # 检查是否能看到障碍物已加载的确认
    planning_frame = scene.get_planning_frame()
    print("Planning frame: ", planning_frame)

    # 添加障碍物
    add_obstacle(scene)

    # 等待Rviz更新障碍物的显示
    rospy.sleep(2)

    rospy.spin()

