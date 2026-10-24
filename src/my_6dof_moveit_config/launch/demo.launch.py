import os
import yaml
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
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
    pkg_moveit_config = FindPackageShare('my_6dof_moveit_config')
    pkg_controllers = FindPackageShare('my_6dof_controllers')

    # Robot state publisher with mock components
    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([pkg_description, 'launch', 'rsp.launch.py'])
        ),
        launch_arguments=[('use_sim_time', 'false'), ('use_mock', 'true')]
    )

    # Controller manager for mock hardware
    ros2_controllers_yaml = PathJoinSubstitution([pkg_controllers, 'config', 'ros2_controllers.yaml'])

    robot_description_config = ParameterValue(
        Command(['xacro ', PathJoinSubstitution([pkg_description, 'urdf', 'my_6dof.urdf.xacro']), ' use_mock:=true']),
        value_type=str
    )

    # Spawn mock ros2_control node
    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            {'robot_description': robot_description_config},
            ros2_controllers_yaml
        ],
        output='screen'
    )

    # Controller spawners
    spawners_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([pkg_controllers, 'launch', 'spawners.launch.py'])
        )
    )

    # MoveGroup launch
    move_group_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([pkg_moveit_config, 'launch', 'move_group.launch.py'])
        ),
        launch_arguments=[('use_sim_time', 'false')]
    )

    # RViz with MoveIt config
    rviz_config_file = PathJoinSubstitution([pkg_moveit_config, 'config', 'moveit.rviz'])

    srdf_content = load_file('my_6dof_moveit_config', 'config/my_6dof.srdf')
    kinematics_yaml = load_yaml('my_6dof_moveit_config', 'config/kinematics.yaml')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file],
        parameters=[
            {'robot_description': robot_description_config},
            {'robot_description_semantic': srdf_content},
            {'robot_description_kinematics': kinematics_yaml}
        ]
    )

    return LaunchDescription([
        rsp_launch,
        control_node,
        spawners_launch,
        move_group_launch,
        rviz_node
    ])
