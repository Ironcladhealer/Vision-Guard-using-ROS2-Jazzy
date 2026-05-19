import rclpy
from rclpy.node import Node

from vision_guard_msgs.msg import Detection
from geometry_msgs.msg import Twist

from collections import defaultdict
import time


class ResponseNode(Node):
    def __init__(self):
        super().__init__('response_node')

        # --- Subscriber ---
        # Listens to tracked detections (with IDs) from tracker node
        self.subscription = self.create_subscription(
            Detection,
            '/tracked_detections',
            self.tracked_callback,
            10
        )

        # --- Publisher ---
        # geometry_msgs/Twist is the standard ROS2 velocity command
        # linear.x  = forward/backward speed (m/s)
        # angular.z = left/right rotation speed (rad/s)
        # Any robot (real or simulated) that accepts /cmd_vel understands this
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Track which IDs we've already alerted about
        # So we don't spam the same alert every 0.1 seconds
        self.alerted_ids = set()

        # Track last seen time per ID — for disappearance detection
        self.last_seen = defaultdict(float)

        # Track counts per label — how many unique IDs per class
        self.label_id_map = defaultdict(set)

        # Timer to check for objects that have disappeared
        self.timer = self.create_timer(1.0, self.check_disappeared)

        self.get_logger().info('Response node started! Watching for objects...')

    def tracked_callback(self, msg):
        track_id = msg.track_id
        label = msg.label
        cx = msg.x
        cy = msg.y

        # Update last seen time
        self.last_seen[track_id] = time.time()
        self.label_id_map[label].add(track_id)

        # --- First time we see this ID: fire an alert ---
        if track_id not in self.alerted_ids:
            self.alerted_ids.add(track_id)
            self.get_logger().warn(
                f'🚨 NEW OBJECT DETECTED: [{label}] '
                f'assigned ID={track_id} at centroid ({cx:.0f}, {cy:.0f})'
            )

        # --- Decide robot response based on label ---
        twist = Twist()  # all zeros by default = stop

        if label == 'person':
            # Simulate robot turning toward the person
            # angular.z > 0 = turn left, < 0 = turn right
            # We use centroid x to decide direction
            # If person is left of center (cx < 320), turn left
            # If person is right of center (cx > 320), turn right
            image_center_x = 320.0
            error = cx - image_center_x

            # Proportional control — bigger error = faster turn
            # This is a mini P-controller, same concept as your PID assignment!
            angular_z = -0.003 * error
            twist.angular.z = float(np.clip(angular_z, -0.5, 0.5)) \
                if False else float(max(-0.5, min(0.5, angular_z)))

            twist.linear.x = 0.1  # move forward slowly toward person

            self.get_logger().info(
                f'  → Person ID={track_id}: '
                f'angular={twist.angular.z:.3f} rad/s, '
                f'linear={twist.linear.x:.2f} m/s'
            )

        elif label in ('car', 'truck', 'bus', 'motorcycle'):
            # Vehicle detected — stop and hold
            twist.linear.x = 0.0
            twist.angular.z = 0.0
            self.get_logger().info(f'  → Vehicle [{label}] detected — holding position')

        elif label in ('cat', 'dog'):
            # Animal detected — back away slowly
            twist.linear.x = -0.1
            self.get_logger().info(f'  → Animal [{label}] detected — backing away')

        # Publish the velocity command
        self.cmd_vel_pub.publish(twist)

    def check_disappeared(self):
        """
        Runs every 1 second.
        If an object hasn't been seen for 2 seconds, log its disappearance.
        """
        now = time.time()
        for track_id, last_t in list(self.last_seen.items()):
            if now - last_t > 2.0 and track_id in self.alerted_ids:
                # Find its label
                label = 'unknown'
                for lbl, ids in self.label_id_map.items():
                    if track_id in ids:
                        label = lbl
                        break

                self.get_logger().info(
                    f'Object [{label}] ID={track_id} has left the scene'
                )
                # Remove from alerted so if it reappears it alerts again
                self.alerted_ids.discard(track_id)
                del self.last_seen[track_id]

        # Print summary every tick
        summary = {lbl: len(ids) for lbl, ids in self.label_id_map.items()}
        if summary:
            self.get_logger().info(f'Session totals: {summary}')


def main(args=None):
    rclpy.init(args=args)
    node = ResponseNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()