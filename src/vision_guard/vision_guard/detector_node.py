import rclpy
from rclpy.node import Node
import sys
import os

sys.path.insert(0, '/home/ironcladhealer769/Vision-Guard-using-ROS2-Jazzy/venv/lib/python3.12/site-packages')

import cv2
import numpy as np
from ultralytics import YOLO

# cv_bridge converts between ROS2 image messages and OpenCV numpy arrays
from cv_bridge import CvBridge

# Our custom message type
from vision_guard_msgs.msg import Detection

# ROS2 built-in message for image data
from sensor_msgs.msg import Image


class DetectorNode(Node):
    def __init__(self):
        # Every ROS2 node must call super().__init__ with a node name
        # This name appears in ros2 node list
        super().__init__('detector_node')

        # --- Publishers ---
        # A publisher sends messages TO a topic
        # QoS (Quality of Service) = 10 means keep last 10 messages in buffer
        self.detection_pub = self.create_publisher(
            Detection,           # message type
            '/detections',       # topic name
            10                   # QoS depth
        )

        self.image_pub = self.create_publisher(
            Image,
            '/annotated_image',
            10
        )

        # --- Load YOLO model ---
        # yolov8n = nano model, fastest, good enough for CPU
        self.model = YOLO('yolov8n.pt')
        self.get_logger().info('YOLOv8 model loaded')

        # --- OpenCV webcam capture ---
        # 0 = first webcam. In WSL this might need to be a video file path
        #self.cap = cv2.VideoCapture(0)
        self.cap = cv2.VideoCapture(
    os.path.expanduser('~/test_video.mp4')
)   

        # cv_bridge instance for converting frames to ROS2 Image messages
        self.bridge = CvBridge()

        # --- Timer ---
        # Instead of a while loop, ROS2 uses timers
        # This calls self.timer_callback every 0.1 seconds (10 FPS)
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.get_logger().info('Detector node started!')

    def timer_callback(self):
        ret, frame = self.cap.read()

        if not ret:
            #self.get_logger().warn('Failed to grab frame')
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            return

        # Run YOLO inference on the frame
        # verbose=False suppresses per-frame console output
        results = self.model(frame, verbose=False)

        # results[0].boxes contains all detections in this frame
        boxes = results[0].boxes

        for box in boxes:
            # box.xyxy gives [x1, y1, x2, y2] corner coordinates
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            # box.conf is confidence score (0.0 to 1.0)
            confidence = float(box.conf[0])

            # box.cls is the class index — model.names maps it to a string
            label = self.model.names[int(box.cls[0])]

            # Only publish detections above 50% confidence
            if confidence < 0.5:
                continue

            # Build our custom Detection message
            msg = Detection()
            msg.label = label
            msg.confidence = confidence
            msg.x = float(x1)
            msg.y = float(y1)
            msg.width = float(x2 - x1)
            msg.height = float(y2 - y1)
            msg.track_id = -1  # tracker node will assign this later

            # Publish to /detections topic
            self.detection_pub.publish(msg)

            # Draw bounding box on frame for visualization
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                          (0, 255, 0), 2)
            cv2.putText(frame, f'{label} {confidence:.2f}',
                        (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Convert OpenCV frame (BGR numpy array) → ROS2 Image message
        # 'bgr8' is the standard OpenCV color encoding
        img_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
        self.image_pub.publish(img_msg)

    def destroy_node(self):
        # Always release the camera when the node shuts down
        self.cap.release()
        super().destroy_node()


def main(args=None):
    # Initialize rclpy — must be called before anything else
    rclpy.init(args=args)

    node = DetectorNode()

    # spin() keeps the node alive and processes callbacks (timers, subs)
    # It blocks until you Ctrl+C
    rclpy.spin(node)

    # Cleanup
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()