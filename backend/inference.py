import cv2
import json
import numpy as np
from ultralytics import YOLO
from datetime import datetime
from config import MODEL_PATH, CONFIDENCE_THRESHOLD, VEHICLE_CLASSES, EVIDENCE_DIR
import os

os.makedirs(EVIDENCE_DIR, exist_ok=True)

model = YOLO(MODEL_PATH)

def load_slots_from_db(conn):
    slots = conn.execute("SELECT * FROM parking_slots").fetchall()
    result = []
    for slot in slots:
        result.append({
            "id": slot["id"],
            "slot_name": slot["slot_name"],
            "polygon": np.array(json.loads(slot["polygon"]), dtype=np.int32),
            "is_restricted": bool(slot["is_restricted"])
        })
    return result

def point_in_polygon(point, polygon):
    return cv2.pointPolygonTest(polygon, point, False) >= 0

def get_vehicle_center(box):
    x1, y1, x2, y2 = box
    return (int((x1 + x2) / 2), int((y1 + y2) / 2))

def detect_vehicles(frame):
    results = model(frame, conf=CONFIDENCE_THRESHOLD, classes=VEHICLE_CLASSES, verbose=False)[0]
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls = int(box.cls[0])
        detections.append({
            "bbox": (x1, y1, x2, y2),
            "confidence": conf,
            "class_id": cls,
            "center": get_vehicle_center((x1, y1, x2, y2))
        })
    return detections

def assign_vehicle_to_slot(center, slots):
    for slot in slots:
        if point_in_polygon(center, slot["polygon"]):
            return slot
    return None

def is_illegal_parking(center, slots):
    assigned_slot = assign_vehicle_to_slot(center, slots)
    if assigned_slot is None:
        return True, "parked outside designated area"
    if assigned_slot["is_restricted"]:
        return True, "parked in restricted zone"
    return False, None

def save_evidence(frame, vehicle_id, reason):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{EVIDENCE_DIR}/illegal_{vehicle_id}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    return filename

def draw_slots(frame, slots, occupied_slot_ids):
    for slot in slots:
        color = (0, 0, 255) if slot["id"] in occupied_slot_ids else (0, 255, 0)
        cv2.polylines(frame, [slot["polygon"]], isClosed=True, color=color, thickness=2)
        centroid = slot["polygon"].mean(axis=0).astype(int)
        cv2.putText(frame, slot["slot_name"], tuple(centroid),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
    return frame

def draw_detections(frame, detections, tracker_ids=None):
    for i, det in enumerate(detections):
        x1, y1, x2, y2 = det["bbox"]
        label = f"ID:{tracker_ids[i]}" if tracker_ids and i < len(tracker_ids) else "vehicle"
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 165, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 165, 0), 1)
    return frame