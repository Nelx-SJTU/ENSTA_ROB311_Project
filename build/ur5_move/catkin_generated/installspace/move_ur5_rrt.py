#!/usr/bin/env python3

import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from moveit_commander.conversions import pose_to_list

def move_ur5_to_pose():
    # 初始化MoveIt和ROS节点
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_ur5_rrt_star', anonymous=True)

    # 初始化RobotCommander, PlanningSceneInterface, MoveGroupCommander
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group_name = "manipulator"
    move_group = moveit_commander.MoveGroupCommander(group_name)

    # 获取当前末端执行器的状态
    current_pose = move_group.get_current_pose().pose
    print("Current Pose:", current_pose)

    # 定义目标位姿
    target_pose = geometry_msgs.msg.Pose()
    target_pose.orientation.w = 1.0
    target_pose.position.x = 0.4
    target_pose.position.y = 0.1
    target_pose.position.z = 0.4

    # 设置目标位姿
    move_group.set_pose_target(target_pose)

    # 设置规划算法为RRT*
    move_group.set_planner_id("RRTstar")

    # 规划运动路径并执行
    plan = move_group.go(wait=True)
    move_group.stop()

    # 清除目标
    move_group.clear_pose_targets()

    # 关闭MoveIt!
    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        move_ur5_to_pose()
    except rospy.ROSInterruptException:
        pass

