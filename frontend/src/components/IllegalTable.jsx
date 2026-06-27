export default function IllegalTable({ sessions }) {
  const illegal = sessions.filter(s => s.is_illegal)

  return (
    <div className="bg-gray-800 rounded-xl p-5 shadow">
      <p className="text-gray-400 text-sm mb-3">
        Illegal Parking <span className="text-red-400">({illegal.length})</span>
      </p>
      {illegal.length === 0 ? (
        <p className="text-gray-500 text-xs">No illegal parking detected.</p>
      ) : (
        <table className="w-full text-xs text-gray-300">
          <thead>
            <tr className="text-gray-500 border-b border-gray-700">
              <th className="text-left py-1">Vehicle ID</th>
              <th className="text-left py-1">Entry Time</th>
              <th className="text-left py-1">Slot</th>
            </tr>
          </thead>
          <tbody>
            {illegal.map(s => (
              <tr key={s.id} className="border-b border-gray-700">
                <td className="py-1 text-red-400">{s.vehicle_id}</td>
                <td className="py-1">{new Date(s.entry_time).toLocaleTimeString()}</td>
                <td className="py-1">{s.slot_id ?? "Outside"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}