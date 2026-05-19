# 🛡️ Vision Guard — ROS2 Jazzy Object Detection & Tracking

A real-time computer vision pipeline built on **ROS2 Jazzy**, using **YOLOv8** for object detection and **centroid tracking** to assign persistent IDs to detected objects across frames. Three nodes communicate over ROS2 topics to form a complete perceive → track → respond pipeline.

> Built on Ubuntu 24.04 via WSL2 | ROS2 Jazzy Jalisco | Python 3.12 | YOLOv8n | OpenCV 4.13

---

## 📐 Architecture

```
USB / Webcam / Video File
        │
        ▼
┌─────────────────────┐
│    detector_node    │  ← YOLOv8 inference, publishes raw detections
└─────────────────────┘
        │                        │
        ▼                        ▼
  /detections            /annotated_image
  (Detection.msg)        (sensor_msgs/Image)
        │
        ▼
┌─────────────────────┐
│    tracker_node     │  ← Centroid tracking, assigns persistent IDs
└─────────────────────┘
        │
        ▼
  /tracked_detections
  (Detection.msg with track_id)
        │
        ▼
┌─────────────────────┐
│    response_node    │  ← Reacts to detections, publishes /cmd_vel
└─────────────────────┘
        │
        ▼
   /cmd_vel
   (geometry_msgs/Twist)
```

---

## 📦 Package Structure

```
Vision-Guard-using-ROS2-Jazzy/
├── src/
│   ├── vision_guard_msgs/        # Custom message definitions
│   │   ├── msg/
│   │   │   └── Detection.msg     # label, confidence, bbox, track_id
│   │   ├── CMakeLists.txt
│   │   └── package.xml
│   └── vision_guard/             # Main Python package
│       ├── vision_guard/
│       │   ├── __init__.py
│       │   ├── detector_node.py  # YOLOv8 + OpenCV, publishes detections
│       │   ├── tracker_node.py   # Centroid tracker, assigns IDs, logs CSV
│       │   └── response_node.py  # Reacts to tracked objects, cmd_vel
│       ├── launch/
│       │   └── vision_guard.launch.py
│       ├── resource/
│       │   └── vision_guard
│       ├── setup.py
│       ├── setup.cfg
│       └── package.xml
└── venv/                         # Python venv (--system-site-packages)
```

---

## 🗂️ Custom Message — `Detection.msg`

```
string label        # e.g. "person", "car"
float32 confidence  # 0.0 to 1.0
float32 x           # top-left x of bounding box
float32 y           # top-left y of bounding box
float32 width       # box width in pixels
float32 height      # box height in pixels
int32 track_id      # assigned by tracker node (-1 if untracked)
```

---

## 🧠 How Each Node Works

### `detector_node`
- Captures frames from a webcam or video file via `cv2.VideoCapture`
- Runs **YOLOv8 nano** inference on each frame at ~10 FPS
- Filters detections below 50% confidence
- Publishes one `Detection` message per detected object to `/detections`
- Publishes an annotated frame with bounding boxes to `/annotated_image`

### `tracker_node`
- Subscribes to `/detections` and batches messages per timer tick
- Implements **centroid tracking** — computes a distance matrix between existing tracked centroids and new detections, greedily assigns matches under a 100px threshold
- Objects that disappear for >30 frames are deregistered
- Publishes tracked detections with persistent `track_id` to `/tracked_detections`
- Logs every detection to a timestamped CSV in `~/vision_guard_logs/`

### `response_node`
- Subscribes to `/tracked_detections`
- Fires a first-seen alert for every new `track_id`
- Applies a **proportional controller** to turn toward detected persons (same P-control concept as PID tuning)
- Publishes `geometry_msgs/Twist` to `/cmd_vel`:
  - `person` → move forward + turn toward centroid
  - `car/truck/bus` → hold position
  - `cat/dog` → back away
- Detects when objects leave the scene (2 second timeout)
- Prints per-session detection totals every second

---

## ⚙️ Prerequisites

- Ubuntu 24.04 (native or WSL2)
- [ROS2 Jazzy Jalisco](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)
- Python 3.12
- `colcon`, `cv_bridge`

---

## 🚀 Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/Vision-Guard-using-ROS2-Jazzy.git
cd Vision-Guard-using-ROS2-Jazzy
```

### 2. Create the virtual environment

```bash
python3 -m venv venv --system-site-packages
touch venv/COLCON_IGNORE
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
# Install to system Python (required for ROS2 node launching)
sudo pip3 install ultralytics opencv-python --break-system-packages
sudo pip3 install catkin-pkg empy==3.3.4 lark --break-system-packages
```

### 4. Source ROS2

```bash
source /opt/ros/jazzy/setup.bash
```

### 5. Build the workspace

```bash
colcon build --symlink-install --cmake-args -DPYTHON_EXECUTABLE=/usr/bin/python3
source install/setup.bash
```

### 6. Verify the custom message compiled

```bash
ros2 interface show vision_guard_msgs/msg/Detection
```

---

## ▶️ Running

### Launch all three nodes at once

```bash
ros2 launch vision_guard vision_guard.launch.py
```

### Or run nodes individually (3 terminals)

```bash
# Terminal 1
ros2 run vision_guard detector_node

# Terminal 2
ros2 run vision_guard tracker_node

# Terminal 3
ros2 run vision_guard response_node
```

---

## 🔍 Inspecting the Pipeline

```bash
# List all active topics
ros2 topic list

# Watch raw detections
ros2 topic echo /detections

# Watch tracked detections with IDs
ros2 topic echo /tracked_detections

# Watch velocity commands
ros2 topic echo /cmd_vel

# Check node graph
ros2 node list
ros2 run rqt_graph rqt_graph
```

---

## 📝 Detection Logs

Every session automatically writes a CSV to `~/vision_guard_logs/`:

```
timestamp, track_id, label, centroid_x, centroid_y
1779217243.570, 0, person, 312.4, 245.1
1779217243.670, 1, car, 540.2, 310.8
```

---

## 🗺️ ROS2 Concepts Demonstrated

| Concept | Where used |
|---|---|
| Custom message types | `vision_guard_msgs/Detection` |
| Publishers | `detector_node` → `/detections`, `/annotated_image` |
| Subscribers | `tracker_node`, `response_node` |
| Timers | All three nodes use `create_timer()` |
| Topic chaining | detector → tracker → response |
| Launch files | `vision_guard.launch.py` |
| `cv_bridge` | OpenCV ↔ ROS2 Image conversion |
| `geometry_msgs/Twist` | `/cmd_vel` velocity commands |
| `colcon build` | Workspace build system |
| `--symlink-install` | Live editing without rebuilding |

---

## 🔧 WSL2 Notes

WSL2 cannot directly access USB webcams. Use a video file instead:

```python
# In detector_node.py
self.cap = cv2.VideoCapture(os.path.expanduser('~/test_video.mp4'))
```

A sample video with people, bicycles and cars:
```bash
wget -O ~/test_video.mp4 "https://github.com/intel-iot-devkit/sample-videos/raw/master/person-bicycle-car-detection.mp4"
```

---

## 📚 References

- [ROS2 Jazzy Documentation](https://docs.ros.org/en/jazzy/)
- [YOLOv8 by Ultralytics](https://docs.ultralytics.com/)
- [OpenCV Python](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)
- [Siegwart & Nourbakhsh — Introduction to Autonomous Mobile Robots](https://mitpress.mit.edu/9780262015356/)

---

## 📄 License

MIT