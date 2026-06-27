from fastapi import APIRouter
from database import get_connection

router = APIRouter()

@router.get("/dashboard")
def get_dashboard_stats():
    conn = get_connection()

    total_slots = conn.execute("SELECT COUNT(*) FROM parking_slots").fetchone()[0]
    occupied = conn.execute(
        "SELECT COUNT(*) FROM parking_sessions WHERE exit_time IS NULL"
    ).fetchone()[0]
    illegal_count = conn.execute(
        "SELECT COUNT(*) FROM illegal_parking_events"
    ).fetchone()[0]
    avg_duration = conn.execute(
        "SELECT AVG(duration_seconds) FROM parking_sessions WHERE duration_seconds IS NOT NULL"
    ).fetchone()[0] or 0

    conn.close()

    available = max(total_slots - occupied, 0)
    occupancy_pct = round((occupied / total_slots * 100), 1) if total_slots > 0 else 0

    return {
        "total_slots": total_slots,
        "occupied_slots": occupied,
        "available_slots": available,
        "occupancy_percentage": occupancy_pct,
        "illegal_count": illegal_count,
        "avg_duration_seconds": round(avg_duration, 1)
    }