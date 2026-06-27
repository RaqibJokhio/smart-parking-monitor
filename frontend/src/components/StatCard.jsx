export default function StatCard({ title, value, sub, color = "blue" }) {
  const colors = {
    blue: "bg-blue-600",
    green: "bg-green-600",
    red: "bg-red-600",
    yellow: "bg-yellow-500"
  }

  return (
    <div className="bg-gray-800 rounded-xl p-5 flex flex-col gap-1 shadow">
      <div className={`w-2 h-2 rounded-full ${colors[color]} mb-1`} />
      <p className="text-gray-400 text-sm">{title}</p>
      <p className="text-white text-3xl font-bold">{value ?? "—"}</p>
      {sub && <p className="text-gray-500 text-xs">{sub}</p>}
    </div>
  )
}