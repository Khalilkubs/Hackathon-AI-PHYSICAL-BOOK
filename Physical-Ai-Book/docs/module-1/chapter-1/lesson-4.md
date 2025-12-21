---
title: Workspaces and Packages - Building and organizing ROS 2 projects
description: Understanding ROS 2 workspaces and package organization
tags: [ros2, workspace, packages, build-system, colcon]
---

# Workspaces and Packages - Building and organizing ROS 2 projects

## Learning Objectives
- Create and manage ROS 2 workspaces
- Understand the structure and purpose of ROS 2 packages
- Use colcon build system for project compilation
- Organize code following ROS 2 best practices

## Prerequisites
- Basic understanding of ROS 2 architecture
- Familiarity with command line interfaces
- Basic programming knowledge (Python or C++)

## Introduction
ROS 2 projects are organized into workspaces containing packages. A workspace is a directory that contains one or more packages, build directories, and installation directories. Understanding how to properly organize your code into packages and workspaces is fundamental to developing maintainable and reusable ROS 2 applications.

## Core Content

### Workspaces
A ROS 2 workspace is a directory that contains:
- **Source directory** (`src`): Contains package source code
- **Build directory** (`build`): Contains intermediate build files
- **Install directory** (`install`): Contains compiled and installed packages
- **Log directory** (`log`): Contains build logs and other logs

The typical workspace structure:
```
my_workspace/
├── src/
│   ├── package_1/
│   ├── package_2/
│   └── ...
├── build/
├── install/
└── log/
```

### Packages
A package is the basic unit of code organization in ROS 2 that contains:
- **Source code** (C++ and/or Python)
- **Launch files** for starting multiple nodes
- **Configuration files**
- **Message/service/action definitions**
- **Documentation**
- **Tests**

A minimal package contains:
- `package.xml`: Package manifest with metadata
- `CMakeLists.txt`: CMake build configuration (for C++)
- `setup.py`: Python setup configuration (for Python packages)

### Colcon Build System
Colcon is the build tool used in ROS 2 that:
- Builds packages in the correct dependency order
- Supports multiple programming languages
- Provides parallel builds
- Integrates with various build systems (CMake, ament_cmake, etc.)

Common colcon commands:
- `colcon build`: Build all packages in the workspace
- `colcon build --packages-select <pkg_name>`: Build specific packages
- `colcon test`: Run tests for packages
- `colcon build --symlink-install`: Create symbolic links instead of copying files

### Package Structure
A typical ROS 2 package structure:
```
my_package/
├── CMakeLists.txt
├── package.xml
├── src/
│   └── my_node.cpp (or nodes/ directory)
├── include/my_package/
│   └── my_header.hpp
├── launch/
│   └── my_launch_file.launch.py
├── config/
│   └── my_config.yaml
├── test/
│   └── test_my_package.cpp
└── scripts/ (for Python scripts)
    └── my_script.py
```

## Practical Exercise
1. Create a new ROS 2 workspace
2. Create a simple package with a basic node
3. Build the workspace using colcon
4. Source the workspace and run the node

Creating a workspace:
```bash
# Create workspace directory
mkdir -p ~/ros2_workspace/src
cd ~/ros2_workspace

# Create a simple package
cd src
ros2 pkg create --build-type ament_python my_first_package

# Build the workspace
cd ~/ros2_workspace
colcon build

# Source the workspace
source install/setup.bash
```

## Summary
ROS 2 workspaces and packages provide a structured way to organize and build robotic applications. Understanding the workspace structure, package organization, and build system is essential for developing maintainable ROS 2 projects. Following the established conventions ensures compatibility with the ROS 2 ecosystem and enables code sharing and reuse.

## Further Reading
- ROS 2 Workspaces: https://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/Creating-A-Workspace/Creating-A-Workspace.html
- Package Creation: https://docs.ros.org/en/rolling/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html
- Colcon Build Tool: https://colcon.readthedocs.io/en/released/