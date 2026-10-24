# System Architecture

This document describes the software architecture of the **my_6dof** MoveIt2 robot workspace. Understanding how the components connect will help you debug, extend, and tune the system.

---

## High-Level Architecture

```mermaid
flowchart TD
    User["👤 User / Python Script"]

    subgraph RViz["RViz2"]
        MP["Motion Planning Panel\n(moveit_ros_visualization)"]
        RobotModel["Robot Model\ndisplay"]
        PlanningScene["Planning Scene\ndisplay"]
    end

    subgraph MoveGroup["move_group node"]
        PlanReq["Planning Request\nHandler"]
        OMPL["OMPL Planning Pipeline\nompl_interface"]
        KDL["KDL Kinematics Plugin\nkdl_kinematics_plugin"]
        PScene["Planning Scene\nMonitor"]
        TrajExec["Trajectory\nExecution Manager"]
    end

    subgraph Ctrl["ros2_control"]
        CM["Controller Manager"]
        JTC["JointTrajectoryController"]
        GripCtrl["GripperActionController"]
    end

    subgraph Sim["Gazebo Harmonic (gz-sim8)"]
        World["Robot World\n(my_6dof_world.sdf)"]
        GzCtrl["gz_ros2_control\nplugin"]
    end

    User -->|"MoveGroupInterface API\nor RViz interactive\nmarkers"| MP
    MP -->|"MoveGroup Action /move_action"| PlanReq
    PlanReq --> OMPL
    OMPL -->|"IK queries"| KDL
    OMPL -->|"Collision checking"| PScene
    PlanReq -->|"Planned trajectory"| TrajExec
    TrajExec -->|"FollowJointTrajectory\nAction"| CM
    CM --> JTC
    CM --> GripCtrl
    JTC -->|"joint commands"| GzCtrl
    GzCtrl --> World
    World -->|"joint states"| CM
    CM -->|"/joint_states"| PScene
    PScene -->|"TF + joint states"| RobotModel
    PScene -->|"collision objects"| PlanningScene
```

---

## Component Details

### 1. `my_6dof_description`
Provides the **URDF/Xacro robot model**:
- 6 revolute joints (arm)
- 1 gripper with 2 mimic finger joints
- Inertia tensors for each link
- Visual meshes + collision geometry
- `<ros2_control>` hardware interface tags (for simulation)

### 2. `my_6dof_moveit_config`
Houses all **MoveIt2 configuration** files:
| File | Purpose |
|------|---------|
| `config/my_6dof.srdf` | Semantic robot description (planning groups, poses, collisions) |
| `config/kinematics.yaml` | KDL solver parameters (timeout, attempts) |
| `config/ompl_planning.yaml` | OMPL planner configuration and defaults |
| `config/moveit_controllers.yaml` | Maps MoveIt trajectories → ros2_control actions |
| `config/joint_limits.yaml` | Velocity/acceleration limits per joint |
| `config/my_6dof.rviz` | Pre-configured RViz2 layout |

### 3. `my_6dof_controllers`
Defines **ros2_control** controller configurations:
- `ros2_controllers.yaml` — JointTrajectoryController for the arm + GripperActionController
- Spawner launch file that activates controllers after robot_state_publisher starts

### 4. `my_6dof_gazebo`
Provides the **simulation environment**:
- Gazebo Harmonic (gz-sim8) SDF world
- Entity spawner (launches the robot into the world from URDF)
- Bridge configuration between Gazebo topics ↔ ROS 2 topics

### 5. `my_6dof_bringup`
**Top-level launch orchestration** — the entry point for users:
| Launch File | What it starts |
|-------------|---------------|
| `rviz_only.launch.py` | Robot state publisher + RViz2 (no simulation) |
| `demo.launch.py` | RViz2 + MoveIt2 move_group (no Gazebo) |
| `gazebo_moveit.launch.py` | Full stack: Gazebo + MoveIt2 + RViz2 |

Also contains `scripts/pick_and_place.py` — a Python demo using `MoveGroupInterface`.

### 6. `panda_ign_moveit2`
**Franka Panda** reference packages:
- `panda_description` — official Panda URDF/meshes
- `panda_moveit_config` — Panda MoveIt2 SRDF + configs

These serve as a reference for students comparing their custom arm to the Panda.

---

## Data Flow: Planning a Motion

```mermaid
sequenceDiagram
    participant U as User/Script
    participant MG as move_group
    participant OMPL as OMPL Planner
    participant KDL as KDL IK
    participant JTC as JointTrajectoryController
    participant SIM as Gazebo

    U->>MG: setPoseTarget(goal_pose)
    U->>MG: plan()
    MG->>OMPL: PlanningRequest (start + goal)
    OMPL->>KDL: computeIK(goal_pose)
    KDL-->>OMPL: joint angles
    loop RRT/RRTConnect sampling
        OMPL->>OMPL: sample + collision check
    end
    OMPL-->>MG: RobotTrajectory
    U->>MG: execute()
    MG->>JTC: FollowJointTrajectory (action)
    JTC->>SIM: joint position commands
    SIM-->>JTC: joint state feedback
    JTC-->>MG: Result (SUCCEEDED)
    MG-->>U: MoveItErrorCode::SUCCESS
```

---

## Key ROS 2 Topics & Actions

| Name | Type | Description |
|------|------|-------------|
| `/joint_states` | `sensor_msgs/JointState` | Current joint positions from controller |
| `/move_group/goal` | `moveit_msgs/MoveGroupAction` | Motion planning requests |
| `/arm_controller/follow_joint_trajectory` | `control_msgs/FollowJointTrajectoryAction` | Trajectory execution |
| `/gripper_controller/gripper_cmd` | `control_msgs/GripperCommandAction` | Gripper open/close |
| `/planning_scene` | `moveit_msgs/PlanningScene` | Collision environment |
| `/tf` | `tf2_msgs/TFMessage` | Robot transforms |

---

## See Also

- [Getting Started](./getting_started.md)
- [Motion Planning Concepts](./motion_planning.md)
- [Pick & Place Demo](./pick_and_place.md)
