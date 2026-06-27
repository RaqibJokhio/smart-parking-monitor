# Smart Parking Monitor

AI-powered parking space monitoring system using computer vision.

## Features
- Real-time vehicle detection with YOLOv8
- Multi-object tracking with ByteTrack
- Parking slot occupancy monitoring
- Illegal parking detection with evidence snapshots
- Live analytics dashboard (React + Tailwind)

## Tech Stack
**Backend:** FastAPI, OpenCV, YOLOv8, ByteTrack, SQLite  
**Frontend:** React, Tailwind CSS, Recharts  
**AI:** YOLOv8n (COCO pretrained)

## Project Structure
```
smart-parking-monitor/
├── backend/
├── frontend/
├── models/
├── data/
├── evidence/
└── notebooks/
```