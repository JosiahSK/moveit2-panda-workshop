import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    """Top-level convenience launcher for MoveIt 2 demo mode (Mock Hardware + RViz)."""
    pkg_moveit_config = FindPackageShare('my_6dof_moveit_config')

    demo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([pkg_moveit_config, 'launch', 'demo.launch.py'])
        )
    )

    return LaunchDescription([
        demo_launch
    ])
