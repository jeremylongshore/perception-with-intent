import { useEffect, useState } from 'react'
import { collection, getDocs } from 'firebase/firestore'
import { db } from '../firebase'

interface Source {
  id: string
  name: string
  type: string
  url: string
  category: string
  status: 'active' | 'disabled'
  lastChecked?: { seconds: number }
  lastSuccess?: { seconds: number }
  articlesLast24h?: number
}

interface SourceStats {
  total: number
  active: number
  disabled: number
  byCategory: Record<string, number>
  byType: Record<string, number>
}

export default function SourceHealthCard() {
  const [sources, setSources] = useState<Source[]>([])
  const [stats, setStats] = useState<SourceStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchSources = async () => {
      try {
        const sourcesRef = collection(db, 'sources')
        const snapshot = await getDocs(sourcesRef)

        const sourcesList = snapshot.docs.map((doc) => ({
          id: doc.id,
          ...doc.data()
        })) as Source[]

        setSources(sourcesList)

        // Calculate stats
        const stats: SourceStats = {
          total: sourcesList.length,
          active: sourcesList.filter((s) => s.status === 'active').length,
          disabled: sourcesList.filter((s) => s.status === 'disabled').length,
          byCategory: {},
          byType: {}
        }

        sourcesList.forEach((source) => {
          // Count by category
          stats.byCategory[source.category] = (stats.byCategory[source.category] || 0) + 1
          // Count by type
          stats.byType[source.type] = (stats.byType[source.type] || 0) + 1
        })

        setStats(stats)
      } catch (err) {
        console.error('Error fetching sources:', err)
        setError(err instanceof Error ? err.message : 'Failed to load sources')
      } finally {
        setLoading(false)
      }
    }

    fetchSources()
  }, [])

  if (loading) {
    return (
      <div className="card">
        <h3 className="text-xl font-bold text-primary mb-4">Source Health & Coverage</h3>
        <div className="flex items-center justify-center py-8">
          <div className="text-zinc-500">Loading sources...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card border-red-200 bg-red-50">
        <h3 className="text-xl font-bold text-red-700 mb-4">Source Health & Coverage</h3>
        <div className="text-red-600 text-sm">
          ⚠️ Error loading sources: {error}
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <h3 className="text-xl font-bold text-primary mb-6">Source Health & Coverage</h3>

      {/* Stats Overview */}
      {stats && (
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="text-center p-3 bg-zinc-50 rounded-lg">
            <div className="text-2xl font-bold text-primary">{stats.total}</div>
            <div className="text-xs text-zinc-500 mt-1">Total Sources</div>
          </div>
          <div className="text-center p-3 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600">{stats.active}</div>
            <div className="text-xs text-zinc-500 mt-1">Active</div>
          </div>
          <div className="text-center p-3 bg-zinc-50 rounded-lg">
            <div className="text-2xl font-bold text-zinc-400">{stats.disabled}</div>
            <div className="text-xs text-zinc-500 mt-1">Disabled</div>
          </div>
        </div>
      )}

      {/* Category Breakdown */}
      {stats && Object.keys(stats.byCategory).length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-zinc-700 mb-3">By Category</h4>
          <div className="space-y-2">
            {Object.entries(stats.byCategory).map(([category, count]) => (
              <div key={category} className="flex items-center justify-between">
                <span className="text-zinc-600 text-sm capitalize">{category}</span>
                <div className="flex items-center gap-2">
                  <div className="h-2 flex-1 w-32 bg-zinc-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary rounded-full"
                      style={{ width: `${(count / stats.total) * 100}%` }}
                    />
                  </div>
                  <span className="text-sm font-semibold text-zinc-700 w-6 text-right">
                    {count}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Source List */}
      <div>
        <h4 className="text-sm font-semibold text-zinc-700 mb-3">Sources</h4>
        <div className="space-y-2 max-h-64 overflow-y-auto">
          {sources.slice(0, 10).map((source) => (
            <div
              key={source.id}
              className="flex items-center justify-between p-2 hover:bg-zinc-50 rounded"
            >
              <div className="flex-1">
                <div className="text-sm font-medium text-zinc-800">{source.name}</div>
                <div className="text-xs text-zinc-500">{source.category} • {source.type}</div>
              </div>
              <div className="flex items-center gap-2">
                {source.articlesLast24h !== undefined && (
                  <span className="text-xs text-zinc-500">
                    {source.articlesLast24h} today
                  </span>
                )}
                <div
                  className={`h-2 w-2 rounded-full ${
                    source.status === 'active' ? 'bg-green-500' : 'bg-zinc-300'
                  }`}
                  title={source.status}
                />
              </div>
            </div>
          ))}
          {sources.length > 10 && (
            <div className="text-center text-xs text-zinc-400 pt-2">
              +{sources.length - 10} more sources
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
