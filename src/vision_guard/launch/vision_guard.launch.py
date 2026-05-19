from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    ROS2 launch files must define a function called generate_launch_description()
    that returns a LaunchDescription object containing all nodes to start.
    """

    detector_node = Node(
        package='vision_guard',        # which package to look in
        executable='detector_node',    # matches entry_points in setup.py
        name='detector_node',          # name that appears in ros2 node list
        output='screen',               # print logs to terminal
        emulate_tty=True               # enables colored output in terminal
    )

    tracker_node = Node(
        package='vision_guard',
        executable='tracker_node',
        name='tracker_node',
        output='screen',
        emulate_tty=True
    )

    response_node = Node(
        package='vision_guard',
        executable='response_node',
        name='response_node',
        output='screen',
        emulate_tty=True
    )

    return LaunchDescription([
        detector_node,
        tracker_node,
        response_node,
    ])