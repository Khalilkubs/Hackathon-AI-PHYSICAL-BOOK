---
title: Nodes, Topics, Services, Actions - Core communication patterns
description: Understanding the fundamental communication patterns in ROS 2
tags: [ros2, nodes, topics, services, actions, communication]
---

# Nodes, Topics, Services, Actions - Core communication patterns

## Learning Objectives
- Understand the fundamental communication patterns in ROS 2
- Implement nodes with different communication patterns
- Choose appropriate communication patterns for specific use cases
- Recognize the trade-offs between different communication approaches

## Prerequisites
- Basic understanding of ROS 2 architecture
- Familiarity with programming in Python or C++
- Understanding of distributed systems concepts

## Introduction
Communication is the backbone of any robotic system. In ROS 2, there are four primary communication patterns that enable nodes to exchange information: nodes (the computational units), topics (asynchronous message passing), services (synchronous request/response), and actions (asynchronous goal-oriented communication). Understanding these patterns is essential for designing effective robotic systems.

## Core Content

### Nodes
Nodes are the fundamental computational units in ROS 2. Each node performs a specific task and communicates with other nodes through messages. A node can:
- Publish messages to topics
- Subscribe to topics to receive messages
- Provide services
- Call services
- Execute actions
- Execute action clients

Nodes are organized into a graph structure where they communicate through topics, services, and actions.

### Topics - Asynchronous Communication
Topics provide asynchronous, many-to-many communication through a publish/subscribe model:
- **Publishers** send messages to a topic
- **Subscribers** receive messages from a topic
- Communication is **fire-and-forget** - no guarantee of delivery
- Suitable for streaming data like sensor readings, robot states
- Supports Quality of Service (QoS) configurations

Example use cases:
- Camera image streams
- Laser scan data
- Robot joint states
- Sensor readings

### Services - Synchronous Communication
Services provide synchronous, request/response communication:
- **Service clients** send requests and wait for responses
- **Service servers** process requests and send responses
- Communication is **request-response** - blocking until response received
- Suitable for tasks that have a clear beginning and end
- Follows a strict request/response pattern

Example use cases:
- Saving map data
- Loading parameters
- Triggering specific actions with immediate feedback
- Requesting computation results

### Actions - Goal-Oriented Communication
Actions provide asynchronous, goal-oriented communication with feedback:
- **Action clients** send goals and can monitor progress
- **Action servers** execute goals and provide feedback
- Supports cancellation and preemption
- Provides goal status, feedback during execution, and final results
- Suitable for long-running tasks

Example use cases:
- Navigation to a goal
- Manipulation tasks
- Calibration procedures
- Any task requiring progress monitoring

## Practical Exercise
1. Create a ROS 2 package with nodes demonstrating each communication pattern
2. Implement a publisher and subscriber for a custom message
3. Create a service server and client
4. Implement an action server and client

Example Topic Publisher:
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TalkerNode(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher = self.create_publisher(String, 'chatter', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.get_clock().now().nanoseconds
        self.publisher.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    talker = TalkerNode()
    rclpy.spin(talker)
    talker.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Summary
ROS 2 provides four core communication patterns that enable flexible and robust robotic systems. Nodes form the computational units, while topics, services, and actions provide different communication semantics for various use cases. Understanding when to use each pattern is crucial for effective robotic system design.

## Further Reading
- ROS 2 Concepts: https://docs.ros.org/en/rolling/Concepts/About-Topics-Services-Actions.html
- Quality of Service: https://docs.ros.org/en/rolling/Concepts/About-Quality-of-Service.html
- Designing ROS 2 Messages: https://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Message.html