from ultralytics import YOLO
import shutil
import os

print("Downloading YOLOv8n pretrained weights...")
model = YOLO("yolov8n.pt")  # auto-downloads on first run
os.makedirs("../models", exist_ok=True)
shutil.copy("yolov8n.pt", "../models/yolov8n.pt")
print("Model saved to ../models/yolov8n.pt")