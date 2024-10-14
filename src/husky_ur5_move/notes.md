# Error when running the demo
run
```
roslaunch husky_ur5_move demo.launch
```
if error:
RLException: while processing /home/nelsonxu/RobotArmControl/src/husky_ur5_move/launch/planning_context.launch:
Invalid <param> tag: Cannot load command parameter [robot_description]: no such command [['/opt/ros/noetic/share/xacro/xacro.py', '/opt/ros/noetic/share/husky_description/urdf/husky.urdf.xacro', '--inorder', 'urdf_extras:=/home/nelsonxu/RobotArmControl/src/husky_manipulation/husky_ur_description/urdf/husky_ur5_description.urdf.xacro']]. 

Param xml is <param if="$(arg load_robot_description)" name="$(arg robot_description)" command="$(find xacro)/xacro.py '$(find husky_description)/urdf/husky.urdf.xacro'     --inorder     urdf_extras:=$(arg urdf_extras)     "/>
The traceback for the exception was written to the log file

go to husky_manipulation/husky_ur_moveit_config/launch/planning_context.launch, delete ".py" (change to (find xacro)/xacro)

go to husky_ur5_move/launch/planning_context.launch, delete ".py" (change to (find xacro)/xacro)


# Source
source Full/Path/To/husky_ur_description/scripts/setup_husky_ur5_envar 
https://github.com/husky/husky_manipulation/issues/9

