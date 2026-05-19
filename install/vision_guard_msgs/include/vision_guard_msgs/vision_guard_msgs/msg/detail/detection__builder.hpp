// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vision_guard_msgs:msg/Detection.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "vision_guard_msgs/msg/detection.hpp"


#ifndef VISION_GUARD_MSGS__MSG__DETAIL__DETECTION__BUILDER_HPP_
#define VISION_GUARD_MSGS__MSG__DETAIL__DETECTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vision_guard_msgs/msg/detail/detection__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vision_guard_msgs
{

namespace msg
{

namespace builder
{

class Init_Detection_track_id
{
public:
  explicit Init_Detection_track_id(::vision_guard_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  ::vision_guard_msgs::msg::Detection track_id(::vision_guard_msgs::msg::Detection::_track_id_type arg)
  {
    msg_.track_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vision_guard_msgs::msg::Detection msg_;
};

class Init_Detection_height
{
public:
  explicit Init_Detection_height(::vision_guard_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_track_id height(::vision_guard_msgs::msg::Detection::_height_type arg)
  {
    msg_.height = std::move(arg);
    return Init_Detection_track_id(msg_);
  }

private:
  ::vision_guard_msgs::msg::Detection msg_;
};

class Init_Detection_width
{
public:
  explicit Init_Detection_width(::vision_guard_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_height width(::vision_guard_msgs::msg::Detection::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_Detection_height(msg_);
  }

private:
  ::vision_guard_msgs::msg::Detection msg_;
};

class Init_Detection_y
{
public:
  explicit Init_Detection_y(::vision_guard_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_width y(::vision_guard_msgs::msg::Detection::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_Detection_width(msg_);
  }

private:
  ::vision_guard_msgs::msg::Detection msg_;
};

class Init_Detection_x
{
public:
  explicit Init_Detection_x(::vision_guard_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_y x(::vision_guard_msgs::msg::Detection::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_Detection_y(msg_);
  }

private:
  ::vision_guard_msgs::msg::Detection msg_;
};

class Init_Detection_confidence
{
public:
  explicit Init_Detection_confidence(::vision_guard_msgs::msg::Detection & msg)
  : msg_(msg)
  {}
  Init_Detection_x confidence(::vision_guard_msgs::msg::Detection::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_Detection_x(msg_);
  }

private:
  ::vision_guard_msgs::msg::Detection msg_;
};

class Init_Detection_label
{
public:
  Init_Detection_label()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Detection_confidence label(::vision_guard_msgs::msg::Detection::_label_type arg)
  {
    msg_.label = std::move(arg);
    return Init_Detection_confidence(msg_);
  }

private:
  ::vision_guard_msgs::msg::Detection msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vision_guard_msgs::msg::Detection>()
{
  return vision_guard_msgs::msg::builder::Init_Detection_label();
}

}  // namespace vision_guard_msgs

#endif  // VISION_GUARD_MSGS__MSG__DETAIL__DETECTION__BUILDER_HPP_
