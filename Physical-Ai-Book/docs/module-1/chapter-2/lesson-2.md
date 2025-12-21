---
title: Services and Clients - Synchronous request/response communication
description: Understanding ROS 2 services and the request/response communication pattern
tags: [ros2, services, client, server, synchronous, request-response]
---

# Services and Clients - Synchronous request/response communication

## Learning Objectives
- Understand the request/response communication pattern in ROS 2
- Implement service servers and clients for synchronous communication
- Design appropriate service interfaces for specific use cases
- Compare service communication with topic communication

## Prerequisites
- Understanding of ROS 2 nodes and topic communication
- Familiarity with programming in Python or C++
- Basic knowledge of synchronous communication patterns

## Introduction
Services in ROS 2 provide synchronous, request/response communication between nodes. Unlike topics which are asynchronous and fire-and-forget, services establish a direct client-server relationship where the client waits for a response from the server. This pattern is ideal for operations that have a clear beginning and end with immediate results.

## Core Content

### Service Communication Model
In ROS 2, services implement a request/response communication pattern:
- **Service Clients** send requests to a named service
- **Service Servers** receive requests and send responses back
- Communication is **synchronous** and **blocking** until response is received
- Each service has a specific interface definition (`.srv` files)
- One server typically serves multiple clients for the same service

### Service Interface Definition
Service interfaces are defined in `.srv` files that contain:
- **Request** message structure
- **Response** message structure
- Separated by `---`

Example service definition (AddTwoInts.srv):
```
int64 a
int64 b
---
int64 sum
```

### Service Characteristics
- **Blocking**: Client waits for response before continuing
- **Stateless**: Each request is independent
- **Reliable**: Request/response guarantee (if server is available)
- **One-to-one**: Each request gets one response
- **Timeout**: Clients can specify timeout for requests

### Use Cases
Services are ideal for:
- Operations with immediate results (e.g., calculations, data retrieval)
- Configuration changes that need confirmation
- Triggering specific actions with results
- Database operations
- Parameter setting/getting

### Comparison with Topics
| Aspect | Topics | Services |
|--------|--------|----------|
| Communication | Asynchronous | Synchronous |
| Coupling | Loose | Tighter (client-server) |
| Guarantee | No delivery guarantee | Request/response guarantee |
| Use Case | Streaming data | One-time operations |
| Blocking | Non-blocking | Blocking |

## Practical Exercise
1. Define a custom service interface
2. Implement a service server that performs a specific operation
3. Create a service client that calls the service
4. Test the request/response pattern with different inputs

Example Service Server:
```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Summary
Services provide a synchronous, request/response communication mechanism in ROS 2. They are appropriate for operations that require immediate results and acknowledgment. Understanding when to use services versus topics is crucial for effective ROS 2 system design.

## Further Reading
- ROS 2 Services: https://docs.ros.org/en/rolling/Concepts/About-Services.html
- Service Definitions: https://docs.ros.org/en/rolling/Concepts/About-ROS-Interfaces.html#services
- Client-Server Patterns in ROS 2: https://docs.ros.org/en/rolling/Tutorials/Services/Understanding-ROS2-Services.html