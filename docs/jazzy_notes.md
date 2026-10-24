# ROS 2 Jazzy — Branch Notes

This document covers Jazzy-specific details, key packages, and build instructions. This is the **default branch** and the primary target for active development.

---

## Branch: `jazzy` (default)

```bash
git clone https://github.com/JosiahSK/moveit2-panda-workshop.git ~/moveit2_ws
# Already on jazzy — no -b flag needed
```

---

## ROS 2 / OS Requirements

| Component | Jazzy Requirement |
|-----------|-------------------|
| Ubuntu | **24.04 LTS** (Noble Numbat) |
| ROS 2 | **Jazzy Jalisco** (May 2024 – May 2029) |
| Gazebo | **Harmonic** (gz-sim8) |
| Python | 3.12 |
| CMake | ≥ 3.28 |

---

## Gazebo Harmonic

Jazzy uses **Gazebo Harmonic** (`gz-sim8`), which replaces the legacy Ignition/Fortress naming.

### Key Changes from Ignition Fortress

| Old (Ignition) | New (Harmonic) |
|----------------|----------------|
| `ign` CLI | `gz` CLI |
| `ign_ros2_control` | `gz_ros2_control` |
| `ros_ign_bridge` | `ros_gz_bridge` |
| `ros_ign_gazebo` | `ros_gz_sim` |
| Topic prefix `ign/` | Topic prefix `gz/` |

### Installing Gazebo Harmonic

```bash
sudo apt-get install curl
sudo curl https://packages.osrfoundation.org/gazebo.gpg \
  --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
  http://packages.osrfoundation.org/gazebo/ubuntu-stable \
  $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-harmonic
```

---

## gz_ros2_control

The workspace uses `gz_ros2_control` to bridge between Gazebo Harmonic physics and `ros2_control`.

### URDF Hardware Plugin (Jazzy)

```xml
<ros2_control name="my_6dof" type="system">
  <hardware>
    <plugin>gz_ros2_control/GazeboSimSystem</plugin>
  </hardware>
  <joint name="joint1">
    <command_interface name="position"/>
    <state_interface name="position"/>
    <state_interface name="velocity"/>
  </joint>
</ros2_control>
```

### Launch Integration

```python
# In spawn_robot.launch.py
gz_ros2_control_node = Node(
    package='controller_manager',
    executable='ros2_control_node',
    parameters=[robot_description, controllers_config],
)
```

---

## Full Build Instructions (Jazzy)

### 1. Install ROS 2 Jazzy

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu \
  $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install -y \
  ros-jazzy-desktop \
  ros-jazzy-moveit \
  ros-jazzy-ros2-control \
  ros-jazzy-ros2-controllers \
  ros-jazzy-gz-ros2-control \
  ros-jazzy-rviz-visual-tools \
  ros-jazzy-robot-state-publisher \
  ros-jazzy-joint-state-publisher-gui
```

### 2. Install Gazebo Harmonic

See section above.

### 3. Clone and Build

```bash
git clone https://github.com/JosiahSK/moveit2-panda-workshop.git ~/moveit2_ws
cd ~/moveit2_ws
source /opt/ros/jazzy/setup.bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
source install/setup.bash
```

### 4. Verify

```bash
ros2 launch my_6dof_bringup rviz_only.launch.py
```

---

## MoveIt2 on Jazzy

Jazzy ships MoveIt2 as binary packages — no source build required:

```bash
sudo apt install ros-jazzy-moveit
```

This installs:
- `moveit_ros_planning` — planning pipeline, move_group server
- `moveit_ros_planning_interface` — Python/C++ client API
- `moveit_ros_visualization` — RViz plugins
- `moveit_kinematics` — KDL, TracIK, BioIK plugins
- `moveit_core` — core data structures

### MoveItPy (Python API)

Fully supported on Jazzy via `moveit.planning`:

```python
from moveit.planning import MoveItPy

moveit = MoveItPy(node_name="my_node")
arm = moveit.get_planning_component("arm")
arm.set_goal_state(configuration_name="ready")
plan_result = arm.plan()
if plan_result:
    moveit.execute(plan_result.trajectory)
```

---

## Environment Variables

Useful for debugging Gazebo Harmonic:

```bash
# Show Gazebo resource search paths
echo $GZ_SIM_RESOURCE_PATH

# Add workspace models to Gazebo
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:~/moveit2_ws/install

# Enable verbose Gazebo output
export GZ_VERBOSE=1
```

---

## Key Jazzy Packages in This Workspace

| Package | Version | Notes |
|---------|---------|-------|
| `moveit` | Jazzy binary | Full MoveIt2 suite |
| `gz_ros2_control` | Jazzy binary | Gazebo Harmonic bridge |
| `ros2_controllers` | Jazzy binary | JTC, GripperAction, etc. |
| `robot_state_publisher` | Jazzy binary | TF + URDF publisher |

---

## See Also

- [Getting Started](./getting_started.md)
- [Humble Notes](./humble_notes.md) — if migrating from Humble
- [Architecture](./architecture.md)
