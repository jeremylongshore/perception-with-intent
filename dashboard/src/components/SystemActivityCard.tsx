import { useEffect, useState } from 'react'
import { collection, query, orderBy, limit, getDocs } from 'firebase/firestore'
import { db } from '../firebase'

interface IngestionRun {
  id: string
  startedAt: { seconds: number }
  completedAt?: { seconds: number }
  status: 'completed' | 'running' | 'failed'
  trigger: string
  stats?: {
    sourcesChecked?: number
    sourcesFailed?: number
    articlesIngested?: number
    articlesDeduplicated?: number
    briefsGenerated?: number
    alertsTriggered?: number
  }
  duration?: number
}

export default function SystemActivityCard() {
  const [runs, setRuns] = useState<IngestionRun[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchRuns = async () => {
      try {
        const runsRef = collection(db, 'ingestion_runs')
        const q = query(runsRef, orderBy('startedAt', 'desc'), limit(10))
        const snapshot = await getDocs(q)

        const runsList = snapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data()
        })) as IngestionRun[]

        setRuns(runsList)
      } catch (err) {
        console.error('Error fetching ingestion runs:', err)
        setError(err instanceof Error ? err.message : 'Failed to load activity')
      } finally {
        setLoading(false)
      }
    }

    fetchRuns()
  }, [])

  if (loading) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-primary mb-4">System Activity</h3>
        <div className="flex items-center justify-center py-8">
          <div className="text-zinc-500">Loading activity...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card border-red-200 bg-red-50">
        <h3 className="text-xl font-bold text-red-700 mb-4">System Activity</h3>
        <div className="text-red-600 text-sm">
          ⚠️ Error loading activity: {error}
        </div>
      </div>
    )
  }

  if (runs.length === 0) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-primary mb-4">System Activity</h3>
        <div className="text-center py-8">
          <div className="text-zinc-400 text-lg">No ingestion runs yet</div>
          <p className="text-zinc-500 text-sm mt-2">
            Run your first ingestion to see activity
          </p>
        </div>
      </div>
    )
  }

  const formatDate = (seconds: number) => {
    const date = new Date(seconds * 1000)
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    })
  }

  const formatDuration = (seconds?: number) => {
    if (!seconds) return '-'
    if (seconds < 60) return `${seconds}s`
    return `${Math.floor(seconds / 60)}m ${seconds % 60}s`
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-700 border-green-200'
      case 'running':
        return 'bg-blue-100 text-blue-700 border-blue-200'
      case 'failed':
        return 'bg-red-100 text-red-700 border-red-200'
      default:
        return 'bg-zinc-100 text-zinc-700 border-zinc-200'
    }
  }

  return (
    <div className="card">
      <h3 className="text-xl font-bold text-primary mb-6">System Activity</h3>

      <div className="space-y-3">
        {runs.map((run) => (
          <div
            key={run.id}
            className="p-4 border border-zinc-200 rounded-lg hover:border-zinc-300 transition-colors"
          >
            <div className="flex justify-between items-start mb-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-semibold text-zinc-800">
                    {formatDate(run.startedAt.seconds)}
                  </span>
                  <span
                    className={`text-xs px-2 py-0.5 rounded border ${getStatusColor(run.status)}`}
                  >
                    {run.status}
                  </span>
                </div>
                <div className="text-xs text-zinc-500 mt-1">
                  Trigger: {run.trigger} • Duration: {formatDuration(run.duration)}
                </div>
              </div>
            </div>

            {run.stats && (
              <div className="grid grid-cols-3 gap-3 mt-3 pt-3 border-t border-zinc-100">
                {run.stats.sourcesChecked !== undefined && (
                  <div>
                    <div className="text-xs text-zinc-500">Sources</div>
                    <div className="text-sm font-semibold text-zinc-700">
                      {run.stats.sourcesChecked}
                      {run.stats.sourcesFailed ? (
                        <span className="text-red-500 text-xs ml-1">
                          ({run.stats.sourcesFailed} failed)
                        </span>
                      ) : null}
                    </div>
                  </div>
                )}
                {run.stats.articlesIngested !== undefined && (
                  <div>
                    <div className="text-xs text-zinc-500">Articles</div>
                    <div className="text-sm font-semibold text-zinc-700">
                      {run.stats.articlesIngested}
                      {run.stats.articlesDeduplicated ? (
                        <span className="text-zinc-400 text-xs ml-1">
                          (-{run.stats.articlesDeduplicated})
                        </span>
                      ) : null}
                    </div>
                  </div>
                )}
                {run.stats.briefsGenerated !== undefined && (
                  <div>
                    <div className="text-xs text-zinc-500">Briefs</div>
                    <div className="text-sm font-semibold text-zinc-700">
                      {run.stats.briefsGenerated}
                    </div>
                  </div>
                )}
                {run.stats.alertsTriggered !== undefined && run.stats.alertsTriggered > 0 && (
                  <div>
                    <div className="text-xs text-zinc-500">Alerts</div>
                    <div className="text-sm font-semibold text-orange-600">
                      {run.stats.alertsTriggered}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {runs.length >= 10 && (
        <div className="text-center text-xs text-zinc-400 mt-4">
          Showing most recent 10 runs
        </div>
      )}
    </div>
  )
}
