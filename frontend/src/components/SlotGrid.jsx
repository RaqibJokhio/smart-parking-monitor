export default function SlotGrid({ slots, sessions }) {
  const occupiedSlotIds = new Set(sessions.map(s => s.slot_id))

  return (
    <div className="bg-gray-800 rounded-xl p-5 shadow">
      <p className="text-gray-400 text-sm mb-3">Parking Slots</p>
      <div className="grid grid-cols-4 gap-2">
        {slots.map(slot => {
          const occupied = occupiedSlotIds.has(slot.id)
          return (
            <div
              key={slot.id}
              className={`rounded-lg p-3 text-center text-xs font-semibold
                ${slot.is_restricted
                  ? "bg-yellow-600 text-white"
                  : occupied
                  ? "bg-red-600 text-white"
                  : "bg-green-600 text-white"}`}
            >
              {slot.slot_name}
              <div className="text-[10px] font-normal mt-1">
                {slot.is_restricted ? "Restricted" : occupied ? "Occupied" : "Free"}
              </div>
            </div>
          )
        })}
        {slots.length === 0 && (
          <p className="col-span-4 text-gray-500 text-xs">No slots defined yet.</p>
        )}
      </div>
    </div>
  )
}