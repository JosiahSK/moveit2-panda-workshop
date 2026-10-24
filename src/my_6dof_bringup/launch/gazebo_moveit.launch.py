import os
import yaml
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

def load_yaml(package_name, file_path):
    pkg_share = FindPackageShare(package_name).find(package_name)
    full_path = os.path.join(pkg_share, file_path)
    try:
        with open(full_path, 'r') as file:
            return yaml.safe_load(file)
    except EnvironmentError:
        return None

def load_file(package_name, file_path):
    pkg_share = FindPackageShare(package_name).find(package_name)
    full_path = os.path.join(pkg_share, file_path)
    try:
        with open(full_path, 'r') as file:
            return file.read()
    except EnvironmentError:
        return None

def generate_launch_description():
    pkg_description = FindPackageShare('my_6dof_description')
    pkg_gazebo = FindPackageShare('my_6dof_gazebo')
    pkg_controllers = FindPackageShare('my_6dof_controllers')
    pkg_moveit_config = FindPackageShare('my_6dof_moveit_config')

    # 1. Gazebo Harmonic Simulation launch
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([pkg_gazebo, 'launch', 'gazebo.launch.py'])
        )
    )

    # 2. Spawners for ros2_control (delayed to ensure Gazebo gz_ros2_control plugin is initialized)
    spawners_launch = TimerAction(
        period=3.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([pkg_controllers, 'launch', 'spawners.launch.py'])
                )
            )
        ]
    )

    # 3. MoveGroup launch with simulation time
    move_group_launch = TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    PathJoinSubstitution([pkg_moveit_config, 'launch', 'move_group.launch.py'])
                ),
                launch_arguments=[('use_sim_time', 'true')]
            )
        ]
    )

    # 4. RViz Node with MoveIt MotionPlanning plugin
    rviz_config_file = PathJoinSubstitution([pkg_moveit_config, 'config', 'moveit.rviz'])
    srdf_content = load_file('my_6dof_moveit_config', 'config/my_6dof.srdf')
    kinematics_yaml = load_yaml('my_6dof_moveit_config', 'config/kinematics.yaml')

    xacro_file = PathJoinSubstitution([pkg_description, 'urdf', 'my_6dof.urdf.xacro'])
    robot_description_config = ParameterValue(
        Command(['xacro ', xacro_file, ' use_mock:=false']),
        value_type=str
    )

    rviz_node = TimerAction(
        period=6.0,
        actions=[
            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                output='screen',
                arguments=['-d', rviz_config_file],
                parameters=[
                    {'robot_description': robot_description_config},
                    {'robot_description_semantic': srdf_content},
                    {'robot_description_kinematics': kinematics_yaml},
                    {'use_sim_time': True}
                ]
            )
        ]
    )

    return LaunchDescription([
        gazebo_launch,
        spawners_launch,
        move_group_launch,
        rviz_node
    ])
