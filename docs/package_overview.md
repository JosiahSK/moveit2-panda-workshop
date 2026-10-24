# Package Overview

This document describes every package in the workspace — what it does, what its key files are, and how it fits into the overall system.

---

## Directory Tree

```
moveit2_ws/
├── src/
│   ├── my_6dof_description/       # Robot URDF/Xacro model
│   ├── my_6dof_moveit_config/     # MoveIt2 configuration
│   ├── my_6dof_controllers/       # ros2_control controller config
│   ├── my_6dof_gazebo/            # Gazebo simulation world
│   ├── my_6dof_bringup/           # Top-level launch files + demo scripts
│   └── deps/                      # Vendored dependencies (not in git)
├── panda_ign_moveit2/             # Franka Panda reference packages
│   ├── panda_description/
│   └── panda_moveit_config/
├── docs/                          # Educational documentation
├── README.md
└── .gitignore
```

---

## `my_6dof_description`

**Role:** Provides the complete robot model as URDF/Xacro.

```
my_6dof_description/
├── CMakeLists.txt
├── package.xml
├── urdf/
│   └── my_6dof.urdf.xacro        # Main robot description
├── config/
│   └── (optional gazebo plugins)
├── launch/
│   └── display.launch.py          # Standalone RViz display
└── rviz/
    └── (optional default rviz config)
```

### Key Concepts

**Xacro** is a macro language for URDF that allows:
- Reusable link/joint macros
- Math expressions (`${pi/2}`)
- Conditional includes
- Clean parameterized robot descriptions

**URDF structure** for each link:
```xml
<link name="link1">
  <visual>
    <geometry><mesh filename="..."/></geometry>
    <material name="blue"/>
  </visual>
  <collision>
    <geometry><cylinder radius="0.05" length="0.1"/></geometry>
  </collision>
  <inertial>
    <mass value="1.5"/>
    <inertia ixx="..." ixy="0" ixz="0" iyy="..." iyz="0" izz="..."/>
  </inertial>
</link>
```

**ros2_control hardware interface tags** (inside the Xacro):
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
  <!-- ... joints 2-6 ... -->
</ros2_control>
```

---

## `my_6dof_moveit_config`

**Role:** All MoveIt2 configuration files. This is the "brain" of the motion planning setup.

```
my_6dof_moveit_config/
├── CMakeLists.txt
├── package.xml
├── config/
│   ├── my_6dof.srdf               # Semantic robot description
│   ├── kinematics.yaml            # IK solver configuration
│   ├── ompl_planning.yaml         # OMPL planner settings
│   ├── moveit_controllers.yaml    # Controller action mapping
│   ├── joint_limits.yaml          # Velocity/acceleration limits
│   ├── pilz_industrial_motion_planner_planning_pipeline.yaml
│   └── my_6dof.rviz               # Pre-configured RViz layout
├── launch/
│   └── move_group.launch.py       # Launches the move_group node
└── test/
    └── ...                        # Launch tests
```

### Key Files Explained

**`my_6dof.srdf`** — Semantic Robot Description Format:
- Defines `<group>` elements (arm, gripper)
- Named poses (`home`, `ready`) with joint values
- End-effector declaration
- Allowed collision pairs (`<disable_collisions>`)

**`kinematics.yaml`**:
```yaml
arm:
  kinematics_solver: kdl_kinematics_plugin/KDLKinematicsPlugin
  kinematics_solver_timeout: 0.005
  kinematics_solver_attempts: 3
```

**`moveit_controllers.yaml`** — bridges MoveIt2 → ros2_control:
```yaml
moveit_controller_manager: moveit_ros_control_interface::MoveItControllerManager
moveit_simple_controller_manager:
  controller_names:
    - arm_controller
    - gripper_controller
  arm_controller:
    type: FollowJointTrajectory
    joints: [joint1, joint2, joint3, joint4, joint5, joint6]
  gripper_controller:
    type: GripperCommand
    joints: [gripper_joint]
```

---

## `my_6dof_controllers`

**Role:** ros2_control controller configuration and spawner launch.

```
my_6dof_controllers/
├── CMakeLists.txt
├── package.xml
├── config/
│   └── ros2_controllers.yaml     # Controller definitions
└── launch/
    └── spawn_controllers.launch.py
```

**`ros2_controllers.yaml`** structure:
```yaml
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz

    arm_controller:
      type: joint_trajectory_controller/JointTrajectoryController

    gripper_controller:
      type: gripper_action_controller/GripperActionController

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

arm_controller:
  ros__parameters:
    joints:
      - joint1
      - joint2
      - joint3
      - joint4
      - joint5
      - joint6
    command_interfaces: [position]
    state_interfaces: [position, velocity]
```

---

## `my_6dof_gazebo`

**Role:** Gazebo Harmonic simulation environment.

```
my_6dof_gazebo/
├── CMakeLists.txt
├── package.xml
├── worlds/
│   └── my_6dof_world.sdf         # Gazebo world file
└── launch/
    └── spawn_robot.launch.py      # Spawns robot into Gazebo
```

The `spawn_robot.launch.py` does:
1. Converts URDF → SDF (via `gz sdf`)
2. Calls `gz service -s /world/my_6dof_world/create` to spawn the robot
3. Starts `gz_ros2_control` hardware plugin

---

## `my_6dof_bringup`

**Role:** Top-level entry point — orchestrates all packages.

```
my_6dof_bringup/
├── CMakeLists.txt
├── package.xml
├── launch/
│   ├── rviz_only.launch.py        # Robot display only
│   ├── demo.launch.py             # MoveIt2 (fake hardware)
│   └── gazebo_moveit.launch.py    # Full simulation stack
└── scripts/
    └── pick_and_place.py          # Python manipulation demo
```

| Launch File | Nodes Started |
|------------|---------------|
| `rviz_only` | `robot_state_publisher`, `joint_state_publisher_gui`, `rviz2` |
| `demo` | Above + `move_group`, `arm_controller` (fake) |
| `gazebo_moveit` | All above + `gz_sim`, `gz_ros2_control`, real controllers |

---

## `panda_ign_moveit2`

**Role:** Reference implementation using the Franka Panda robot.

```
panda_ign_moveit2/
├── panda_description/
│   ├── urdf/                      # Official Panda URDF
│   └── meshes/                    # STL mesh files
└── panda_moveit_config/
    ├── config/
    │   ├── panda.srdf
    │   ├── kinematics.yaml
    │   └── ompl_planning.yaml
    └── launch/
```

**Why include the Panda?** It's the MoveIt2 reference robot. Comparing your `my_6dof` config to the Panda config helps students:
- Understand SRDF structure for a real robot
- See how planning groups are defined for 7-DOF vs 6-DOF
- Learn how gripper mimic joints are configured

---

## Dependency Packages (`src/deps/`)

> [!NOTE]
> These are vendored (source-built) dependencies. They are **not tracked in git** — they are fetched via `vcs import` from `.repos` files or `rosdep`.

| Package | Purpose |
|---------|---------|
| `gz_ros2_control` | Bridge between Gazebo physics and ros2_control |
| `moveit_servo` | Real-time Cartesian jogging (servo control) |
| `ros2_control` | Hardware abstraction layer framework |
| `ros2_controllers` | Standard controller implementations |
| `visualization` (rviz_visual_tools) | Marker visualisation helpers |
| `robot_interaction` | RViz interactive marker manipulation |

---

## See Also

- [Architecture Diagram](./architecture.md)
- [Getting Started](./getting_started.md)
- [Motion Planning Guide](./motion_planning.md)
