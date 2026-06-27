import numpy as np
from collections import defaultdict
from datetime import datetime
from database import get_connection
from inference import assign_vehicle_to_slot, is_illegal_parking, save_evidence
import json

class ParkingTracker:
    def __init__(self):
        self.active_sessions = {}      # vehicle_id -> {slot_id, entry_time, slot_name}
        self.illegal_flagged = set()   # vehicle_ids already flagged
        self.slot_occupancy = {}       # slot_id -> vehicle_id

    def update(self, tracked_objects, slots, frame):
        """
        tracked_objects: list of dicts with keys: track_id, bbox, center
        slots: list of slot dicts from DB
        frame: current video frame for evidence snapshots
        """
        current_ids = set()

        for obj in tracked_objects:
            track_id = str(obj["track_id"])
            center = obj["center"]
            current_ids.add(track_id)

            assigned_slot = assign_vehicle_to_slot(center, slots)
            illegal, reason = is_illegal_parking(center, slots)

            # New vehicle entered
            if track_id not in self.active_sessions:
                slot_id = assigned_slot["id"] if assigned_slot else None
                self.active_sessions[track_id] = {
                    "slot_id": slot_id,
                    "slot_name": assigned_slot["slot_name"] if assigned_slot else "unknown",
                    "entry_time": datetime.now().isoformat(),
                    "is_illegal": illegal
                }
                if slot_id:
                    self.slot_occupancy[slot_id] = track_id
                self._save_session_entry(track_id, slot_id, illegal)

            # Illegal parking alert
            if illegal and track_id not in self.illegal_flagged:
                self.illegal_flagged.add(track_id)
                evidence_path = save_evidence(frame, track_id, reason)
                self._save_illegal_event(track_id, reason, evidence_path)

        # Vehicles that left
        departed = set(self.active_sessions.keys()) - current_ids
        for track_id in departed:
            self._close_session(track_id)

        return self.slot_occupancy

    def _save_session_entry(self, vehicle_id, slot_id, is_illegal):
        conn = get_connection()
        conn.execute(
            """INSERT INTO parking_sessions (vehicle_id, slot_id, entry_time, is_illegal)
               VALUES (?, ?, ?, ?)""",
            (vehicle_id, slot_id, datetime.now().isoformat(), int(is_illegal))
        )
        conn.commit()
        conn.close()

    def _close_session(self, vehicle_id):
        session = self.active_sessions.pop(vehicle_id, None)
        if not session:
            return

        exit_time = datetime.now()
        entry_time = datetime.fromisoformat(session["entry_time"])
        duration = int((exit_time - entry_time).total_seconds())

        # Free up the slot
        slot_id = session.get("slot_id")
        if slot_id and self.slot_occupancy.get(slot_id) == vehicle_id:
            del self.slot_occupancy[slot_id]

        conn = get_connection()
        conn.execute(
            """UPDATE parking_sessions
               SET exit_time = ?, duration_seconds = ?
               WHERE vehicle_id = ? AND exit_time IS NULL""",
            (exit_time.isoformat(), duration, vehicle_id)
        )
        conn.commit()
        conn.close()

    def _save_illegal_event(self, vehicle_id, reason, evidence_path):
        conn = get_connection()
        conn.execute(
            """INSERT INTO illegal_parking_events (vehicle_id, timestamp, reason, evidence_path)
               VALUES (?, ?, ?, ?)""",
            (vehicle_id, datetime.now().isoformat(), reason, evidence_path)
        )
        conn.commit()
        conn.close()

    def get_live_durations(self):
        """Returns {vehicle_id: seconds_parked} for all active sessions."""
        now = datetime.now()
        result = {}
        for vid, session in self.active_sessions.items():
            entry = datetime.fromisoformat(session["entry_time"])
            result[vid] = int((now - entry).total_seconds())
        return result