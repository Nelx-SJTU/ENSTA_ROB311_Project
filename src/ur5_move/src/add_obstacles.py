#!/usr/bin/env python

import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import shape_msgs.msg

def add_obstacle(scene):
    # 创建障碍物
    obstacle = moveit_msgs.msg.CollisionObject()
    obstacle.id = "box1"
    obstacle.header.frame_id = "base_link"  # 使用 UR5 的 base_link 作为参考坐标系

    # 定义障碍物的形状和尺寸
    box = shape_msgs.msg.SolidPrimitive()
    box.type = shape_msgs.msg.SolidPrimitive.BOX
    box.dimensions = [0.4, 0.4, 0.4]  # 立方体的尺寸

    # 定义障碍物的位置
    box_pose = geometry_msgs.msg.Pose()
    box_pose.position.x = 0.6
    box_pose.position.y = 0.6
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

    # 等待场景初始化
    rospy.sleep(2)

    # 添加障碍物
    add_obstacle(scene)

    # 打印当前场景中的物体列表，验证是否成功添加
    print("Current objects in the scene:", scene.get_known_object_names())

    # 等待Rviz更新障碍物的显示
    rospy.sleep(2)

    rospy.spin()

