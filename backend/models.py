from pydantic import BaseModel
from typing import Optional, List

class ParkingSlot(BaseModel):
    slot_name: str
    polygon: str  # JSON string of polygon points
    is_restricted: bool = False

class ParkingSession(BaseModel):
    vehicle_id: str
    slot_id: Optional[int]
    entry_time: str
    exit_time: Optional[str]
    duration_seconds: Optional[int]
    is_illegal: bool = False
    evidence_path: Optional[str]

class DashboardStats(BaseModel):
    total_slots: int
    occupied_slots: int
    available_slots: int
    occupancy_percentage: float
    illegal_count: int
    avg_duration_seconds: float