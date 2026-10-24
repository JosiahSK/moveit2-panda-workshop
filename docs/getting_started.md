# Getting Started

Welcome to the **MoveIt2 6-DOF Robot Workspace**! This guide will get you from zero to a running robot simulation in about 10–15 minutes.

---

## Prerequisites

### Common Requirements (Both Branches)

| Tool | Version | Install Guide |
|------|---------|---------------|
| Ubuntu | 22.04 (Humble) or 24.04 (Jazzy) | [ubuntu.com](https://ubuntu.com/download) |
| ROS 2 | See branch below | [docs.ros.org](https://docs.ros.org) |
| MoveIt2 | Matching ROS 2 version | [moveit.ros.org](https://moveit.ros.org) |
| colcon | Latest | `pip install colcon-common-extensions` |
| vcstool | Latest | `pip install vcstool` |

---

## Branch Selection

> [!IMPORTANT]
> Choose the branch matching your ROS 2 installation **before cloning**.

| Branch | ROS 2 Version | Ubuntu | Gazebo |
|--------|--------------|--------|--------|
| `jazzy` (**default**) | Jazzy Jalisco | 24.04 | Harmonic (gz-sim8) |
| `humble` | Humble Hawksbill | 22.04 | Classic / Fortress |

---

## Installation: ROS 2 Jazzy (jazzy branch)

### 1. Install ROS 2 Jazzy

```bash
# Add ROS 2 apt repository
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install ros-jazzy-desktop ros-jazzy-moveit ros-jazzy-ros2-control \
                 ros-jazzy-ros2-controllers ros-jazzy-gz-ros2-control
```

### 2. Install Gazebo Harmonic

```bash
sudo apt-get install curl
sudo curl https://packages.osrfoundation.org/gazebo.gpg \
  --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] \
  http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-harmonic
```

### 3. Clone & Build (Jazzy)

```bash
# Clone the jazzy branch
git clone -b jazzy https://github.com/JosiahSK/moveit2-panda-workshop.git ~/moveit2_ws
cd ~/moveit2_ws

# Source ROS 2
source /opt/ros/jazzy/setup.bash

# Install dependencies
rosdep update
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build --symlink-install
source install/setup.bash
```

---

## Installation: ROS 2 Humble (humble branch)

### 1. Install ROS 2 Humble

```bash
sudo apt update && sudo apt install curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install ros-humble-desktop ros-humble-moveit ros-humble-ros2-control \
                 ros-humble-ros2-controllers
```

### 2. Clone & Build (Humble)

```bash
# Clone the humble branch
git clone -b humble https://github.com/JosiahSK/moveit2-panda-workshop.git ~/moveit2_ws
cd ~/moveit2_ws

# Source ROS 2
source /opt/ros/humble/setup.bash

# Install dependencies
rosdep update
rosdep install --from-paths src --ignore-src -r -y

# Build
colcon build --symlink-install
source install/setup.bash
```

> [!NOTE]
> For Humble, Gazebo Classic is used instead of Gazebo Harmonic. See [humble_notes.md](./humble_notes.md) for details.

---

## Your First Launch

Open a terminal, source your workspace, and pick a launch mode:

```bash
cd ~/moveit2_ws
source install/setup.bash
```

### Option A — RViz only (no simulation, fastest)
```bash
ros2 launch my_6dof_bringup rviz_only.launch.py
```
Opens RViz with the robot model. Good for checking your URDF and MoveIt2 config.

### Option B — MoveIt2 demo (no Gazebo)
```bash
ros2 launch my_6dof_bringup demo.launch.py
```
Full MoveIt2 stack with fake hardware. Motion planning works but no physics.

### Option C — Full Gazebo + MoveIt2
```bash
ros2 launch my_6dof_bringup gazebo_moveit.launch.py
```
Complete simulation: Gazebo physics + MoveIt2 + RViz2. Takes ~30 s to start.

### Option D — Run the pick & place demo
After launching Option C:
```bash
# In a new terminal
source ~/moveit2_ws/install/setup.bash
ros2 run my_6dof_bringup pick_and_place.py
```

---

## Verifying Your Setup

Check that all nodes are running:
```bash
ros2 node list
```

Expected output includes:
- `/move_group`
- `/robot_state_publisher`
- `/controller_manager`
- `/arm_controller` (or similar)
- `/rviz2`
- `/gz_sim` (if Gazebo mode)

Check active topics:
```bash
ros2 topic list | grep -E "joint_states|planning_scene|move_group"
```

---

## Common Issues

| Problem | Solution |
|---------|----------|
| `rosdep` fails | Run `rosdep update` first |
| RViz shows no robot | Check `robot_state_publisher` is running; source workspace |
| Gazebo won't start | Ensure `gz-harmonic` is installed; check `GZ_SIM_RESOURCE_PATH` |
| Planning always fails | Check planning timeout in OMPL config; collision objects may be blocking |
| `colcon build` errors | Make sure you sourced `/opt/ros/<distro>/setup.bash` |

---

## Next Steps

- 📐 [Architecture Overview](./architecture.md) — understand how the nodes connect
- 🎯 [Motion Planning Guide](./motion_planning.md) — use the RViz planning panel
- 🤖 [Pick & Place Demo](./pick_and_place.md) — step through the demo script
- 📦 [Package Overview](./package_overview.md) — explore each package's files
