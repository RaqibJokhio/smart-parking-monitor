import sqlite3
from config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_name TEXT NOT NULL,
            polygon TEXT NOT NULL,
            is_restricted INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT NOT NULL,
            slot_id INTEGER,
            entry_time TEXT NOT NULL,
            exit_time TEXT,
            duration_seconds INTEGER,
            is_illegal INTEGER DEFAULT 0,
            evidence_path TEXT,
            FOREIGN KEY (slot_id) REFERENCES parking_slots(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS illegal_parking_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            reason TEXT,
            evidence_path TEXT
        )
    """)

    conn.commit()
    conn.close()