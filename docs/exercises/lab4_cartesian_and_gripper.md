# Lab 4: Cartesian Paths & Gripper Manipulation

## 🎯 Learning Objectives
- Differentiate between Free-space (Joint-space) Planning and Cartesian Straight-Line Planning
- Understand End-Effector Waypoints and interpolation steps
- Control gripper open/close actions using `FollowJointTrajectory` or named states
- Avoid kinematic singularities during Cartesian moves

---

## 📐 Joint-Space vs. Cartesian-Space Planning

```
Joint-Space Motion (Free-space):
  End-effector follows curved, non-linear path in 3D space.
  Fast, avoids joint limits, easy for sampling-based planners.

Cartesian-Space Motion:
  End-effector follows strict straight lines in X, Y, Z.
  Required for inserting peg in hole, wiping surfaces, approach/retreat during picking.
```

---

## 🛠️ Experiment: Modifying Approach / Retreat in Code
Open [`src/my_6dof_bringup/scripts/pick_and_place.py`](../../src/my_6dof_bringup/scripts/pick_and_place.py):
1. Locate the approach waypoints:
   - Pre-grasp pose: `[x=0.45, y=0.0, z=0.55]`
   - Grasp pose: `[x=0.45, y=0.0, z=0.42]` (straight downward linear approach)
2. Notice the Gripper action commands:
   - Open: position `0.04` (40mm finger gap)
   - Close: position `0.0` (gripping object)
3. Modify the approach velocity scaling:
   ```python
   # Slow down approach for precision:
   trajectory.points[i].time_from_start = ...
   ```
