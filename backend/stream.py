import cv2
import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from database import get_connection, init_db
from inference import load_slots_from_db, draw_slots, draw_detections
from bytetrack_wrapper import run_tracker
from tracker import ParkingTracker

router = APIRouter()
parking_tracker = ParkingTracker()

def generate_frames(video_path: str):
    init_db()
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Cannot open video: {video_path}")
        return

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        frame_count += 1
        if frame_count % 2 != 0:
            continue

        frame = cv2.resize(frame, (1280, 720))
        conn = get_connection()
        slots = load_slots_from_db(conn)
        conn.close()

        tracked_objects = run_tracker(frame)
        occupied_slot_ids = parking_tracker.update(tracked_objects, slots, frame)

        frame = draw_slots(frame, slots, set(occupied_slot_ids.keys()))
        frame = draw_detections(frame, [
            {"bbox": obj["bbox"]} for obj in tracked_objects
        ], [obj["track_id"] for obj in tracked_objects])

        # Live duration overlay
        durations = parking_tracker.get_live_durations()
        for obj in tracked_objects:
            tid = str(obj["track_id"])
            if tid in durations:
                x1, y1, _, _ = obj["bbox"]
                mins, secs = divmod(durations[tid], 60)
                cv2.putText(frame, f"{mins:02d}:{secs:02d}",
                            (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, (0, 255, 255), 1)

        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
        )

    cap.release()


@router.get("/stream")
def video_stream(video_path: str = "data/sample.mp4"):
    return StreamingResponse(
        generate_frames(video_path),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )