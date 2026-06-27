from fastapi import APIRouter
from database import get_connection

router = APIRouter()

@router.get("/")
def get_sessions():
    conn = get_connection()
    sessions = conn.execute(
        "SELECT * FROM parking_sessions ORDER BY entry_time DESC LIMIT 50"
    ).fetchall()
    conn.close()
    return [dict(s) for s in sessions]

@router.get("/active")
def get_active_sessions():
    conn = get_connection()
    sessions = conn.execute(
        "SELECT * FROM parking_sessions WHERE exit_time IS NULL"
    ).fetchall()
    conn.close()
    return [dict(s) for s in sessions]