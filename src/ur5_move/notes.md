# Installation
```
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws
catkin_make
```

```
source ~/catkin_ws/devel/setup.bash
cd ~/catkin_ws/src
catkin_create_pkg ur5_move rospy moveit_commander geometry_msgs
```

open CMakeLists.txt and add
```
## Add the Python scripts to be executable
catkin_install_python(PROGRAMS
  src/move_ur5_to_pose.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
```

# Run a demo
```
cd RobotArmTools
source devel/setup.bash
```
Run in a terminal
```
roslaunch ur5_moveit_config demo.launch
```
Run in another terminal
```
rosrun ur5_move move_ur5_demo.py
```

# Activate virtual env
```
source ~/robotarm/bin/activate
```

# Load Rviz settings
```
rviz -d ./config/rviz/rviz_config.rviz
```

# Run the RRT planning
```
roslaunch ur5_move ur5_planning.launch
```
