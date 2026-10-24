# Screenshots

This directory is the home for all workspace screenshots and demo recordings.

Add screenshots here and reference them in the main `README.md` or other docs using relative paths:
```markdown
![Motion Planning Panel](./screenshots/rviz_motion_planning.png)
```

---

## Recommended Screenshots to Capture

### 1. RViz with Robot Model and Motion Planning Panel
**File:** `screenshots/rviz_overview.png`

**How to capture:**
1. Run `ros2 launch my_6dof_bringup rviz_only.launch.py`
2. Ensure the robot model is visible and coloured correctly
3. Open the Motion Planning panel (Panels menu → Motion Planning)
4. Take a full-window screenshot

**What to show:** The complete RViz window with the robot model centred, Motion Planning panel on the left, and the 3D viewport showing the robot from a 3/4 angle.

---

### 2. Planning Scene with Collision Objects
**File:** `screenshots/planning_scene_collision.png`

**How to capture:**
1. Run `ros2 launch my_6dof_bringup demo.launch.py`
2. Add a collision object (box/cylinder) via the `PlanningSceneInterface` or RViz panel
3. Screenshot showing the collision object (typically green) next to the robot

**What to show:** Robot arm with a visible collision box in the scene, showing how MoveIt2 avoids obstacles.

---

### 3. Robot in "Home" vs "Ready" Pose
**File:** `screenshots/home_pose.png` and `screenshots/ready_pose.png`

**How to capture:**
1. Run demo, set goal to `home` → Plan & Execute → screenshot
2. Set goal to `ready` → Plan & Execute → screenshot

**What to show:** Two side-by-side or separate images illustrating the two named joint configurations.

---

### 4. Motion Planning Trajectory Visualization
**File:** `screenshots/trajectory_viz.png`

**How to capture:**
1. Run `ros2 launch my_6dof_bringup demo.launch.py`
2. Set a reachable goal pose using the interactive marker
3. Click **Plan** (do not execute yet)
4. Screenshot showing the ghost/orange trajectory preview in RViz

**What to show:** The planned ghost trajectory (orange/translucent) overlaid on the current robot state (grey/opaque), illustrating the planned motion.

---

### 5. Gazebo Simulation View
**File:** `screenshots/gazebo_simulation.png`

**How to capture:**
1. Run `ros2 launch my_6dof_bringup gazebo_moveit.launch.py`
2. Wait for Gazebo to fully load (~30 s)
3. Take a screenshot of the Gazebo window with the robot visible

**What to show:** Gazebo Harmonic viewport with the 6-DOF arm and its environment, demonstrating the physics simulation.

---

### 6. Pick and Place Demo Sequence
**Files:** `screenshots/pick_approach.png`, `screenshots/pick_grasp.png`, `screenshots/pick_transport.png`, `screenshots/pick_place.png`

**How to capture:**
1. Run the full stack: `ros2 launch my_6dof_bringup gazebo_moveit.launch.py`
2. Run the demo: `ros2 run my_6dof_bringup pick_and_place.py`
3. Take screenshots at each major phase (approach, grasp, transport, place)

**What to show:** A sequence of 3–4 images walking through the pick and place stages, ideally in both RViz and Gazebo views.

---

## Naming Convention

Use descriptive, lowercase names with underscores:
```
rviz_overview.png
gazebo_simulation.png
trajectory_viz.png
home_pose.png
ready_pose.png
planning_scene_collision.png
pick_approach.png
pick_grasp.png
pick_transport.png
pick_place.png
```

## Recommended Tools

- **gnome-screenshot** — `gnome-screenshot -w` (active window)
- **Flameshot** — `flameshot gui` (area selection with annotation)
- **ImageMagick** — `import screenshot.png` (click to capture window)
- **Peek** — for GIF recordings of demo sequences

## Image Guidelines

- Format: PNG preferred (lossless), JPEG acceptable for photos
- Resolution: at least 1280×720
- Keep file sizes reasonable — compress large PNGs with `optipng`
- GIFs/videos: upload to YouTube or Imgur and embed as links in the README
