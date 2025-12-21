---
title: Actions - Long-running tasks with feedback
description: Understanding ROS 2 actions for long-running goal-oriented communication
tags: [ros2, actions, goal-oriented, feedback, long-running]
---

# Actions - Long-running tasks with feedback

## Learning Objectives
- Understand the goal-oriented communication pattern in ROS 2 actions
- Implement action servers and clients for long-running tasks
- Design appropriate action interfaces for specific use cases
- Compare action communication with topic and service communication

## Prerequisites
- Understanding of ROS 2 nodes, topics, and services
- Familiarity with programming in Python or C++
- Basic knowledge of state machines and goal-oriented programming

## Introduction
Actions in ROS 2 provide a communication pattern for long-running, goal-oriented tasks that require feedback during execution. Unlike services which are synchronous and blocking, or topics which are asynchronous and fire-and-forget, actions provide a way to send a goal, receive continuous feedback during execution, and get a final result when the task is complete. This makes them ideal for tasks like navigation, manipulation, or calibration.

## Core Content

### Action Communication Model
In ROS 2, actions implement a goal-oriented communication pattern with three key components:
- **Goal**: Request sent by the action client to start a long-running task
- **Feedback**: Continuous updates sent by the action server during execution
- **Result**: Final outcome sent by the action server when the task completes

### Action Interface Definition
Action interfaces are defined in `.action` files that contain three parts:
- **Goal**: Input parameters for the action
- **Result**: Output parameters when the action completes
- **Feedback**: Intermediate updates during execution

Example action definition (Fibonacci.action):
```
int32 order
---
int32[] sequence
---
int32[] partial_sequence
```

### Action Characteristics
- **Non-blocking**: Client can continue working after sending a goal
- **Feedback**: Continuous updates on task progress
- **Cancelability**: Clients can cancel goals in progress
- **Preemption**: New goals can preempt ongoing goals
- **Status tracking**: Clients can monitor goal status

### Action States
Actions can be in various states:
- **PENDING**: Goal accepted but not started
- **ACTIVE**: Goal is currently executing
- **PREEMPTED**: Goal was replaced by a higher priority goal
- **SUCCEEDED**: Goal completed successfully
- **ABORTED**: Goal failed during execution
- **RECALLED**: Goal was canceled before execution started

### Use Cases
Actions are ideal for:
- Navigation to a goal location
- Robot manipulation tasks
- Calibration procedures
- Any long-running task requiring progress monitoring
- Tasks that might need cancellation

### Comparison with Other Communication Patterns
| Aspect | Topics | Services | Actions |
|--------|--------|----------|---------|
| Communication | Asynchronous | Synchronous | Asynchronous |
| Feedback | No | No | Yes |
| Blocking | No | Yes | No |
| Cancelable | No | No | Yes |
| Use Case | Streaming | One-time | Long-running |

## Practical Exercise
1. Define a custom action interface for a navigation task
2. Implement an action server that simulates navigation with feedback
3. Create an action client that sends goals and monitors progress
4. Test goal cancellation and status monitoring

Example Action Server:
```python
import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1])

            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result

def main(args=None):
    rclpy.init(args=args)
    fibonacci_action_server = FibonacciActionServer()
    rclpy.spin(fibonacci_action_server)
    fibonacci_action_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Summary
Actions provide a sophisticated communication mechanism in ROS 2 for long-running, goal-oriented tasks that require feedback and cancellation capabilities. They are essential for complex robotic tasks like navigation and manipulation where progress monitoring is important.

## Further Reading
- ROS 2 Actions: https://docs.ros.org/en/rolling/Concepts/About-Actions.html
- Action Definitions: https://docs.ros.org/en/rolling/Concepts/About-ROS-Interfaces.html#actions
- Action Client/Server Implementation: https://docs.ros.org/en/rolling/Tutorials/Actions/Writing-an-Action-Server-Cpp.html