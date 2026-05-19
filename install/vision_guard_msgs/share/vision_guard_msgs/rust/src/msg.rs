#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to vision_guard_msgs__msg__Detection

// This struct is not documented.
#[allow(missing_docs)]

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct Detection {
    /// e.g. "person", "car"
    pub label: std::string::String,

    /// 0.0 to 1.0
    pub confidence: f32,

    /// top-left x of bounding box
    pub x: f32,

    /// top-left y of bounding box
    pub y: f32,

    /// box width in pixels
    pub width: f32,

    /// box height in pixels
    pub height: f32,

    /// assigned by tracker node (-1 if untracked)
    pub track_id: i32,

}



impl Default for Detection {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::Detection::default())
  }
}

impl rosidl_runtime_rs::Message for Detection {
  type RmwMsg = super::msg::rmw::Detection;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        label: msg.label.as_str().into(),
        confidence: msg.confidence,
        x: msg.x,
        y: msg.y,
        width: msg.width,
        height: msg.height,
        track_id: msg.track_id,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        label: msg.label.as_str().into(),
      confidence: msg.confidence,
      x: msg.x,
      y: msg.y,
      width: msg.width,
      height: msg.height,
      track_id: msg.track_id,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      label: msg.label.to_string(),
      confidence: msg.confidence,
      x: msg.x,
      y: msg.y,
      width: msg.width,
      height: msg.height,
      track_id: msg.track_id,
    }
  }
}


