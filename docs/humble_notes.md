# ROS 2 Humble — Branch Notes

This document covers all Humble-specific differences, workarounds, and build instructions. If you're on ROS 2 Jazzy, see [jazzy_notes.md](./jazzy_notes.md) instead.

---

## Branch: `humble`

```bash
git clone -b humble https://github.com/JosiahSK/moveit2-panda-workshop.git ~/moveit2_ws
```

---

## ROS 2 / OS Requirements

| Component | Humble Requirement |
|-----------|--------------------|
| Ubuntu | **22.04 LTS** (Jammy Jellyfish) |
| ROS 2 | **Humble Hawksbill** (May 2022 – May 2027) |
| Gazebo | **Classic** (9/11) or **Fortress** (6.x) |
| Python | 3.10 |
| CMake | ≥ 3.22 |

---

## Gazebo Version Differences

### Jazzy branch uses: **Gazebo Harmonic** (`gz-sim8`)

### Humble branch uses: **Gazebo Classic** or **Gazebo Fortress**

| Feature | Gazebo Classic | Gazebo Fortress | Gazebo Harmonic |
|---------|---------------|-----------------|-----------------|
| Package prefix | `gazebo_ros_pkgs` | `ros_gz` | `ros_gz` |
| Control bridge | `ign_ros2_control` | `ign_ros2_control` | `ign_ros2_control` |
| Sim plugin tag | `libgazebo_ros2_control.so` | `libign_ros2_control.so` | `libign_ros2_control.so` |
| World format | SDF | SDF | SDF |

> [!IMPORTANT]
> The hardware plugin name in the URDF's `<ros2_control>` block is different:
>
> **Humble (Classic/Fortress):**
> ```xml
> <plugin>ign_ros2_control/IgnitionSystem</plugin>
> ```
>
> **Jazzy (Harmonic):**
> ```xml
> <plugin>ign_ros2_control/GazeboSimSystem</plugin>
> ```

---

## API Differences

### ros2_control Package Names

| Jazzy | Humble |
|-------|--------|
| `ign_ros2_control` | `ign_ros2_control` |
| `ign_ros2_control_demos` | `ign_ros2_control_demos` |

### MoveIt2 Python API

The MoveIt2 Python bindings changed between Humble and later versions:

| Feature | Humble | Jazzy |
|---------|--------|-------|
| Import | `from moveit.planning import MoveItPy` | Same |
| Robot state | `moveit.core.robot_state` | Same |
| Available | from `moveit2` source | `ros-jazzy-moveit` |

> [!NOTE]
> On Humble, `MoveItPy` may need to be built from source as it was not available in early binary releases. Check: `apt list --installed | grep moveit`

### moveit_commander (Alternative API)

Humble supports the `moveit_commander` Python wrapper which is simpler:

```python
import moveit_commander
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group = moveit_commander.MoveGroupCommander("arm")

# Plan to named pose
group.set_named_target("ready")
group.go(wait=True)
group.stop()
```

---

## Build Instructions (Humble)

### 1. Install ROS 2 Humble

```bash
sudo apt update && sudo apt install -y curl gnupg lsb-release
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install -y \
  ros-humble-desktop \
  ros-humble-moveit \
  ros-humble-ros2-control \
  ros-humble-ros2-controllers \
  ros-humble-ign-ros2-control \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-rviz-visual-tools
```

### 2. Install Gazebo Classic (if preferred)

```bash
sudo apt install -y gazebo libgazebo-dev ros-humble-gazebo-ros-pkgs
```

### 3. Source and Build

```bash
source /opt/ros/humble/setup.bash
cd ~/moveit2_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
source install/setup.bash
```

---

## Launch Commands (Humble)

```bash
# Source humble
source /opt/ros/humble/setup.bash
source ~/moveit2_ws/install/setup.bash

# RViz only
ros2 launch my_6dof_bringup rviz_only.launch.py

# Demo (fake hardware)
ros2 launch my_6dof_bringup demo.launch.py

# Gazebo Classic + MoveIt2
ros2 launch my_6dof_bringup gazebo_moveit.launch.py use_gazebo_classic:=true
```

---

## Known Issues on Humble

| Issue | Status | Workaround |
|-------|--------|-----------|
| `ign_ros2_control` not available | Expected — use `ign_ros2_control` | See package name differences above |
| MoveItPy binary not in apt | May require source build | Build `moveit2` from source on Humble |
| Gazebo topic bridge names differ | `ros_gz_bridge` vs `gazebo_ros` | Use `ign_ros2_control` launch files |
| Python3.10 type hints differ | Older Python | Minor — no functional impact |

---

## Migrating to Jazzy

If you want to upgrade from Humble to Jazzy:

1. Install Ubuntu 24.04 (clean install recommended)
2. Install ROS 2 Jazzy
3. Switch to the `jazzy` branch: `git checkout jazzy`
4. Replace `ign_ros2_control` → `ign_ros2_control` in URDF
5. Update Gazebo from Classic/Fortress → Harmonic

See [jazzy_notes.md](./jazzy_notes.md) for Jazzy-specific details.

## Key API Differences from Jazzy

### Gazebo Plugin Tag
**Jazzy (Harmonic):**
```xml
<plugin filename="gz_ros2_control-system" name="gz_ros2_control::GazeboSimROS2ControlPlugin"/>
```
**Humble (Fortress/Classic):**
```xml
<plugin filename="libign_ros2_control-system.so" name="ign_ros2_control::IgnitionROS2ControlPlugin"/>
```

### Launch file imports
**Jazzy:** `from launch_ros.actions import Node` with `gz_ros2_control`
**Humble:** Uses `ign_ros2_control` package name

### Colcon build
```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash
```
