# Lab 1: RViz Jogging & Forward Kinematics

## 🎯 Learning Objectives
- Inspect the Robot Description (URDF / Xacro) in RViz2
- Understand Link-Joint coordinate frames and TF tree
- Jog joints manually using `joint_state_publisher_gui`
- Learn how Forward Kinematics determines end-effector position

---

## 🛠️ Step 1: Launch RViz Only
```bash
source install/setup.bash
ros2 launch my_6dof_bringup rviz_only.launch.py
```

## 🔍 Step 2: TF & Coordinate Inspection
1. In RViz's **Displays** panel on the left, check the **TF** checkbox.
2. Notice the frame names:
   - `world` -> `base_link` -> `shoulder_link` -> `upper_arm_link` -> `forearm_link` -> `wrist_1_link` -> `wrist_2_link` -> `wrist_3_link` -> `tool0` -> `gripper`
3. Notice how each joint's rotation alters all child frames downstream.

## 🧪 Step 3: Interactive Challenge
In the Joint State Publisher GUI window:
- Move slider `joint1` from `0` to `1.57` rad (90°). Observe base rotation.
- Move slider `joint2` and `joint3`. Observe the arm reaching forward or upward.
- Move slider `gripper_joint`. Notice both `left_finger` and `right_finger` moving symmetrically.

## 📝 Checkpoint Questions
1. What type of joint is `joint1` through `joint6`? (Hint: revolute vs prismatic)
2. What frame serves as the parent of `tool0`?
3. What is the physical unit of the sliders in `joint_state_publisher_gui`?
