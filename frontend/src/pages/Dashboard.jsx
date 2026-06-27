import StatCard from "../components/StatCard"
import OccupancyChart from "../components/OccupancyChart"
import SlotGrid from "../components/SlotGrid"
import IllegalTable from "../components/IllegalTable"
import { useParking } from "../hooks/useParking"

export default function Dashboard() {
  const { stats, sessions, slots, loading } = useParking(3000)

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-6xl mx-auto">
        <div className="mb-6">
          <h1 className="text-2xl font-bold">Smart Parking Monitor</h1>
          <p className="text-gray-400 text-sm">Live occupancy dashboard · updates every 3s</p>
        </div>

        {loading ? (
          <p className="text-gray-500">Loading...</p>
        ) : (
          <div className="flex flex-col gap-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <StatCard title="Total Slots" value={stats?.total_slots} color="blue" />
              <StatCard
                title="Available"
                value={stats?.available_slots}
                sub={`${100 - (stats?.occupancy_percentage ?? 0)}% free`}
                color="green"
              />
              <StatCard
                title="Occupied"
                value={stats?.occupied_slots}
                sub={`${stats?.occupancy_percentage}% full`}
                color="red"
              />
              <StatCard
                title="Illegal"
                value={stats?.illegal_count}
                color="yellow"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <OccupancyChart
                occupied={stats?.occupied_slots ?? 0}
                available={stats?.available_slots ?? 0}
              />
              <SlotGrid slots={slots} sessions={sessions} />
            </div>

            <IllegalTable sessions={sessions} />
          </div>
        )}
      </div>
    </div>
  )
}