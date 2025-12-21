---
title: Parameters and Configuration - Runtime configuration management
description: Understanding ROS 2 parameters for runtime configuration management
tags: [ros2, parameters, configuration, runtime, dynamic]
---

# Parameters and Configuration - Runtime configuration management

## Learning Objectives
- Understand the parameter system in ROS 2 for runtime configuration
- Implement parameter handling in ROS 2 nodes
- Use parameter files for configuration management
- Compare parameter configuration with other approaches

## Prerequisites
- Understanding of ROS 2 nodes and basic architecture
- Familiarity with programming in Python or C++
- Basic knowledge of configuration management concepts

## Introduction
Parameters in ROS 2 provide a way to configure nodes at runtime without recompilation. They allow for dynamic adjustment of node behavior, making systems more flexible and adaptable. Parameters can be set at launch time, changed during runtime, and managed through configuration files.

## Core Content

### Parameter System Overview
Parameters in ROS 2 are:
- **Typed values** that configure node behavior
- **Accessible at runtime** without recompilation
- **Dynamically changeable** during node execution
- **Hierarchically organized** with node-specific namespacing
- **Introspectable** through command-line tools

### Parameter Types
ROS 2 supports several parameter types:
- **Integer**: 8, 16, 32, 64-bit signed and unsigned integers
- **Float**: 32-bit and 64-bit floating-point numbers
- **Boolean**: True/false values
- **String**: Text values
- **Array**: Lists of other parameter types (integer_array, double_array, string_array, bool_array)
- **Byte array**: Binary data

### Parameter Declaration and Usage
Parameters must be declared before use:
- **Declarable**: Parameters can be declared with default values and constraints
- **Validation**: Type checking and range validation
- **Callbacks**: Notification when parameters change
- **Automatic**: Some parameters are automatically handled

### Parameter Access Methods
- **Command line**: `ros2 param` tools for runtime management
- **Launch files**: Set parameters at launch time
- **Configuration files**: YAML files for complex parameter sets
- **Programmatic**: Set and get parameters from within nodes
- **Node parameters**: Individual node parameter management

### Use Cases
Parameters are ideal for:
- Algorithm configuration (thresholds, gains, tolerances)
- Hardware-specific settings (port names, calibration values)
- Runtime tunable parameters (speed limits, safety margins)
- Environment-specific configuration (simulation vs. real robot)
- Debugging and development settings

### Parameter Best Practices
- **Naming**: Use descriptive, consistent parameter names
- **Documentation**: Document parameter meaning and valid ranges
- **Validation**: Validate parameter values at runtime
- **Defaults**: Provide sensible default values
- **Grouping**: Group related parameters logically
- **Constraints**: Define valid ranges and value types

## Practical Exercise
1. Create a node that declares and uses various parameter types
2. Create a YAML configuration file with parameters
3. Launch the node with parameters from the file
4. Change parameters at runtime using command-line tools

Example Parameter Node:
```python
import rclpy
from rclpy.parameter import Parameter
from rclpy.node import Node
from rclpy.parameter_service import SetParametersResult

class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')

        # Declare parameters with default values
        self.declare_parameter('robot_name', 'default_robot')
        self.declare_parameter('max_velocity', 1.0)
        self.declare_parameter('use_sim_time', False)
        self.declare_parameter('sensors.enabled', [True, False, True])

        # Get parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.max_velocity = self.get_parameter('max_velocity').value
        self.use_sim_time = self.get_parameter('use_sim_time').value

        # Set up parameter callback for changes
        self.add_on_set_parameters_callback(self.parameter_callback)

        self.get_logger().info(f'Initialized with robot: {self.robot_name}, max vel: {self.max_velocity}')

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'max_velocity' and param.type_ == Parameter.Type.DOUBLE:
                self.get_logger().info(f'Changed max_velocity to: {param.value}')
                self.max_velocity = param.value
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    node = ParameterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Summary
Parameters provide a flexible way to configure ROS 2 nodes at runtime without recompilation. They enable dynamic adjustment of behavior and make systems more adaptable to different environments and requirements. Proper parameter design is essential for maintainable and configurable robotic systems.

## Further Reading
- ROS 2 Parameters: https://docs.ros.org/en/rolling/Concepts/About-Parameters.html
- Parameter Client Libraries: https://docs.ros.org/en/rolling/Tutorials/Parameters/Understanding-ROS2-Parameters.html
- Parameter Validation: https://docs.ros.org/en/rolling/How-To-Guides/Using-Parameters-in-a-class-CPP.html