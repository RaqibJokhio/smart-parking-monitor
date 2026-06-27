import { useState, useEffect } from "react"
import axios from "axios"

export function useParking(interval = 3000) {
  const [stats, setStats] = useState(null)
  const [sessions, setSessions] = useState([])
  const [slots, setSlots] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetch = async () => {
      try {
        const [statsRes, sessionsRes, slotsRes] = await Promise.all([
          axios.get("/api/analytics/dashboard"),
          axios.get("/api/sessions/active"),
          axios.get("/api/slots/")
        ])
        setStats(statsRes.data)
        setSessions(sessionsRes.data)
        setSlots(slotsRes.data)
      } catch (e) {
        console.error("API error:", e)
      } finally {
        setLoading(false)
      }
    }

    fetch()
    const timer = setInterval(fetch, interval)
    return () => clearInterval(timer)
  }, [interval])

  return { stats, sessions, slots, loading }
}