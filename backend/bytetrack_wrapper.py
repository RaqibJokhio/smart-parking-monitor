import numpy as np
from supervision import ByteTrack, Detections
from inference import detect_vehicles, get_vehicle_center

tracker = ByteTrack()

def run_tracker(frame):
    """
    Runs YOLO detection + ByteTrack on a frame.
    Returns list of tracked objects with track_id, bbox, center.
    """
    raw_detections = detect_vehicles(frame)

    if not raw_detections:
        return []

    xyxy = np.array([d["bbox"] for d in raw_detections], dtype=np.float32)
    confidences = np.array([d["confidence"] for d in raw_detections], dtype=np.float32)
    class_ids = np.array([d["class_id"] for d in raw_detections], dtype=int)

    detections = Detections(
        xyxy=xyxy,
        confidence=confidences,
        class_id=class_ids
    )

    tracked = tracker.update_with_detections(detections)

    results = []
    for i in range(len(tracked)):
        x1, y1, x2, y2 = map(int, tracked.xyxy[i])
        track_id = int(tracked.tracker_id[i])
        center = get_vehicle_center((x1, y1, x2, y2))
        results.append({
            "track_id": track_id,
            "bbox": (x1, y1, x2, y2),
            "center": center,
            "class_id": int(tracked.class_id[i])
        })

    return results