# Lab 2: MoveIt 2 Motion Planning & OMPL Planners

## 🎯 Learning Objectives
- Interact with the MoveIt 2 Motion Planning Plugin in RViz2
- Understand Start State vs Goal State
- Compare different OMPL algorithms (`RRTConnect`, `RRT*`, `KPIECE`, `PRM`)
- Analyze planning time, trajectory path length, and smoothness

---

## 🛠️ Step 1: Launch MoveIt Demo Mode
```bash
source install/setup.bash
ros2 launch my_6dof_bringup demo.launch.py
```

## 🔍 Step 2: Plan to Named Poses
1. In the **MotionPlanning** panel, navigate to the **Planning** tab.
2. Under **Query**:
   - Set **Planning Group**: `arm`
   - Set **Start State**: `<current>`
   - Set **Goal State**: Select named state `ready`
3. Click the **Plan** button.
4. Watch the translucent orange ghost arm demonstrate the planned path.
5. Click **Execute** to move the mock robot to the `ready` configuration.

## 🧪 Step 3: Planner Comparison Experiment
Test planning between random valid poses using different OMPL planners:

| Planner | Algorithm Type | Typical Plan Time | Path Smoothness | Optimality Guarantee |
|---------|---------------|-------------------|-----------------|----------------------|
| **RRTConnect** | Bi-directional tree | Fast (< 0.05s) | Moderate (jagged) | Feasible only |
| **RRT\*** | Asymptotically optimal tree | Slower (0.5 - 2s) | High (shorter) | Asymptotically optimal |
| **KPIECE** | Projection-based | Fast (< 0.1s) | Moderate | Feasible only |
| **PRM** | Roadmap pre-computation | Multi-query fast | High | Probabilistically complete |

### Experiment Task:
1. In the **Planning** tab, open **Context** -> **Planner** dropdown.
2. Select `RRTConnectkConfigDefault`. Plan 5 times, record average planning time in terminal logs.
3. Switch to `RRTstarkConfigDefault`. Set **Planning Time** to `5.0` seconds. Observe how the path refines and straightens as time progresses.
