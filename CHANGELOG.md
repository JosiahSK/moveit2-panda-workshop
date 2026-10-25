# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2026-10-25

### Added
- Complete 6-DOF robot description with xacro macros and realistic inertial calculations.
- Parallel two-finger gripper model with mimic joint constraints.
- MoveIt 2 configuration package featuring KDL kinematics plugin, OMPL planning pipeline, and pre-configured collision matrix.
- `ros2_control` integration with `JointTrajectoryController` for arm and `GripperActionController` for the end effector.
- Gazebo simulation worlds and entity spawner (`gz_ros2_control` for Jazzy, `ign_ros2_control` for Humble).
- Top-level unified bringup launch files: `rviz_only.launch.py`, `demo.launch.py`, `gazebo_moveit.launch.py`.
- Automated Python Pick-and-Place demonstration node (`pick_and_place.py`).
- Comprehensive student documentation suite including architecture graphs, OMPL planner comparisons, and 5 interactive lab modules.
- Multi-distro branch support: `jazzy` (default) and `humble`.
- Dockerfile, Docker Compose GUI forwarding configuration, and automated GitHub Actions CI.
