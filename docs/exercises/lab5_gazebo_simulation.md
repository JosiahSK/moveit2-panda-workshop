# Lab 5: Full Stack Gazebo Simulation & Pick-and-Place

## 🎯 Learning Objectives
- Run complete closed-loop physics simulation in Gazebo
- Understand `ros2_control` hardware abstraction layer (`gz_ros2_control` / `ign_ros2_control`)
- Monitor `joint_states` and controller execution in real-time
- Execute end-to-end automated Pick-and-Place routine

---

## 🛠️ Step 1: Launch Full Gazebo + MoveIt Stack
In your terminal:
```bash
source install/setup.bash
ros2 launch my_6dof_bringup gazebo_moveit.launch.py
```
*Allow 15-20 seconds for the Gazebo world and controller managers to initialize.*

## 🔍 Step 2: Verify Active ros2_control Controllers
In a second terminal, verify that controllers are active:
```bash
ros2 control list_controllers
```
You should see:
```text
joint_state_broadcaster[joint_state_broadcaster/JointStateBroadcaster] active
arm_controller         [joint_trajectory_controller/JointTrajectoryController] active
gripper_controller     [joint_trajectory_controller/JointTrajectoryController] active
```

## 🚀 Step 3: Run Automated Pick-and-Place
In a third terminal:
```bash
source install/setup.bash
ros2 run my_6dof_bringup pick_and_place.py
```

Observe the sequence:
1. Scene objects (Table and Target Box) are added to the planning scene.
2. Arm moves to Home pose.
3. Gripper opens.
4. Arm executes Cartesian approach down to the target object.
5. Gripper closes to grasp.
6. Arm retreats vertically upwards.
7. Arm transfers object across to the place location.
8. Gripper releases object.
9. Arm returns safely to Home pose.

---

## 🏆 Student Challenge
Modify `pick_and_place.py` to change the place target to `y = 0.3` instead of `y = -0.3`.
Re-run and verify the robot computes a smooth collision-free transit across the opposite side!
