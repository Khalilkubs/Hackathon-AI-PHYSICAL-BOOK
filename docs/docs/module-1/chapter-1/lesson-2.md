---
title: ROS 2 vs ROS 1 - Key differences and improvements
description: Understanding the differences between ROS 1 and ROS 2
tags: [ros2, ros1, comparison, improvements, migration]
---

# ROS 2 vs ROS 1 - Key differences and improvements

## Learning Objectives
- Compare the architecture of ROS 1 and ROS 2
- Identify key improvements in ROS 2 over ROS 1
- Understand the reasons for migration from ROS 1 to ROS 2
- Recognize the impact of these changes on robotics development

## Prerequisites
- Basic understanding of ROS 1 concepts (nodes, topics, services)
- Familiarity with distributed systems concepts

## Introduction
ROS 2 was developed as the next generation of the Robot Operating System to address the limitations of ROS 1 and provide enhanced capabilities for modern robotics applications. Understanding the differences between these two systems is crucial for making informed decisions about which to use and how to migrate existing systems.

## Core Content

### Architecture Differences

#### Communication Layer
- **ROS 1**: Uses a centralized master architecture with roscore as the central communication hub
- **ROS 2**: Uses DDS (Data Distribution Service) as the middleware layer, enabling decentralized communication

#### Real-time Support
- **ROS 1**: Limited real-time capabilities
- **ROS 2**: Built-in real-time support for time-critical applications

#### Quality of Service (QoS)
- **ROS 1**: Fixed communication patterns with limited configuration
- **ROS 2**: Configurable QoS policies for different communication needs (reliability, durability, history, etc.)

### Key Improvements

#### Security
- **ROS 1**: No built-in security features; security had to be implemented externally
- **ROS 2**: Built-in security with authentication, access control, and encryption capabilities

#### Multi-robot Systems
- **ROS 1**: Challenging to coordinate multiple robots due to single master limitation
- **ROS 2**: Better support for multi-robot systems with decentralized architecture

#### Cross-platform Support
- **ROS 1**: Primarily Linux-focused with limited Windows and macOS support
- **ROS 2**: Enhanced cross-platform support including Windows, macOS, and various Linux distributions

#### Language Support
- **ROS 1**: Primarily Python and C++
- **ROS 2**: Expanded language support with better client library implementations

#### Lifecycle Management
- **ROS 1**: Limited node lifecycle management
- **ROS 2**: Enhanced lifecycle management for complex system control

### Migration Considerations

When migrating from ROS 1 to ROS 2, developers should consider:
- **Build System**: Moving from catkin to colcon
- **API Changes**: Updated client library APIs
- **Tooling**: Different command-line tools and visualization tools
- **Middleware**: Understanding DDS concepts and configuration

## Practical Exercise
1. Compare the basic publisher/subscriber examples between ROS 1 and ROS 2
2. Identify the differences in code structure and API calls
3. Run both versions and observe the communication patterns

ROS 1 Example:
```python
# ROS 1 publisher example
import rospy
from std_msgs.msg import String

rospy.init_node('talker')
pub = rospy.Publisher('chatter', String, queue_size=10)
```

ROS 2 Example:
```python
# ROS 2 publisher example
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

rclpy.init()
node = Node('talker')
pub = node.create_publisher(String, 'chatter', 10)
```

## Summary
ROS 2 represents a significant advancement over ROS 1 with improvements in architecture, security, real-time capabilities, and multi-robot support. These improvements make ROS 2 more suitable for commercial and industrial applications, though the migration requires understanding of new concepts and APIs.

## Further Reading
- ROS 1 vs ROS 2 Migration Guide: https://docs.ros.org/en/rolling/Migration-Guide.html
- DDS Introduction: https://www.dds-foundation.org/what-is-dds-3/
- Real-time ROS 2: https://docs.ros.org/en/rolling/Tutorials/Real-Time-Programming.html