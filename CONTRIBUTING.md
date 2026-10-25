# Contributing Guidelines

Thank you for your interest in improving the **MoveIt 2 & 6-DOF Robot Workshop**! We welcome contributions from students, instructors, and robotics enthusiasts.

---

## 🛠️ How to Contribute

### 1. Reporting Bugs
- Search existing issues to ensure the bug hasn't been reported.
- Open a new issue using our [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md).
- Include terminal logs, ROS 2 distribution (`humble` or `jazzy`), and steps to reproduce.

### 2. Suggesting Enhancements or Lab Exercises
- Open an issue describing the proposed lab exercise, planner comparison, or new robot model.
- Detail how this enhances student understanding of MoveIt 2 concepts.

### 3. Pull Request Guidelines
1. Fork the repository and create a descriptive feature branch:
   ```bash
   git checkout -b feat/add-trajectory-analysis
   ```
2. Adhere to ROS 2 code formatting standards:
   - Python: PEP 8 formatting (`flake8`, `black`)
   - C++: ROS 2 / Google style (`ament_clang_format`)
3. Test your changes locally before submitting:
   ```bash
   colcon build --symlink-install
   colcon test
   ```
4. Target PRs against the appropriate branch:
   - Target `jazzy` for Jazzy-specific or general improvements.
   - Target `humble` for Humble-specific fixes.
