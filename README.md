# Voice-Guided Automated Grasping System Using UR5 Robotic Arm

## Overview
This project aims to develop an automated grasping system using a Husky AGV equipped with a UR5 robotic arm, guided by human voice commands. The primary objective is to enable the robot to execute simple grasping tasks based on voice input, such as ``place the green cylinder to the right of the blue cylinder." By leveraging vision-based object recognition and a simplified voice processing technique, the system will detect objects and perform the desired actions using a gripper attached to the end-effector of the robotic arm.
## Prerequisites

### Dependencies:
- **ROS**: Ensure you have ROS installed. This package assumes the use of ROS with MoveIt for motion planning. The whole project is tested with `ROS Melodic`.
- **MoveIt**
  - `moveit`
  - `ur5_moveit_config`

To install `moveit`:
```bash
sudo apt install ros-melodic-moveit
```
To install `ur5_moveit_config`:
```bash
cd /catkin_ws/src
git clone https://github.com/ros-industrial/universal_robot.git
```

- **Python**: Python is used for scripting. Required Python packages include:
  - `rospy`
  - `yaml`
  - `tf-conversions`
  - `spacy` (tested with version 2.2.3)

We use the NLP model `en_core_web_sm`, to install it:
```bash
python -m spacy download en_core_web_sm
```

Ensure these are installed in your ROS workspace.

- **Support for microphone**
Install all the necessary packages:
```bash
sudo apt install -y alsa-utils alsa-oss libasound2 libasound2-dev
python2 -m pip install pyaudio===0.2.11
```

- **Support for Docker**
If you run our project in Docker, ensure that you run the following two commands:

To enable the rviz, run this command in your local terminal:
```bash
xhost +
``` 
To enable audio support in your container, add to your `docker-compose.yml`:
```bash
devices:
  - "/dev/snd:/dev/snd"
```
## Installation

1. Clone this repository into your ROS workspace:
   ```bash
   cd ~/catkin_ws
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
### Path Planning

- **ur5_move/src/add_obstacles.py**:  
  This script loads and adds obstacles to the MoveIt planning scene based on the configuration provided in the `obstacles.yaml` file.

- **ur5_move/src/move_ur5_rrt.py**:  
  This script moves the UR5 arm to a series of target poses using the RRT* algorithm. The target poses are read from the `grab_poses.yaml` file.

- **ur5_move/launch/ur5_planning.launch** and **ur5_move/launch/ur5_setup.launch**:  
  These launch files set up the necessary ROS nodes for MoveIt and robot control, as well as loading the necessary parameters for planning and executing motions.

- **ur5_move/config/environments/obstacles.yaml**:  
  This YAML file defines the obstacles that are loaded into the planning scene. Each obstacle includes an ID, frame of reference, dimensions, and pose (position and orientation).

- **ur5_move/config/poses/grab_poses.yaml**:  
  This YAML file defines a series of target poses that the UR5 arm will move to. The poses are defined in terms of position (x, y, z) and orientation (roll, pitch, yaw), which are converted to quaternions during execution.

## Usage Instructions

### Connection with UR5
The model of robot arm is UR5, so make sure the cable of UR5 arm is connected directly to your computer (instead of Husky). To connect to robot Arm UR5:
1. Install the driver.
```bash
sudo apt install ros-melodic-ur-robot-driver ros-melodic-ur-calibration
```
2. Load the external_control on the control panel of UR5.
3. Run the bring_up file. Replace the robot_ip with the one of your actual robot.
```bash
roslaunch ur_robot_driver ur5_bringup.launch robot_ip:=192.168.131.40
```
### Launch the Full Setup
   You can launch the entire setup using the provided launch files:
   ```bash
   roslaunch ur5_move ur5_planning.launch
   ```
   This will initialize the environment, load obstacles, and start the RRT-Connect planning. This program waits for the publish of rostopic `task_name`, which is sent in the NLP part. After receiving the rostopic, it will start to move the objects.

### Launch the Command parser (voice recognition module)
To give your command to the robot arm, you should run the launch file of `command_parser` package to enable the voice recognition node and the NLP node:
```bash
roslaunch command_parser test.launch
```

In order to get the index of your microphone, you can run the script `find_device.py` in folder `commander_parser/src`, and change the `DEVICE_INDEX` in the script `voice_recognition.py`

Once you see `Recording...` shown in the terminal, you have seven seconds to give your voice command.

## Interaction Guidelines

In the default configuration of the system, the environment is initialized as follows:

```
Position 1      Position 2      Position 3      Position 4
   Book            Flask           Jar           Container

                             UR5
```

To interact effectively with the robotic system, users must adhere to the following operational rules:

1. **Object Relocation Constraint**: Only the designated objects (*Flask*, *Jar*, *Container*) may be moved, and they can only be relocated to positions 2, 3, or 4. Position 1, containing the *Book*, remains static and inaccessible for these operations.

2. **Prohibition on Redundant Moves**: An object cannot be moved to the position it currently occupies. Attempts to execute such redundant actions will be invalid within the system's operational framework.

To ensure accurate recognition and processing of voice commands, users must utilize a high-quality microphone capable of capturing clear audio. Additionally, all spoken commands should strictly adhere to proper grammatical structure for optimal system performance.

### Examples of Voice Commands

1. **Move the flask to the left of the container.**  
   This command directs the system to reposition the *flask* to a position immediately to the left of the *container*.

2. **Move the container to the right of the book.**  
   This command instructs the system to relocate the *container* to a position immediately to the right of the *book*. 

These guidelines are essential for ensuring accurate and efficient interaction with the UR5 robotic manipulator in the specified environment configuration.
