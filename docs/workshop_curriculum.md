# 🎓 MoveIt 2 & Robot Manipulation Workshop Curriculum

> **Course Level:** Undergraduate / Graduate Robotics or Hands-on Workshop  
> **Duration:** 1 Day (6 Hours) or 5-Week Lab Module  
> **Target Platforms:** ROS 2 Jazzy (Ubuntu 24.04) / ROS 2 Humble (Ubuntu 22.04)

---

## 📅 Workshop Schedule Overview

| Time | Session | Hands-on Lab | Topics Covered |
|------|---------|--------------|----------------|
| **09:00 - 10:00** | Module 1: Introduction | [Lab 1: RViz Jogging](exercises/lab1_rviz_jogging.md) | URDF / Xacro, Joints, Links, Kinematic Chains, TF Tree |
| **10:00 - 11:30** | Module 2: MoveIt 2 Architecture | [Lab 2: OMPL Planners](exercises/lab2_ompl_planners.md) | `move_group`, SRDF, KDL IK solver, OMPL (RRTConnect vs RRT*) |
| **11:30 - 12:30** | Module 3: Environment & Obstacles | [Lab 3: Collision Avoidance](exercises/lab3_collision_avoidance.md) | Planning Scene Monitor, Collision Matrix (ACM), Dynamic obstacles |
| **12:30 - 13:30** | *Lunch Break* | — | — |
| **13:30 - 14:45** | Module 4: Trajectory & Grippers | [Lab 4: Cartesian & Gripper](exercises/lab4_cartesian_and_gripper.md) | Cartesian paths, Singularity avoidance, Gripper actions |
| **14:45 - 16:00** | Module 5: Physics Simulation | [Lab 5: Gazebo Pick-and-Place](exercises/lab5_gazebo_simulation.md) | `ros2_control`, Gazebo simulation, Full pick-and-place loop |
| **16:00 - 16:30** | Wrap-up & Q&A | Mini-project presentation | Optimization, real hardware deployment considerations |

---

## 🎒 Student Prerequisites
Students should have basic familiarity with:
1. Linux command line (bash, environment variables)
2. Basic ROS 2 concepts (Nodes, Topics, Actions, Launch files)
3. Basic Python or C++ syntax

---

## 📊 Evaluation & Grading Rubric
- **Lab 1-3 Checkpoints:** 30% (Proper pose definitions & collision understanding)
- **Lab 4 Implementation:** 30% (Smooth Cartesian path generation)
- **Lab 5 Pick-and-Place Demo:** 40% (Successful simulated object transfer without collisions)
