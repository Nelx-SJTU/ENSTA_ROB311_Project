#!/usr/bin/env python3

import sys
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from moveit_commander.conversions import pose_to_list

def all_close(goal, actual, tolerance):
    """辅助函数，用于检查目标和实际位姿是否接近"""
    all_equal = True
    for index in range(len(goal)):
        if abs(actual[index] - goal[index]) > tolerance:
            return False
    return True

def move_ur5_to_pose():
    # 初始化 moveit_commander 和 ROS 节点
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('move_ur5_to_pose', anonymous=True)

    # 初始化 `RobotCommander`, `PlanningSceneInterface`, `MoveGroupCommander`
    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()

    group_name = "manipulator"  # 通常 UR5 的 MoveIt! 群组名为 "manipulator"
    move_group = moveit_commander.MoveGroupCommander(group_name)

    # 获取当前机器人的状态
    planning_frame = move_group.get_planning_frame()
    print("Planning frame:", planning_frame)

    # 获取当前末端执行器的状态
    eef_link = move_group.get_end_effector_link()
    print("End effector link:", eef_link)

    # 获取机器人当前的关节状态
    current_joint_values = move_group.get_current_joint_values()
    print("Current Joint Values:", current_joint_values)

    # 获取机器人当前的位姿
    current_pose = move_group.get_current_pose().pose
    print("Current Pose:", current_pose)

    # 定义目标位姿
    target_pose = geometry_msgs.msg.Pose()
    target_pose.orientation.w = 1.0
    target_pose.position.x = 0.4
    target_pose.position.y = 0.1
    target_pose.position.z = 0.4

    # 设置机器人目标位姿
    move_group.set_pose_target(target_pose)

    # 计划运动并执行
    plan = move_group.go(wait=True)
    move_group.stop()

    # 清除目标
    move_group.clear_pose_targets()

    # 确认是否移动成功
    current_pose = move_group.get_current_pose().pose
    success = all_close(pose_to_list(target_pose), pose_to_list(current_pose), 0.01)
    print("Move success:", success)

    # 关闭并退出 moveit_commander
    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    try:
        move_ur5_to_pose()
    except rospy.ROSInterruptException:
        pass

