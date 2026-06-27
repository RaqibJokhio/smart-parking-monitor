import cv2
import json
import numpy as np
import sys
from database import get_connection, init_db

"""
Parking Slot Polygon Editor
----------------------------
Usage: python slot_editor.py <video_path>

Controls:
  Left click     → add point to current polygon
  R              → reset current polygon
  S              → save current polygon as a slot
  D              → toggle restricted zone for next slot
  Q              → quit and save all to DB
  Z              → undo last point
"""

points = []
slots = []
is_restricted = False
slot_counter = 1
frame_display = None
frame_clean = None

def mouse_callback(event, x, y, flags, param):
    global points, frame_display
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        redraw()

def redraw():
    global frame_display
    frame_display = frame_clean.copy()

    # Draw saved slots
    for slot in slots:
        color = (0, 0, 255) if slot["is_restricted"] else (0, 255, 0)
        poly = np.array(slot["polygon"], dtype=np.int32)
        cv2.polylines(frame_display, [poly], isClosed=True, color=color, thickness=2)
        centroid = poly.mean(axis=0).astype(int)
        cv2.putText(frame_display, slot["name"], tuple(centroid),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # Draw current polygon in progress
    if points:
        for i, pt in enumerate(points):
            cv2.circle(frame_display, pt, 4, (255, 255, 0), -1)
            if i > 0:
                cv2.line(frame_display, points[i - 1], pt, (255, 255, 0), 1)

    # HUD
    status = f"Slot {slot_counter} | Points: {len(points)} | Restricted: {is_restricted}"
    cv2.putText(frame_display, status, (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame_display, "[S] Save  [R] Reset  [Z] Undo  [D] Toggle Restricted  [Q] Quit",
                (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)

def save_slots_to_db():
    init_db()
    conn = get_connection()
    saved = 0
    for slot in slots:
        existing = conn.execute(
            "SELECT id FROM parking_slots WHERE slot_name = ?", (slot["name"],)
        ).fetchone()
        if not existing:
            conn.execute(
                "INSERT INTO parking_slots (slot_name, polygon, is_restricted) VALUES (?, ?, ?)",
                (slot["name"], json.dumps(slot["polygon"]), int(slot["is_restricted"]))
            )
            saved += 1
    conn.commit()
    conn.close()
    print(f"Saved {saved} new slots to database.")

def main():
    global points, slots, is_restricted, slot_counter
    global frame_display, frame_clean

    if len(sys.argv) < 2:
        print("Usage: python slot_editor.py <video_path>")
        sys.exit(1)

    video_path = sys.argv[1]
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Cannot open video: {video_path}")
        sys.exit(1)

    ret, frame = cap.read()
    cap.release()

    if not ret:
        print("Could not read frame from video.")
        sys.exit(1)

    frame_clean = cv2.resize(frame, (1280, 720))
    frame_display = frame_clean.copy()

    cv2.namedWindow("Slot Editor")
    cv2.setMouseCallback("Slot Editor", mouse_callback)

    print("Slot Editor started. Click to define polygon points.")
    print("[S] Save slot | [R] Reset | [Z] Undo | [D] Toggle restricted | [Q] Save & quit")

    while True:
        cv2.imshow("Slot Editor", frame_display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            if len(points) < 3:
                print("Need at least 3 points to define a slot.")
            else:
                slot_name = f"S{slot_counter}"
                slots.append({
                    "name": slot_name,
                    "polygon": points.copy(),
                    "is_restricted": is_restricted
                })
                print(f"Saved slot {slot_name} ({'restricted' if is_restricted else 'normal'})")
                slot_counter += 1
                points = []
                is_restricted = False
                redraw()

        elif key == ord('r'):
            points = []
            redraw()

        elif key == ord('z'):
            if points:
                points.pop()
                redraw()

        elif key == ord('d'):
            is_restricted = not is_restricted
            print(f"Restricted zone: {is_restricted}")
            redraw()

        elif key == ord('q'):
            if slots:
                save_slots_to_db()
            else:
                print("No slots defined.")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()