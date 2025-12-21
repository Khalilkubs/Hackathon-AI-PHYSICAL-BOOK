---
title: Topics and Publishers/Subscribers - Asynchronous communication
description: Understanding ROS 2 topics and the publisher/subscriber communication pattern
tags: [ros2, topics, publisher, subscriber, asynchronous]
---

# Topics and Publishers/Subscribers - Asynchronous communication

## Learning Objectives
- Understand the publish/subscribe communication pattern in ROS 2
- Implement publishers and subscribers for message passing
- Configure Quality of Service (QoS) settings for topics
- Design appropriate message types for specific use cases

## Prerequisites
- Understanding of ROS 2 nodes and basic architecture
- Familiarity with programming in Python or C++
- Basic knowledge of asynchronous communication patterns

## Introduction
Topics form the backbone of ROS 2's communication system, enabling asynchronous, many-to-many communication between nodes. The publish/subscribe pattern allows nodes to exchange messages without direct coupling, promoting loose coupling and scalability in robotic systems.

## Core Content

### Topic Communication Model
In ROS 2, topics implement a publish/subscribe communication pattern:
- **Publishers** send messages to a named topic
- **Subscribers** receive messages from a named topic
- Communication is **asynchronous** and **non-blocking**
- Multiple publishers can publish to the same topic
- Multiple subscribers can subscribe to the same topic
- Uses DDS (Data Distribution Service) as the underlying middleware

### Message Passing
- Messages are published to topics with specific types (e.g., std_msgs/String, sensor_msgs/LaserScan)
- Messages are queued and delivered based on QoS policies
- No acknowledgment or guarantee of delivery (fire-and-forget model)
- Suitable for streaming data like sensor readings, robot states, or status updates

### Quality of Service (QoS)
ROS 2 provides QoS settings to control communication behavior:
- **Reliability**: Best effort vs. reliable delivery
- **Durability**: Volatile vs. transient local (ability to receive old messages)
- **History**: Keep all messages vs. keep last N messages
- **Depth**: Size of message queue

### Use Cases
Topics are ideal for:
- Sensor data streams (camera images, laser scans, IMU data)
- Robot state information (joint states, odometry)
- Status updates and notifications
- Broadcasting information to multiple recipients

## Practical Exercise
1. Create a publisher node that publishes a custom message
2. Create a subscriber node that receives and processes the message
3. Experiment with different QoS settings
4. Observe the asynchronous nature of topic communication

Example Publisher:
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Summary
Topics provide a flexible, asynchronous communication mechanism in ROS 2. The publish/subscribe pattern enables loose coupling between nodes and supports various QoS configurations for different requirements. Understanding when and how to use topics is fundamental to effective ROS 2 development.

## Further Reading
- ROS 2 Topics: https://docs.ros.org/en/rolling/Concepts/About-Topics.html
- Quality of Service: https://docs.ros.org/en/rolling/Concepts/About-Quality-of-Service.html
- Message Types: https://docs.ros.org/en/rolling/Concepts/About-ROS-Interfaces.html