# UR5 MoveIt RRT Planning with Obstacles

## Overview

This project provides a MoveIt-based motion planning setup for the UR5 robotic arm using the RRT* (Rapidly-exploring Random Tree Star) algorithm for path planning. It includes obstacle addition from a YAML configuration file and pose-based motion commands for moving the UR5 arm. The robot's environment and target positions can be dynamically set using the provided YAML files.

### Key Features:
- **RRT Planning**: The robot arm plans its path using the RRT* algorithm for efficient and optimized motion planning.
- **Dynamic Obstacle Handling**: Obstacles are loaded from a YAML file and added to the MoveIt planning scene.
- **Custom Poses**: Target poses for the UR5 arm are loaded from YAML and converted from Euler angles to quaternions for MoveIt compatibility.

## Prerequisites

### Dependencies:
- **ROS**: Ensure you have ROS installed. This package assumes the use of ROS with MoveIt for motion planning.
- **MoveIt**: The package uses MoveIt for robotic arm control and path planning.
- **Python**: Python is used for scripting. Required Python packages include:
  - `rospy`
  - `moveit_commander`
  - `yaml`
  - `tf.transformations`

Ensure these are installed in your ROS workspace.

## Installation

1. Clone this repository into your ROS workspace:
   ```bash
   cd ~/catkin_ws/src
   git clone https://github.com/Nelx-SJTU/ENSTA_ROB311_Project.git
   ```

2. Build the workspace:
   ```bash
   cd ~/catkin_ws
   catkin_make
   ```

3. Source the workspace:
   ```bash
   source devel/setup.bash
   ```

## File Descriptions

- **add_obstacles.py**:  
  This script loads and adds obstacles to the MoveIt planning scene based on the configuration provided in the `obstacles.yaml` file.
  - **Usage**:  
    ```bash
    rosrun ur5_move add_obstacles.py
    ```

- **move_ur5_rrt.py**:  
  This script moves the UR5 arm to a series of target poses using the RRT* algorithm. The target poses are read from the `grab_poses.yaml` file.
  - **Usage**:  
    ```bash
    rosrun ur5_move move_ur5_rrt.py
    ```

- **ur5_planning.launch** and **ur5_setup.launch**:  
  These launch files set up the necessary ROS nodes for MoveIt and robot control, as well as loading the necessary parameters for planning and executing motions.

- **obstacles.yaml**:  
  This YAML file defines the obstacles that are loaded into the planning scene. Each obstacle includes an ID, frame of reference, dimensions, and pose (position and orientation).

- **grab_poses.yaml**:  
  This YAML file defines a series of target poses that the UR5 arm will move to. The poses are defined in terms of position (x, y, z) and orientation (roll, pitch, yaw), which are converted to quaternions during execution.

## Usage Instructions
**Launch the Full Setup**:
   You can launch the entire setup using the provided launch files:
   ```bash
   roslaunch ur5_move ur5_planning.launch
   ```
   This will initialize the environment, load obstacles, and start the RRT* planning. This program grabs the first item on the table and places it at the position of the third item.

## Configuration

### Adding Obstacles
Obstacles are configured in the `config/environments/obstacles.yaml` file. Each obstacle should be defined with an ID, frame reference, dimensions (as a box), and pose. Modify this file to add or change obstacles.

### Defining Target Poses
Target poses for the UR5 arm are set in the `config/poses/grab_poses.yaml` file. The positions and orientations (in Euler angles) for each pose are specified here. Modify this file to change the target poses.



