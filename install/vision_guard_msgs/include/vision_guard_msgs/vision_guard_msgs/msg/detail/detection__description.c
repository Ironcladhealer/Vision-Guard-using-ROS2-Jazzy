// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from vision_guard_msgs:msg/Detection.idl
// generated code does not contain a copyright notice

#include "vision_guard_msgs/msg/detail/detection__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_vision_guard_msgs
const rosidl_type_hash_t *
vision_guard_msgs__msg__Detection__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x59, 0xa7, 0x6a, 0xa2, 0xf3, 0xd6, 0x1c, 0xfe,
      0x0c, 0x67, 0xd3, 0xdc, 0x87, 0x06, 0x5f, 0x44,
      0x94, 0xa1, 0x3a, 0xf8, 0x81, 0x25, 0x84, 0xdc,
      0x7e, 0xca, 0xbc, 0xca, 0xa8, 0x9a, 0x6e, 0x71,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char vision_guard_msgs__msg__Detection__TYPE_NAME[] = "vision_guard_msgs/msg/Detection";

// Define type names, field names, and default values
static char vision_guard_msgs__msg__Detection__FIELD_NAME__label[] = "label";
static char vision_guard_msgs__msg__Detection__FIELD_NAME__confidence[] = "confidence";
static char vision_guard_msgs__msg__Detection__FIELD_NAME__x[] = "x";
static char vision_guard_msgs__msg__Detection__FIELD_NAME__y[] = "y";
static char vision_guard_msgs__msg__Detection__FIELD_NAME__width[] = "width";
static char vision_guard_msgs__msg__Detection__FIELD_NAME__height[] = "height";
static char vision_guard_msgs__msg__Detection__FIELD_NAME__track_id[] = "track_id";

static rosidl_runtime_c__type_description__Field vision_guard_msgs__msg__Detection__FIELDS[] = {
  {
    {vision_guard_msgs__msg__Detection__FIELD_NAME__label, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_STRING,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {vision_guard_msgs__msg__Detection__FIELD_NAME__confidence, 10, 10},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {vision_guard_msgs__msg__Detection__FIELD_NAME__x, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {vision_guard_msgs__msg__Detection__FIELD_NAME__y, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {vision_guard_msgs__msg__Detection__FIELD_NAME__width, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {vision_guard_msgs__msg__Detection__FIELD_NAME__height, 6, 6},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_FLOAT,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {vision_guard_msgs__msg__Detection__FIELD_NAME__track_id, 8, 8},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT32,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
vision_guard_msgs__msg__Detection__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {vision_guard_msgs__msg__Detection__TYPE_NAME, 31, 31},
      {vision_guard_msgs__msg__Detection__FIELDS, 7, 7},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "string label        # e.g. \"person\", \"car\"\n"
  "float32 confidence  # 0.0 to 1.0\n"
  "float32 x           # top-left x of bounding box\n"
  "float32 y           # top-left y of bounding box\n"
  "float32 width       # box width in pixels\n"
  "float32 height      # box height in pixels\n"
  "int32 track_id      # assigned by tracker node (-1 if untracked)";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
vision_guard_msgs__msg__Detection__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {vision_guard_msgs__msg__Detection__TYPE_NAME, 31, 31},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 323, 323},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
vision_guard_msgs__msg__Detection__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *vision_guard_msgs__msg__Detection__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
