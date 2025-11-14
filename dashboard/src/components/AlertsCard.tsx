import { useEffect, useState } from 'react'
import { collection, getDocs } from 'firebase/firestore'
import { db, auth } from '../firebase'

interface Alert {
  id: string
  name?: string
  type?: string
  status?: 'active' | 'disabled'
  condition?: string
  threshold?: number
  lastTriggered?: { seconds: number }
  triggerCount?: number
}

export default function AlertsCard() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const user = auth.currentUser
        if (!user) {
          setError('Not authenticated')
          setLoading(false)
          return
        }

        const alertsRef = collection(db, 'users', user.uid, 'alerts')
        const snapshot = await getDocs(alertsRef)

        const alertsList = snapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data()
        })) as Alert[]

        setAlerts(alertsList)
      } catch (err) {
        console.error('Error fetching alerts:', err)
        setError(err instanceof Error ? err.message : 'Failed to load alerts')
      } finally {
        setLoading(false)
      }
    }

    fetchAlerts()
  }, [])

  if (loading) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-primary mb-4">Alerts & Thresholds</h3>
        <div className="flex items-center justify-center py-8">
          <div className="text-zinc-500">Loading alerts...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card border-red-200 bg-red-50">
        <h3 className="text-xl font-bold text-red-700 mb-4">Alerts & Thresholds</h3>
        <div className="text-red-600 text-sm">
          ⚠️ Error loading alerts: {error}
        </div>
      </div>
    )
  }

  if (alerts.length === 0) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-primary mb-4">Alerts & Thresholds</h3>
        <div className="text-center py-8">
          <div className="text-zinc-400 text-lg">No alerts configured</div>
          <p className="text-zinc-500 text-sm mt-2">
            Set up alerts to monitor important conditions
          </p>
        </div>
      </div>
    )
  }

  const activeAlerts = alerts.filter((a) => a.status === 'active')
  const disabledAlerts = alerts.filter((a) => a.status === 'disabled')

  return (
    <div className="card">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-xl font-bold text-primary">Alerts & Thresholds</h3>
        <div className="flex gap-3 text-sm">
          <span className="text-green-600 font-medium">{activeAlerts.length} active</span>
          <span className="text-zinc-400">{disabledAlerts.length} disabled</span>
        </div>
      </div>

      <div className="space-y-3">
        {alerts.map((alert) => (
          <div
            key={alert.id}
            className={`p-4 border rounded-lg transition-colors ${
              alert.status === 'active'
                ? 'border-zinc-200 hover:border-zinc-300 bg-white'
                : 'border-zinc-100 bg-zinc-50'
            }`}
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <h4 className="font-semibold text-zinc-800">
                    {alert.name || alert.id}
                  </h4>
                  <div
                    className={`h-2 w-2 rounded-full ${
                      alert.status === 'active' ? 'bg-green-500' : 'bg-zinc-300'
                    }`}
                    title={alert.status}
                  />
                </div>
                {alert.condition && (
                  <p className="text-sm text-zinc-600 mt-1">{alert.condition}</p>
                )}
                {alert.threshold !== undefined && (
                  <p className="text-xs text-zinc-500 mt-1">
                    Threshold: {alert.threshold}
                  </p>
                )}
              </div>
              {alert.type && (
                <span className="text-xs text-zinc-500 bg-zinc-100 px-2 py-1 rounded">
                  {alert.type}
                </span>
              )}
            </div>
            <div className="flex items-center gap-4 mt-3 text-xs text-zinc-500">
              {alert.triggerCount !== undefined && (
                <span>Triggered {alert.triggerCount} times</span>
              )}
              {alert.lastTriggered && (
                <span>
                  Last: {new Date(alert.lastTriggered.seconds * 1000).toLocaleDateString()}
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
