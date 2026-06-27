import { RadialBarChart, RadialBar, Legend, ResponsiveContainer } from "recharts"

export default function OccupancyChart({ occupied, available }) {
  const data = [
    { name: "Occupied", value: occupied, fill: "#ef4444" },
    { name: "Available", value: available, fill: "#22c55e" }
  ]

  return (
    <div className="bg-gray-800 rounded-xl p-5 shadow">
      <p className="text-gray-400 text-sm mb-3">Slot Occupancy</p>
      <ResponsiveContainer width="100%" height={220}>
        <RadialBarChart innerRadius="30%" outerRadius="90%" data={data}>
          <RadialBar dataKey="value" cornerRadius={6} />
          <Legend iconType="circle" />
        </RadialBarChart>
      </ResponsiveContainer>
    </div>
  )
}