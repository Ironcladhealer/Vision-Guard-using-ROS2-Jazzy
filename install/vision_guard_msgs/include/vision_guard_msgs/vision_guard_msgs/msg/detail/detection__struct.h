// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vision_guard_msgs:msg/Detection.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "vision_guard_msgs/msg/detection.h"


#ifndef VISION_GUARD_MSGS__MSG__DETAIL__DETECTION__STRUCT_H_
#define VISION_GUARD_MSGS__MSG__DETAIL__DETECTION__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

// Include directives for member types
// Member 'label'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Detection in the package vision_guard_msgs.
typedef struct vision_guard_msgs__msg__Detection
{
  /// e.g. "person", "car"
  rosidl_runtime_c__String label;
  /// 0.0 to 1.0
  float confidence;
  /// top-left x of bounding box
  float x;
  /// top-left y of bounding box
  float y;
  /// box width in pixels
  float width;
  /// box height in pixels
  float height;
  /// assigned by tracker node (-1 if untracked)
  int32_t track_id;
} vision_guard_msgs__msg__Detection;

// Struct for a sequence of vision_guard_msgs__msg__Detection.
typedef struct vision_guard_msgs__msg__Detection__Sequence
{
  vision_guard_msgs__msg__Detection * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vision_guard_msgs__msg__Detection__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VISION_GUARD_MSGS__MSG__DETAIL__DETECTION__STRUCT_H_
