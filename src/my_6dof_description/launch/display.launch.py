import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_description = FindPackageShare('my_6dof_description')

    rviz_config_file = PathJoinSubstitution([pkg_description, 'config', 'view_robot.rviz'])

    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([pkg_description, '/launch/rsp.launch.py']),
        launch_arguments={'use_sim_time': 'false', 'use_mock': 'true'}.items()
    )

    jsp_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        rsp_launch,
        jsp_gui_node,
        rviz_node
    ])
