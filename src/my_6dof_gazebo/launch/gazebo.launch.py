import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_gazebo_share = get_package_share_directory('my_6dof_gazebo')
    pkg_description = FindPackageShare('my_6dof_description')
    pkg_ros_gz_sim = FindPackageShare('ros_gz_sim')

    world_path = os.path.join(pkg_gazebo_share, 'worlds', 'empty_world.sdf')
    gz_args = f"-r -v 2 {world_path}"

    # Start Gazebo sim server and client
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'])
        ),
        launch_arguments=[('gz_args', gz_args)]
    )

    # Robot State Publisher (with simulation hardware interface)
    rsp_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([pkg_description, 'launch', 'rsp.launch.py'])
        ),
        launch_arguments=[('use_sim_time', 'true'), ('use_mock', 'false')]
    )

    # Spawn Robot Entity in Gazebo
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', '/robot_description', '-name', 'my_6dof', '-z', '0.0'],
        output='screen'
    )

    # ROS-GZ Bridge for Clock
    gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )

    return LaunchDescription([
        gz_sim,
        rsp_launch,
        spawn_robot,
        gz_bridge
    ])
