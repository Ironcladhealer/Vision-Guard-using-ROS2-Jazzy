import rclpy
from rclpy.node import Node

import numpy as np
import csv
import os
from datetime import datetime

from vision_guard_msgs.msg import Detection


class CentroidTracker:
    """
    Tracks objects across frames by matching centroids.
    Each unique object gets an integer ID that persists across frames.
    """
    def __init__(self, max_disappeared=30):
        self.next_id = 0
        self.objects = {}        # id -> centroid (x, y)
        self.labels = {}         # id -> label string
        self.disappeared = {}    # id -> frames since last seen
        # If an object disappears for this many frames, deregister it
        self.max_disappeared = max_disappeared

    def register(self, centroid, label):
        self.objects[self.next_id] = centroid
        self.labels[self.next_id] = label
        self.disappeared[self.next_id] = 0
        self.next_id += 1

    def deregister(self, obj_id):
        del self.objects[obj_id]
        del self.labels[obj_id]
        del self.disappeared[obj_id]

    def update(self, detections):
        """
        detections: list of (centroid_x, centroid_y, label) tuples
        returns: list of (centroid_x, centroid_y, label, track_id) tuples
        """
        # If no detections, mark all existing objects as disappeared
        if len(detections) == 0:
            for obj_id in list(self.disappeared.keys()):
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self.deregister(obj_id)
            return []

        # If we have no tracked objects yet, register all detections
        if len(self.objects) == 0:
            for (cx, cy, label) in detections:
                self.register((cx, cy), label)
        else:
            # --- Centroid matching ---
            # Compare each new detection centroid against all tracked centroids
            # Assign new detection to whichever tracked object is closest

            obj_ids = list(self.objects.keys())
            obj_centroids = list(self.objects.values())
            new_centroids = [(cx, cy) for (cx, cy, _) in detections]

            # Build a distance matrix: rows = existing objects, cols = new detections
            # D[i][j] = euclidean distance between tracked object i and detection j
            D = np.zeros((len(obj_centroids), len(new_centroids)))
            for i, oc in enumerate(obj_centroids):
                for j, nc in enumerate(new_centroids):
                    D[i][j] = np.sqrt((oc[0]-nc[0])**2 + (oc[1]-nc[1])**2)

            # Greedy matching: sort by smallest distance, assign in order
            # rows = sorted row indices, cols = corresponding col indices
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()

            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                # Distance threshold — if too far, don't match
                if D[row][col] > 100:
                    continue

                obj_id = obj_ids[row]
                self.objects[obj_id] = new_centroids[col]
                self.labels[obj_id] = detections[col][2]
                self.disappeared[obj_id] = 0
                used_rows.add(row)
                used_cols.add(col)

            # Register unmatched detections as new objects
            unused_cols = set(range(len(new_centroids))) - used_cols
            for col in unused_cols:
                self.register(
                    (detections[col][0], detections[col][1]),
                    detections[col][2]
                )

            # Mark unmatched existing objects as disappeared
            unused_rows = set(range(len(obj_centroids))) - used_rows
            for row in unused_rows:
                obj_id = obj_ids[row]
                self.disappeared[obj_id] += 1
                if self.disappeared[obj_id] > self.max_disappeared:
                    self.deregister(obj_id)

        # Build output list with assigned track IDs
        results = []
        for obj_id, centroid in self.objects.items():
            results.append((centroid[0], centroid[1],
                            self.labels[obj_id], obj_id))
        return results


class TrackerNode(Node):
    def __init__(self):
        super().__init__('tracker_node')

        # Our centroid tracker instance
        self.tracker = CentroidTracker(max_disappeared=30)

        # Buffer to collect detections within one timer tick
        # Multiple Detection messages arrive per frame (one per object)
        # We batch them before passing to the tracker
        self.detection_buffer = []

        # --- Subscriber ---
        # Subscribes to /detections published by the detector node
        # Every message triggers self.detection_callback
        self.subscription = self.create_subscription(
            Detection,
            '/detections',
            self.detection_callback,
            10
        )

        # Publisher — republishes detections WITH track IDs assigned
        self.tracked_pub = self.create_publisher(
            Detection,
            '/tracked_detections',
            10
        )

        # --- CSV logging ---
        # Log every tracked detection with timestamp to a CSV file
        log_dir = os.path.expanduser('~/vision_guard_logs')
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_path = os.path.join(log_dir, f'detections_{timestamp}.csv')

        self.csv_file = open(log_path, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(
            ['timestamp', 'track_id', 'label', 'centroid_x', 'centroid_y']
        )
        self.get_logger().info(f'Logging to {log_path}')

        # Timer runs at 10 FPS — processes buffered detections each tick
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.get_logger().info('Tracker node started!')

    def detection_callback(self, msg):
        # Just buffer incoming detections — don't process yet
        # Processing happens in timer_callback so all detections
        # from one frame are handled together
        self.detection_buffer.append(msg)

    def timer_callback(self):
        if not self.detection_buffer:
            return

        # Convert buffered Detection messages to centroid tuples
        detections = []
        for msg in self.detection_buffer:
            cx = msg.x + msg.width / 2.0   # centroid x
            cy = msg.y + msg.height / 2.0  # centroid y
            detections.append((cx, cy, msg.label))

        # Clear buffer for next tick
        self.detection_buffer = []

        # Run centroid tracker
        tracked = self.tracker.update(detections)

        now = self.get_clock().now().to_msg()

        for (cx, cy, label, track_id) in tracked:
            # Log to CSV
            self.csv_writer.writerow([
                f'{now.sec}.{now.nanosec}',
                track_id, label, f'{cx:.1f}', f'{cy:.1f}'
            ])

            # Publish tracked detection with ID assigned
            out = Detection()
            out.label = label
            out.confidence = 1.0   # confidence managed by detector
            out.x = cx
            out.y = cy
            out.width = 0.0
            out.height = 0.0
            out.track_id = track_id
            self.tracked_pub.publish(out)

            self.get_logger().info(
                f'[ID {track_id}] {label} @ ({cx:.0f}, {cy:.0f})'
            )

    def destroy_node(self):
        self.csv_file.close()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = TrackerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()