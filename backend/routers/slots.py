from fastapi import APIRouter
from database import get_connection
from models import ParkingSlot

router = APIRouter()

@router.get("/")
def get_slots():
    conn = get_connection()
    slots = conn.execute("SELECT * FROM parking_slots").fetchall()
    conn.close()
    return [dict(s) for s in slots]

@router.post("/")
def add_slot(slot: ParkingSlot):
    conn = get_connection()
    conn.execute(
        "INSERT INTO parking_slots (slot_name, polygon, is_restricted) VALUES (?, ?, ?)",
        (slot.slot_name, slot.polygon, int(slot.is_restricted))
    )
    conn.commit()
    conn.close()
    return {"message": "Slot added"}

@router.delete("/{slot_id}")
def delete_slot(slot_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM parking_slots WHERE id = ?", (slot_id,))
    conn.commit()
    conn.close()
    return {"message": "Slot deleted"}