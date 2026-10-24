#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import Pose, PoseStamped
from shape_msgs.msg import SolidPrimitive
from moveit_msgs.msg import (
    PlanningScene,
    CollisionObject,
    AttachedCollisionObject,
    Constraints,
    JointConstraint,
    PositionConstraint,
    OrientationConstraint,
    BoundingVolume
)
from moveit_msgs.action import MoveGroup
from moveit_msgs.srv import ApplyPlanningScene
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from control_msgs.action import FollowJointTrajectory

class PickAndPlaceDemo(Node):
    def __init__(self):
        super().__init__('pick_and_place_demo')
        self.get_logger().info('Initializing 6-DOF Pick and Place Demo Node...')

        # Publishers & Service Clients
        self.scene_pub = self.create_publisher(PlanningScene, '/planning_scene', 10)
        self.apply_scene_client = self.create_client(ApplyPlanningScene, '/apply_planning_scene')

        # Action clients for MoveGroup and Controllers
        self.move_group_client = ActionClient(self, MoveGroup, '/move_action')
        self.arm_action_client = ActionClient(self, FollowJointTrajectory, '/arm_controller/follow_joint_trajectory')
        self.gripper_action_client = ActionClient(self, FollowJointTrajectory, '/gripper_controller/follow_joint_trajectory')

        # Wait for services/actions
        self.get_logger().info('Waiting for MoveGroup action server...')
        self.move_group_client.wait_for_server()
        self.get_logger().info('Connected to MoveGroup action server!')

    def add_collision_objects(self):
        """Adds table and cube objects to the MoveIt planning scene."""
        scene_msg = PlanningScene()
        scene_msg.is_diff = True

        # 1. Table
        table = CollisionObject()
        table.header.frame_id = 'world'
        table.id = 'table'
        table.operation = CollisionObject.ADD

        table_shape = SolidPrimitive()
        table_shape.type = SolidPrimitive.BOX
        table_shape.dimensions = [0.6, 0.8, 0.4]

        table_pose = Pose()
        table_pose.position.x = 0.5
        table_pose.position.y = 0.0
        table_pose.position.z = 0.2
        table_pose.orientation.w = 1.0

        table.primitives.append(table_shape)
        table.primitive_poses.append(table_pose)

        # 2. Target Cube
        cube = CollisionObject()
        cube.header.frame_id = 'world'
        cube.id = 'cube'
        cube.operation = CollisionObject.ADD

        cube_shape = SolidPrimitive()
        cube_shape.type = SolidPrimitive.BOX
        cube_shape.dimensions = [0.04, 0.04, 0.04]

        cube_pose = Pose()
        cube_pose.position.x = 0.45
        cube_pose.position.y = 0.0
        cube_pose.position.z = 0.42
        cube_pose.orientation.w = 1.0

        cube.primitives.append(cube_shape)
        cube.primitive_poses.append(cube_pose)

        scene_msg.world.collision_objects.append(table)
        scene_msg.world.collision_objects.append(cube)

        self.scene_pub.publish(scene_msg)
        self.get_logger().info('Published table and cube collision objects to planning scene.')

    def send_gripper_command(self, position):
        """Sends command to gripper trajectory controller."""
        if not self.gripper_action_client.wait_for_server(timeout_sec=2.0):
            self.get_logger().warn('Gripper action server not available. Skipping command.')
            return

        goal = FollowJointTrajectory.Goal()
        goal.trajectory.joint_names = ['gripper_joint']

        point = JointTrajectoryPoint()
        point.positions = [position]
        point.time_from_start.sec = 1
        goal.trajectory.points.append(point)

        self.gripper_action_client.send_goal_async(goal)
        time.sleep(1.5)

    def attach_object(self, object_id='cube'):
        """Attaches object to the gripper frame."""
        scene_msg = PlanningScene()
        scene_msg.is_diff = True

        attached_obj = AttachedCollisionObject()
        attached_obj.link_name = 'tool0'
        attached_obj.object.id = object_id
        attached_obj.object.operation = CollisionObject.ADD
        attached_obj.touch_links = ['gripper', 'left_finger', 'right_finger', 'tool0']

        scene_msg.robot_state.attached_collision_objects.append(attached_obj)
        self.scene_pub.publish(scene_msg)
        self.get_logger().info(f'Attached object {object_id} to tool0.')

    def detach_object(self, object_id='cube'):
        """Detaches object from gripper."""
        scene_msg = PlanningScene()
        scene_msg.is_diff = True

        attached_obj = AttachedCollisionObject()
        attached_obj.link_name = 'tool0'
        attached_obj.object.id = object_id
        attached_obj.object.operation = CollisionObject.REMOVE

        scene_msg.robot_state.attached_collision_objects.append(attached_obj)
        self.scene_pub.publish(scene_msg)
        self.get_logger().info(f'Detached object {object_id}.')

    def plan_and_move_to_joints(self, joint_values):
        """Plans and executes movement to target joint positions."""
        goal_msg = MoveGroup.Goal()
        goal_msg.request.group_name = 'arm'
        goal_msg.request.num_planning_attempts = 10
        goal_msg.request.allowed_planning_time = 5.0
        goal_msg.request.max_velocity_scaling_factor = 0.5
        goal_msg.request.max_acceleration_scaling_factor = 0.5

        joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        constraints = Constraints()

        for name, val in zip(joint_names, joint_values):
            jc = JointConstraint()
            jc.joint_name = name
            jc.position = val
            jc.tolerance_above = 0.01
            jc.tolerance_below = 0.01
            jc.weight = 1.0
            constraints.joint_constraints.append(jc)

        goal_msg.request.goal_constraints.append(constraints)

        self.get_logger().info(f'Planning motion to joint positions: {joint_values}')
        future = self.move_group_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected by MoveGroup!')
            return False

        res_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, res_future)
        result = res_future.result()

        if result.result.error_code.val == 1: # SUCCESS
            self.get_logger().info('Motion planning and execution succeeded!')
            return True
        else:
            self.get_logger().error(f'Motion failed with error code: {result.result.error_code.val}')
            return False

    def run_pick_and_place(self):
        self.add_collision_objects()
        time.sleep(1.0)

        # Step 1: Move to Ready / Approach Pose
        self.get_logger().info('Step 1: Moving to Ready Pose...')
        self.send_gripper_command(0.04) # Open gripper
        ready_joints = [0.0, -0.5, 1.0, -0.5, 0.0, 0.0]
        self.plan_and_move_to_joints(ready_joints)

        # Step 2: Approach Cube
        self.get_logger().info('Step 2: Approaching Pick Pose...')
        pick_approach_joints = [0.0, -0.7, 1.3, -0.6, 0.0, 0.0]
        self.plan_and_move_to_joints(pick_approach_joints)

        # Step 3: Close Gripper & Attach Cube
        self.get_logger().info('Step 3: Closing Gripper & Attaching Cube...')
        self.send_gripper_command(0.015)
        self.attach_object('cube')

        # Step 4: Retreat / Lift
        self.get_logger().info('Step 4: Retreating / Lifting Cube...')
        self.plan_and_move_to_joints(ready_joints)

        # Step 5: Move to Place Pose
        self.get_logger().info('Step 5: Moving to Place Pose...')
        place_approach_joints = [0.6, -0.7, 1.3, -0.6, 0.0, 0.0]
        self.plan_and_move_to_joints(place_approach_joints)

        # Step 6: Detach Cube & Open Gripper
        self.get_logger().info('Step 6: Opening Gripper & Detaching Cube...')
        self.send_gripper_command(0.04)
        self.detach_object('cube')

        # Step 7: Retreat to Ready Pose
        self.get_logger().info('Step 7: Returning to Home/Ready Pose...')
        self.plan_and_move_to_joints(ready_joints)

        self.get_logger().info('=== Pick and Place Demo Completed Successfully! ===')

def main(args=None):
    rclpy.init(args=args)
    demo_node = PickAndPlaceDemo()
    try:
        demo_node.run_pick_and_place()
    except Exception as e:
        demo_node.get_logger().error(f'Pick and Place Demo failed: {e}')
    finally:
        demo_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
