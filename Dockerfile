# Multi-arch ready Dockerfile for MoveIt 2 & Gazebo Workshop
ARG ROS_DISTRO=jazzy
FROM osrf/ros:${ROS_DISTRO}-desktop-full

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-c"]

# Install build tools & essential utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-pip \
    ros-${ROS_DISTRO}-moveit \
    ros-${ROS_DISTRO}-moveit-ros-visualization \
    ros-${ROS_DISTRO}-ros2-control \
    ros-${ROS_DISTRO}-ros2-controllers \
    ros-${ROS_DISTRO}-joint-state-publisher-gui \
    && rm -rf /var/lib/apt/lists/*

# Initialize rosdep
RUN rosdep update || true

# Setup workshop workspace
WORKDIR /root/moveit2_ws
COPY . /root/moveit2_ws/

# Install package dependencies
RUN rosdep install --from-paths src --ignore-src -y -r --rosdistro ${ROS_DISTRO} || true

# Build workspace
RUN source /opt/ros/${ROS_DISTRO}/setup.bash && \
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

# Setup entrypoint environment
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /root/.bashrc && \
    echo "source /root/moveit2_ws/install/setup.bash" >> /root/.bashrc

CMD ["bash"]
