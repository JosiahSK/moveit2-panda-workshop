# Lab 3: Planning Scene & Collision Avoidance

## 🎯 Learning Objectives
- Learn how MoveIt 2's `PlanningSceneMonitor` manages the environment
- Publish static and dynamic collision objects into the planning scene
- Observe how OMPL paths automatically warp around obstacles
- Understand self-collision matrix (ACM) generated from SRDF

---

## 🛠️ Step 1: Launch MoveIt Demo
```bash
source install/setup.bash
ros2 launch my_6dof_bringup demo.launch.py
```

## 🔍 Step 2: Add Obstacles via RViz Scene Objects Tab
1. Select the **Scene Objects** tab in the MotionPlanning panel.
2. In the shape dropdown, choose **Box**.
3. Set dimensions: `X=0.2, Y=0.2, Z=0.5`.
4. Position the box at `X=0.4, Y=0.0, Z=0.25` (right in front of the arm's reach).
5. Click **Publish Scene**. The green obstacle appears in the 3D view.

## 🧪 Step 3: Test Obstacle Avoidance
1. Set Start State to `home` and Goal State to a pose behind the obstacle.
2. Click **Plan**.
3. Notice how OMPL generates a trajectory that arches **above** or swings **around** the obstacle.
4. Try moving the obstacle closer until no collision-free path exists; observe MoveIt reporting `PLANNING_FAILED: Timed out without finding a valid solution`.

## 💻 Step 4: Python Scripting Challenge
Try using the Python API or MoveGroup action client to add an obstacle programmatically. Refer to the helper function inside [`pick_and_place.py`](../../src/my_6dof_bringup/scripts/pick_and_place.py#L42):
```python
table = CollisionObject()
table.header.frame_id = 'world'
table.id = 'obstacle_box'
# Add primitive and pose ...
```
