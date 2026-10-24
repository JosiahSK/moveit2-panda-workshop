import os
import yaml
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
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
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    pkg_description = FindPackageShare('my_6dof_description')
    pkg_moveit_config = FindPackageShare('my_6dof_moveit_config')

    # Robot Description (URDF)
    xacro_file = PathJoinSubstitution([pkg_description, 'urdf', 'my_6dof.urdf.xacro'])
    robot_description_config = ParameterValue(Command(['xacro ', xacro_file, ' use_mock:=true']), value_type=str)
    robot_description = {'robot_description': robot_description_config}

    # Robot Description Semantic (SRDF)
    srdf_content = load_file('my_6dof_moveit_config', 'config/my_6dof.srdf')
    robot_description_semantic = {'robot_description_semantic': srdf_content}

    # Kinematics YAML
    kinematics_yaml = load_yaml('my_6dof_moveit_config', 'config/kinematics.yaml')
    robot_description_kinematics = {'robot_description_kinematics': kinematics_yaml}

    # Joint limits YAML
    joint_limits_yaml = load_yaml('my_6dof_moveit_config', 'config/joint_limits.yaml')
    robot_description_planning = {'robot_description_planning': joint_limits_yaml}

    # Planning Pipeline Configuration (OMPL)
    ompl_planning_yaml = load_yaml('my_6dof_moveit_config', 'config/ompl_planning.yaml')
    ompl_config = {
        'planning_pipelines': ['ompl'],
        'default_planning_pipeline': 'ompl',
        'ompl': ompl_planning_yaml
    }

    # MoveIt Controllers Configuration
    moveit_controllers = load_yaml('my_6dof_moveit_config', 'config/moveit_controllers.yaml')

    # Trajectory Execution parameters
    trajectory_execution = {
        'moveit_manage_controllers': True,
        'trajectory_execution.allowed_execution_duration_scaling': 1.2,
        'trajectory_execution.allowed_goal_duration_margin': 0.5,
        'trajectory_execution.allowed_start_tolerance': 0.01,
    }

    # Planning Scene Monitor parameters
    planning_scene_monitor = {
        'publish_planning_scene': True,
        'publish_geometry_updates': True,
        'publish_state_updates': True,
        'publish_transforms_updates': True,
    }

    # Move Group Node
    move_group_node = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        parameters=[
            robot_description,
            robot_description_semantic,
            robot_description_kinematics,
            robot_description_planning,
            ompl_config,
            moveit_controllers,
            trajectory_execution,
            planning_scene_monitor,
            {'use_sim_time': use_sim_time}
        ]
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false', description='Use simulation time'),
        move_group_node
    ])
