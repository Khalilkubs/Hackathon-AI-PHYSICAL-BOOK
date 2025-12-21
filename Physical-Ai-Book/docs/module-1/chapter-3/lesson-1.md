---
title: ROS 2 Command Line Tools - Essential tools for development
description: Understanding ROS 2 command line tools for development and debugging
tags: [ros2, command-line, tools, debugging, development]
---

# ROS 2 Command Line Tools - Essential tools for development

## Learning Objectives
- Use essential ROS 2 command line tools for development and debugging
- Understand the purpose and functionality of each tool
- Apply command line tools to inspect and manage ROS 2 systems
- Troubleshoot ROS 2 systems using command line tools

## Prerequisites
- Basic understanding of ROS 2 architecture and concepts
- Familiarity with command line interfaces
- Basic understanding of ROS 2 nodes, topics, services, and parameters

## Introduction
ROS 2 provides a comprehensive set of command line tools that enable developers to inspect, manage, and debug ROS 2 systems. These tools are essential for development, testing, and maintenance of ROS 2 applications. Understanding how to use these tools effectively can significantly improve productivity and system reliability.

## Core Content

### Essential Command Line Tools

#### `ros2 run`
- Execute a specific node from a package
- Syntax: `ros2 run <package_name> <executable_name>`
- Used to start individual nodes for testing and development

#### `ros2 launch`
- Launch multiple nodes and configurations from launch files
- Syntax: `ros2 launch <package_name> <launch_file.py>`
- Manages complex system startup with parameters and dependencies

#### `ros2 topic`
- Inspect and interact with topics
- Commands: `list`, `info`, `echo`, `pub`
- Essential for debugging message flow and node communication

#### `ros2 service`
- Inspect and interact with services
- Commands: `list`, `info`, `call`
- Used to test service-based communication

#### `ros2 action`
- Inspect and interact with actions
- Commands: `list`, `info`, `send_goal`
- For testing goal-oriented communication patterns

#### `ros2 param`
- Manage node parameters at runtime
- Commands: `list`, `get`, `set`, `dump`
- Enables dynamic configuration without recompilation

#### `ros2 node`
- Inspect node information
- Commands: `list`, `info`
- Shows node connections and communication patterns

#### `ros2 pkg`
- Package management and information
- Commands: `list`, `executables`, `create`
- For package development and management

### Advanced Tool Usage

#### System Inspection
- `ros2 doctor`: Check system configuration and connectivity
- `ros2 bag`: Record and replay ROS 2 message data
- `ros2 interface`: Get information about message/service/action definitions

#### Network and Performance
- `ros2 daemon`: Manage the ROS 2 daemon process
- `ros2 security`: Handle security features (if enabled)
- Using tools with specific DDS implementations and configurations

### Practical Debugging Scenarios

#### Communication Issues
1. Use `ros2 topic list` to verify topic availability
2. Use `ros2 topic echo <topic_name>` to check message content
3. Use `ros2 node info <node_name>` to check node connections
4. Use `ros2 topic info <topic_name>` to verify QoS settings

#### Parameter Issues
1. Use `ros2 param list <node_name>` to see available parameters
2. Use `ros2 param get <node_name> <param_name>` to check values
3. Use `ros2 param set <node_name> <param_name> <value>` to change values

#### Performance Issues
1. Use `ros2 topic hz <topic_name>` to check message frequency
2. Use `ros2 bag record` to capture data for analysis
3. Monitor system resources during operation

## Practical Exercise
1. Launch a simple ROS 2 system with multiple nodes
2. Use `ros2 node list` and `ros2 topic list` to inspect the system
3. Use `ros2 topic echo` to monitor messages
4. Use `ros2 param` commands to view and modify parameters
5. Practice debugging a communication issue using the tools

Example Commands:
```bash
# List all available nodes
ros2 node list

# List all available topics
ros2 topic list

# Echo messages from a specific topic
ros2 topic echo /chatter std_msgs/msg/String

# Call a service
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 1, b: 2}"

# List parameters of a node
ros2 param list <node_name>

# Set a parameter
ros2 param set <node_name> param_name value
```

## Summary
ROS 2 command line tools are essential for development, debugging, and maintenance of ROS 2 systems. Mastering these tools enables effective system inspection, parameter management, and issue resolution. Regular use of these tools during development helps identify and resolve issues early in the development cycle.

## Further Reading
- ROS 2 CLI Tools: https://docs.ros.org/en/rolling/Concepts/About-Command-Line-Tools.html
- Command Line Tool Tutorials: https://docs.ros.org/en/rolling/Tutorials/Tools/Command-Line-Tools.html
- Advanced Tool Usage: https://docs.ros.org/en/rolling/Tutorials/Tools/Doctor.html