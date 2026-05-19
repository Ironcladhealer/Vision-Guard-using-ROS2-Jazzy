string label        # e.g. "person", "car"
float32 confidence  # 0.0 to 1.0
float32 x           # top-left x of bounding box
float32 y           # top-left y of bounding box
float32 width       # box width in pixels
float32 height      # box height in pixels
int32 track_id      # assigned by tracker node (-1 if untracked)