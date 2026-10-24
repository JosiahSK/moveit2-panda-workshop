#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from moveit_msgs.srv import GetStateValidity
from moveit_msgs.msg import RobotState
from sensor_msgs.msg import JointState

def test_default_state_validity():
    rclpy.init()
    node = Node('test_state_validity_node')
    client = node.create_client(GetStateValidity, '/check_state_validity')

    assert client.wait_for_service(timeout_sec=10.0), "Service /check_state_validity not available"

    req = GetStateValidity.Request()
    req.group_name = 'arm'
    req.robot_state = RobotState()
    req.robot_state.joint_state = JointState()
    req.robot_state.joint_state.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
    req.robot_state.joint_state.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    future = client.send_goal_async(req) if hasattr(client, 'send_goal_async') else client.call_async(req)
    rclpy.spin_until_future_complete(node, future, timeout_sec=5.0)

    res = future.result()
    assert res is not None, "GetStateValidity service call failed"
    assert res.valid is True, f"Default robot state is in collision! Contacts: {res.contacts}"

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    test_default_state_validity()
    print("State validity test passed successfully! valid == True")
