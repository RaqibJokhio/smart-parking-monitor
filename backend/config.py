import os

DB_PATH = "parking.db"
EVIDENCE_DIR = "../evidence"
MODEL_PATH = "../models/yolov8n.pt"
CONFIDENCE_THRESHOLD = 0.4
VEHICLE_CLASSES = [2, 3, 5, 7]  # COCO: car, motorcycle, bus, truck
FRAME_SKIP = 2  # process every nth frame